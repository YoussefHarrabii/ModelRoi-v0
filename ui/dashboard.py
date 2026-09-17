import sqlite3
from pathlib import Path
import time
import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import json

from app.config import DEFAULT_MODEL_REGISTRY, settings

st.set_page_config(page_title="ModelEval ROI Engine", layout="wide")

st.title("⚡ ModelEval ROI & Cluster Analytics")
st.markdown("Real-time telemetry, capacity scaling, and financial unit economics for local LLMs.")

status_container = st.sidebar.container()

# Force Absolute Path to SQLite Database
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "benchmark_history.db"

# ------------------- Helper Functions -------------------
def get_available_models() -> list[str]:
    """Fetch installed local Ollama models matching default registry configurations."""
    try:
        res = requests.get(f"{settings.OLLAMA_HOST}/api/tags", timeout=2)
        if res.status_code == 200:
            local_tags = [m["name"] for m in res.json().get("models", [])]
            return [m for m in local_tags if m in DEFAULT_MODEL_REGISTRY]
    except Exception:
        pass
    return list(DEFAULT_MODEL_REGISTRY.keys())

def load_benchmark_runs() -> pd.DataFrame:
    """Load all runs from benchmark_runs."""
    if not DB_PATH.exists():
        return pd.DataFrame()
    try:
        with sqlite3.connect(str(DB_PATH)) as conn:
            return pd.read_sql_query("SELECT * FROM benchmark_runs ORDER BY id DESC", conn)
    except Exception as e:
        st.error(f"Error loading benchmark_runs: {e}")
        return pd.DataFrame()

_TASK_LOG_QUERIES = {
    "extraction": "SELECT b.model_name, e.* FROM extraction_logs e JOIN benchmark_runs b ON e.run_id = b.id",
    "sql": "SELECT b.model_name, s.* FROM sql_logs s JOIN benchmark_runs b ON s.run_id = b.id",
    "math": "SELECT b.model_name, m.* FROM math_logs m JOIN benchmark_runs b ON m.run_id = b.id",
}

def load_task_logs(task: str) -> pd.DataFrame:
    """Load per-task logs joined with model names."""
    if not DB_PATH.exists():
        return pd.DataFrame()
    try:
        with sqlite3.connect(str(DB_PATH)) as conn:
            return pd.read_sql_query(_TASK_LOG_QUERIES[task], conn)
    except Exception as e:
        st.error(f"Error loading {task} logs: {e}")
        return pd.DataFrame()

# ------------------- Sidebar Controls -------------------
st.sidebar.header("Run Benchmark Suite")
available_models = get_available_models()
selected_models = st.sidebar.multiselect(
    "Select Models to Evaluate",
    options=available_models,
    default=available_models[:3] if len(available_models) >= 3 else available_models
)

# Task selection
task_options = ["extraction", "sql", "math"]
selected_tasks = st.sidebar.multiselect(
    "Select Tasks to Evaluate",
    options=task_options,
    default=task_options
)

tests_per_task = st.number_input(
    "Max tests per task",
    min_value=1,
    max_value=None,
    value=5,
    step=1,
    help="Limit the total number of test cases per task (sampled across categories) for faster debugging."
)

seed = st.number_input(
    "Random seed",
    min_value=0,
    max_value=None,
    value=42,
    step=1,
    help="Seed for sampling test cases. Reuse for reproducible runs, change for a different sample."
)

with st.sidebar.expander("🖥️ Hardware Cluster Config", expanded=True):
    cluster_name = st.text_input("Cluster Name", value="4x_RTX4090_Node")
    gpu_count = st.number_input("GPU Count", min_value=1, value=4, step=1)
    gpu_vram_gb = st.number_input("VRAM per GPU (GB)", min_value=1.0, value=24.0, step=2.0)
    upfront_cost_eur = st.number_input("Hardware Purchase (€)", min_value=0.0, value=8000.0, step=500.0)
    power_draw_kw = st.number_input("Power Draw (kW)", min_value=0.1, value=1.2, step=0.1)
    electricity_cost = st.number_input("Electricity Rate (€/kWh)", min_value=0.01, value=0.40, step=0.05)
    required_rps = st.number_input("Target Required RPS", min_value=0.1, value=5.0, step=0.5)

