from ts_modeling_db.db import get_session
from ts_modeling_db.insert import insert_experiment_results
from datetime import date, timedelta

# Example configuration
model_type = "greykite"
config_name = "basic_greykite_config"
parameters = {
    "changepoint_n": 15,
    "seasonality": "auto",
    "growth": "linear"
}

eval_config = {
    "cv_type": "rolling",
    "cv_horizon": 3,
    "cv_folds": 2,
    "metrics": ["RMSE", "MAE"]
}

target_variable = "monthly_sales"
notes = "Example experiment with synthetic Greykite-style config."

# Synthetic fold data
folds_data = []
start_date = date(2024, 1, 1)
for fold_num in range(1, 3):
    train_end = start_date + timedelta(days=30 * (fold_num * 2))
    test_start = train_end + timedelta(days=1)
    test_end = test_start + timedelta(days=89)

    folds_data.append({
        "fold_number": fold_num,
        "train_end_date": train_end,
        "test_start_date": test_start,
        "test_end_date": test_end,
        "metrics": [
            {"name": "RMSE", "value": 123.4 + fold_num},
            {"name": "MAE", "value": 56.7 + fold_num}
        ],
        "forecasts": [
            {
                "timestamp": test_start + timedelta(days=i * 30),
                "forecast": 1000 + i * 50 + fold_num,
                "actual": 990 + i * 45 + fold_num
            } for i in range(3)
        ]
    })

# Optional final forecast
final_forecast_data = [
    {
        "timestamp": date(2025, 1, 1) + timedelta(days=i * 30),
        "forecast": 1100 + i * 40,
        "actual": 1080 + i * 35
    } for i in range(3)
]

# Insert all data
with get_session() as session:
    experiment = insert_experiment_results(
        session=session,
        model_type=model_type,
        config_name=config_name,
        parameters=parameters,
        eval_config=eval_config,
        target_variable=target_variable,
        folds_data=folds_data,
        final_forecast_data=final_forecast_data,
        notes=notes
    )
    session.commit()
    print(f"Inserted experiment ID: {experiment.id}")
