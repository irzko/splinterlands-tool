from splint import *
import json, os
os.system('cls')


def cleanHistory():
    h = History.history
    for m in h:
        i = 0
        length = len(h[m])
        while(i < length):
            myteam = h[m][i]['my_team']['team']
            if len(myteam) == 0:
                h[m].pop(i)
                length = len(h[m])
            i += 1
    History.historyFile.wJSon(History.history)