if "latest_summary" not in st.session_state:
    st.session_state["latest_summary"] = None

# Execute benchmark
if st.sidebar.button("Execute Benchmark"):
    if not selected_models:
        st.sidebar.error("Please select at least one model to benchmark.")
    elif not selected_tasks:
        st.sidebar.error("Please select at least one task to benchmark.")
    else:
        payload = {
            "models": selected_models,
            "tasks": selected_tasks,  # <-- send tasks list
            "tests_per_task": tests_per_task,
            "seed": seed,
            "required_rps": required_rps,
            "cluster_config": {
                "name": cluster_name,
                "gpu_count": gpu_count,
                "gpu_vram_gb": gpu_vram_gb,
                "upfront_cost_eur": upfront_cost_eur,
                "power_draw_kw": power_draw_kw,
                "electricity_cost_per_kwh": electricity_cost,
                "admin_hours_per_month": 4.0,
                "admin_hourly_rate_eur": 60.0
            }
        }
        try:
            res = requests.post("http://api:8000/api/v1/benchmark", json=payload, timeout=(5, 10))
            if res.status_code == 202:
                run_id = res.json().get("run_id")
                with status_container:
                    st.write("---")
                    st.subheader("⏳ Live Execution Status")
                    progress_bar = st.progress(0.0)
                    status_text = st.empty()
                with requests.Session() as session:
                    while True:
                        try:
                            status_res = session.get(f"http://api:8000/api/v1/status/{run_id}", timeout=(3, 5))
                            if status_res.status_code == 200:
                                status_data = status_res.json()
                                current_status = status_data.get("status")
                                progress_val = float(status_data.get("progress", 0.0))
                                msg = status_data.get("message", "Processing...")
                                progress_bar.progress(progress_val)
                                status_text.markdown(f"**Status:** {msg}")
                                if current_status == "completed":
                                    result_data = status_data.get("result", {})
                                    st.session_state["latest_summary"] = result_data.get("executive_summary")
                                    st.sidebar.success("Benchmark completed successfully!")
                                    time.sleep(1.5)
                                    st.rerun()
                                    break
                                elif current_status == "failed":
                                    st.sidebar.error(f"Benchmark failed: {msg}")
                                    break
                        except requests.exceptions.RequestException:
                            pass
                        time.sleep(1)
            else:
                st.sidebar.error(f"Trigger failed with status: {res.status_code}")
        except Exception as e:
            st.sidebar.error(f"Connection error: {e}")

# Display Executive Summary Callout
if st.session_state["latest_summary"]:
    st.subheader("💡 Executive Summary (Cloud Synthesis)")
    st.info(st.session_state["latest_summary"])
    st.divider()

# ------------------- Load Data -------------------
df_runs = load_benchmark_runs()
if df_runs.empty:
    st.warning("Database contains no records yet. Run a benchmark test from the sidebar!")
    st.stop()

# ------------------- Tabs -------------------
# Build tab list based on selected tasks
tab_names = ["Overview"]
if "extraction" in selected_tasks:
    tab_names.append("Extraction")
if "sql" in selected_tasks:
    tab_names.append("SQL")
if "math" in selected_tasks:
    tab_names.append("Math")
tab_names.append("Raw Data")

tabs = st.tabs(tab_names)

