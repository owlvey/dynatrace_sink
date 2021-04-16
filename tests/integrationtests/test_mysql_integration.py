import unittest
import os
from app.Components.MySqlSyncComponent import MySqlSyncComponent
from app.Gateways.MySqlGateway import MySqlGateway
from app.Gateways.CSVGateway import CSVGateway


class MySqlIntegrationTest(unittest.TestCase):

    def test_mysql_insert(self):   
        file_gateway = CSVGateway('./wip/data.csv')  
        mysql_gateway = MySqlGateway("127.0.0.1", "root", 'thefalcon123', 'owlveydb')    
        mysql_sync_component = MySqlSyncComponent(mysql_gateway, file_gateway)
        mysql_sync_component.sync()

    
