from class_Job import Researcher

class Structure:
    def __init__(self):
        self.durability = 30
        self.battery_cost = 10
        self.durability_cost = 1

class Freezer(Structure):
    def __init__(self, level = 1):
        super().__init__()
        self.level = level
        self.battery_cost = 10 + (level-1) * 5
        self.ice = 0
        self.operator = []

    def generate_ice(self,storage):
        if len(self.operator) < self.level:
            print('연구원 수 부족')
            return

        for researcher in self.operator:
            if not isinstance(researcher, Researcher):
                print('머라는거야')
                return
            if len(researcher.assistants) < researcher.required_assistants:
                print('보조 수 부족')
                return

        possible = min(storage.water,storage.medicine,storage.level)
        storage.water -= possible
        storage.medicine -= possible
        self.ice += possible

class Storage(Structure):

    def __init__(self, level = 1):
        super().__init__()
        self.level = level
        self.capabilty = 200 * level
        self.battery_cost = 10 + (level-1) * 5
        self.food = 0
        self.water = 0
        self.medicine = 0
        self.battery = 0

    def add_resource(self, resources: dict):
        for kind, amount in resources.items():
            current = getattr(self, kind)
            maximum = self.capabilty
            new_amount = min(current + amount, maximum)
            setattr(self, kind, new_amount)