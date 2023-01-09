import tensorflow as tf
import os
from src.Logger.logger import logger
import argparse
from src.utils.common import read_config, create_directories
from src.utils.model_utils import load_model, save_model, callbacks_list
from PIL import ImageFile
import mlflow
import mlflow.keras

STAGE = "stage_03_Model_training"

class model_training:
    def __init__(self, config_file, param_file):
        logs.write_log(f"***** IN src.stage_03_model_training", 'info')
        self.config = read_config(config_file)
        self.params = read_config(param_file)
        ImageFile.LOAD_TRUNCATED_IMAGES = False
    def train(self):
        logs.write_log(f"****In model_training.train********", 'info')
        root_data_folder = os.path.join(self.config['DataPath'])
        print(root_data_folder)
        try:
            # getting data
            train_data = tf.keras.preprocessing.image_dataset_from_directory(root_data_folder,
                        validation_split=self.params['data_train_val']['validation_split'],
                        subset='training',
                        image_size=tuple(self.params['data_train_val']['image_size']),
                        batch_size=self.params['data_train_val']['batch_size'],
                        seed=self.params['data_train_val']['seed']
            )
            
            val_data = tf.keras.preprocessing.image_dataset_from_directory(
                        root_data_folder,
                        validation_split=self.params['data_train_val']['validation_split'],
                        subset='validation',
                        batch_size=self.params['data_train_val']['batch_size'],
                        image_size=self.params['data_train_val']['image_size'],
                        seed=self.params['data_train_val']['seed']
            )

            # load the base model
            path_to_base_model = os.path.join(self.config['Model']['Model_dir'], self.config['Model']['baseModel_name'])
            logs.write_log(f"loading model from {path_to_base_model} ", 'info')
            loaded_model = load_model(path_to_base_model)
        
            # prefetch data in memory for faster training
            train_data = train_data.prefetch(buffer_size=self.params['data_train_val']['prefetch_buffer_batch'])
            val_data = val_data.prefetch(buffer_size=self.params['data_train_val']['prefetch_buffer_batch'])
            epoch = self.params['epoch']
            
            logs.write_log(f"getting callbacks", "info")
            call_backs = callbacks_list()
            logs.write_log(f'training started with total {epoch} epoch', 'info')
            print(f'training started with total {epoch} epoch')
            # start training
            with mlflow.start_run() as runs:
                
            # loaded_model.fit(train_data, epochs=epoch, validation_data=val_data, use_multiprocessing=self.params['use_multiprocessing'])
                loaded_model.fit(train_data, epochs=epoch, validation_data=val_data, use_multiprocessing=True, callbacks=call_backs)
                # save trained model
                path_for_trained_model = os.path.join(self.config['Model']['Model_dir'], self.config['Model']['TrainedModel_name'])
                logs.write_log(f"saving model at {path_for_trained_model}")
                save_model(loaded_model, path_for_trained_model, 'Trained')
                print(f"Trained model saved at {path_for_trained_model}")

                # for testing
                print(f"Testing score")
                score = loaded_model.evaluate(val_data, verbose=0)
                print(score)
                logs.write_log(f"testing score {score}")

                 # Log mlflow attributes for mlflow UI
                logs.write_log(f"loging mlflow", 'info')
                # mlflow.log_metrics(score)
                mlflow.log_params(self.params)
                mlflow.keras.log_model(loaded_model, "model")
                mlflow.keras.autolog()
                # mlflow.tensorflow.autolog(every_n_iter=2)
            

           
        except Exception as e:
            print(f"Exception {e}")
            logs.write_log(f"Error occurred {e}", "ERROR")



if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--config", "--c", default="config/config.yaml")
    arg_parser.add_argument("--params", "--p", default="config/param.yaml")
    parsed_args = arg_parser.parse_args()
    logs = logger(parsed_args.config)
    try:
        logs.write_log(f'**********{STAGE} Started************')
        training_ob = model_training(parsed_args.config, parsed_args.params)
        training_ob.train()
    except Exception as e:
        logs.write_log(f'Error ocurred {e}', 'ERROR')
