import sys
import tkinter as tk
import json
import os

from PyQt5 import QtCore
from PyQt5.sip import delete
 #absolute directory of this script
#script_dir = os.path.join(os.path.dirname(__file__), "data")
script_dir = os.path.join('Program Files', 'data')


from Model.Project import Project, new_proj
from tkinter.constants import FALSE, TRUE, Y
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ChapterWindow import ChapterWindow
from json import *


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create and Access Projects")
        root = tk.Tk()

        #grid layout
        QWidget.__init__(self)
        self.QLayout = QGridLayout(self)
        self.QLayout.setVerticalSpacing(20)
        self.placeholder = QWidget(self)
       

        #placeholder cells to prevent spacing issues
        self.QLayout.addWidget(self.placeholder, 0, 0, alignment = 
                                                        Qt.AlignLeft | Qt.AlignTop)
        self.QLayout.addWidget(self.placeholder, 0, 1, alignment = 
                                                        Qt.AlignLeft | Qt.AlignTop)
        self.QLayout.addWidget(self.placeholder, 0, 2, alignment = 
                                                        Qt.AlignLeft | Qt.AlignTop)
        self.QLayout.addWidget(self.placeholder, 0, 3, alignment = 
                                                        Qt.AlignLeft | Qt.AlignTop)
        self.QLayout.addWidget(self.placeholder, 0, 4, alignment = 
                                                        Qt.AlignLeft | Qt.AlignTop)
                                                      
            
        #self.setLayout(self.QLayout)
        
        #new project menubar action
        newProjAction = QAction("New Project", self)
        newProjAction.setShortcut('Ctrl+N')
        newProjAction.triggered.connect(self.new_project_prompt)

        #delete proj menubar action
        deleteProjAction = QAction("Delete", self)
        deleteProjAction.setShortcut('Ctrl+R')
        deleteProjAction.triggered.connect(self.delete_project_prompt)

        #toolbar
        menuBar = QMenuBar(self)
        fileBarFile = menuBar.addMenu("File")
        fileBarFile.addAction(newProjAction)
        fileBarFile.addSeparator()

        fileBarFile.addAction(deleteProjAction)
        self.QLayout.setMenuBar(menuBar)

        #scrollbar
        
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.QLayout.addWidget(self.scrollArea)
        self.setLayout(self.QLayout)

        # note: this will return the sum resolution on a two monitor setup
        width: float = root.winfo_screenwidth() * (1/2)
        height: float  = root.winfo_screenheight() * (1/2)
        self.setFixedSize(int(width), int(height))
        
        self.count = 0
        self.row = 0
        self.windows = []
        
        self.populate_projects()


    def populate_projects(self):
        #rel_path = "data/sample.json"
        #abs_file_path = os.path.join(script_dir, rel_path)
        projects = []
        abs_file_path = script_dir

        #if file exists on launch, read and populate link to existing projects
        for filename in os.listdir(abs_file_path):
            if filename.endswith(".json"):
                with open(os.path.join(abs_file_path, filename), "r") as f:
                    if len(f.readlines()) >= 1: # to make sure file has content
                        
                        f.seek(0)
                        data = json.load(f)
                        p = []
                        for i in data:
                            proj = new_proj(i)
                            p.append(proj)
                            self.newProjectClicked(proj.name, os.path.join(abs_file_path, filename))
                f.close()
                

    #prompts user to input project data
    def new_project_prompt(self):
        name, done1 = QtWidgets.QInputDialog.getText(
            self, 'Input Dialog', 'Enter the project/book name:')
        if done1:
            description, done2 = QtWidgets.QInputDialog.getText(
                self, 'Input Dialog', 'Enter a project description:')

        if done1 and done2 : 
            self.new_project_JSON_object(name, description)
        else:
            #Display some sort of error: "must have both name and description"
            pass
        

    
    #user inputs data and then a json object is created
    def new_project_JSON_object(self, name, desc):
        x = 1
        if (os.path.exists(os.path.join(script_dir, name) + '.json')):
            while (os.path.exists(os.path.join(script_dir, name) + str(x) +'.json')):
                x = x + 1
            abs_file_path = os.path.join(script_dir, name) + str(x) + '.json'
            os.makedirs(os.path.join(script_dir, name + str(x) + "-chapters"))
            folder = os.path.join(script_dir, name + str(x) + "-chapers")
        else:
            abs_file_path = os.path.join(script_dir, name) + '.json'
            os.makedirs(os.path.join(script_dir, name + "-chapters"))
            folder = os.path.join(script_dir, name + "-chapters")

        count = 0
        #determine how many objects in json file based on number of lines
        if os.path.isfile(abs_file_path) == TRUE:
            for line in open(abs_file_path):
                if len(line) > 5:
                    #5 is arbitrary length that is more than lines without objects on them
                    count += 1 
    
        #json entry of new project
        projectJsonEntry = {
            'id' : count,
            'name': name,
            'description': desc,
            'chapters' : [],
            'folder' : folder
        }

        j = json.dumps(projectJsonEntry)
        iLine = 0
        #check if file exists and count 
        if os.path.isfile(abs_file_path) == TRUE:
            with open(abs_file_path, 'r+') as r:
                lines = r.readlines()
                if not lines:
                    r.seek(0)
                    print('FILE IS EMPTY')
                    r.write('[' + '\n' + ']')
                    iLine = 1
                else:
                    for line in lines:
                        iLine += 1
                #iLine -= 1               
            with open(abs_file_path, "w") as f:
                for i, line in enumerate(lines):
                    if i == iLine:
                        f.write(',' + '\n' + j  +  "\n")
                    f.write(line)
        else:
            with open(abs_file_path, 'w') as f:
                f.write('[' + '\n' + j + '\n' + ']')         
        f.close  
        self.newProjectClicked(name, abs_file_path)

    #adds a btn link for a newly created project displaying project name
    def delete_project(self, name):
        file_path = name + '.json'
        os.remove(os.path.join(script_dir, file_path))

        directory_path = name + '-chapters'

        try:
            os.rmdir(os.path.join(script_dir, directory_path))
        except OSError as e:
            print("Error: %s : %s" % (os.path.join(script_dir, directory_path), e.strerror))

    def delete_project_prompt(self):
        abs_file_path = script_dir
        p = []
        for filename in os.listdir(abs_file_path):
            if filename.endswith(".json"):
                with open(os.path.join(abs_file_path, filename), "r") as f:
                    if len(f.readlines()) >= 1: # to make sure file has content
                        f.seek(0)
                        data = json.load(f)
                        for i in data:
                            proj = new_proj(i)
                            l = len(filename)
                            Remove_ext = filename[:l-5]
                            p.append(Remove_ext)
                f.close()
        
        pro, okPressed = QInputDialog.getItem(self, "Select project to delete", "Project:", p, 0, False )
        if okPressed and pro:
            self.delete_project(pro)
            #iterate through widgets and reload project links
            #items = (self.gridLayout.itemAt(i) for i in range(self.gridLayout.count()))
            for i in range(self.gridLayout.count()):
                self.gridLayout.itemAt(i).widget().deleteLater()
            self.populate_projects()
            

 
    @pyqtSlot()
    def newProjectClicked(self, name, file_path):
       
       btn = QPushButton(name, self)
       c = self.count
       r = self.row
       path = file_path
       btn.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                                QtWidgets.QSizePolicy.MinimumExpanding))

       root = tk.Tk()
       btn.setMaximumHeight(round(root.winfo_screenwidth() * (1/8)))
       btn.setMaximumWidth(round(root.winfo_screenwidth() * (1/8)))
       btn.setMinimumWidth(round(root.winfo_screenwidth() * (1/9)))
       btn.setMinimumHeight(round(root.winfo_screenwidth() * (1/9)))
       self.gridLayout.addWidget(btn, r, c, alignment = Qt.AlignTop)
       #self.QLayout.set

       if self.count == 3:
           self.count = -1
           self.row = self.row + 1
       self.count = self.count + 1
       
       #stopped here     

       if (file_path):
           btn.clicked.connect(lambda: self.openChapter(path))

       #btn.show()

    def openChapter(self, file_path):
               chapter = ChapterWindow()
               chapter.setFilepath(file_path)
               self.windows.append(chapter)
               chapter.showMaximized()
               pass

    def openProject(self, file_path):
        chapter = ChapterWindow()
        chapter.setFilepath(file_path)
        #Need to create a "Populate Scenes" function
        #chapter.addScene()
        #self.windows.append(chapter)
        chapter.showMaximized()
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()
    sys.exit(app.exec())      

