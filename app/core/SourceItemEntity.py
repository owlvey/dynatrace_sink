from dateutil.parser import parse


class SourceItemEntity:

    def __init__(self) -> None:
        self.source = None
        self.start = None
        self.end = None
        self.total = 0
        self.availability = 0
        self.experience = 0
        self.latency = 0 
    
    def parse(self, line:str):
        if line:
            items = line.split(';')
            self.source = items[0]
            self.start = parse(items[1])
            self.end = parse(items[2])
            self.total = int(items[3])
            self.availability = int(items[4])
            self.experience = int(items[5])
            self.latency = float(items[6])
    
    def __str__(self) -> str:
        return self.__dict__.__str__()

    def to_tuple(self):
        return (self.source, self.start, self.end, self.total, self.availability, self.experience, self.latency)