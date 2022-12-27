import io
from src.Logger.logger import logger
from src.utils.common import read_config, create_directories

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