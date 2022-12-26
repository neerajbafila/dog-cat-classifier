import mlflow
import os
from src.Logger.logger import logger

logs = logger()

def main():
    with mlflow.start_run() as run:
        logs.write_log(f'{__name__} Main started', 'info')
        mlflow.run(".", "get_data", env_manager='local')
        
    

if __name__ == '__main__':
    logs.write_log('Main starting', 'info')
    main()
    logs.write_log('Main ended', 'info')
    logs.write_log('****************************')
