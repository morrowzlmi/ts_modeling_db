
from ts_modeling_db.query import (
    get_experiment_by_id,
    get_all_experiments,
    filter_experiments,
    get_experiment_metrics,
    get_final_forecast,
    get_fold_forecasts
)
from datetime import date

# --- Example: Get all experiments ---
experiments = get_all_experiments()
print(f"Found {len(experiments)} experiments")
for exp in experiments:
    print(f"Experiment ID: {exp.id}, Model: {exp.model_config.config_name}, Target: {exp.target_variable}, Date: {exp.created_at}")

# --- Example: Filter experiments by model type and date ---
filtered = filter_experiments(
    model_type="greykite",
    start_date=date(2024, 1, 1),
    end_date=date(2025, 12, 31)
)
print(f"Filtered experiments: {len(filtered)}")

# --- Example: Get metrics for a specific experiment ---
if filtered:
    exp_id = filtered[0].id
    metrics = get_experiment_metrics(exp_id, metric_names=["RMSE", "MAE"])
    print(f"Metrics for Experiment {exp_id}: {metrics}")

# --- Example: Get final forecast for a specific experiment ---
    forecast = get_final_forecast(exp_id, start_date=date(2025, 1, 1))
    for row in forecast:
        print(f"{row.timestamp}: forecast = {row.forecast_value}, actual = {row.actual_value}")

# --- Example: Get fold forecasts ---
    fold_forecasts = get_fold_forecasts(exp_id)
    for fold in fold_forecasts:
        print(f"Fold {fold['fold_number']} has {len(fold['forecasts'])} forecast entries")
