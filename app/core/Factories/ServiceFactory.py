from app.core.ServiceEntity import ServiceEntity

class ServiceFactory:

    @staticmethod
    def parse(representations, entity_name, entity_tag):
        result = dict()
        for rep in representations:
            entity = ServiceEntity(rep["entityId"], rep["displayName"])            
            for tag in rep["tags"]:
                entity.tags.append(tag["key"])
                if "value" in tag:
                    entity.tags.append(tag["value"])
                    entity.tags.append('{}:{}'.format(tag["key"], tag["value"]))            
            if entity_name in entity.name and entity_tag in entity.tags:
                result[entity.service_id] = entity

        return result



