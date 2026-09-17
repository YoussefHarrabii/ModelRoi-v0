import pytest
from unittest.mock import MagicMock, patch
from typing import NamedTuple

from app.calculator import (
    calculate_cluster_tco,
    calculate_cluster_throughput,
    calculate_cluster_breakeven,
    calculate_financial_roi,
)
from app.config import ClusterConfig


# ---------------------------------------------------------------------------
# Fixtures & Mocks
# ---------------------------------------------------------------------------

@pytest.fixture
def base_cluster():
    """Provides a standard ClusterConfig fixture for predictable testing."""
    return ClusterConfig(
        name="Test-Cluster-A100",
        gpu_count=4,
        gpu_vram_gb=80.0,
        upfront_cost_eur=20000.0,
        power_draw_kw=1.5,
        electricity_cost_per_kwh=0.30,
        admin_hours_per_month=10.0,
        admin_hourly_rate_eur=50.0,
        lifespan_months=36,
    )


class MockModelConfig(NamedTuple):
    input_cost_per_1k: float
    output_cost_per_1k: float
    provider_alias: str
    vram: float


@pytest.fixture
def mock_settings_registry():
    """Mocks settings.model_registry for calculate_financial_roi tests."""
    with patch("app.calculator.settings") as mock_settings:
        mock_settings.model_registry = {
            "gemma2:2b": MockModelConfig(
                input_cost_per_1k=0.0001,
                output_cost_per_1k=0.0002,
                provider_alias="Google",
                vram=3.0,
            ),
            "llama3:8b": MockModelConfig(
                input_cost_per_1k=0.0005,
                output_cost_per_1k=0.0015,
                provider_alias="Meta",
                vram=8.0,
            ),
        }
        yield mock_settings


# ---------------------------------------------------------------------------
# 1. Tests for calculate_cluster_tco (Tests 1–10)
# ---------------------------------------------------------------------------

def test_tco_basic_calculation(base_cluster):
    """Test 1: Normal TCO dict structure and fields."""
    res = calculate_cluster_tco(base_cluster)
    assert res["cluster_name"] == "Test-Cluster-A100"
    assert res["upfront_cost_eur"] == 20000.0
    assert res["lifespan_months"] == 36
    assert isinstance(res["total_monthly_tco_eur"], float)


def test_tco_rounding_precision(base_cluster):
    """Test 2: Verify rounding outputs to two decimal places."""
    base_cluster.upfront_cost_eur = 10000.33333
    res = calculate_cluster_tco(base_cluster)
    assert res["hardware_monthly_eur"] == round(base_cluster.hardware_monthly_eur, 2)
    assert res["electricity_monthly_eur"] == round(base_cluster.electricity_monthly_eur, 2)
    assert res["labor_monthly_eur"] == round(base_cluster.labor_monthly_eur, 2)
    assert res["total_monthly_tco_eur"] == round(base_cluster.total_monthly_tco_eur, 2)


@pytest.mark.parametrize("upfront, lifespan", [
    (12000.0, 12),
    (24000.0, 24),
    (36000.0, 36),
    (0.0, 36),
])
def test_tco_varying_lifespans(base_cluster, upfront, lifespan):
    """Tests 3–6: Check TCO across different hardware lifespans."""
    base_cluster.upfront_cost_eur = upfront
    base_cluster.lifespan_months = lifespan
    res = calculate_cluster_tco(base_cluster)
    expected_hardware_monthly = upfront / lifespan if lifespan > 0 else 0
    assert res["hardware_monthly_eur"] == round(expected_hardware_monthly, 2)


def test_tco_zero_labor_and_electricity(base_cluster):
    """Test 7: Verify zero operational costs."""
    base_cluster.power_draw_kw = 0.0
    base_cluster.admin_hours_per_month = 0.0
    res = calculate_cluster_tco(base_cluster)
    assert res["electricity_monthly_eur"] == 0.0
    assert res["labor_monthly_eur"] == 0.0


