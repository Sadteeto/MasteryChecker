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
    def add_message(content, message = ""):
        if (len(content) < 16) and (len(content) % 2 == 0):
            leftside = rightside =(16-len(content))/2
            #construct message
            message = message + blank*int(leftside) + content + blank*int(rightside)
        elif (len(content) < 16) and (len(content) % 2 != 0):
            leftside = rightside =(15-len(content))/2
            #construct message
            message = message + blank + blank*int(leftside) + content + blank*int(rightside)
        elif (len(content) == 16):
            message = message + content
        else :
            message = message + blank*16
        return message
    
    return add_message(message2, add_message(message1))

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
