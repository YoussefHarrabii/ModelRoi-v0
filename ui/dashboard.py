import sqlite3
from pathlib import Path
import time
import pandas as pd
import streamlit as st
import plotly.express as px
import requests

from app.config import DEFAULT_MODEL_REGISTRY, settings

st.set_page_config(page_title="ModelEval ROI Engine", layout="wide")

st.title("⚡ ModelEval ROI & Cluster Analytics")
st.markdown("Real-time telemetry, capacity scaling, and financial unit economics for local LLMs.")

status_container = st.sidebar.container()

# Force Absolute Path to SQLite Database
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "benchmark_history.db"

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


# --- Sidebar: Benchmark Execution Controls ---
st.sidebar.header("Run Benchmark Suite")
available_models = get_available_models()
selected_models = st.sidebar.multiselect(
    "Select Models to Evaluate",
    options=available_models,
    default=available_models[:3] if len(available_models) >= 3 else available_models
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

if st.sidebar.button("Execute Benchmark"):
    if not selected_models:
        st.sidebar.error("Please select at least one model to benchmark.")
    else:
        payload = {
            "models": selected_models,
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
                                
                                # Update progress bar and text live per prompt
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


def load_data() -> pd.DataFrame:
    """Reads top-level benchmark run history safely using context managers."""
    if not DB_PATH.exists():
        return pd.DataFrame()
    try:
        with sqlite3.connect(str(DB_PATH)) as conn:
            return pd.read_sql_query("SELECT * FROM benchmark_runs ORDER BY id DESC", conn)
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()


def load_category_breakdown() -> pd.DataFrame:
    """Reads detailed per-category prompt evaluation logs safely using context managers."""
    if not DB_PATH.exists():
        return pd.DataFrame()
    try:
        query = """
            SELECT 
                model_name,
                category AS category_id,
                COUNT(*) as total_cases,
                SUM(is_correct) as passed_cases,
                (CAST(SUM(is_correct) AS REAL) / COUNT(*)) * 100.0 as accuracy
            FROM prompt_logs
            GROUP BY model_name, category
            ORDER BY model_name, category
        """
        with sqlite3.connect(str(DB_PATH)) as conn:
            return pd.read_sql_query(query, conn)
    except Exception:
        return pd.DataFrame()


df = load_data()

if df.empty:
    st.warning("Database contains no records yet. Run a benchmark test from the sidebar!")
else:
    latest_df = df.groupby("model_name").first().reset_index()

    # --- KPI Summary Cards ---
    col1, col2, col3, col4, col5 = st.columns(5)
    top_acc = latest_df.sort_values(by="accuracy", ascending=False).iloc[0]
    top_tps = latest_df.sort_values(by="avg_tps", ascending=False).iloc[0]
    latest_tco = (
        latest_df["cluster_monthly_tco_eur"].dropna().iloc[0]
        if "cluster_monthly_tco_eur" in latest_df and not latest_df["cluster_monthly_tco_eur"].dropna().empty
        else None
    )

    col1.metric("Top Accuracy Model", top_acc["model_name"], f"{top_acc['accuracy']}%")
    col2.metric("Fastest TTFT", f"{latest_df['avg_ttft_ms'].min():.1f} ms")
    col3.metric("Peak Throughput", top_tps["model_name"], f"{top_tps['avg_tps']:.1f} tok/s")
    col4.metric("Cluster TCO", f"€{latest_tco:.2f}/mo" if latest_tco else "N/A")
    col5.metric("Total Runs Captured", len(df))

    st.divider()

    # --- SECTION 1: Accuracy & Cluster Capacity ---
    c_acc, c_rps = st.columns(2)
    with c_acc:
        st.subheader("🎯 Model Accuracy (%)")
        fig_acc = px.bar(latest_df, x="model_name", y="accuracy", color="model_name", text="accuracy", range_y=[0, 110])
        fig_acc.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig_acc, use_container_width=True)

    with c_rps:
        st.subheader("📊 Max Cluster Capacity (RPS)")
        if "max_rps" in latest_df and not latest_df["max_rps"].isna().all():
            fig_rps = px.bar(latest_df, x="model_name", y="max_rps", color="model_name", text_auto='.1f')
            st.plotly_chart(fig_rps, use_container_width=True)
        else:
            st.info("No cluster capacity data recorded yet.")

    st.divider()

    # --- SECTION 2: Generation Speed & Latency Breakdown ---
    st.subheader("⚡ Speed & Latency Telemetry")
    c_tps, c_ttft = st.columns(2)

    with c_tps:
        st.markdown("##### Token Generation Velocity (TPS)")
        fig_tps = px.bar(latest_df, x="model_name", y="avg_tps", color="model_name", text_auto='.1f')
        st.plotly_chart(fig_tps, use_container_width=True)

    with c_ttft:
        st.markdown("##### Time to First Token (TTFT - ms)")
        fig_ttft = px.bar(latest_df, x="model_name", y="avg_ttft_ms", color="model_name", text_auto='.1f')
        st.plotly_chart(fig_ttft, use_container_width=True)

    st.divider()

    # --- SECTION 3: Efficiency & Cloud Breakeven ---
    c_eff, c_break = st.columns(2)

    with c_eff:
        st.subheader("💡 Efficiency Score (Accuracy / Latency)")
        if "efficiency_score" in latest_df:
            fig_eff = px.bar(latest_df, x="model_name", y="efficiency_score", color="model_name", text_auto='.2f')
            st.plotly_chart(fig_eff, use_container_width=True)

    with c_break:
        st.subheader("📈 Monthly Cloud Breakeven Requests")
        if "breakeven_requests" in latest_df and not latest_df["breakeven_requests"].isna().all():
            fig_break = px.bar(latest_df, x="model_name", y="breakeven_requests", color="model_name", text_auto=',d')
            st.plotly_chart(fig_break, use_container_width=True)

    st.divider()

    # --- SECTION 4: Granular Category-Level Multi-Panel Bar Charts ---
    st.subheader("🧩 Granular Performance by Intent Category")
    st.markdown("Detailed breakdown tracking accuracy per model across individual intent categories.")

    df_cat = load_category_breakdown()

    if df_cat.empty:
        st.info("No granular prompt log records available yet. Run a new benchmark to populate category telemetry.")
    else:
        category_map = {
            "1": "Billing/Invoices",
            "2": "Technical Support",
            "3": "Account Management",
            "4": "Enterprise Sales",
            "5": "Feature Requests & Product Feedback",
            "6": "Security & Privacy",
            "7": "General Support & Onboarding",
            "8": "Spam"
        }
        df_cat["category_name"] = df_cat["category_id"].map(category_map).fillna(df_cat["category_id"].astype(str))

        unique_categories = df_cat["category_name"].unique()
        cat_cols = st.columns(2)
        for idx, cat_name in enumerate(sorted(unique_categories)):
            subset = df_cat[df_cat["category_name"] == cat_name]
            
            fig_cat = px.bar(
                subset, 
                x="model_name", 
                y="accuracy", 
                color="model_name",
                title=f"Category: {cat_name}",
                range_y=[0, 105],
                text="accuracy"
            )
            fig_cat.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_cat.update_layout(showlegend=False, height=350, margin=dict(t=40, b=20, l=20, r=20))
            
            with cat_cols[idx % 2]:
                st.plotly_chart(fig_cat, use_container_width=True)

    st.divider()
    st.subheader("🗄️ Raw Telemetry Table")
    st.dataframe(df, use_container_width=True)