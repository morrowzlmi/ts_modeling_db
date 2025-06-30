from ts_modeling_db.models import (
    ModelConfiguration, ConfigParameter, EvaluationConfig,
    Experiment, Fold, FoldMetric, FoldForecast, FinalForecast
)
from ts_modeling_db.db import get_session
from sqlalchemy.exc import IntegrityError
from datetime import date
import hashlib
import json


def insert_model_configuration(session, *, model_type: str, implementation: str, parameters: dict, config_name: str = None, notes: str = None):
    # Hash config for uniqueness
    hash_input = f"{model_type}-{implementation}-{sorted(parameters.items())}"
    config_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    # Check for existing config
    existing = session.query(ModelConfiguration).filter_by(config_hash=config_hash).first()
    if existing:
        return existing

    config = ModelConfiguration(
        model_type=model_type,
        config_name=config_name,
        implementation=implementation,
        config_hash=config_hash,
        notes=notes
    )
    session.add(config)
    session.flush()

    for k, v in parameters.items():
        if k == "regressors":
            for reg in v.split():
                param = ConfigParameter(
                    config_id=config.id,
                    param_name="regressor",
                    param_value=str(reg)
                )
                session.add(param)
        else:
            param = ConfigParameter(
                config_id=config.id,
                param_name=k,
                param_value=json.dumps(v) if isinstance(v, (list, dict)) else str(v)
            )
            session.add(param)

    return config


def insert_evaluation_config(session, *, cv_type: str, cv_horizon: int, gap: int, metrics_spec: list):
    metrics_str = ",".join(metrics_spec)
    existing = session.query(EvaluationConfig).filter_by(
        cv_type=cv_type, cv_horizon=cv_horizon, metrics_spec=metrics_str
    ).first()
    if existing:
        return existing

    eval_config = EvaluationConfig(
        cv_type=cv_type,
        cv_horizon=cv_horizon,
        gap=gap,
        metrics_spec=metrics_str
    )
    session.add(eval_config)
    session.flush()
    return eval_config


def insert_experiment_results(session, *, model_type: str, implementation: str, parameters: dict, eval_config: dict,
                               target_variable: str, folds_data: list, config_name: str = None, final_forecast_data: list = None, notes: str = None):
    model_config = insert_model_configuration(
        session=session,
        model_type=model_type,
        implementation=implementation,
        config_name=config_name,
        parameters=parameters
        )
    eval_conf = insert_evaluation_config(session, **eval_config)

    experiment = Experiment(
        model_config_id=model_config.id,
        eval_config_id=eval_conf.id,
        target_variable=target_variable,
        created_at=date.today(),
        notes=notes
    )
    session.add(experiment)
    session.flush()

    for fold_indexer, fold_dict in enumerate(folds_data):
        
        negative_folds_count = -abs(len(folds_data))
        fold_number = negative_folds_count + fold_indexer + 1

        fold = Fold(
            experiment_id=experiment.id,
            fold_number=fold_number,
            train_start_date=fold_dict["train_start_date"],
            train_end_date=fold_dict["train_end_date"],
            test_start_date=fold_dict["test_start_date"],
            test_end_date=fold_dict["test_end_date"]
        )
        session.add(fold)
        session.flush()

        for m in fold_dict.get("metrics", []):
            session.add(FoldMetric(
                fold_id=fold.id,
                metric_name=m["name"],
                metric_value=m["value"]
            ))

        for f in fold_dict.get("forecasts", []):
            session.add(FoldForecast(
                fold_id=fold.id,
                timestamp=f["timestamp"],
                forecast_value=f["forecast"],
                actual_value=f.get("actual")
            ))

    if final_forecast_data:
        for row in final_forecast_data:
            session.add(FinalForecast(
                experiment_id=experiment.id,
                timestamp=row["timestamp"],
                forecast_value=row["forecast"],
                actual_value=row.get("actual")
            ))

    return experiment

def insert_experiment_run(*, model_type: str, implementation: str, parameters: dict, eval_config: dict,
                          target_variable: str, folds_data: list, config_name:str = None, final_forecast_data: list = None, notes: list = None):
    """
    Convenience wrapper for inserting a full modeling run in one call.
    """
    from ts_modeling_db.db import get_session

    with get_session() as session:
        experiment = insert_experiment_results(
            session,
            model_type=model_type,
            implementation=implementation,
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
        return experiment
