from tkinter import *
from tkinter import ttk
#download webpage and save 
from urllib.request import urlopen
# regex
from re import findall
key ='your API KEY'
summoner = 'nKodta5l2_IqJpVOatbcT4SuBdvMIFAi704o_VXJP19ftCY?'
# create main window
root = Tk()
root.title("Teemo")
def enquire():
    teemo = urlopen(f'https://oc1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner}api_key={key}', timeout=5)
    # find string
    masterypoint = findall("championId\":17.+?ints\":([0-9]+)",teemo.read().decode('utf-8'))
    #update label
    masterypoint = f'My Teemo mastery is {masterypoint[0]}'
    print (masterypoint)
    message.config(text=masterypoint)

message = ttk.Label(root, text="here will displlay your champion mastery")
message.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

Button = ttk.Button(root, text="Click Me!", command=enquire)
Button.grid(row=1, column=0, padx=10, pady=10, sticky=N)
#mainloop
root.mainloop()
