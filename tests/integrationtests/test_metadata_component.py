from app.Gateways.CSVGateway import CSVGateway
import configparser
from app.Gateways.DynatraceGateway import DynatraceGateway
from app.Gateways.ConfigurationGateway import ConfigurationGateway
from tests.integrationtests.helper import Helper
from app.Components.MetadataComponent import MetadataComponent
import unittest

class MetadataComponentTest(unittest.TestCase):

    def test_process_metadata(self): 
        Helper.load_variables_from_ini()
        configuration = ConfigurationGateway()
        filesystem = CSVGateway(configuration.app__dir_output, configuration.app__dyn_tag)
        dynatrace = DynatraceGateway(configuration.app__dyn_host, configuration.app__dyn_token, configuration.app__dyn_tag)
        component = MetadataComponent(dynatrace, configuration.app__dyn_prefix, configuration.app__start_on, 
            configuration.app__dyn_entity, configuration.app__dyn_tag, filesystem)        
        component.collect()

    def test_process_metadata_cache(self):
        Helper.load_variables_from_ini()
        configuration = ConfigurationGateway()
        filesystem = CSVGateway(configuration.app__dir_output, configuration.app__dyn_tag)
        dynatrace = DynatraceGateway(configuration.app__dyn_host, configuration.app__dyn_token, configuration.app__dyn_tag)
        component = MetadataComponent(dynatrace, configuration.app__dyn_prefix, configuration.app__start_on, 
            configuration.app__dyn_entity, configuration.app__dyn_tag, filesystem)        
        temp_a = component.seek()
        temp_b = component.seek()
        self.assertTrue(temp_a is temp_b)


