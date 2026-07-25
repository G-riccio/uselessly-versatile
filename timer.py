from random import *
from time import *
from math import ceil, copysign
import os
second_length = 1.0

##### Translating between timer and clock #####
def read_timer(timer:int,Formatted:bool=True) -> str|list:
    if timer < 0:
        if Formatted:
            return f'-{read_timer(-timer)}'
        else :
            return read_timer(-timer)[:-1] + [-1]
    seconds = int(timer % 60)
    minutes = int((timer % 3600) // 60)
    hours = int((timer % 86400) // 3600)
    days = int(timer // 86400)
    if Formatted:
        if days:
            return f'{days}d {hours:02d}:{minutes:02d}:{seconds:02d}'
        elif hours:
            return f'{hours}:{minutes:02d}:{seconds:02d}'
        else:
            return f'{minutes:02d}:{seconds:02d}'
    else:
        return [seconds,minutes,hours,days,1]

def read_clock(clock:str|list,Formatted:bool=False) -> int:
    if Formatted:
        pass # Come on now
    else:
        return (clock[0] + 60*clock[1] + 3600*clock[2] + 86400*clock[3])*clock[4]


##### Possible events #####
# Simple time events
eDecrease_1, eDecrease_5, eDecrease_min = lambda timer,spentTime:timer-1, lambda timer,spentTime:timer-5, lambda timer,spentTime:timer - 60
eIncrease_1, eIncrease_5, eIncrease_min = lambda timer,spentTime:timer+1, lambda timer,spentTime:timer+5, lambda timer,spentTime:timer + 60
eDiv_2, eDiv_5, eDiv_X = lambda timer,spentTime:timer//2, lambda timer,spentTime:timer//5, lambda timer,spentTime:timer//1.5
eMult_2, eMult_5, eMult_X = lambda timer,spentTime:timer*2, lambda timer,spentTime:timer*5, lambda timer,spentTime:ceil(timer*1.5)

# Advanced time events
def eDampen_2(timer:int,spentTime:int):
    if timer > spentTime:
        timer /= 2
    elif timer < spentTime:
        timer *= 2
    return eDecrease_1(timer,spentTime)
def eDampen_5(timer:int,spentTime:int):
    if timer > spentTime:
        timer /= 5
    elif timer < spentTime:
        timer *= 5
    return eDecrease_1(timer,spentTime)
def eDampen_X(timer:int,spentTime:int):
    if timer > spentTime:
        timer //= 1.5
    elif timer < spentTime:
        timer = ceil(timer*1.5)
    return eDecrease_1(timer,spentTime)
def eShuffleDigits(timer:int,spentTime:int) -> int:
    listChr = lambda x:list(f'{x:02d}')
    T = list(map(listChr,read_timer(timer,False)))[:-1]
    if T[3] == ['0','0']:
        T[3] = []
        if T[2] == ['0','0']:
            T[2] = []
    elif T[3][0] == '0':
        T[3] = T[3][1:]
    formT = T[0]+T[1]+T[2]+T[3]
    shuffle(formT)
    shufT = ''.join(formT)
    if len(shufT) > 4:
        if len(shufT)>6:
            return read_clock(list(map(int,[shufT[0:2], shufT[2:4], shufT[4:6], shufT[6:], copysign(1,timer)])))
        else:
            return read_clock(list(map(int,[shufT[0:2], shufT[2:4], shufT[4:6], '0', copysign(1,timer)])))
    else:
        return read_clock(list(map(int,[shufT[0:2], shufT[2:4], '0', '0', copysign(1,timer)])))
def eFreeze(timer:int,spentTime:int) -> int:
    global second_length
    sleep(4*second_length)
    return eDecrease_1(timer,spentTime)
# Lasting time event

def eFast_Second(timer:int,spentTime:int) -> int:
    global second_length
    second_length /= 2
    return eDecrease_1(timer,spentTime)
def eVeryFast_Second(timer:int,spentTime:int) -> int:
    global second_length
    second_length /= 3
    return eDecrease_1(timer,spentTime)
def eSlow_Second(timer:int,spentTime:int) -> int:
    global second_length
    second_length *= 2
    return eDecrease_1(timer,spentTime)
def eVerySlow_Second(timer:int,spentTime:int) -> int:
    global second_length
    second_length *= 3
    return eDecrease_1(timer,spentTime)
def eDampen_Second(timer:int,spentTime:int) -> int:
    global second_length
    if second_length > 1.0:
        second_length /= 2
    elif second_length < 1.0:
        second_length *= 2
    return eDecrease_1(timer,spentTime)
def eVeryDampen_Second(timer:int,spentTime:int) -> int:
    global second_length
    if second_length > 1.0:
        second_length /= 3
    elif second_length < 1.0:
        second_length *= 3
    return eDecrease_1(timer,spentTime)
def eReset_Second(timer:int,spentTime:int) -> int:
    global second_length
    second_length = 1.0
    return eDecrease_1(timer,spentTime)


##### Clock-running #####
# Advancing the clock
def step(timer:int,spentTime:int,DoShow:bool=True) -> int:
    global Events,Weight,second_length
    value = randint(1,sum(Weight)) # Select a random event
    running_total = 0
    for i in range(len(Events)):
        running_total += Weight[i]
        if running_total >= value:
            selectedEvent = Events[i]
            break

    timer = selectedEvent(timer,spentTime) # Event
    os.system('cls') # Timer display
    if DoShow:
        print(f'Second length: {second_length:.3f}s')
        print(read_timer(timer))
    sleep(second_length)
    return timer

# Mode set-up
Events = []
Weight = []

def set_up(mode:int = 1) -> None:
    global Events,Weight
    
    if mode == 1: # Basic mode
        Events=[eDecrease_1,eDecrease_5,eDecrease_min,eIncrease_1,eIncrease_5,eIncrease_min,eDiv_X,eDiv_2,eDiv_5,eMult_X,eMult_2,eMult_5,
                eDampen_2,eDampen_5,eDampen_X,eShuffleDigits,eFreeze,
                eFast_Second,eVeryFast_Second,eSlow_Second,eVerySlow_Second,eDampen_Second,eVeryDampen_Second,eReset_Second]
        Weight=[100        ,4          ,2            ,8          ,4          ,2            ,6     ,4     ,1     ,4      ,2      ,1      ,
                5        ,3        ,1        ,2             ,4      ,
                8           ,6               ,8           ,6               ,12            ,6                 ,3            ]

    else: # Bland Mode
        Events=[eDecrease_1]
        Weight=[1          ]

def launch(timerValue:int,mode:int=1) -> None:
    timer = timerValue
    set_up(mode)
    start = monotonic()
    while timer > .0:
        timer = step(timer,int(timerValue+start-monotonic()))
    os.system('cls')
    print(f'Second length: {second_length}s')
    print(read_timer(timer))
    print(f'{read_timer(timerValue)} completed in {read_timer(monotonic()-start)}')


##### Test Zone #####
os.system('cls')
print('Second length: 1.0s')
print('00:00')
print('10:00 completed in 08:08')