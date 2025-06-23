# utils.py
from insert import insert_experiment_run

def extract_folds_data_from_cvout(cvout_str: str):
    evaluated_cvout_str = eval(cvout_str) # expected to evaluate to list of dicts
    # for dict in list, store dict['timing'] in new list


def passport_pydict_insert (model: dict, config: dict, cvout: str, *args, **kwargs):
    command = model['command']
    params = model['params']
    agg_method = config['cross-valdation']['aggmethod']
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
    eval_config = dict(cv_type=config['cross-valdation']['type'], # str
                       cv_horizon=int(config['cross-valdation']['testwindlen']), # int
                       metrics_spec=[str(agg_method),'aggmae','aggmape','aggmedae','aggr2','aggrmse','mae','mape','medae','r2','rmse']) # list
    target_variable = command[0]
    ####################################
    folds_data = eval(cvout) # needs to be list of dictionaries, basically "constituents"
    #############################
    if kwargs and 'config_name' in kwargs.keys:
        config_name = kwargs['config_name']
    else:
        config_name = None
    ####################################
    final_forecast = args[6]
    #############################
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