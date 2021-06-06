import configparser
import os


class ConfigurationGateway:    

    def __init__(self, use_dev = True ) -> None:
        config = configparser.ConfigParser()
        self.config_source = None
        if use_dev and os.path.exists('development.ini'):
            config.read('development.ini')            
            self.config_source = config['DEFAULT']


        self.app__start_on = self.__read_variable('app__start_on', "2021-05-18 00:00:00")
        self.app__dyn_entity = self.__read_variable('app__dyn_entity', "Controller")
        self.app__dyn_tag = self.__read_variable('app__dyn_tag') 
        self.app__dyn_host = self.__read_variable('app__dyn_host')
        self.app__dyn_token = self.__read_variable('app__dyn_token') 
        self.app__dyn_prefix = self.__read_variable('app__dyn_prefix', "")
        self.app__dir_output = self.__read_variable('app__dir_output') 
        self.app__enable_dyn_metric = True if int(self.__read_variable('app__enable_dyn_metric', '0')) == 1 else False
        self.app__enable_dyn_problem = True if int(self.__read_variable('app__enable_dyn_problem', '0')) == 1 else False 
        self.app__enable_dyn_metadata = True if int(self.__read_variable('app__enable_dyn_metadata', '0')) == 1 else False 
    
    def __read_variable(self, key , default = None):        
        if self.config_source:
            return self.config_source.get(key, default)
        else:            
            if default is not None:
                return os.environ.get(key, default)
            else:
                return os.environ[key]

