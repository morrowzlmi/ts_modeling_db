# utils.py
from insert import insert_experiment_run

def passport_pydict_insert (*args, **kwargs):
    model = kwargs['model']
    command = model['command']
    params = model['params']
    config = kwargs['config']
    model_type = params['modelfam']
    implementation = 'passport_pydict'
    parameters = dict(p=params['pdq'][0],
                      d=params['pdq'][1],
                      q=params['pdq'][2],
                      sp=params['PDQS'][0],
                      sd=params['PDQS'][1],
                      sq=params['PDQS'][2],
                      ss=params['PDQS'][3],
                      lmbda=params['lmbda'],
                      regressors=command[1:],
                      )
    eval_config = dict(cv_type=config['cross-valdation']['type'],
                       cv_horizon=config['cross-valdation']['testwindlen'],
                       cv_folds=Column(Integer),
                       metrics_spec=Column(String))
    target_variable = command[0]
    folds_data = args[5]
    if kwargs and 'config_name' in kwargs.keys:
        config_name = kwargs['config_name']
    else:
        config_name = None
    final_forecast = args[6]
    if kwargs and 'notes' in kwargs.keys:
        notes = kwargs['notes']
    else:
        notes = None            
    
    insert_experiment_run(model_type=model_type, 
                          implementation=implementation, 
                          parameters=parameters, 
                          eval_config=eval_config, 
                          target_variable=target_variable, 
                          folds_data=folds_data, 
                          config_name = None, 
                          final_forecast_data=None, 
                          notes=None)

    return