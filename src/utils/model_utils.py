import io
from src.Logger.logger import logger
from src.utils.common import read_config, create_directories
import os
import tensorflow as tf

logs = logger()
def log_model_summary(model):
    """_summary_
        It will log the model summary
    Args:
        model (tensorflow model): model
    """
    with io.StringIO() as stream:
        model.summary( print_fn = lambda x: stream.write(f"{x} \n"))
        summary_str = stream.getvalue()
    return summary_str

def save_model(model, path_to_save, model_type="Base"):
    try:
        logs.write_log(f"In model_utils.save_model")
        create_directories(path_to_save)
        model.save(path_to_save)
        logs.write_log(f"{model_type} Model saved at {path_to_save}")
    except Exception as e:
        logs.write_log(f'Exception occurred \n{e}', 'ERROR')
    
def callbacks_list(config_file='config/config.yaml', param_file='config/param.yaml'):

    logs.write_log(f"***In Utils.model_utils.callbacks****", 'info')
    print(f"preparing callbacks")
    logs.write_log(f"******preparing callbacks***********")

    try:

        config_file = os.path.join("", config_file)
        param_file = os.path.join("", param_file)
        config = read_config(config_file)
        param = read_config(param_file)
        restore_best_weights = param['callbacks']['restore_best_weights']
        patience = param['callbacks']['patience']
        path_to_model = os.path.join(config['Model']['Model_dir'], config['Model']['ckpd_model_name'])
        create_directories(path_to_model)
        # early stopping call backs
        earlyStopingCalblbacks = tf.keras.callbacks.EarlyStopping(restore_best_weights=restore_best_weights, patience=patience)
        # Model check point
        modelCheckPoint = tf.keras.callbacks.ModelCheckpoint(path_to_model, save_best_only=True)
        logs.write_log(f"******callbacks prepared***********")
        return [earlyStopingCalblbacks, modelCheckPoint]
    except Exception as e:
        logs.write_log(f"***Error occurred in Utils.model_utils.callbacks {e}")
        print(e)
    

def load_model(model_full_path):
    try:
        loaded_model = tf.keras.models.load_model(model_full_path)
        return loaded_model
    except Exception as e:
        logs.write_log(f"Error occurred {e}", "ERROR")