# --- Overview Tab ---
with tabs[0]:
    st.header("📊 Overall Performance")
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    # Overall accuracy: average across all runs (latest per model per task)
    latest_runs = df_runs.groupby(["model_name", "task"]).first().reset_index()
    avg_acc = latest_runs["accuracy"].mean()
    avg_lat = latest_runs["avg_latency_ms"].mean()
    avg_tps = latest_runs["avg_tps"].mean()
    total_runs = len(df_runs)
    col1.metric("Average Accuracy", f"{avg_acc:.1f}%")
    col2.metric("Average Latency", f"{avg_lat:.1f} ms")
    col3.metric("Average TPS", f"{avg_tps:.1f} tok/s")
    col4.metric("Total Runs", total_runs)

    st.divider()
    # Model ranking across tasks (grouped bar chart)
    st.subheader("Model Performance Across Tasks")
    # Aggregate: average accuracy per model per task
    agg_df = latest_runs.groupby(["model_name", "task"], as_index=False)["accuracy"].mean()
    fig_rank = px.bar(
        agg_df,
        x="model_name",
        y="accuracy",
        color="task",
        barmode="group",
        title="Accuracy per Model by Task",
        labels={"accuracy": "Accuracy (%)", "model_name": "Model"}
    )
    st.plotly_chart(fig_rank, use_container_width=True)

    # Speed comparison
    st.subheader("Speed Comparison (Latency per Task)")
    latency_df = latest_runs.groupby(["model_name", "task"], as_index=False)["avg_latency_ms"].mean()
    fig_lat = px.bar(
        latency_df,
        x="model_name",
        y="avg_latency_ms",
        color="task",
        barmode="group",
        title="Average Latency per Model by Task",
        labels={"avg_latency_ms": "Latency (ms)", "model_name": "Model"}
    )
    st.plotly_chart(fig_lat, use_container_width=True)

# --- Extraction Tab ---
if "extraction" in selected_tasks:
    tab_idx = tab_names.index("Extraction")
    with tabs[tab_idx]:
        st.header("📄 Extraction Task")
        df_ext = load_task_logs("extraction")
        if df_ext.empty:
            st.info("No extraction data available.")
        else:
            # KPI: overall F1, precision, recall per model
            ext_agg = df_ext.groupby("model_name", as_index=False).agg({
                "f1": "mean",
                "precision": "mean",
                "recall": "mean",
                "latency_ms": "mean"
            })
            ext_agg["f1"] *= 100
            ext_agg["precision"] *= 100
            ext_agg["recall"] *= 100
            col1, col2, col3, col4 = st.columns(4)
            best_f1_model = ext_agg.loc[ext_agg["f1"].idxmax()]
            col1.metric("Best F1", f"{best_f1_model['f1']:.1f}%", best_f1_model["model_name"])
            col2.metric("Avg Precision", f"{ext_agg['precision'].mean():.1f}%")
            col3.metric("Avg Recall", f"{ext_agg['recall'].mean():.1f}%")
            col4.metric("Avg Latency", f"{ext_agg['latency_ms'].mean():.1f} ms")

            # Per‑category F1 (like old)
            st.subheader("Per‑Category F1 Score")
            # compute per model, category
            cat_f1 = df_ext.groupby(["model_name", "category"], as_index=False)["f1"].mean()
            cat_f1["f1"] *= 100
            cat_f1["category_name"] = cat_f1["category"].astype(str).map({
                "1": "Biomedical / Health",
                "2": "Cybersecurity",
                "3": "Corporate Finance",
                "4": "Environmental Science",
                "5": "Law & Contract",
                "6": "Hardware Engineering",
                "7": "Educational Pedagogy",
                "8": "Cinema / Narrative Theory"
            }).fillna(cat_f1["category"].astype(str))
            fig_cat = px.bar(
                cat_f1,
                x="model_name",
                y="f1",
                color="category_name",
                barmode="group",
                title="F1 by Category",
                labels={"f1": "F1 (%)", "model_name": "Model"}
            )
            st.plotly_chart(fig_cat, use_container_width=True)

            # Model comparison bar chart
            st.subheader("Model Comparison (F1)")
            fig_ext = px.bar(
                ext_agg,
                x="model_name",
                y="f1",
                color="model_name",
                title="Extraction F1 per Model",
                text_auto='.1f',
                labels={"f1": "F1 (%)"}
            )
            fig_ext.update_traces(texttemplate='%{text}%', textposition='outside')
            st.plotly_chart(fig_ext, use_container_width=True)

