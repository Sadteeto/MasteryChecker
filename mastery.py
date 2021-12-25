import serial
from time import sleep
from datetime import datetime
from urllib.request import urlopen
from re import findall


key = 'Your API Key'
summoner = 'Sadmo'
champname = 'Teemo'

ser = serial.Serial()
ser.port = '/dev/ttyACM0' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 10
i = 0

try:
    ser.open()
except:
    print("Serial port not available")
    exit()


def generate_message(message1, message2):
    blank = ' '
    #top row message
    if (len(message1) < 16) and (len(message1) % 2 == 0):
        leftside = rightside =(16-len(message1))/2
        #construct message
        message = blank*int(leftside) + message1 + blank*int(rightside)
    elif (len(message1) < 16) and (len(message1) % 2 != 0):
        leftside = rightside =(15-len(message1))/2
        #construct message
        message = ' ' + blank*int(leftside) + message1 + blank*int(rightside)
    elif (len(message1) == 16):
        message = message1

    #bottom row message
    if (len(message2) < 16) and (len(message2) % 2 == 0):
        leftside = rightside =(16-len(message2))/2
        #construct message
        message = message + blank*int(leftside) + message2 + blank*int(rightside)
    elif (len(message2) < 16) and (len(message2) % 2 != 0):
        leftside = rightside =(15-len(message2))/2
        #construct message
        message = message + ' ' + blank*int(leftside) + message2 + blank*int(rightside)
    elif (len(message2) == 16):
        message = message + message2
    
    return message

while 1:
    if i%900 == 0:
        try:
            masterylist = urlopen(f'https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={key}', timeout=5)
            masterylist = masterylist.read().decode('utf-8')
            summonerId = findall(r'\"id\":\"(.+?)\"',masterylist)
            summonerId = summonerId[0]
            level = findall(r'Level\":(.+?)}',masterylist)
            level = level[0]

            masterylist = urlopen(f'https://oc1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}?api_key={key}', timeout=5)
            # find string
            masterypoint = findall("championId\":17.+?ints\":([0-9]+)",masterylist.read().decode('utf-8'))
            #update label
            masterypoint = masterypoint[0]


        except:
            masterypoint = 'error'
            level = 'error'

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")

    if (i%8 == 0) or(i%8 == 1):
        ser.write(generate_message(current_time,current_date).encode())
    elif(i%8 == 2) or(i%8 == 3):
        ser.write(generate_message(current_time,f" {champname}Mastery").encode())
    elif(i%8 == 4) or(i%8 == 5):
        ser.write(generate_message(current_time,f"  {masterypoint} Points").encode())
    elif(i%8 == 6) or(i%8 == 7):
        ser.write(generate_message(current_time,f"Level {level}").encode())
    
    if i < 1798:
        i += 1
    else :
        i = 0
    sleep(1)
