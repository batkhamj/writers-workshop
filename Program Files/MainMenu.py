from os import name
import sys
from typing import Text
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from text_editor import TextWindow
from SceneWindow import SceneWindow


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        #Adding functionality for opening multiple windows
        self.textWindows = [] #Array for storing new windows
        self.open_text_window = QAction("New", self)
        self.open_text_window.setShortcut("Ctrl+N")
        self.open_text_window.triggered.connect(self.OpenTextWindow)

        self.open_scene_window = QAction("New Scene", self)
        self.open_scene_window.triggered.connect(self.OpenSceneWindow)

        #Quit Button
        self.quit_app = QAction("Quit", self)
        self.quit_app.triggered.connect(self.QuitApp)

        #Taskbar variables
        self.TB_Status = 0
        self.TaskBar = QTabWidget()

        #file actions tool bar "grid"
        QWidget.__init__(self)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
    
        #resize main window
        self.resize(500, 500)
        self.setWindowTitle("Testing")

        #create menu bar
        menubar = QMenuBar()
        self.layout.addWidget(menubar, 0, 0)

        #File btn
        fileBarSave = menubar.addMenu("Menu")
        fileBarSave.addAction(self.open_text_window)
        fileBarSave.addAction(self.open_scene_window)
        fileBarSave.addSeparator()
        fileBarSave.addAction(self.quit_app)

        #Add close button to tabs to make them closeable
        self.TaskBar.setTabsClosable(True)
        self.TaskBar.tabCloseRequested.connect(self.CloseTab)

        #Make tabs moveable
        self.TaskBar.setMovable(True)
        
    def OpenTextWindow(self):
        w = TextWindow()
        w.showMaximized()
        self.textWindows.append(w)
        self.TaskBarCheck(w)

    def OpenSceneWindow(self):
        w = SceneWindow()
        w.showMaximized()
        self.textWindows.append(w)
        self.TaskBarCheck(w)

    #TaskBarCheck -- check if there are enough windows to start taskbar and update taskbar
    def TaskBarCheck(self,w):
        #Add original Doc to tabs
        if len(self.textWindows) <= 1:
            self.TaskBar.setDocumentMode(True)
            self.tab = w
            i = self.TaskBar.addTab(self.tab, str(len(self.textWindows)))
            self.layout.addWidget(self.TaskBar)
            self.TaskBar.setCurrentIndex(i)
            
        #at 2 docs display taskbar
        elif len(self.textWindows) > 1 and self.TB_Status == 0:
            self.TB_Status = 1
            self.tab = w
            i = self.TaskBar.addTab(self.tab, str(len(self.textWindows)))
            self.layout.addWidget(self.TaskBar)
            self.TaskBar.setCurrentIndex(i)

        #every new doc opened from main menu adds a tab
        elif len(self.textWindows) > 1 and self.TB_Status == 1:
            self.tab = w
            i = self.TaskBar.addTab(self.tab, str(len(self.textWindows)))
            self.TaskBar.setCurrentIndex(i)  

  
    def CloseTab(self, i):
        if len(self.textWindows) < 2:
            self.quit_app.triggered.connect(self.QuitApp)
        self.TaskBar.removeTab(i)
        self.textWindows.pop()
         
    #Quit Button Functionality
    def QuitApp(self):
        sys.exit(app.exec())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()
    sys.exit(app.exec())


