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
    def __init__(self):
        super().__init__('군인', hp_cost = 15)

    # 군인은 1명은 일꾼 2명까지 데리고 갈 수 있고 데려가는 일꾼당 50% 채집 보너스를 받음.
    def work(self, worker_count=0):
        worker_bonus = 1 + (worker_count * 0.5)
        return{
            'food' : round(get_resource() * worker_bonus),
            'water' : round(get_resource() * worker_bonus),
            'medicine' : round(get_resource() * worker_bonus),
            'battery' : round(get_resource*() * worker_bonus)
        }

# 연구원
class Researcher(Job):

    # 연구원은 하루에 15의 체력을 소모함.
    # 연구원은 2명의 보조(일꾼)을 필요로 함.
    def __init__(self):
        super().__init__('연구원', hp_cost = 15)
        self.required_workers = 2

    def work(self):
        pass
    
# 요리사
class Chef(Job):
    
    def __init__(self):
        super().__init__('요리사', hp_cost = 15)
        self.required_workers = 2

    def work(self):
        pass

# 건설 엔지니어

class Construction_engineer(Job):

    def __init__(self):
        super().__init__('건설 엔지니어', hp_cost = 15)
        self.required_workers = 2

    def work(self):
        pass

# 기계 엔지니어

class Mechanical_engineer(Job):

    def __init__(self):
        super().__init__('기계 엔지니어', hp_cost = 15)
        self.required_workers = 2

    def work(self):
        pass