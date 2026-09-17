from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseModel):
    name: str = Field(..., description="Actual model identifier")
    vram: float = Field(..., description="Vram occupancy")
    provider_alias: str = Field(..., description="Simulated commercial provider name")
    input_cost_per_1k: float = Field(..., ge=0.0, description="Simulated cost per 1,000 input tokens in EURO")
    output_cost_per_1k: float = Field(..., ge=0.0, description="Simulated cost per 1,000 output tokens in EURO")

class ClusterConfig(BaseModel):
    name: str = Field(..., description="Cluster identifier")
    gpu_count: int = Field(..., ge=1, description="Number of GPUs")
    gpu_vram_gb: float = Field(..., gt=0, description="VRAM per GPU in GB")
    upfront_cost_eur: float = Field(..., ge=0, description="Total hardware purchase cost")
    power_draw_kw: float = Field(..., gt=0, description="Power consumption under load in kilowatts")
    lifespan_months: int = Field(default=36, ge=1, description="Hardware amortization period")
    electricity_cost_per_kwh: float = Field(default=0.40, gt=0, description="Electricity rate in EUR/kWh")
    admin_hours_per_month: float = Field(default=4.0, ge=0, description="Monthly maintenance labor hours")
    admin_hourly_rate_eur: float = Field(default=60.0, ge=0, description="Labor cost per hour in EUR")

    @property
    def hardware_monthly_eur(self) -> float:
        return self.upfront_cost_eur / self.lifespan_months

    @property
    def electricity_monthly_eur(self) -> float:
        hours_per_month = 730.0
        return self.power_draw_kw * hours_per_month * self.electricity_cost_per_kwh

    @property
    def labor_monthly_eur(self) -> float:
        return self.admin_hours_per_month * self.admin_hourly_rate_eur

    @property
    def total_monthly_tco_eur(self) -> float:
        return self.hardware_monthly_eur + self.electricity_monthly_eur + self.labor_monthly_eur


# Pluggable Pricing Registry (Fictionalized/Simulated Commercial Tiers)
DEFAULT_MODEL_REGISTRY: dict[str, ModelConfig] = {
    # 2B Class
    "gemma2:2b": ModelConfig(
        name="gemma2:2b",
        vram=1.6,
        provider_alias="Local-Google-Compact",
        input_cost_per_1k=0.00004,
        output_cost_per_1k=0.00015,
    ),
    "granite3.1-dense:2b": ModelConfig(
        name="granite3.1-dense:2b",
        vram=1.6,
        provider_alias="Local-IBM-Enterprise",
        input_cost_per_1k=0.00006,
        output_cost_per_1k=0.00022,
    ),
    "qwen3.5:2b": ModelConfig(
        name="qwen3.5:2b",
        vram=2.7,
        provider_alias="Local-Alibaba-UltraLite",
        input_cost_per_1k=0.00003,
        output_cost_per_1k=0.00012,
    ),
    "qwen-legal:latest": ModelConfig(
            name="qwen-legal:latest",
            vram=1.6,
            provider_alias="Local-be-UltraLite",
            input_cost_per_1k=0.00003,
            output_cost_per_1k=0.00012,
        ),
    # 3B Class
    "llama3.2:3b": ModelConfig(
        name="llama3.2:3b",
        vram=2.0,
        provider_alias="Local-Meta-Fast",
        input_cost_per_1k=0.00005,
        output_cost_per_1k=0.00033,
    ),
    "qwen2.5:3b-instruct": ModelConfig(
        name="qwen2.5:3b-instruct",
        vram=1.9,
        provider_alias="Local-Alibaba-Lite",
        input_cost_per_1k=0.00008,
        output_cost_per_1k=0.00035,
    ),
    "phi3:latest": ModelConfig(
        name="phi3:latest",
        vram=2.2,
        provider_alias="Local-Redmond-Demo",
        input_cost_per_1k=0.00007,
        output_cost_per_1k=0.00028,
    ),

    # 4B Class
    "gemma3:4b": ModelConfig(
        name="gemma3:4b",
        vram=3.3,
        provider_alias="Local-Google-Midtier",
        input_cost_per_1k=0.00012,
        output_cost_per_1k=0.00045,
    ),
    "phi4-mini:latest": ModelConfig(
        name="phi4-mini:latest",
        vram=2.2,
        provider_alias="Local-Redmond-SmartMini",
        input_cost_per_1k=0.00015,
        output_cost_per_1k=0.00050,
    ),
    "qwen3.5:4b": ModelConfig(
        name="qwen3.5:4b",
        vram=3.4,
        provider_alias="Local-Alibaba-Balanced",
        input_cost_per_1k=0.00010,
        output_cost_per_1k=0.00040,
    ),
}


class Settings(BaseSettings):
    """Global Application Settings loaded from environment variables or .env file."""
    
    # App Information
    PROJECT_NAME: str = "ModelEval ROI Engine"
    VERSION: str = "0.1.0"
    
    # Ollama Host Setup
    OLLAMA_HOST: str = Field(
        default="http://localhost:11434",
        description="Ollama server endpoint (Docker uses http://host.docker.internal:11434)"
    )
    
    # Financial Scale Defaults
    # OpenRouter / Cloud Synthesis Settings
    OPENROUTER_API_KEY: str = Field(
        default="",
        description="OpenRouter API key for external cloud synthesis"
    )
    OPENROUTER_MODEL: str = Field(
        default="nvidia/nemotron-3-ultra-550b-a55b:free",
        description="OpenRouter target model slug for executive summaries"
    )
    
    # Active Models Registry
    model_registry: dict[str, ModelConfig] = DEFAULT_MODEL_REGISTRY

    # FIX: Added explicit type annotation (ClusterConfig) so Pydantic v2 validates it
    DEFAULT_CLUSTER: ClusterConfig = ClusterConfig(
        name="4xA4000-Inference-Node",
        gpu_count=4,
        gpu_vram_gb=16.0,
        upfront_cost_eur=9400.0,
        power_draw_kw=0.9,
    )

    # Pydantic-Settings V2 Config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instantiated global settings object
settings = Settings()