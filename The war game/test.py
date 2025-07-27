import random
from class_Job import Soldier
from class_Job import Researcher
from class_Job import Worker
from class_Structure import Storage
from class_Structure import Freezer

soldier = Soldier('김병장')
researcher = Researcher('김박사')
w1 = Worker('김씨')
w2 = Worker('이씨')
w3 = Worker('최씨')
w4 = Worker('박씨')

storage = Storage()
freezer = Freezer()

researcher.accept_assistant(w1)
w1.assist(soldier)
w2.assist(soldier)
w3.assist(researcher)
w4.assist(researcher)
freezer.operator.append(researcher)

resources = soldier.work()
storage.add_resource(resources)
freezer.generate_ice(storage)

print(f'물: {storage.water} / 식량: {storage.food} / 약 : {storage.medicine} / 배터리 : {storage.battery} / 해열 얼음 : {freezer.ice}')