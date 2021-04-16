class ServiceMethodEntity:

    def __init__(self):
        self.name = None
        self.tags = list()
        self.service_id = None
        self.service = None
        self.method_id = None
        self.points = dict()

    def __str__(self):
        return "{}, {}".format(self.name, self.service_id)