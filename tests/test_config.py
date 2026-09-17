import os
import pytest
from pydantic import ValidationError
from app.config import (
    ModelConfig,
    ClusterConfig,
    Settings,
    DEFAULT_MODEL_REGISTRY,
)


# ----------------------------------------------------------------------
# 1. ModelConfig Validation Tests
# ----------------------------------------------------------------------

def test_01_model_config_valid_instantiation():
    model = ModelConfig(
        name="test-model",
        vram=4.0,
        provider_alias="Test-Provider",
        input_cost_per_1k=0.0001,
        output_cost_per_1k=0.0002
    )
    assert model.name == "test-model"
    assert model.vram == 4.0
    assert model.input_cost_per_1k == 0.0001
    assert model.output_cost_per_1k == 0.0002


def test_02_model_config_negative_costs_raise_validation_error():
    with pytest.raises(ValidationError):
        ModelConfig(
            name="invalid-model",
            vram=2.0,
            provider_alias="Bad-Provider",
            input_cost_per_1k=-0.01,  # ge=0.0 validation check
            output_cost_per_1k=0.0002
        )

    with pytest.raises(ValidationError):
        ModelConfig(
            name="invalid-model",
            vram=2.0,
            provider_alias="Bad-Provider",
            input_cost_per_1k=0.0001,
            output_cost_per_1k=-0.05  # ge=0.0 validation check
        )


def test_03_model_config_missing_required_fields():
    with pytest.raises(ValidationError):
        ModelConfig(name="incomplete-model")


# ----------------------------------------------------------------------
# 2. ClusterConfig Validation & Computed Properties Tests
# ----------------------------------------------------------------------

def test_04_cluster_config_valid_defaults():
    cluster = ClusterConfig(
        name="Small-Node",
        gpu_count=2,
        gpu_vram_gb=12.0,
        upfront_cost_eur=3600.0,
        power_draw_kw=0.5
    )
    assert cluster.lifespan_months == 36
    assert cluster.electricity_cost_per_kwh == 0.40
    assert cluster.admin_hours_per_month == 4.0
    assert cluster.admin_hourly_rate_eur == 60.0


def test_05_cluster_config_computed_properties():
    cluster = ClusterConfig(
        name="Calc-Node",
        gpu_count=4,
        gpu_vram_gb=16.0,
        upfront_cost_eur=7200.0,       # 7200 / 36 = 200.0
        power_draw_kw=1.0,             # 1.0 * 730.0 * 0.50 = 365.0
        lifespan_months=36,
        electricity_cost_per_kwh=0.50,
        admin_hours_per_month=5.0,     # 5.0 * 100.0 = 500.0
        admin_hourly_rate_eur=100.0
    )

    assert cluster.hardware_monthly_eur == pytest.approx(200.0)
    assert cluster.electricity_monthly_eur == pytest.approx(365.0)
    assert cluster.labor_monthly_eur == pytest.approx(500.0)
    assert cluster.total_monthly_tco_eur == pytest.approx(1065.0)


def test_06_cluster_config_invalid_gpu_count():
    with pytest.raises(ValidationError):
        ClusterConfig(
            name="Zero-GPU",
            gpu_count=0,  # ge=1 validation check
            gpu_vram_gb=16.0,
            upfront_cost_eur=1000.0,
            power_draw_kw=0.5
        )


def test_07_cluster_config_invalid_vram_or_power():
    with pytest.raises(ValidationError):
        ClusterConfig(
            name="Zero-VRAM",
            gpu_count=1,
            gpu_vram_gb=0.0,  # gt=0 validation check
            upfront_cost_eur=1000.0,
            power_draw_kw=0.5
        )

    with pytest.raises(ValidationError):
        ClusterConfig(
            name="Zero-Power",
            gpu_count=1,
            gpu_vram_gb=8.0,
            upfront_cost_eur=1000.0,
            power_draw_kw=0.0  # gt=0 validation check
        )


def test_08_cluster_config_negative_upfront_cost():
    with pytest.raises(ValidationError):
        ClusterConfig(
            name="Negative-Cost",
            gpu_count=1,
            gpu_vram_gb=8.0,
            upfront_cost_eur=-500.0,  # ge=0 validation check
            power_draw_kw=0.5
        )


# ----------------------------------------------------------------------
# 3. Model Registry Tests
# ----------------------------------------------------------------------

def test_09_default_model_registry_entries():
    assert len(DEFAULT_MODEL_REGISTRY) >= 9
    assert "gemma2:2b" in DEFAULT_MODEL_REGISTRY
    assert "llama3.2:3b" in DEFAULT_MODEL_REGISTRY
    assert "phi4-mini:latest" in DEFAULT_MODEL_REGISTRY


def test_10_default_model_registry_types():
    for name, config in DEFAULT_MODEL_REGISTRY.items():
        assert isinstance(config, ModelConfig)
        assert config.name == name
        assert config.vram > 0.0
        assert config.input_cost_per_1k >= 0.0
        assert config.output_cost_per_1k >= 0.0


# ----------------------------------------------------------------------
# 4. Global Settings & Environment Override Tests
# ----------------------------------------------------------------------

def test_11_settings_default_values():
    settings = Settings()
    assert settings.PROJECT_NAME == "ModelEval ROI Engine"
    assert settings.VERSION == "0.1.0"
    assert settings.OLLAMA_HOST == "http://localhost:11434"
    assert settings.DEFAULT_CLUSTER.name == "4xA4000-Inference-Node"


def test_12_settings_environment_variable_override(monkeypatch):
    monkeypatch.setenv("PROJECT_NAME", "Custom ROI Engine")
    monkeypatch.setenv("OLLAMA_HOST", "http://ollama-container:11434")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-testkey123")

    custom_settings = Settings()
    assert custom_settings.PROJECT_NAME == "Custom ROI Engine"
    assert custom_settings.OLLAMA_HOST == "http://ollama-container:11434"
    assert custom_settings.OPENROUTER_API_KEY == "sk-or-v1-testkey123"


def test_13_settings_extra_environment_vars_ignored(monkeypatch):
    monkeypatch.setenv("UNRECOGNIZED_ENV_VAR", "some_value")
    # Should not raise a ValidationError due to extra="ignore"
    custom_settings = Settings()
    assert custom_settings.PROJECT_NAME == "ModelEval ROI Engine"


def test_14_settings_default_cluster_computed_tco():
    settings = Settings()
    cluster = settings.DEFAULT_CLUSTER
    
    # 9400 / 36 = ~261.11
    # 0.9 * 730 * 0.40 = 262.80
    # 4.0 * 60.0 = 240.00
    # Total TCO = ~763.91
    assert cluster.total_monthly_tco_eur == pytest.approx(763.91, rel=1e-3)