def test_tco_large_cluster_numbers():
    """Test 8: Handle large enterprise data without numeric overflow."""
    huge_cluster = ClusterConfig(
        name="Mega-DataCenter",
        gpu_count=1024,
        gpu_vram_gb=80.0,
        upfront_cost_eur=10_000_000.0,
        power_draw_kw=500.0,
        electricity_cost_per_kwh=0.15,
        admin_hours_per_month=160.0,
        admin_hourly_rate_eur=100.0,
        lifespan_months=60,
    )
    res = calculate_cluster_tco(huge_cluster)
    assert res["total_monthly_tco_eur"] > 200_000.0


def test_tco_dict_keys_completeness(base_cluster):
    """Test 9: Assert all required keys exist in dictionary."""
    expected_keys = {
        "cluster_name", "upfront_cost_eur", "hardware_monthly_eur",
        "electricity_monthly_eur", "labor_monthly_eur",
        "total_monthly_tco_eur", "lifespan_months"
    }
    res = calculate_cluster_tco(base_cluster)
    assert set(res.keys()) == expected_keys


def test_tco_immutability_of_cluster(base_cluster):
    """Test 10: Ensure function does not mutate input object properties."""
    orig_upfront = base_cluster.upfront_cost_eur
    _ = calculate_cluster_tco(base_cluster)
    assert base_cluster.upfront_cost_eur == orig_upfront


# ---------------------------------------------------------------------------
# 2. Tests for calculate_cluster_throughput (Tests 11–22)
# ---------------------------------------------------------------------------

def test_throughput_basic(base_cluster):
    """Test 11: Standard throughput calculation test."""
    res = calculate_cluster_throughput(
        cluster=base_cluster,
        model_vram_gb=16.0,
        base_latency_ms=200.0,
        single_instance_rps=5.0,
    )
    # 80GB VRAM * 0.8 headroom = 64GB available / 16GB = 4 models per GPU
    # 4 models * 4 GPUs = 16 total concurrent models
    assert res["models_per_gpu"] == 4
    assert res["total_concurrent_models"] == 16
    assert res["max_rps"] == 80.0  # 16 * 5.0


def test_throughput_min_one_model_per_gpu(base_cluster):
    """Test 12: Ensure models_per_gpu uses max(1, ...) when model VRAM is huge."""
    res = calculate_cluster_throughput(
        cluster=base_cluster,
        model_vram_gb=100.0,  # Larger than 80GB GPU
        base_latency_ms=500.0,
        single_instance_rps=1.0,
    )
    assert res["models_per_gpu"] == 1
    assert res["total_concurrent_models"] == 4


def test_throughput_loaded_latency(base_cluster):
    """Test 13: Verify latency penalty scaling under load."""
    # total_concurrent_models = 4 models/GPU * 4 GPUs = 16
    # penalty = 0.15 * 16 = 2.4 multiplier increase -> base * (1 + 2.4) = 100 * 3.4 = 340
    res = calculate_cluster_throughput(
        cluster=base_cluster,
        model_vram_gb=16.0,
        base_latency_ms=100.0,
        single_instance_rps=2.0,
        latency_penalty_per_instance=0.15,
    )
    assert res["latency_under_load_ms"] == 340.0


@pytest.mark.parametrize("headroom, expected_models", [
    (0.5, 2),  # 80 * 0.5 / 16 = 2
    (0.8, 4),  # 80 * 0.8 / 16 = 4
    (1.0, 5),  # 80 * 1.0 / 16 = 5
])
def test_throughput_headroom_variations(base_cluster, headroom, expected_models):
    """Tests 14–16: Validate VRAM headroom scaling behavior."""
    res = calculate_cluster_throughput(
        cluster=base_cluster,
        model_vram_gb=16.0,
        base_latency_ms=100.0,
        single_instance_rps=1.0,
        vram_headroom=headroom,
    )
    assert res["models_per_gpu"] == expected_models


