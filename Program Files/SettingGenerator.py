#Generate setting recommendations for story and display them in pop up box
from urllib.request import urlopen
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def SettingGenerator():    
    url = 'http://chaoticshiny.com/placenamegen.php'
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    start = html.find('<div id=output>')
    end = html.find('<br>')

    scrapeSetting = html[start:end]
    saveState = 0
    temp = ""

    # a loop gets all the temp and puts them into a single string
    for i in range(0, len(scrapeSetting)):
        if(scrapeSetting[i] == '<'): saveState = 0
        if(scrapeSetting[i] == '>'): saveState = 1
        if(saveState == 1 and scrapeSetting[i] >= chr(65) and scrapeSetting[i] <= chr(90)): temp += scrapeSetting[i]
        if(saveState == 1 and scrapeSetting[i] >= chr(97) and scrapeSetting[i] <= chr(122)): temp += scrapeSetting[i]

    count = 0
    for i in range(0, len(temp)):
        if(temp[i].isupper()): count += 1
        if(count == 2):
            temp = temp[:i] + ' ' + temp[i:]
            count = 0
    
    return temp

