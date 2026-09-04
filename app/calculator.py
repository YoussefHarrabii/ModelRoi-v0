from typing import Dict, Any, Optional
from app.config import settings
from app.config import ClusterConfig

def calculate_cluster_tco(cluster: ClusterConfig) -> dict[str, Any]:
    return {
        "cluster_name": cluster.name,
        "upfront_cost_eur": cluster.upfront_cost_eur,
        "hardware_monthly_eur": round(cluster.hardware_monthly_eur, 2),
        "electricity_monthly_eur": round(cluster.electricity_monthly_eur, 2),
        "labor_monthly_eur": round(cluster.labor_monthly_eur, 2),
        "total_monthly_tco_eur": round(cluster.total_monthly_tco_eur, 2),
        "lifespan_months": cluster.lifespan_months,
    }


def calculate_cluster_throughput(
    cluster: ClusterConfig,
    model_vram_gb: float,
    base_latency_ms: float,
    single_instance_rps: float,
    vram_headroom: float = 0.8,
    latency_penalty_per_instance: float = 0.15,
) -> dict[str, Any]:
    models_per_gpu = max(1, int((cluster.gpu_vram_gb / model_vram_gb) * vram_headroom))
    total_concurrent_models = models_per_gpu * cluster.gpu_count
    max_rps = total_concurrent_models * single_instance_rps
    
    loaded_latency_ms = base_latency_ms * (1 + latency_penalty_per_instance * total_concurrent_models)
    
    return {
        "cluster_name": cluster.name,
        "gpu_count": cluster.gpu_count,
        "gpu_vram_gb": cluster.gpu_vram_gb,
        "model_vram_gb": model_vram_gb,
        "models_per_gpu": models_per_gpu,
        "total_concurrent_models": total_concurrent_models,
        "max_rps": round(max_rps, 2),
        "base_latency_ms": round(base_latency_ms, 2),
        "latency_under_load_ms": round(loaded_latency_ms, 2),
        "vram_headroom": vram_headroom,
    }


def calculate_cluster_breakeven(
    cluster: ClusterConfig,
    cloud_cost_per_request_eur: float,
    required_rps: float,
    cluster_max_rps: float,
) -> dict[str, Any]:
    cluster_monthly = round(cluster.total_monthly_tco_eur, 2)

    # 1. Calculate utilization safely to prevent ZeroDivisionError
    if cluster_max_rps > 0:
        utilization_pct = round((required_rps / cluster_max_rps) * 100, 1)
    else:
        # Infinite utilization if capacity is zero but demand exists
        utilization_pct = float("inf") if required_rps > 0 else 0.0

    # 2. Check capacity feasibility
    if required_rps > cluster_max_rps or cluster_max_rps <= 0:
        return {
            "feasible": False,
            "reason": f"Cluster max {cluster_max_rps} RPS < required {required_rps} RPS",
            "cluster_monthly_tco_eur": cluster_monthly,
            "required_rps": required_rps,
            "cluster_max_rps": cluster_max_rps,
            "recommendation": "Scale cluster or use cloud",
            "cloud_cheaper_above_requests": None,
            "utilization_pct": utilization_pct,
        }

    # 3. Calculate breakeven using round() before int() to fix IEEE-754 precision drift
    if cloud_cost_per_request_eur > 0:
        breakeven_requests = int(round(cluster_monthly / cloud_cost_per_request_eur))
    else:
        breakeven_requests = 0

    return {
        "feasible": True,
        "cluster_monthly_tco_eur": cluster_monthly,
        "required_rps": required_rps,
        "cluster_max_rps": cluster_max_rps,
        "cloud_cost_per_request_eur": round(cloud_cost_per_request_eur, 6),
        "breakeven_monthly_requests": breakeven_requests,
        "cloud_cheaper_above_requests": breakeven_requests,
        "cluster_cheaper_above_requests": breakeven_requests,
        "utilization_pct": utilization_pct,
        "recommendation": f"Cloud cheaper below {breakeven_requests:,} req/mo; cluster cheaper above",
    }

def calculate_financial_roi(
    model_name: str,
    total_input_tokens: int,
    total_output_tokens: int,
    total_requests: int,
    local_avg_latency_ms: float,
    local_accuracy: float,
    cluster: Optional[ClusterConfig] = None,
    required_rps: float = 1.0,
) -> Dict[str, Any]:
    """
    Calculates operational unit economics, cluster capacity, and financial ROI.
    """
    # 1. Fetch Model Registry Config
    model_cfg = settings.model_registry.get(model_name)
    if not model_cfg:
        raise ValueError(f"Model '{model_name}' not found in registry.")

    input_rate = model_cfg.input_cost_per_1k
    output_rate = model_cfg.output_cost_per_1k
    provider_alias = model_cfg.provider_alias
    model_vram = model_cfg.vram

    # 2. Compute Simulated Cloud API Cost
    total_input_cost = (total_input_tokens / 1_000.0) * input_rate
    total_output_cost = (total_output_tokens / 1_000.0) * output_rate
    total_run_cloud_cost = total_input_cost + total_output_cost

    cloud_cost_per_request = (
        total_run_cloud_cost / total_requests if total_requests > 0 else 0.0
    )

    # 3. Efficiency Score (Accuracy relative to latency in seconds)
    latency_sec = local_avg_latency_ms / 1000.0
    efficiency_score = round(local_accuracy / latency_sec, 2) if latency_sec > 0 else 0.0

    # Base payload setup
    payload: Dict[str, Any] = {
        "model_name": model_name,
        "provider_alias": provider_alias,
        "model_vram_gb": model_vram,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_run_cloud_cost_eur": round(total_run_cloud_cost, 6),
        "cloud_cost_per_request_eur": round(cloud_cost_per_request, 6),
        "efficiency_score": efficiency_score,
        "cluster_analysis": None,
    }

    # 4. Perform Cluster Capacity & Breakeven Analysis if cluster is provided
    if cluster:
        # Calculate dynamic single instance RPS from local average latency
        single_instance_rps = 1000.0 / local_avg_latency_ms if local_avg_latency_ms > 0 else 0.0

        tco_data = calculate_cluster_tco(cluster)
        
        throughput_data = calculate_cluster_throughput(
            cluster=cluster,
            model_vram_gb=model_vram,
            base_latency_ms=local_avg_latency_ms,
            single_instance_rps=single_instance_rps,
        )

        breakeven_data = calculate_cluster_breakeven(
            cluster=cluster,
            cloud_cost_per_request_eur=cloud_cost_per_request,
            required_rps=required_rps,
            cluster_max_rps=throughput_data["max_rps"],
        )

        payload["cluster_analysis"] = {
            "tco": tco_data,
            "throughput": throughput_data,
            "breakeven": breakeven_data,
        }

    return payload