def test_throughput_zero_single_instance_rps(base_cluster):
    """Test 17: Zero RPS input should produce 0 max_rps."""
    res = calculate_cluster_throughput(
        cluster=base_cluster,
        model_vram_gb=8.0,
        base_latency_ms=100.0,
        single_instance_rps=0.0,
    )
    assert res["max_rps"] == 0.0


def test_throughput_single_gpu_cluster():
    """Test 18: Validate throughput calculation on single-GPU hardware."""
    single_gpu = ClusterConfig(
        name="Single-RTX4090",
        gpu_count=1,
        gpu_vram_gb=24.0,
        upfront_cost_eur=2000.0,
        power_draw_kw=0.45,
        electricity_cost_per_kwh=0.30,
        admin_hours_per_month=1.0,
        admin_hourly_rate_eur=50.0,
        lifespan_months=24,
    )
    res = calculate_cluster_throughput(
        cluster=single_gpu,
        model_vram_gb=6.0,
        base_latency_ms=50.0,
        single_instance_rps=10.0,
        vram_headroom=0.75,  # 24 * 0.75 = 18 / 6 = 3
    )
    assert res["total_concurrent_models"] == 3
    assert res["max_rps"] == 30.0


@pytest.mark.parametrize("base_lat, penalty, expected_lat", [
    (100.0, 0.0, 100.0),    # Zero penalty
    (100.0, 0.1, 260.0),    # 100 * (1 + 0.1 * 16)
    (50.0, 0.2, 210.0),     # 50 * (1 + 0.2 * 16)
])
def test_throughput_penalty_variations(base_cluster, base_lat, penalty, expected_lat):
    """Tests 19–21: Test different penalty rates on loaded latency."""
    res = calculate_cluster_throughput(
        cluster=base_cluster,
        model_vram_gb=16.0,
        base_latency_ms=base_lat,
        single_instance_rps=1.0,
        latency_penalty_per_instance=penalty,
    )
    assert res["latency_under_load_ms"] == expected_lat


def test_throughput_keys_structure(base_cluster):
    """Test 22: Confirm all expected throughput keys exist."""
    res = calculate_cluster_throughput(base_cluster, 8.0, 100.0, 1.0)
    expected = {
        "cluster_name", "gpu_count", "gpu_vram_gb", "model_vram_gb",
        "models_per_gpu", "total_concurrent_models", "max_rps",
        "base_latency_ms", "latency_under_load_ms", "vram_headroom"
    }
    assert set(res.keys()) == expected


# ---------------------------------------------------------------------------
# 3. Tests for calculate_cluster_breakeven (Tests 23–34)
# ---------------------------------------------------------------------------

def test_breakeven_unfeasible_capacity(base_cluster):
    """Test 23: Return infeasible payload when required_rps exceeds cluster_max_rps."""
    res = calculate_cluster_breakeven(
        cluster=base_cluster,
        cloud_cost_per_request_eur=0.001,
        required_rps=100.0,
        cluster_max_rps=50.0,
    )
    assert res["feasible"] is False
    assert "Cluster max 50.0 RPS < required 100.0 RPS" in res["reason"]
    assert res["cloud_cheaper_above_requests"] is None
    assert res["recommendation"] == "Scale cluster or use cloud"
    assert res["utilization_pct"] == 200.0


def test_breakeven_feasible_calculation(base_cluster):
    """Test 24: Standard feasible breakeven calculation."""
    res = calculate_cluster_breakeven(
        cluster=base_cluster,
        cloud_cost_per_request_eur=0.001,
        required_rps=10.0,
        cluster_max_rps=50.0,
    )
    assert res["feasible"] is True
    assert res["utilization_pct"] == 20.0

    # Calculate expected requests using rounded TCO to prevent float drift
    expected_requests = round(res["cluster_monthly_tco_eur"] / 0.001)
    
    # Use absolute tolerance (abs=10) to account for integer rounding boundaries
    assert res["breakeven_monthly_requests"] == pytest.approx(expected_requests, abs=10)


