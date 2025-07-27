import random

class Job:
    def __init__(self, role, hp_cost):
        self.role = role
        self.hp_cost = hp_cost

    def work(self):
        raise NotImplementedError('직업별 작업 구현 필요')

# 자원 채집 함수
def get_resource(m=5,s=2):
    value = random.gauss(m,s)
    value = round(value)
    return max(0,min(10,value))

# 군인
class Soldier(Job):
    
    # 군인은 하루 15의 체력을 소모함.
    def __init__(self,name):
        super().__init__('군인', hp_cost = 15)
        self.name = name
        self.assistants = []

    def accept_assistant(self, worker):
        if len(self.assistants) < 2:
            self.assistants.append(worker)
            print(f'{self.name} 보조: ({len(self.assistants)}/2)명')
        else:
            print(f'{self.name} 보조: ({len(self.assistants)}/2)명 - 모집 완료')

    # 군인은 1명은 일꾼 2명까지 데리고 갈 수 있고 데려가는 일꾼당 50% 채집 보너스를 받음.
    def work(self):
        assist_bonus = 1 + (len(self.assistants) * 0.5)
        return{
            'food' : round(get_resource() * assist_bonus),
            'water' : round(get_resource() * assist_bonus),
            'medicine' : round(get_resource() * assist_bonus),
            'battery' : round(get_resource() * assist_bonus)
        }

# 연구원
class Researcher(Job):

    # 연구원은 하루에 15의 체력을 소모함.
    # 연구원은 2명의 보조(일꾼)을 필요로 함.
    def __init__(self,name):
        super().__init__('연구원', hp_cost = 15)
        self.name = name
        self.required_assistants = 2
        self.assistants = []
    
    def accept_assistant(self, worker):
        if len(self.assistants) < 2:
            self.assistants.append(worker)
            print(f'{self.name} 보조: ({len(self.assistants)}/2)명')
        else:
            print(f'{self.name} 보조: ({len(self.assistants)}/2)명 - 모집 완료')

    def work(self):
        pass

# 일꾼
class Worker(Job):

    def __init__(self,name):
        super().__init__('일꾼', hp_cost = 10)
        self.name = name
        self.assisting = None
    
    def assist(self, target):
        if isinstance(target, (Researcher, Soldier)):
            if self.assisting is not None:
                print(f'{self.name}은 {self.assisting.name}을 보조 중 입니다.')
                return
            
            target.accept_assistant(self)
            self.assisting = target
            print(f'{self.name}이 {target.name}을 보조합니다.')
        else:
            print('보조대상이 아닙니다.')




class Structure:
    def __init__(self):
        self.durability = 30
        self.battery_cost = 10

class Freezer(Structure):
    def __init__(self, level = 1):
        super().__init__()
        self.level = level
        self.battery_cost = 10 + level * 5
        self.ice = 0
        self.operator = []

    def generate_ice(self,storage):
        if len(self.operator) < self.level:
            print('연구원 수 부족')
            return

        for researcher in self.operator:
            if not isinstance(researcher, Researcher):
                print('머라는거야 씨발')
                return
            if len(researcher.assistants) < researcher.required_assistants:
                print('보조 수 부족')
                return

        possible = min(storage.water,storage.medicine,self.level)
        storage.water -= possible
        storage.medicine -= possible
        self.ice += possible

class Storage(Structure):

    def __init__(self, level = 1):
        super().__init__()
        self.level = level
        self.capabilty = 200 * level
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


soldier = Soldier('김병장')
researcher = Researcher('김박사')
w1 = Worker('김씨')
w2 = Worker('이씨')
w3 = Worker('최씨')
w4 = Worker('박씨')

storage = Storage()
freezer = Freezer()

w1.assist(soldier)
w2.assist(soldier)
w3.assist(researcher)
w4.assist(researcher)
freezer.operator.append(researcher)

resources = soldier.work()
storage.add_resource(resources)
freezer.generate_ice(storage)

print(f'물: {storage.water} / 식량: {storage.food} / 약 : {storage.medicine} / 배터리 : {storage.battery} / 해열 얼음 : {freezer.ice}')