import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)
import re
import warnings

# Parser noise: model outputs like '{1,2}(x)' compile to set-literal calls;
# harmless (they score False) but spam stderr without this.
warnings.filterwarnings('ignore', category=SyntaxWarning)


TOL = 1e-6
SIMPLIFY_TIMEOUT = 5.0


def _simplify_guarded(a, b, timeout: float = None) -> bool:
    """Run hang-prone equals/simplify off-thread with a timeout.

    The worker is daemonic: on timeout we abandon it (a timed-out simplify
    may keep spinning, but it can never wedge the run or block exit).
    # ponytail: leaked thread per timeout; acceptable — timeouts are rare.
    """
    import threading
    box = {}

    def run():
        try:
            box["v"] = _simplify_eq(a, b)
        except Exception:
            box["v"] = False

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(SIMPLIFY_TIMEOUT if timeout is None else timeout)
    return bool(box.get("v", False))


def clean_text(s: str) -> str:
    """Normalize a string for exact comparison."""
    s = str(s).lower().strip()
    # Remove common wrappers and decorations
    s = s.replace("$", "").replace("%", "")
    if s.endswith(".00"):
        s = s[:-3]
    # Remove all whitespace
    s = re.sub(r'\s+', '', s)
    return s


def extract_final(s: str) -> str:
    """Take last non-empty line, strip wrappers like Answer:/d/dx/f'(x)=."""
    s = str(s).strip().strip('"').strip("'")
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    s = lines[-1] if lines else s
    # Strip leading Answer: / Result: prefixes
    s = re.sub(r'^(answer|result)\s*:\s*', '', s, flags=re.IGNORECASE)
    # A bare leading '=' is a leftover wrapper ('= [[8, -2], ...'), never content
    s = re.sub(r'^=\s*', '', s)
    # Multi-answer lists: strip per-item variable prefixes, keep all items
    if ',' in s or ';' in s:
        return s
    # Single value: take text after last '=' (handles f'(x)=, d/dx=, integral=)
    if '=' in s:
        s = s.rsplit('=', 1)[-1].strip()
    return s.strip().strip('"').strip("'")

