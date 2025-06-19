from ts_modeling_db.db import get_session
from ts_modeling_db.models import (
    Experiment, ModelConfiguration, EvaluationConfig,
    Fold, FoldMetric, FoldForecast, FinalForecast
)
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload
from datetime import date

def get_experiment_by_id(experiment_id):
    with get_session() as session:
        return session.query(Experiment).filter_by(id=experiment_id).first()

def get_all_experiments():
    with get_session() as session:
        return session.query(Experiment).options(
            joinedload(Experiment.model_config),
            joinedload(Experiment.eval_config)
        ).order_by(Experiment.created_at.desc()).all()

def get_model_config_by_hash(config_hash):
    with get_session() as session:
        return session.query(ModelConfiguration).filter_by(config_hash=config_hash).first()

def get_experiment_metrics(experiment_id, metric_names=None):
    with get_session() as session:
        folds = session.query(Fold).filter_by(experiment_id=experiment_id).all()
        all_metrics = []
        for fold in folds:
            metric_query = session.query(FoldMetric).filter_by(fold_id=fold.id)
            if metric_names:
                metric_query = metric_query.filter(FoldMetric.metric_name.in_(metric_names))
            metrics = metric_query.all()
            all_metrics.append({
                "fold_number": fold.fold_number,
                "metrics": [{"name": m.metric_name, "value": m.metric_value} for m in metrics]
            })
        return all_metrics

def get_final_forecast(experiment_id, start_date=None, end_date=None):
    with get_session() as session:
        query = session.query(FinalForecast).filter_by(experiment_id=experiment_id)
        if start_date:
            query = query.filter(FinalForecast.timestamp >= start_date)
        if end_date:
            query = query.filter(FinalForecast.timestamp <= end_date)
        return query.order_by(FinalForecast.timestamp).all()

def get_fold_forecasts(experiment_id, start_date=None, end_date=None):
    with get_session() as session:
        folds = session.query(Fold).filter_by(experiment_id=experiment_id).all()
        results = []
        for fold in folds:
            forecast_query = session.query(FoldForecast).filter_by(fold_id=fold.id)
            if start_date:
                forecast_query = forecast_query.filter(FoldForecast.timestamp >= start_date)
            if end_date:
                forecast_query = forecast_query.filter(FoldForecast.timestamp <= end_date)
            forecasts = forecast_query.order_by(FoldForecast.timestamp).all()
            results.append({
                "fold_number": fold.fold_number,
                "forecasts": [
                    {
                        "timestamp": f.timestamp,
                        "forecast": f.forecast_value,
                        "actual": f.actual_value
                    } for f in forecasts
                ]
            })
        return results

def filter_experiments(model_type=None, config_name=None, target_variable=None,
                        start_date=None, end_date=None):
    with get_session() as session:
        query = session.query(Experiment).join(ModelConfiguration)

        if model_type:
            query = query.filter(ModelConfiguration.model_type == model_type)
        if config_name:
            query = query.filter(ModelConfiguration.config_name == config_name)
        if target_variable:
            query = query.filter(Experiment.target_variable == target_variable)
        if start_date:
            query = query.filter(Experiment.created_at >= start_date)
        if end_date:
            query = query.filter(Experiment.created_at <= end_date)

        return query.order_by(Experiment.created_at.desc()).all()
