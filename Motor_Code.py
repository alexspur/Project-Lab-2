import time
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import random


#Manual Combination Input
num1 = 9
num2 = 23
num3 = 1
#Combination List Maker set r = 1 to enable 
r = 0
if (r == 1):
    nums = list(range(0,40))
    combs = []
    for i in range(len(nums)):
        for j in range(len(nums)):
            comb = [i,j]
            combs.append(comb)
    trial = random.randrange(1599)
    trial_comb = combs[trial]
    num1 = trial_comb[0]
    num2 = trial_comb[1]
    num3 = random.randrange(39)
    print("Random Combination:", num1, num2,num3)
    # Full = 200 steps per revolution
    # Half = 400
    # 1/4 =  800
    # 1/8 =  1600
    

#Stepper Motor Setup Code
cur_num = 0
GPIO_pins = (6, 13) # Microstep Resolution MS1-MS2 -> GPIO Pin Set, Can be set to (-1,-1) 
direction= 26       # Direction -> GPIO Pin
step = 19
mymotortest = RpiMotorLib.A3967EasyNema(direction, step, GPIO_pins)

#Steps per tick
full_inc = 200/40

#delay between steps
t = .001

GPIO.setup(5, GPIO.OUT)
servo = GPIO.PWM(5,50)
servo.start(2.5)
servo.ChangeDutyCycle(10)


#mymotortest.motor_move(.001, 200 , False, True, "Full", .05)
def lock_reset():
    time.sleep(3.5)
    mymotortest.motor_move(.002, 600 , False, True, "Full", .05)
    time.sleep(3.5)
def rot_360(direction):
    mymotortest.motor_move(t, 200 , direction, True, "Full", .05)
    time.sleep(1)

def rotate1(num1,direction):
    num = 40 - num1
    mymotortest.motor_move(t, int(num*full_inc) , direction, True, "Full", .05)
    time.sleep(1)
    global cur_num
    cur_num = num2

def rotate2(num1,num2,direction):
    if(num1 >= num2):
        num1 = 40 - (num1 - num2)
    elif(num2 > num1):
        num1 = num2-num1
    mymotortest.motor_move(t, int(num1*full_inc) , direction, True, "Full", .05)
    time.sleep(1)
    global cur_num
    cur_num = num2
def rotate3(num2,num3, direction):
    if(num3 >= num2):
        num = 40 - (num3 - num2)
    elif(num2 > num3):
        num = num2-num3
    mymotortest.motor_move(t, int(num*full_inc) , direction, True, "Full", .05)
    time.sleep(1)
    global cur_num
    cur_num = num3
    #mymotortest.motor_move(t, 500 , True, True, "Full", .05)
def unlock():
    mymotortest.motor_move(.0035, int(15*full_inc) , True, True, "Full", .05)
    time.sleep(1)
    servo.ChangeDutyCycle(7)
    time.sleep(1)
def reset_0():
    global cur_num
    print("reset_0", cur_num)
    if(cur_num > 20):
        num = 40-cur_num
        print(cur_num)
        print("1", num)
        mymotortest.motor_move(t, int(num*full_inc) , True, True, "Full", .05)
        time.sleep(3.5)
    elif(cur_num <= 20):
        num = cur_num
        print(cur_num)
        print("2", num)        
        mymotortest.motor_move(t, int(num*full_inc) , False, True, "Full", .05)
        time.sleep(3.5)
    cur_num = 0
def find_last_num():
    mymotortest.motor_move(.006, 1600 , False, True, "1/8", .05)
    time.sleep(1)
    
#lowers servo arm    
servo.ChangeDutyCycle(5)
time.sleep(.5)
#Test Codes
while(False):
    input("TEST: Press <Enter> to Reset")
    lock_reset()
    rotate1(num1, False)
    rot_360(True)
    rotate2(num1,num2,True)
    rotate3(num2,num3, False)
    input("TEST: Press <Enter> to rotate to try again")
    reset_0()
    trial = random.randrange(1599)
    trial_comb = combs[trial]
    num1 = trial_comb[0]
    num2 = trial_comb[1]
    num3 = random.randrange(39)
    print("Random Combination:", num1, num2,num3)
i = 0
while(i != 0):
    print("Random Combination:", num1, num2,num3)
    print("Iteration:", i)
    lock_reset()
    rotate1(num1, False)
    rot_360(True)
    rotate2(num1,num2,True)
    find_last_num()
    reset_0()
    trial = random.randrange(1599)
    trial_comb = combs[trial]
    num1 = trial_comb[0]
    num2 = trial_comb[1]
    i = i -1
#ignore all except this one
j = 1
while(j != 0):
    input("TEST: Press <Enter> to rotate to try again")
    lock_reset()
    rotate1(num1, False)
    rot_360(True)
    rotate2(num1,num2,True)
    rotate3(num2,num3, False)
    unlock()
    j = j-1

#Servo Test Code



    
servo.stop()
GPIO.cleanup()
exit()
