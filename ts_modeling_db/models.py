from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class ModelConfiguration(Base):
    __tablename__ = "model_configurations"

    id = Column(Integer, primary_key=True)
    model_type = Column(String)
    implementation = Column(String)  # e.g., "pmdarima", "Greykite", "statsmodels"
    config_name = Column(String, nullable=True)
    config_hash = Column(String, unique=True)
    notes = Column(Text)

    parameters = relationship("ConfigParameter", back_populates="config")
    experiments = relationship("Experiment", back_populates="model_config")

class ConfigParameter(Base):
    __tablename__ = "config_parameters"

    id = Column(Integer, primary_key=True)
    config_id = Column(Integer, ForeignKey("model_configurations.id"))
    param_name = Column(String)
    param_value = Column(String)

    config = relationship("ModelConfiguration", back_populates="parameters")

class EvaluationConfig(Base):
    __tablename__ = "evaluation_configs"

    id = Column(Integer, primary_key=True)
    cv_type = Column(String)
    cv_horizon = Column(Integer)
    metrics_spec = Column(String)  # Comma-separated list

    experiments = relationship("Experiment", back_populates="eval_config")

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    model_config_id = Column(Integer, ForeignKey("model_configurations.id"))
    eval_config_id = Column(Integer, ForeignKey("evaluation_configs.id"))
    target_variable = Column(String)
    created_at = Column(Date, default=datetime.date.today)
    notes = Column(Text)

    model_config = relationship("ModelConfiguration", back_populates="experiments")
    eval_config = relationship("EvaluationConfig", back_populates="experiments")
    folds = relationship("Fold", back_populates="experiment")
    final_forecasts = relationship("FinalForecast", back_populates="experiment")

class Fold(Base):
    __tablename__ = "folds"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    fold_number = Column(Integer)
    train_start_date = Column(Date)
    train_end_date = Column(Date)
    test_start_date = Column(Date)
    test_end_date = Column(Date)

    experiment = relationship("Experiment", back_populates="folds")
    metrics = relationship("FoldMetric", back_populates="fold")
    forecasts = relationship("FoldForecast", back_populates="fold")

class FoldMetric(Base):
    __tablename__ = "fold_metrics"

    id = Column(Integer, primary_key=True)
    fold_id = Column(Integer, ForeignKey("folds.id"))
    metric_name = Column(String)
    metric_value = Column(Float)

    fold = relationship("Fold", back_populates="metrics")

class FoldForecast(Base):
    __tablename__ = "fold_forecasts"

    id = Column(Integer, primary_key=True)
    fold_id = Column(Integer, ForeignKey("folds.id"))
    timestamp = Column(Date)
    forecast_value = Column(Float)
    actual_value = Column(Float)

    fold = relationship("Fold", back_populates="forecasts")

class FinalForecast(Base):
    __tablename__ = "final_forecasts"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    timestamp = Column(Date)
    forecast_value = Column(Float)
    actual_value = Column(Float)

    experiment = relationship("Experiment", back_populates="final_forecasts")