def build_prompt(case: dict) -> tuple[str, str]:
    system_prompt = """You are a mathematical reasoning assistant. You must output ONLY the final answer, with no explanations, steps, or extra text.

STRICT FORMAT RULES:
- Use plain calculator notation: "*" for multiplication, "/" for division, "^" or "**" for exponents.
- Write functions exactly as: sin(x), cos(x), tan(x), sec(x), csc(x), cot(x), asin(x), acos(x), asec(x), acsc(x), acot(x), atan(x), log(x), sqrt(x), abs(x), factorial(n), binomial(n,k), pi, e.
- Do NOT use LaTeX, backslashes, or special formatting.
- Do NOT include prefixes like "x =", "y =", "f'(x) =", "d/dx", "Answer:", or any unit.
- Output only the final mathematical expression or numeric value.
- Write the exponent immediately before the parantheses : example: sin^2(x), cos^3(x), sec^2(x), ln^2(x)

CATEGORY-SPECIFIC RULES:

1. **Derivatives**: Output only the derivative expression. Do NOT include "f'(x) =" or "d/dx".
   - Example: Derivative of sin(x) → cos(x)
   - Example: Derivative of x^2 * e^x → 2*x*e^x + x^2*e^x

2. **Indefinite Integrals**: Output the antiderivative with "+ C" at the end.
   - Example: Integral of x dx → x^2/2 + C
   - Example: Integral of cos(x) dx → sin(x) + C

3. **Solving Equations**: Output all solutions separated by a comma and a space. Do NOT include "x =".
   - Example: Solve x^2 = 4 → 2, -2
   - Example: Solve 2x + 3 = 7 → 2
   For systems with multiple solution pairs, separate pairs with a semicolon:
   - Example: Solve x² + y² = 25, x + y = 7 → 3, 4; 4, 3

4. **Systems of Equations**: Output the values of x and y separated by a comma and a space, WITHOUT variables.
   - Example: Solve x + y = 5, x - y = 1 → 3, 2

5. **Matrices and Vectors**:
   - Matrix: Use nested brackets: [[a, b], [c, d]]
   - Vector: Use single brackets: [a, b, c]
   - Example: Matrix [[1,2],[3,4]] → [[1,2],[3,4]]

6. **Probability and Statistics**:
   - Output simplified fractions or decimals (no "%" sign unless the problem specifically asks for a percentage).
   - Example: Probability of rolling a 6 on a fair die → 1/6
   - Example: Expected value of a fair coin flip → 0.5

7. **Yes/No Questions**:
   - Output exactly "Yes" or "No" (capitalized, no punctuation).
   - Example: Is 2+2=4? → Yes

8. **Word Problems**:
   - Output only the numeric answer (no units, no explanation).
   - Example: A car travels 60 mph for 2 hours. How far? → 120

9. **Series and Sequences**:
   - For a term, output the value.
   - For a sum, output the sum as a simplified number or expression.
   - For convergence questions, output "Yes" or "No".

10. **Percentages**:
    - If the answer is a percentage, output the numeric value without the "%" sign (unless the problem says "in percent").
    - Example: What is 20% of 50? → 10

11. **Logarithms**:
    - Use log(x) always 

12. **Absolute Values**:
    - Use abs(x). Example: |x| → abs(x)

13. **Factorials and Binomials**:
    - Use factorial(n) and binomial(n, k).
    - Example: 5! = factorial(5), C(5,2) = binomial(5,2)

14. **Complex Expressions**:
    - Fully simplify where possible, but do not change the form if it is already simplified.
    - Use parentheses to avoid ambiguity.

15. **Multiple Answers**:
    - Separate all answers with a comma and a space. Do not add extra commas or brackets.
    - Example: Roots of x^2 - 5x + 6 = 0 → 2, 3

16. **Undefined or No Solution**:
    - If there is no solution, output "No solution".
    - If there are infinitely many solutions, output "Infinite solutions".

EXAMPLES OF CORRECT OUTPUT:
- Derivative of x^3 → 3*x^2
- Integral of 1/x → ln(abs(x)) + C
- Solve x^2 + 2x + 1 = 0 → -1
- Matrix [[1,2],[3,4]] + [[5,6],[7,8]] → [[6,8],[10,12]]
- Probability of drawing a heart from a deck → 1/4
- Yes/No: Is the series 1+1/2+1/4+... convergent? → Yes

FAILURE TO FOLLOW THESE RULES WILL RESULT IN THE ANSWER BEING MARKED AS INCORRECT, EVEN IF THE MATHEMATICAL CONTENT IS RIGHT.

Now, solve the following problem and output only the final answer according to the above rules.
"""
    user_prompt = f"{case['question']}\n\nAnswer:"
    return system_prompt, user_prompt


def check_sets(expected: str, predicted: str) -> bool:
    """
    Compare comma-separated roots as sets, ';'-separated pairs as sets of tuples.
    Uses 1e-6 tolerance for numerics.
    """
    def parse_item(part: str):
        part = part.strip()
        # Strip per-item variable prefixes (x=, y=)
        if '=' in part and not any(op in part for op in ('==', '>=', '<=')):
            part = part.rsplit('=', 1)[-1].strip()
        part = re.sub(r'^[xy]\s*', '', part).strip()
        try:
            return ('num', float(sp.Rational(part)))
        except Exception:
            try:
                return ('num', float(part))
            except Exception:
                return ('str', part)

    def norm_set(items):
        nums, strs = [], []
        for kind, v in items:
            (nums if kind == 'num' else strs).append(v)
        return nums, sorted(strs)

    try:
        # Systems with multiple pairs: '3, 4; 4, 3'
        if ';' in expected or ';' in predicted:
            def parse_pairs(s):
                pairs = []
                for grp in s.split(';'):
                    grp = grp.strip()
                    if not grp:
                        continue
                    items = [parse_item(p) for p in grp.split(',') if p.strip()]
                    pairs.append(tuple(items))
                return pairs

            exp_pairs = parse_pairs(re.sub(r'[=\[\]{} ]', '', expected, flags=re.IGNORECASE))
            # keep raw for predicted so parse_item can strip '=' per item
            pred_pairs = parse_pairs(predicted)
            # Re-parse expected with same path for symmetry
            exp_pairs = parse_pairs(expected)
            if len(exp_pairs) != len(pred_pairs):
                return False
            # Order-insensitive match on pairs with tolerance
            unmatched = list(pred_pairs)
            for ep in exp_pairs:
                found = False
                for i, pp in enumerate(unmatched):
                    if len(ep) != len(pp):
                        continue
                    ok = True
                    for (k1, v1), (k2, v2) in zip(ep, pp):
                        if k1 != k2:
                            ok = False
                            break
                        if k1 == 'num' and abs(v1 - v2) > TOL:
                            ok = False
                            break
                        if k1 == 'str' and v1 != v2:
                            ok = False
                            break
                    if ok:
                        unmatched.pop(i)
                        found = True
                        break
                if not found:
                    return False
            return True

        def parse_numbers(s: str):
            s = re.sub(r'[xy=\(\)\[\]{} ]', '', s)
            parts = [p.strip() for p in s.split(',') if p.strip()]
            return [parse_item(p) for p in parts]

        exp, pred = parse_numbers(expected), parse_numbers(predicted)
        if len(exp) != len(pred):
            return False
        en, es = norm_set(exp)
        pn, ps = norm_set(pred)
        if es != ps:
            return False
        # Tolerance-based multiset match
        unmatched = list(pn)
        for v in en:
            hit = next((i for i, u in enumerate(unmatched) if abs(v - u) <= TOL), None)
            if hit is None:
                return False
            unmatched.pop(hit)
        return True
    except Exception:
        return False


