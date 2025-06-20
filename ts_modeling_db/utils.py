# utils.py
def passport_pydict_insert (*args):
    model_type = args[0]
    implementation = args[8]
    config_name = args[1]
    parameters = args[2]
    eval_config = args[3]
    target_variable = args[4]
    folds_data = args[5]
    final_forecast = args[6]
    notes = args[7]
    return

def insert_experiment_run(*, model_type, implementation, config_name, parameters, eval_config,
                          target_variable, folds_data, final_forecast_data=None, notes=None):
    return