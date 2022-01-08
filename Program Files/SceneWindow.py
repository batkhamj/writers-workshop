import sys
from PyQt5.QtGui import QFocusEvent, QFont, QTextDocument
from PyQt5.QtWidgets import QAction, QFileDialog, QLineEdit, QMenuBar, QTextEdit, QLineEdit, QVBoxLayout, QWidget, QApplication, QMainWindow, QStatusBar
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from text_editor import TextWindow
import json
import os
import io

class SceneWindow(QMainWindow):
    saved = pyqtSignal(dict)

    def WordCount(self):
        #Count the number of words in a document
        #May have to rework this implementation
        text = self.text.scrollable_text_area.toPlainText()
        self.count = 0
        words = text.split()
        for word in words:
            self.count = self.count + 1
            
        message = "Word Count : " + str(self.count)
        self.statusBar().showMessage(message)
        return str(self.count)
    
    def __init__(self, path = "", title = ""):
        super().__init__()
        self.setGeometry (300, 300, 500, 500)

        #Create Text box widget
        self.id = 0
        self.chapter = ""
        self.setWindowTitle("New Scene " + str(self.id))
        central = QWidget()
        layout = QVBoxLayout()
        self.menubar = QMenuBar()
        self.title = QLineEdit()
        self.title.setFont(QFont('Times', 12))
        self.text = TextWindow()
        self.text.setFont(QFont('Times', 12))

        file = self.menubar.addMenu("File")
        #self.open = QAction("Open", self)
        #file.addAction(self.open)
        #self.open.setShortcut("Ctrl+O")
        #self.open.triggered.connect(self.open_file)

        self.save = QAction("Save", self)
        file.addAction(self.save)
        self.save.setShortcut("Ctrl+S")
        self.save.triggered.connect(self.save_file)
        
        self.chapterdir = ""
        if path != "":
            self.filepath = path
            if title != "":
                self.open_file(self.filepath, title)
        else: self.filepath = ""


        self.title.setPlaceholderText("New Scene")

        layout.addWidget(self.menubar)
        layout.addWidget(self.title)
        layout.addWidget(self.text)
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.text.scrollable_text_area.textChanged.connect(self.WordCount)
        #self.WordCount()

    def set_id(self, id):
        self.id = id
        self.setWindowTitle("New Scene " + str(self.id))

    def open_file(self, path = "", title = ""):
        print(path)
        if path != "":
            file = open(path)
            textfile = json.load(file)
            print(textfile)
            if title != "":
                for item in textfile['scenes']:
                    if item['title'] == title:
                        self.setWindowTitle(item['title'])
                        self.title.setText(item['title'])
                        
                        filepath = self.chapterdir + "/" + item['title'] + ".html"
                        if os.path.isfile(filepath):
                            file2 = io.open(filepath, "r")
                            text = file2.read()
                            file2.close()
                            self.text.scrollable_text_area.setText(text)
                        else:
                            self.text.scrollable_text_area.setText(item['body'])
                return
            else:
                file.close()
                self.filepath = path
                return

        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open file",
                "", "JSON files (*.json)")

        if self.file_path != "":
            file = open(self.file_path)
            textfile = json.load(file)
            self.title.setText(textfile['title'])

            filepath = self.chapterdir + "/" + textfile['title'] + ".html"
            if os.path.isfile(filepath):
                file2 = io.open(filepath, "r")
                text = file2.read()
                file2.close()
                self.text.scrollable_text_area.setText(text)
            else:
                self.text.scrollable_text_area.setText(textfile['body'])

            file.close()

    def save_file(self):
        textfile = {'title': self.title.text(), 'body': self.text.scrollable_text_area.toPlainText(), 'wordcount' : self.WordCount()}
        #filepath = ""
        #if textfile['title'] == "" and textfile['body'] == "":
            #return
        #if self.title.text() == "":
            #filepath = os.path.join(self.chapterdir, ("NewScene" + str(self.id) + ".json"))
            #pass
        #else:
            #x = 1
            #if (os.path.exists(os.path.join(self.chapterdir, (self.title.text() + '.json')))):
                #while(os.path.exists(os.path.join(self.chapterdir, (self.title.text() + str(x) + '.json')))):
                    #x = x + 1
                #filepath = os.path.join(self.chapterdir, (self.title.text() + str(x) + ".json"))
            #else:
                #filepath = os.path.join(self.chapterdir, (self.title.text() + ".json"))
        #with open (filepath, 'w') as file:
            #json.dump(textfile, file)
        self.saved.emit(textfile)
        self.setWindowTitle(self.title.text())

        formattedFile = self.chapterdir + "/" + self.title.text() + ".html"
        formattedText = self.text.scrollable_text_area.toHtml()
        file2 = io.open(formattedFile, "w")
        file2.write(formattedText)
        file2.close

        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SceneWindow()
    window.showMaximized()
    sys.exit(app.exec_())