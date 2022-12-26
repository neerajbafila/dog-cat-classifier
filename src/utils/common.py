import yaml
import datetime
import os



def read_config(config_file='config/config.yaml') -> dict:
    with open (config_file, 'r') as yaml_file:
        content = yaml.safe_load(yaml_file)
    # print(content)
    return content

def unique_name()->str:
    now = datetime.datetime.now()
    # name = now.strftime("%Y-%m-%d_%H.%M.%S")
    name = now.strftime("%Y-%m-%d")
    # print(name)
    return name

def create_directories(path_to_dir: list):
    full_path = ""
    for path in path_to_dir:
        full_path =os.path.join(full_path,path)
    os.makedirs(full_path, exist_ok=True)
    