def test_breakeven_zero_cloud_cost(base_cluster):
    """Test 25: Handle zero cloud cost per request gracefully (no ZeroDivisionError)."""
    res = calculate_cluster_breakeven(
        cluster=base_cluster,
        cloud_cost_per_request_eur=0.0,
        required_rps=5.0,
        cluster_max_rps=10.0,
    )
    assert res["feasible"] is True
    assert res["breakeven_monthly_requests"] == 0


def test_breakeven_zero_cluster_max_rps(base_cluster):
    """Test 26: Handle zero cluster_max_rps without ZeroDivisionError."""
    res = calculate_cluster_breakeven(
        cluster=base_cluster,
        cloud_cost_per_request_eur=0.001,
        required_rps=1.0,
        cluster_max_rps=0.0,
    )
    assert res["feasible"] is False
    assert res["utilization_pct"] == float("inf")


@pytest.mark.parametrize("req_rps, max_rps, expected_util", [
    (10.0, 100.0, 10.0),
    (50.0, 100.0, 50.0),
    (100.0, 100.0, 100.0),
])
def test_breakeven_utilization_percentages(base_cluster, req_rps, max_rps, expected_util):
    """Tests 27–29: Verify utilization percentage calculation."""
    res = calculate_cluster_breakeven(
        cluster=base_cluster,
        cloud_cost_per_request_eur=0.01,
        required_rps=req_rps,
        cluster_max_rps=max_rps,
    )
    assert res["utilization_pct"] == expected_util


def test_breakeven_recommendation_string_formatting(base_cluster):
    """Test 30: Check that the formatted recommendation string includes commas."""
    res = calculate_cluster_breakeven(
        cluster=base_cluster,
        cloud_cost_per_request_eur=0.00001,
        required_rps=1.0,
        cluster_max_rps=10.0,
    )
    assert "Cloud cheaper below" in res["recommendation"]
    assert "req/mo; cluster cheaper above" in res["recommendation"]


def test_breakeven_cloud_cost_rounding_precision(base_cluster):
    """Test 31: Verify cloud_cost_per_request_eur is rounded to 6 decimal places."""
    res = calculate_cluster_breakeven(
        cluster=base_cluster,
        cloud_cost_per_request_eur=0.0001234567,
        required_rps=1.0,
        cluster_max_rps=10.0,
    )
    assert res["cloud_cost_per_request_eur"] == 0.000123


def test_breakeven_equal_required_and_max_rps(base_cluster):
    """Test 32: Edge case where required_rps == cluster_max_rps (Boundary: feasible)."""
    res = calculate_cluster_breakeven(
        cluster=base_cluster,
        cloud_cost_per_request_eur=0.001,
        required_rps=25.0,
        cluster_max_rps=25.0,
    )
    assert res["feasible"] is True
    assert res["utilization_pct"] == 100.0


def test_breakeven_slightly_exceeding_max_rps(base_cluster):
    """Test 33: Edge case where required_rps > cluster_max_rps by a tiny fraction."""
    res = calculate_cluster_breakeven(
        cluster=base_cluster,
        cloud_cost_per_request_eur=0.001,
        required_rps=25.001,
        cluster_max_rps=25.0,
    )
    assert res["feasible"] is False


def test_breakeven_keys_completeness(base_cluster):
    """Test 34: Check returned keys for feasible output."""
    res = calculate_cluster_breakeven(base_cluster, 0.001, 1.0, 10.0)
    expected_keys = {
        "feasible", "cluster_monthly_tco_eur", "required_rps",
        "cluster_max_rps", "cloud_cost_per_request_eur",
        "breakeven_monthly_requests", "cloud_cheaper_above_requests",
        "cluster_cheaper_above_requests", "utilization_pct", "recommendation"
    }
    assert set(res.keys()) == expected_keys