def sympy_preprocess(s: str) -> str:
    """Minimal preprocessing for SymPy parsing."""
    s = str(s).lower().strip()
    # Replace ln with log (SymPy uses log for natural log)
    s = re.sub(r'\bln\b', 'log', s)
    # Replace arc functions with SymPy equivalents
    s = s.replace('arcsin', 'asin')
    s = s.replace('arccos', 'acos')
    s = s.replace('arctan', 'atan')
    s = s.replace('arcsec', 'asec')
    s = s.replace('arccsc', 'acsc')
    s = s.replace('arccot', 'acot')
    # Prompt-mandated power notation: sin^2(x) -> (sin(x))^2
    s = re.sub(
        r'(sin|cos|tan|sec|csc|cot|asin|acos|atan|asec|acsc|acot|log|sqrt)\^(\d+(?:\.\d+)?|\([^)]+\))\s*\(([^)]+)\)',
        r'(\1(\3))^\2',
        s,
    )
    # log|...| / ln|...| -> log(abs(...)) so the abs isn't glued to log
    s = re.sub(r'log\s*\|([^|]+)\|', r'log(abs(\1))', s)
    # Convert remaining |x| to abs(x)
    s = re.sub(r'\|([^|]+)\|', r'abs(\1)', s)
    # Standalone e is Euler, not a Symbol
    s = re.sub(r'\be\b', 'E', s)
    return s


def _tol_eq(x, y) -> bool:
    """Element equality: exact first, 1e-6 float fallback (Float vs Rational)."""
    try:
        if sp.simplify(x - y) == 0:
            return True
    except Exception:
        pass
    try:
        return abs(float(x.evalf()) - float(y.evalf())) <= TOL
    except Exception:
        return False


def check_matrices(expected: str, predicted: str) -> bool:
    """Order-sensitive compare for [..]/[[..]] answers. Handles fractions,
    decimals, expressions; ';' and whitespace work as separators."""
    try:
        if '[' not in expected or '[' not in predicted:
            return False
        transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
        # 1. Proper matrix parse (handles 1/2 vs 0.5, 1/sqrt(2), pi)
        try:
            a = parse_expr(sympy_preprocess(expected.replace(';', ',')), transformations=transformations)
            b = parse_expr(sympy_preprocess(predicted.replace(';', ',')), transformations=transformations)
            from sympy import MatrixBase
            if isinstance(a, MatrixBase) and isinstance(b, MatrixBase) and a.shape == b.shape:
                return all(_tol_eq(x, y) for x, y in zip(a, b))
        except Exception:
            pass
        # 2. Fallback: ordered token compare for loose spacing ('[1 2 3]')
        exp_toks = [p for p in re.split(r'[\[\],;\s]+', expected) if p.strip()]
        pred_toks = [p for p in re.split(r'[\[\],;\s]+', predicted) if p.strip()]
        if not exp_toks or len(exp_toks) != len(pred_toks):
            return False
        for et, pt in zip(exp_toks, pred_toks):
            try:
                x = parse_expr(sympy_preprocess(et), transformations=transformations)
                y = parse_expr(sympy_preprocess(pt), transformations=transformations)
            except Exception:
                return False
            if not _tol_eq(x, y):
                return False
        return True
    except Exception:
        return False


