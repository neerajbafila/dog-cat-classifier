import mlflow
import tensorflow as tf
from src.utils.common import read_config



dev = tf.config.list_physical_devices()
print(dev)
