from app.core.SourceItemEntity import SourceItemEntity
from app.Gateways.CSVGateway import CSVGateway
from app.Gateways.MySqlGateway import MySqlGateway

class MySqlSyncComponent:

    def __init__(self, 
        mysql_gateway: MySqlGateway,
        file_gateway: CSVGateway) -> None:
        self.mysql_gateway = mysql_gateway
        self.file_gateway = file_gateway

    def sync(self):
        anchor = self.mysql_gateway.get_anchor()
        items = self.file_gateway.get_data_from(anchor)
        entities = list()
        for item in items:
            entity = SourceItemEntity()
            entity.parse(item)
            entities.append(entity)
        
        self.mysql_gateway.post_entries(entities)
            