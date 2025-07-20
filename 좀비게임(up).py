import csv
import random

#1. 시작 맴버 불러오기
def load_report(filepath):
    start_member = []
    with open(filepath, newline = '' , encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fieldname = {'이름':row['name'],
                         '체력':int(row['health']),
                         '식량':int(row['food']),
                         '해독제':int(row['antidote']),
                         '감염':row['infected'],
                         '연속감염':0
                         }
            start_member.append(fieldname)
    return start_member

#2. 하루 살아남기
def survive_a_day(member_status):
    
    update_status=[]

    for status in member_status:
        #탐험 결과
        if random.random() <= 0.3:
            status['식량'] += 1
            print(f"{status['이름']}님이 식량을 얻었습니다.")
        if random.random() <= 0.1:
            status['해독제'] += 1
            print(f"{status['이름']}님이 해독제를 얻었습니다.")
    
        # 하루 체력 소모
        status['체력'] -= 10
        if status['식량'] > 1:
            status['식량'] -= 1
            status['체력'] += 10

        # 감염 판단
        if status['감염'] == 'False':
            status['연속감염'] = 0
            status['감염'] = str(bool(random.randint(0,1)))

        # 연속 감염 판단
        if status['감염'] == 'True':
            if status['해독제'] > 0:
                status['해독제'] -= 1
                status['감염'] = 'False'
                status['연속감염'] = 0
            else:
                status['연속감염'] += 1
        
        update_status.append(status)
    return update_status

#3. 사망 판단
def check_death(update_status):
    survive_member_status=[]
    for death in update_status:
        if death['체력'] == 0:
            print(f"{death['이름']}님이 굶어 죽었습니다....")
        elif death['연속감염'] == 14:
            print(f"{death['이름']}님이 감염을 치료하지 못해 죽었습니다....")
        else:
            survive_member_status.append(death)
    return survive_member_status

#4. 리포트 저장하기
def save_report(savepath, update_status):
    save_field = ['name','health','food','antidote','infected']
    save_file = []
    for row in update_status:
         row = {'name':row['이름'],
                 'health':int(row['체력']),
                 'food':int(row['식량']),
                 'antidote':int(row['해독제']),
                 'infected':row['감염'],
                 } 
         save_file.append(row)
        
    with open(savepath, 'w', newline = '' , encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, fieldnames = save_field)
        writer.writeheader()
        writer.writerows(save_file)

def main():
    day = int(input('시작 일을 입력하세요.(처음은 0): '))
    during_day = int(input('기간을 입력하세요(일): '))
    input_day = during_day
    if day == 0:
        filepath = 'C:\\python_lesson\\수업자료\\250718\\day_start_report.csv'
    else:  
        filepath = f'C:\\python_lesson\\수업자료\\250718\\day_{day}_report.csv'

    status_start = load_report(filepath)
    while during_day:
        during_day -= 1
        status = status_start
        update_status = survive_a_day(status)
        survive_member_status = check_death(update_status)
        status_start = survive_member_status           

    savepath = f'C:\\python_lesson\\수업자료\\250718\\day_{day+input_day}_report.csv'
    save_report(savepath, survive_member_status)

if __name__ == '__main__':
    main()