def check_numeric(expected: str, predicted: str) -> bool:
    """1e-6 tolerance for single constant values (1/6 vs 0.166667)."""
    try:
        transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
        a = parse_expr(sympy_preprocess(expected), transformations=transformations)
        b = parse_expr(sympy_preprocess(predicted), transformations=transformations)
        return bool(a.is_number and b.is_number) and _tol_eq(a, b)
    except Exception:
        return False


def _simplify_eq(a, b) -> bool:
    """Hang-prone part: structural equality + full simplify. Runs in guard thread."""
    try:
        if a.equals(b):
            return True
        return sp.simplify(a - b) == 0
    except Exception:
        return False


def _numeric_probe_eq(a, b, need: int = 3, tries: int = 60) -> bool:
    """Substitute random real values; agree within TOL at `need` points. No simplify."""
    try:
        syms = list((a.free_symbols | b.free_symbols))
        if not syms:
            return False
        import random
        hits = 0
        for _ in range(tries):
            if hits >= need:
                break
            subs = {s: random.uniform(-2.0, 2.0) for s in syms}
            try:
                va = complex(a.subs(subs).evalf())
                vb = complex(b.subs(subs).evalf())
            except Exception:
                continue  # singular point: try another
            if abs(va.imag) > 1e-9 or abs(vb.imag) > 1e-9:
                continue  # non-real (sqrt/log of negative): try another
            if abs(va.real - vb.real) <= TOL * max(1.0, abs(va.real), abs(vb.real)):
                hits += 1
            else:
                return False
        return hits >= need
    except Exception:
        return False


def check_sympy(expr1: str, expr2: str) -> bool:
    """Symbolic equivalence: cheap checks first, simplify time-boxed."""
    transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

    try:
        a = parse_expr(sympy_preprocess(expr1), transformations=transformations)
        b = parse_expr(sympy_preprocess(expr2), transformations=transformations)
    except Exception:
        return False

    # Numeric tolerance (fractions vs decimals)
    try:
        if a.is_number and b.is_number:
            if abs(float(a.evalf()) - float(b.evalf())) <= TOL:
                return True
    except Exception:
        pass

    # Antiderivatives differing by a constant: compare derivatives via expand
    # (cheap, no simplify). Only when both sides agree on '+C' so a missing
    # constant still fails per prompt rules, and never when Abs is involved:
    # log|x| vs log(x) share a derivative but are different functions.
    try:
        x = sp.Symbol('x')
        c = sp.Symbol('c')
        sa, sb = str(a), str(b)
        if ((c in a.free_symbols) == (c in b.free_symbols)
                and 'Abs' not in sa and 'Abs' not in sb
                and (a.has(x) or b.has(x))):
            if sp.expand(sp.diff(a - b, x)) == 0:
                return True
    except Exception:
        pass

    # Random-point probe catches most algebraic equivalences without simplify
    if _numeric_probe_eq(a, b):
        return True

    # Full simplify last, time-boxed so one bad output can't wedge the run
    return _simplify_guarded(a, b)


def are_equivalent(expected: str, predicted: str) -> bool:
    predicted = extract_final(predicted)
    expected = extract_final(expected)
    # 1. Direct cleaned string equality
    if clean_text(expected) == clean_text(predicted):
        return True

    # 2. Matrices / vectors (order-sensitive, ';' as delimiter)
    if '[' in expected and '[' in predicted:
        if check_matrices(expected, predicted):
            return True

    # 3. Set comparison for comma-separated roots (order-insensitive by design).
    # Never for matrices: entry order is significant there (handled above).
    if not ('[' in expected and '[' in predicted):
        if ',' in expected or ',' in predicted or ';' in expected or ';' in predicted:
            if check_sets(expected, predicted):
                return True

    # 4. Numeric tolerance for single values
    if check_numeric(expected, predicted):
        return True

    # 5. Symbolic equivalence (for algebraic expressions, derivatives, integrals)
    if check_sympy(expected, predicted):
        return True

    return False


def score(raw: dict, case: dict) -> dict:
    expected = case.get("answer", case.get("expected", "")).strip().strip('"').strip("'")
    predicted = raw.get("response", "").strip().strip('"').strip("'")

    is_correct = are_equivalent(expected, predicted)

    return {
        "score": 1.0 if is_correct else 0.0,
        "is_correct": is_correct,
        "expected_answer": expected,
        "predicted_answer": predicted,
        "math_category": case.get("category", 0),
    }