# ---------------------------------------------------------------------------
# 4. Tests for calculate_financial_roi (Tests 35–52)
# ---------------------------------------------------------------------------

def test_roi_unregistered_model_raises_value_error(mock_settings_registry):
    """Test 35: Raising ValueError when model is missing from registry."""
    with pytest.raises(ValueError, match="Model 'unknown_model' not found in registry."):
        calculate_financial_roi(
            model_name="unknown_model",
            total_input_tokens=1000,
            total_output_tokens=500,
            total_requests=10,
            local_avg_latency_ms=200.0,
            local_accuracy=90.0,
        )


def test_roi_without_cluster(mock_settings_registry):
    """Test 36: Calculate ROI without providing cluster config."""
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=10_000,
        total_output_tokens=5_000,
        total_requests=10,
        local_avg_latency_ms=200.0,
        local_accuracy=80.0,
    )
    assert res["model_name"] == "gemma2:2b"
    assert res["provider_alias"] == "Google"
    assert res["model_vram_gb"] == 3.0
    assert res["cluster_analysis"] is None
    # 10k * 0.0001 / 1k = 0.001 input cost
    # 5k * 0.0002 / 1k = 0.001 output cost -> Total = 0.002
    assert res["total_run_cloud_cost_eur"] == 0.002
    assert res["cloud_cost_per_request_eur"] == 0.0002


def test_roi_efficiency_score(mock_settings_registry):
    """Test 37: Validate efficiency score calculation (Accuracy / Latency in seconds)."""
    # Latency: 500ms = 0.5s -> Accuracy: 90.0 / 0.5 = 180.0
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=100,
        total_output_tokens=100,
        total_requests=1,
        local_avg_latency_ms=500.0,
        local_accuracy=90.0,
    )
    assert res["efficiency_score"] == 180.0


def test_roi_zero_latency_efficiency_score(mock_settings_registry):
    """Test 38: Handle 0 latency without ZeroDivisionError."""
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=100,
        total_output_tokens=100,
        total_requests=1,
        local_avg_latency_ms=0.0,
        local_accuracy=90.0,
    )
    assert res["efficiency_score"] == 0.0


def test_roi_zero_total_requests(mock_settings_registry):
    """Test 39: Zero requests should yield cloud_cost_per_request_eur = 0.0."""
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=1000,
        total_output_tokens=500,
        total_requests=0,
        local_avg_latency_ms=100.0,
        local_accuracy=100.0,
    )
    assert res["cloud_cost_per_request_eur"] == 0.0


def test_roi_with_cluster(mock_settings_registry, base_cluster):
    """Test 40: Calculate ROI with cluster integration."""
    res = calculate_financial_roi(
        model_name="llama3:8b",
        total_input_tokens=20_000,
        total_output_tokens=10_000,
        total_requests=50,
        local_avg_latency_ms=250.0,
        local_accuracy=85.0,
        cluster=base_cluster,
        required_rps=2.0,
    )
    assert res["cluster_analysis"] is not None
    assert "tco" in res["cluster_analysis"]
    assert "throughput" in res["cluster_analysis"]
    assert "breakeven" in res["cluster_analysis"]


@pytest.mark.parametrize("input_tokens, output_tokens, expected_cost", [
    (0, 0, 0.0),
    (1000, 1000, 0.0003),  # (1 * 0.0001) + (1 * 0.0002)
    (5000, 2000, 0.0009),  # (5 * 0.0001) + (2 * 0.0002)
])
def test_roi_cloud_cost_token_scaling(mock_settings_registry, input_tokens, output_tokens, expected_cost):
    """Tests 41–43: Check simulated cloud API cost across different token volumes."""
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=input_tokens,
        total_output_tokens=output_tokens,
        total_requests=1,
        local_avg_latency_ms=100.0,
        local_accuracy=100.0,
    )
    assert res["total_run_cloud_cost_eur"] == expected_cost


