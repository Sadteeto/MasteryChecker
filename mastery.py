import serial
from time import sleep
from datetime import datetime
from urllib.request import urlopen
from json import loads

def main():
    #change the following
    key = 'Your API Key'
    summoner = 'Sadmo'
    region = 'oc1'
    champname = 'Teemo'


    recall = True
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

    def get_champ_id():
        try:
            version_list = 'https://ddragon.leagueoflegends.com/api/versions.json'
            version = urlopen(version_list).read().decode('utf-8')
            version = version.split('","')
            version = version[0][2:]

            champion_list = f'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json'
            champion_list = urlopen(champion_list).read().decode('utf-8')
            champion_list = loads(champion_list)
            championId = champion_list["data"][champname]["key"]
            recall = False

        except:
            print("Error in fetching championId")
            championId = ""
            recall = True
        
        return championId, recall

    championId, recall = get_champ_id()

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

    while ser.isOpen():
        try:
            if i%900 == 0:
                print(datetime.now().strftime("%H:%M:%S"))
                try:
                    if recall == True:
                        championId, recall = get_champ_id()
                    
                    if championId != "":
                        masterylist = urlopen(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={key}', timeout=5)
                        masterylist = loads(masterylist.read().decode('utf-8'))
                        summonerId, level = masterylist["id"], masterylist["summonerLevel"]

                        # fetch mastery point
                        masterylist = urlopen(f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}/by-champion/{championId}?api_key={key}', timeout=5)
                        masterylist = loads(masterylist.read().decode('utf-8'))
                        masterypoint = masterylist['championPoints']


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
        except KeyboardInterrupt:
            print("\nExiting")
            ser.close()
            exit()
        except serial.SerialException:
            print("Error in sending message, trying in 5 seconds")
            sleep(5)
            main()

if __name__ == "__main__":
    main()
