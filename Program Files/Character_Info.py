'''
    Main program for character biographies

    keeps information about characters as a way for authors to keep notes
'''

import sys
import os
from os import *
import io
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class characterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(500, 50, 1000, 900)

        self.setWindowTitle("Character Biographies")

        #filename keeps track of the currently open file
        self.filename = ""

        #label for character name
        nameLabel = QLabel("Character Name:", self)
        nameLabel.setFont(QFont("Helvetica", 17))
        nameLabel.resize(1000, 50)
        nameLabel.move(20,20)

        #text box for character name
        self.nameText = QTextEdit(self)
        self.nameText.setFont(QFont("Helvetica", 14))
        self.nameText.resize(360, 40)
        self.nameText.move(20, 70)

        #label for age
        ageLabel = QLabel("Age:", self)
        ageLabel.setFont(QFont("Helvetica", 17))
        ageLabel.resize(1000, 50)
        ageLabel.move(20, 120)

        #text box for age
        self.ageText = QTextEdit(self)
        self.ageText.setFont(QFont("Helvetica", 14))
        self.ageText.resize(100, 40)
        self.ageText.move(90, 130)

        #label for sex
        sexLabel = QLabel("Sex:", self)
        sexLabel.setFont(QFont("Helvetica", 17))
        sexLabel.resize(1000, 50)
        sexLabel.move(210, 120)

        #text box for sex
        self.sexText = QTextEdit(self)
        self.sexText.setFont(QFont("Helvetica", 14))
        self.sexText.resize(100, 40)
        self.sexText.move(280, 130)

        #label for relatives and relationships
        relationLabel = QLabel("Relatives and Relationships:", self)
        relationLabel.setFont(QFont("Helvetica", 17))
        relationLabel.resize(1000, 50)
        relationLabel.move(20, 180)

        #text box for relatives and relationships
        self.relationText = QTextEdit(self)
        self.relationText.setFont(QFont("Helvetica", 14))
        self.relationText.resize(360, 150)
        self.relationText.move(20, 230)

        #label for occupation or titles
        jobLabel = QLabel("Occupation or Title(s):", self)
        jobLabel.setFont(QFont("Helvetica", 17))
        jobLabel.resize(1000, 50)
        jobLabel.move(450, 20)

        #text box for occupation or titles
        self.jobText = QTextEdit(self)
        self.jobText.setFont(QFont("Helvetica", 14))
        self.jobText.resize(530, 100)
        self.jobText.move(450, 70)

        #label for misc. details
        miscLabel = QLabel("Miscellaneous Details:", self)
        miscLabel.setFont(QFont("Helvetica", 17))
        miscLabel.resize(1000, 50)
        miscLabel.move(450, 180)

        #text box for misc details
        self.miscText = QTextEdit(self)
        self.miscText.setFont(QFont("Helvetica", 14))
        self.miscText.resize(530, 150)
        self.miscText.move(450, 230)

        #label for the description
        descriptionLabel = QLabel("Character Description:", self)
        descriptionLabel.setFont(QFont("Helvetica", 17))
        descriptionLabel.resize(1000, 50)
        descriptionLabel.move(20, 390)

        #text box for the description
        self.descriptionText = QTextEdit(self)
        self.descriptionText.setFont(QFont("Helvetica", 14))
        self.descriptionText.resize(960, 440)
        self.descriptionText.move(20, 440)

        #menu bar that holds all of the save features
        menu = self.menuBar()
        saveMenu = menu.addMenu("File")

        #for saving a new file
        saveNew = QAction("Save New", self)
        saveNew.triggered.connect(self.saveNew)
        saveMenu.addAction(saveNew)

        #for saving an already existing file
        saveOld = QAction("Save", self)
        saveOld.triggered.connect(self.saveOld)
        saveMenu.addAction(saveOld)

        #for loading already made files
        loadFolder = QAction("Load", self)
        loadFolder.triggered.connect(self.loadFolder)
        saveMenu.addAction(loadFolder)

    #Save a new file
    def saveNew(self):
        #obtains the directory name for the new character
        directory = "Program Files/data/characterSaves/"
        name = self.nameText.toPlainText()
        name = name.split()[0]
        name2 = name
        directory = directory + name

        #makes sure the characterSaves directory exists
        if not os.path.isdir("Program Files/data/characterSaves"):
            os.makedirs("Program Files/data/characterSaves")   

        #if the character's name is already in use, put a number after it to signify a duplicate name
        if os.path.isdir(directory):
            duplicate = 2
            while 1:
                directory = directory + str(duplicate)
                if not os.path.isdir(directory):
                    name2 = name2 + str(duplicate)
                    break
                directory = directory[:-1]
                duplicate += 1

        #record the final directory name in filename and make the directory for it
        self.filename = name2
        os.makedirs(directory)

        #writes all of the informations into respective text files 
        namePath = directory + "/name.txt"
        name = self.nameText.toPlainText()
        f = io.open(namePath, "x")
        f.write(name)
        f.close()

        namePath = directory + "/filename.txt"
        f = io.open(namePath, "x")
        f.write(name2)
        f.close()

        agePath = directory + "/age.txt"
        age = self.ageText.toPlainText()
        f = io.open(agePath, "x")
        f.write(age)
        f.close()

        sexPath = directory + "/sex.txt"
        sex = self.sexText.toPlainText()
        f = io.open(sexPath, "x")
        f.write(sex)
        f.close()

        relationPath = directory + "/relation.txt"
        relation = self.relationText.toPlainText()
        f = io.open(relationPath, "x")
        f.write(relation)
        f.close()

        jobPath = directory + "/job.txt"
        job = self.jobText.toPlainText()
        f = io.open(jobPath, "x")
        f.write(job)
        f.close()

        miscPath = directory + "/misc.txt"
        misc = self.miscText.toPlainText()
        f = io.open(miscPath, "x")
        f.write(misc)
        f.close()

        descriptionPath = directory + "/description.txt"
        description = self.descriptionText.toPlainText()
        f = io.open(descriptionPath, "x")
        f.write(description)
        f.close()

        #lets the user know what the character was saved as
        popup = QMessageBox()
        popup.setText("File saved as:  " + name2)
        popup.exec_()

    #save the progress on the currently open character
    def saveOld(self):
        #makes sure the currently open character is already a directory
        if self.filename == "":
            popup = QMessageBox()
            popup.setText("Non-existing file: use " + '"Save New"')
            popup.exec_()
            return

        #gets the character's directory
        directory = "data/characterSaves/" + self.filename

        #updates the character's information into the respective files
        namePath = directory + "/name.txt"
        name = self.nameText.toPlainText()
        f = io.open(namePath, "w")
        f.write(name)
        f.close()

        agePath = directory + "/age.txt"
        age = self.ageText.toPlainText()
        f = io.open(agePath, "w")
        f.write(age)
        f.close()

        sexPath = directory + "/sex.txt"
        sex = self.sexText.toPlainText()
        f = io.open(sexPath, "w")
        f.write(sex)
        f.close()

        relationPath = directory + "/relation.txt"
        relation = self.relationText.toPlainText()
        f = io.open(relationPath, "w")
        f.write(relation)
        f.close()

        jobPath = directory + "/job.txt"
        job = self.jobText.toPlainText()
        f = io.open(jobPath, "w")
        f.write(job)
        f.close()

        miscPath = directory + "/misc.txt"
        misc = self.miscText.toPlainText()
        f = io.open(miscPath, "w")
        f.write(misc)
        f.close()

        descriptionPath = directory + "/description.txt"
        description = self.descriptionText.toPlainText()
        f = io.open(descriptionPath, "w")
        f.write(description)
        f.close()

        #lets the user know that their progress has been saved
        popup = QMessageBox()
        popup.setText("File Updated")
        popup.exec_()

    #loads up a character that has already been made
    def loadFolder(self):
        #if there is no characters made, let the user know
        if not os.path.isdir("data/characterSaves"):
            popup = QMessageBox()
            popup.setText("No characters have been made yet")
            popup.exec_()
            return

        #lets the user select which character they want to open
        directory = QFileDialog.getExistingDirectory(self, "Select character's name in " + '"characterSaves"', "data/characterSaves")

        #if the user has cancelled, stops the function
        if not directory:
            return

        #loads in the character information into their respective text boxes
        name = directory + "/filename.txt"
        text = io.open(name, "r").read()
        self.filename = text

        name = directory + "/name.txt"
        text = io.open(name, "r").read()
        self.nameText.setText(text)

        age = directory + "/age.txt"
        text = io.open(age, "r").read()
        self.ageText.setText(text)
        
        sex = directory + "/sex.txt"
        text = io.open(sex, "r").read()
        self.sexText.setText(text)

        relation = directory + "/relation.txt"
        text = io.open(relation, "r").read()
        self.relationText.setText(text)

        job = directory + "/job.txt"
        text = io.open(job, "r").read()
        self.jobText.setText(text)

        misc = directory + "/misc.txt"
        text = io.open(misc, "r").read()
        self.miscText.setText(text)

        description = directory + "/description.txt"
        text = io.open(description, "r").read()
        self.descriptionText.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
   
    window = characterWindow()

    window.show()

    sys.exit(app.exec())