# --- SQL Tab ---
if "sql" in selected_tasks:
    tab_idx = tab_names.index("SQL")
    with tabs[tab_idx]:
        st.header("🗄️ SQL Task")
        df_sql = load_task_logs("sql")
        if df_sql.empty:
            st.info("No SQL data available.")
        else:
            # Overall accuracy per model
            sql_agg = df_sql.groupby("model_name", as_index=False).agg({
                "is_correct": "mean",
                "latency_ms": "mean"
            })
            sql_agg["accuracy"] = sql_agg["is_correct"] * 100
            col1, col2, col3 = st.columns(3)
            best_sql = sql_agg.loc[sql_agg["accuracy"].idxmax()]
            col1.metric("Best Accuracy", f"{best_sql['accuracy']:.1f}%", best_sql["model_name"])
            col2.metric("Avg Accuracy", f"{sql_agg['accuracy'].mean():.1f}%")
            col3.metric("Avg Latency", f"{sql_agg['latency_ms'].mean():.1f} ms")

            st.subheader("SQL Accuracy per Model")
            fig_sql = px.bar(
                sql_agg,
                x="model_name",
                y="accuracy",
                color="model_name",
                title="SQL Accuracy",
                text_auto='.1f',
                labels={"accuracy": "Accuracy (%)"}
            )
            fig_sql.update_traces(texttemplate='%{text}%', textposition='outside')
            st.plotly_chart(fig_sql, use_container_width=True)

# --- Math Tab ---
if "math" in selected_tasks:
    tab_idx = tab_names.index("Math")
    with tabs[tab_idx]:
        st.header("🧮 Math Task")
        df_math = load_task_logs("math")
        if df_math.empty:
            st.info("No math data available.")
        else:
            # Per‑model accuracy
            math_agg = df_math.groupby("model_name", as_index=False).agg({
                "is_correct": "mean",
                "latency_ms": "mean"
            })
            math_agg["accuracy"] = math_agg["is_correct"] * 100
            col1, col2, col3 = st.columns(3)
            best_math = math_agg.loc[math_agg["accuracy"].idxmax()]
            col1.metric("Best Accuracy", f"{best_math['accuracy']:.1f}%", best_math["model_name"])
            col2.metric("Avg Accuracy", f"{math_agg['accuracy'].mean():.1f}%")
            col3.metric("Avg Latency", f"{math_agg['latency_ms'].mean():.1f} ms")

            # Math category breakdown (math_category)
            st.subheader("Per‑Math‑Category Accuracy")
            cat_math = df_math.groupby(["model_name", "math_category"], as_index=False)["is_correct"].mean()
            cat_math["accuracy"] = cat_math["is_correct"] * 100
            # map category numbers to names
            math_cat_names = {
                1: "Derivatives",
                2: "Integrals",
                3: "Equations",
                4: "Probability",
                5: "Linear Algebra",
                6: "Sequences",
                7: "Word Problems"
            }
            cat_math["math_category_name"] = cat_math["math_category"].map(math_cat_names).fillna(cat_math["math_category"].astype(str))
            fig_math_cat = px.bar(
                cat_math,
                x="model_name",
                y="accuracy",
                color="math_category_name",
                barmode="group",
                title="Accuracy by Math Category",
                labels={"accuracy": "Accuracy (%)", "model_name": "Model"}
            )
            st.plotly_chart(fig_math_cat, use_container_width=True)

            # Overall model comparison
            st.subheader("Math Accuracy per Model")
            fig_math = px.bar(
                math_agg,
                x="model_name",
                y="accuracy",
                color="model_name",
                title="Math Accuracy",
                text_auto='.1f',
                labels={"accuracy": "Accuracy (%)"}
            )
            fig_math.update_traces(texttemplate='%{text}%', textposition='outside')
            st.plotly_chart(fig_math, use_container_width=True)

# --- Raw Data Tab ---
with tabs[-1]:
    st.header("📋 Raw Telemetry Table")
    st.dataframe(df_runs, use_container_width=True)