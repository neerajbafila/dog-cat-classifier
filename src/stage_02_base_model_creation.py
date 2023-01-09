import mlflow
import tensorflow as tf
import argparse
import os
from src.utils.common import read_config, create_directories
from src.Logger.logger import logger
from src.utils.model_utils import log_model_summary, save_model

STAGE = "Stage_02_base_model_creation"
class BaseModelCreation:
    def __init__(self, parameters_file, config_file):
        self.params = read_config(parameters_file)
        self.config = read_config(config_file)
    
    def base_model_architecture(self):
        logs.write_log(f"In {BaseModelCreation}.base_model_architecture ", 'info')
        LAYERS = [
            tf.keras.layers.Input(shape=tuple(self.params['IMG_SHAPE'])),
            tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), strides=1, kernel_initializer=self.params['kernel_initializer'], activation="relu"),
            tf.keras.layers.MaxPool2D(pool_size=(2,2)),
            tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), kernel_initializer=self.params['kernel_initializer'], activation='relu'),
            tf.keras.layers.MaxPool2D(pool_size=(2,2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(8, activation='relu'),
            tf.keras.layers.Dense(2, activation=self.params['final_activation'])
        ]

        classifier = tf.keras.Sequential(LAYERS)
        model_summary = log_model_summary(classifier)
        # print(classifier.summary())
        logs.write_log(model_summary, 'info')
        # compile model with optimizer
        classifier.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.params['optimizer']['lr']), 
                                loss=self.params['optimizer']['loss'],
                                metrics=self.params['metrics'])
        logs.write_log(f"Model compiled with Adam optimizer lr={self.params['optimizer']['lr']}, loss={self.params['optimizer']['loss']} "
                                f"metrics={self.params['metrics']}")
        # save base model
        model_dir = self.config['Model']['Model_dir']
        # create_directories(model_dir)
        base_model_name = self.config['Model']['baseModel_name']
        path_to_baseModel = os.path.join(model_dir, base_model_name)
        save_model(classifier, path_to_baseModel)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "--c", default="config\config.yaml")
    # parser.add_argument("--config", "--c", default="config\config.yaml")
    parser.add_argument("--param", "--p", default="config\param.yaml")
    parsed_args = parser.parse_args()
    logs = logger(parsed_args.config)
    print(f'***********{STAGE} started*********')
    try:
        logs.write_log(f'***********{STAGE} started*********')
        base_model_object = BaseModelCreation(parsed_args.param, parsed_args.config)
        base_model_object.base_model_architecture()
    except Exception as e:
        logs.write_log(f'Exception occured\n{e}', 'ERROR')
        print(e)
    logs.write_log(f'***********{STAGE} completed*********')
    print(f'***********{STAGE} completed*********')