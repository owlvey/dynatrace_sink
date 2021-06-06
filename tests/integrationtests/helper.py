import os 
import configparser

class Helper:
    @staticmethod
    def load_variables_from_ini():
        config = configparser.ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        target = os.path.join(dir_path, './../../development.ini')
        if os.path.exists(target):
            config.read(target)            
            target = config['DEFAULT']

        for k, v in target.items():
            os.environ.setdefault(k, v)        