def test_roi_single_instance_rps_derivation(mock_settings_registry, base_cluster):
    """Test 44: Single instance RPS derived from local average latency (1000 / latency_ms)."""
    # 200ms latency = 5.0 RPS
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=1000,
        total_output_tokens=1000,
        total_requests=10,
        local_avg_latency_ms=200.0,
        local_accuracy=90.0,
        cluster=base_cluster,
    )
    throughput = res["cluster_analysis"]["throughput"]
    # 80GB * 0.8 / 3.0 VRAM = 21 models per GPU * 4 GPUs = 84 models
    # 84 models * 5.0 single_instance_rps = 420.0 max_rps
    assert throughput["max_rps"] == 420.0


def test_roi_default_required_rps_fallback(mock_settings_registry, base_cluster):
    """Test 45: Verify default required_rps=1.0 fallback parameter."""
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=1000,
        total_output_tokens=1000,
        total_requests=10,
        local_avg_latency_ms=200.0,
        local_accuracy=90.0,
        cluster=base_cluster,
    )
    assert res["cluster_analysis"]["breakeven"]["required_rps"] == 1.0


def test_roi_top_level_dict_keys(mock_settings_registry):
    """Test 46: Check structure of top-level ROI payload without cluster."""
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=100,
        total_output_tokens=100,
        total_requests=1,
        local_avg_latency_ms=100.0,
        local_accuracy=100.0,
    )
    expected_keys = {
        "model_name", "provider_alias", "model_vram_gb",
        "total_input_tokens", "total_output_tokens",
        "total_run_cloud_cost_eur", "cloud_cost_per_request_eur",
        "efficiency_score", "cluster_analysis"
    }
    assert set(res.keys()) == expected_keys


def test_roi_large_token_counts(mock_settings_registry):
    """Test 47: Check numerical precision with millions of tokens."""
    res = calculate_financial_roi(
        model_name="llama3:8b",
        total_input_tokens=10_000_000,  # 10k units * 0.0005 = 5.0
        total_output_tokens=5_000_000,   # 5k units * 0.0015 = 7.5
        total_requests=100_000,
        local_avg_latency_ms=150.0,
        local_accuracy=92.5,
    )
    assert res["total_run_cloud_cost_eur"] == 12.5
    assert res["cloud_cost_per_request_eur"] == 0.000125


def test_roi_zero_accuracy_efficiency_score(mock_settings_registry):
    """Test 48: Zero accuracy yields 0.0 efficiency score."""
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=100,
        total_output_tokens=100,
        total_requests=1,
        local_avg_latency_ms=100.0,
        local_accuracy=0.0,
    )
    assert res["efficiency_score"] == 0.0


@pytest.mark.parametrize("latency, accuracy, expected_score", [
    (1000.0, 100.0, 100.0),   # 100 / 1s
    (2000.0, 50.0, 25.0),     # 50 / 2s
    (250.0, 75.0, 300.0),     # 75 / 0.25s
])
def test_roi_efficiency_score_parameterized(mock_settings_registry, latency, accuracy, expected_score):
    """Tests 49–51: Validate efficiency scores across different latencies and accuracies."""
    res = calculate_financial_roi(
        model_name="gemma2:2b",
        total_input_tokens=100,
        total_output_tokens=100,
        total_requests=1,
        local_avg_latency_ms=latency,
        local_accuracy=accuracy,
    )
    assert res["efficiency_score"] == expected_score


def test_roi_cluster_analysis_nested_structure(mock_settings_registry, base_cluster):
    """Test 52: Verify all sub-dictionary components exist in cluster analysis."""
    res = calculate_financial_roi(
        model_name="llama3:8b",
        total_input_tokens=1000,
        total_output_tokens=1000,
        total_requests=10,
        local_avg_latency_ms=200.0,
        local_accuracy=90.0,
        cluster=base_cluster,
    )
    analysis = res["cluster_analysis"]
    assert set(analysis.keys()) == {"tco", "throughput", "breakeven"}