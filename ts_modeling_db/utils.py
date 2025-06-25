# utils.py
import datetime
from insert import insert_experiment_run

def extract_fold_data_from_cvout(input_cvout_str: str) -> list[dict]:
    output_fold_data_list = []
    cvout_list = eval(input_cvout_str)
    for obj in cvout_list:
        train_start, train_end, test_start, test_end = obj['timing']
        output_fold_data_list.append({
            "train_start_date": datetime.strptime(train_start, "%Y-%m-%d").date(),
            "train_end_date": datetime.strptime(train_end, "%Y-%m-%d").date(),
            "test_start_date": datetime.strptime(test_start, "%Y-%m-%d").date(),
            "test_end_date": datetime.strptime(test_end, "%Y-%m-%d").date()
        })
    return output_fold_data_list

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
    folds_data = extract_fold_data_from_cvout(cvout) # needs to be list of dictionaries, basically "constituents"
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