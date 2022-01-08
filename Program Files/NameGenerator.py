#Program goal: generate names and display in a pop up box
import sys
from urllib.request import urlopen
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class NameGen:
    def __init__(self):
        super().__init__()
        self.names_list = self.Generate()
        self.msg = QMessageBox()
        
        self.msg.setText('Generated names:')
        self.msg.setInformativeText(self.names_list)


    def Generate_Names():
        #base code gets a list of names from a website
        url = 'http://random-name-generator.info/'
        page = urlopen(url)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        names_list_start = html.find('<ol class="nameList">')
        names_list_end = html.find('</ol>')

        scrape_names_list = html[names_list_start:names_list_end]
        names = []
        sv = 0
        temp = ""

        # a loop gets all the names and puts them into a single string
        for i in range(0, len(scrape_names_list)):
            if(scrape_names_list[i] == '<'): sv = 0
            if(scrape_names_list[i] == '>'): sv = 1
            if(sv == 1 and scrape_names_list[i] >= chr(65) and scrape_names_list[i] <= chr(90)): temp += scrape_names_list[i]
            if(sv == 1 and scrape_names_list[i] >= chr(97) and scrape_names_list[i] <= chr(122)): temp += scrape_names_list[i]

        # loop to separate names into a list containing first and last name in each indice
        cl = 0
        st = 0
        for i in range(0, len(temp)):
            if(temp[i].isupper()): cl += 1
            if(cl % 3 == 0 and cl != 0):
                names.append(str(temp[st:i]))
                st = i
                cl = 1

        # loop through the names list to correct spacing
        cl = 0
        for i in range(0, len(names)):
            for j in range(0, len(names[i])):
                if(names[i][j].isupper()): cl += 1
                if(cl == 2):
                    names[i] = names[i][:j] + ' ' + names[i][j:]
                    cl = 0
        return names
