from PIL import Image
import imghdr
import argparse
import os
import shutil
import mlflow
from src.utils.common import read_config, create_directories
from src.Logger.logger import logger
from PIL import ImageFile
import warnings
# warnings.filterwarnings("error")
warnings.simplefilter('error', UserWarning)

ImageFile.LOAD_TRUNCATED_IMAGES = True

STAGE = "STAGE 01"

class get_data:
    def __init__(self, config_file='config\config.yaml'):
        logs = logger(config_file)
        logs.write_log(f'********In {__class__}**********')
        logs.write_log(f"reading config file")
        try:

            self.config = read_config(config_file)
            self.data_root_folder = self.config['DataPath']
        except Exception as e:
            logs.write_log(f"Exception occurred \n {e}", 'error')
    def get_and_validate_data(self):
        logs.write_log(f"********** In get_data.get_and_validate_data ************ ")  
        self.root_data_folder_path = os.path.join(self.config['DataPath'])
        root_bad_data_folder = os.path.join(self.config['BadDataPath']['root_folder'])
        bad_data_file = os.path.join(root_bad_data_folder, self.config['BadDataPath']['BadDataFile'])
        create_directories([root_bad_data_folder, "cat"])
        create_directories([root_bad_data_folder, "dog"])
        try:
            invalid_img_count = 0
            print(f"Image validation started....")
            logs.write_log(f"********************  Image validation started *******************************","info")
            for dirs in os.listdir(self.data_root_folder):
                path_to_img = os.path.join(self.root_data_folder_path, dirs)
                for imgs in os.listdir(path_to_img):
                    # img full path
                    img = os.path.join(path_to_img, imgs)
                    try:
                        # validation 1, image is opening or not
                        try:
                            im = Image.open(img).load()
                        except Exception as e:
                            bad_data_path = os.path.join(root_bad_data_folder, dirs)
                            logs.write_log(f"Image {img} not a valid image, It is truncated image: {e} \n", "error")
                            logs.write_log(f"moving {img} to {bad_data_path}")
                            print(f"moving {img} to {bad_data_path}")
                            shutil.move(img, bad_data_path)
                            invalid_img_count  +=1
                            continue
                        im = Image.open(img)
                        result = im.verify()
                        if result is not None:
                            bad_data_path = os.path.join(root_bad_data_folder, dirs)
                            logs.write_log(f"Image {img} not a valid image \n")
                            logs.write_log(f"moving {img} to {bad_data_path}")
                            print(f"moving {img} to {bad_data_path}")
                            shutil.move(img, bad_data_path)
                            invalid_img_count  +=1
                            im.close()
                            continue
                            
                        stat_file = os.stat(img)
                        filesize = stat_file.st_size
                        if filesize < 10000:
                            bad_data_path = os.path.join(root_bad_data_folder, dirs)
                            logs.write_log(f"Image {img} not a valid file, it is less than size of {filesize} \n")
                            logs.write_log(f"moving {img} to {bad_data_path}")
                            print(f"moving {img} to {bad_data_path}")
                            shutil.move(img, bad_data_path)
                            invalid_img_count  +=1
                            continue
                        
                        # validation 2 and 3, is image is rgb and in [jpeg, png] format
                        if (len(im.getbands()) != 3 or (imghdr.what(img) not in ['jpeg', 'png'])):
                            print(f"******{img} Not a valid image ******")
                            with open(bad_data_file, 'a+') as f:
                                f.writelines(f"Image {img} not a valid file \n")
                            bad_data_path = os.path.join(root_bad_data_folder, dirs)
                            logs.write_log(f"moving {img} to {bad_data_path}")
                            print(f"moving {img} to {bad_data_path}")
                            shutil.move(img, bad_data_path)
                            invalid_img_count  +=1
                    except Exception as e:
                        print(f"******{img} Not a valid image ******", e)
                        invalid_img_count  +=1
                        try:
                            bad_data_path = os.path.join(root_bad_data_folder, dirs)
                            print(f'****Moving Bad image { img} to {bad_data_path}****')
                            shutil.move(img, bad_data_path)
                        except Exception as e:
                            print(e)
                        with open(bad_data_file, 'a+') as f:
                                f.writelines(f"Image {img} not a valid file {e} \n")
            print(f"Image validation completed")
            logs.write_log(f"********************  Image validation completed *******************************", "info")    
                    
        except Exception as e:
            logs.write_log(f'Exception occurred \n {e}', 'error')
        print(f"Total invalid image are {invalid_img_count}")
        logs.write_log(f"*******Total no of invalid images are {invalid_img_count}*******")
        # mlflow.log_artifact(self.root_data_folder_path)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "--c", default="config\config.yaml")
    pared_args = parser.parse_args()
    try:
        logs = logger(pared_args.config)
        logs.write_log(f'{STAGE} Started')
        get_data_ob = get_data(pared_args.config)
        get_data_ob.get_and_validate_data()
    except Exception as e:
        logs.write_log(e, 'error')
        print(e)

        





