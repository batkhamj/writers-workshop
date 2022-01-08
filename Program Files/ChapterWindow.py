import sys
from tkinter.constants import FALSE, TRUE
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from SceneWindow import SceneWindow
from Character_Info import characterWindow
import json
import os

class NewSceneWidget(QWidget):
    new_scene = pyqtSignal(dict)

    def __init__(self, index):
        super().__init__()

        self.windows = []
        self.file = ""
        self.dir = ""
        self.name = ""
        self.layout = QHBoxLayout()
        self.title = QLabel()
        self.wordcount = QLabel()
        self.open = QPushButton()
        self.rename = QPushButton()
        self.index = index + 1

        self.title.setText(str(self.index) + "     -     New Scene")
        self.open.setText("Open")
        self.open.setFixedWidth(100)
        self.rename.setText("Rename")
        self.rename.setFixedWidth(100)

        self.open.clicked.connect(self.openScene)
        self.rename.clicked.connect(self.Rename)

        self.layout.addWidget(self.open, 1)
        self.layout.addWidget(self.rename, 1)
        self.layout.addWidget(self.title, 2)
        self.layout.addWidget(self.wordcount, 1)
        self.setLayout(self.layout)

    def openScene(self):
        self.w = SceneWindow()
        self.w.set_id(self.index)
        self.w.chapterdir = self.dir
        self.w.save.triggered.connect(self.changeScene)
        self.w.saved.connect(self.setFilepath)
        self.windows.append(self.w)
        if self.file != "":
            self.w.open_file(self.file, self.name)
        self.w.showMaximized()

    def setFilepath(self, filepath):
        #self.file = filepath
        self.new_scene.emit(filepath)
        self.changeScene
        pass

    def Rename(self):
            name, done = QInputDialog.getText(self, 'Input Dialog', 'Enter the Scene Name:')

            found = 0
            if done:
                self.title.setText(str(self.index) + "     -     " + name)
            
            if os.path.exists(self.file):
                chapter = open(self.file)
                object = json.load(chapter)
                for item in object['scenes']:
                    if item['title'] == self.name:
                        item['title'] = name
                        found = 1
                        break
                if found == 0:
                    scene = {
                    'title': name,
                    'body': "",
                    'words': 0
                    }
                    object['scenes'].insert(self.index - 1, scene)
                chapter.close()
                with open(self.file, 'w') as f:
                    f.seek(0)
                    json.dump(object, f)
                    f.truncate()
                    f.close()

                self.name = name
                pass


    def changeScene(self):
        print("changeScene")
        if self.w.text.scrollable_text_area.toPlainText() == "" and self.w.title.text() == "":
            return
        if self.w.title.text() != "":
            self.name = self.w.title.text()
            self.title.setText(str(self.index) + "     -     " + self.w.title.text())
        if self.w.count != 0:
            self.wordcount.setText("Words: " + str(self.w.count))



class NewChapterWidget(QWidget):
    def __init__(self, index, filepath):
        super().__init__()

        self.chapters = []
        self.file = filepath
        self.filename = ""

        self.layout = QHBoxLayout()
        self.wordcount = QLabel()
        self.button = QPushButton()
        self.rename = QPushButton()
        self.index = index + 1

        self.button.setText(str(self.index) + "    -    New Chapter")
        self.rename.setText("Rename")
        self.button.setFixedWidth(200)

        self.rename.clicked.connect(self.Rename)

        self.layout.addWidget(self.rename)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.wordcount)
        self.setLayout(self.layout)

    def Rename(self):
        name, done = QInputDialog.getText(
            self, 'Input Dialog', 'Enter the Chapter Name:')

        if done:
            self.button.setText(str(self.index) + "   -   " + name)

            oldfilename = self.filename
            self.filename = str(self.index) + name
            file = os.path.join(self.file, oldfilename + ".json")
            if os.path.exists(file):
                chapter = open(file)
                object = json.load(chapter)
                object['title'] = name
                with open(file, 'w') as f:
                    f.seek(0)
                    json.dump(object, f)
                    f.truncate()
                    f.close()
                chapter.close()
                os.rename(os.path.join(self.file, oldfilename + ".json"), 
                os.path.join(self.file, self.filename + ".json"))
                return 0

            file = os.path.join(self.file, str(self.index) + name + ".json")
            if os.path.exists(file):
                chapter = open(file)
                object = json.load(chapter)
                object['title'] = name
                with open(file, 'w') as f:
                    json.dump(object, f)
            else:
                chapter = {
                    'index' : self.index,
                    'title' : name,
                    'scenes' : []
                }
                with open(file, 'w') as f:
                    json.dump(chapter, f)
        else:
            return -1
                
            #Create a new Chapter json





class Sidebar(QWidget):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.chapters = []
        self.index = 0

        self.layout = QVBoxLayout()
        self.new = QPushButton()

        self.new.setText("New Chapter")
        self.new.setFixedWidth(200)

        self.layout.addWidget(self.new)
        self.setLayout(self.layout)

        self.new.clicked.connect(lambda:self.addChapter())

    def setFilepath(self, path):
        self.filepath = path
        self.populateChapters()
        for chapter in self.chapters:
            chapter.file = path
        pass

    def populateChapters(self):
        i = 0
        for file in os.listdir(self.filepath):
            if file.endswith(".json"):
                chapter = open(os.path.join(self.filepath, file))
                object = json.load(chapter)
                self.addChapter(object['title'], FALSE)
                if i == 0 and self.chapters != []:
                    print("here")
                    self.parentWindow.populateScenes(self.chapters[0].file, self.chapters[0].filename)
                    i = 1
        pass

    def addChapter(self, title = "", populate = TRUE):
        c = NewChapterWidget(self.index, self.filepath)
        self.chapters.append(c)
        #c.new_scene.connect(self.saveToJson)
        #c.dir = self.scenepath
        self.index = self.index + 1

        self.layout.removeWidget(self.new)
        self.layout.addWidget(c)
        self.layout.addWidget(self.new, alignment=Qt.AlignCenter)
        c.button.clicked.connect(lambda:self.parentWindow.populateScenes(c.file, c.filename))
        if title == "":
            done = c.Rename()
            if done == -1:
                c.button.disconnect()
                self.layout.removeWidget(self.new)
                self.layout.removeWidget(c)
                self.chapters.remove(c)
                self.layout.addWidget(self.new, alignment=Qt.AlignCenter)
                self.index = self.index - 1
                return
        else:
            if populate == TRUE: self.parentWindow.populateScenes(c.file, c.filename)
            c.button.setText(str(c.index) + "   -   " + title)
            c.filename = str(self.index) + title
            print(c.filename)



class ChapterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setGeometry (300, 300, 500, 500)
        self.scenes = []
        self.characters = []
        self.index = 0
        self.filepath = ""
        self.scenepath = ""

        #Create Text box widget
        self.setWindowTitle("New Project")
        self.chapterLabel = QLabel()
        self.projectLabel = QLabel()
        central = QWidget()
        left = QWidget()
        right = QWidget()
        self.leftlayout = QVBoxLayout()
        self.rightlayout = QVBoxLayout()
        mainlayout = QHBoxLayout()
        windowlayout = QVBoxLayout()
        self.menubar = QMenuBar()
        self.new = QPushButton()

        menu = self.menubar.addMenu("Menu")

        self.sidebar = Sidebar(self.filepath)
        self.sidebar.parentWindow = self
        #self.new_scene = QAction("New Scene", self)
        #self.new_scene.triggered.connect(self.addScene)
        #self.new_scene.setShortcut("Ctrl+N")
        #menu.addAction(self.new_scene)

        self.characterAction = QAction("Character Info.", self)
        self.characterAction.triggered.connect(self.characterInfo)
        menu.addAction(self.characterAction)
        
        self.new.setText("New Scene")
        self.new.setFixedWidth(100)
        self.new.clicked.connect(lambda:self.addScene())

        windowlayout.addWidget(menu)

        #Chapter menu setup
        self.leftlayout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.projectLabel.setText("No Current Project")
        self.leftlayout.addWidget(self.projectLabel, alignment=Qt.AlignCenter)
        self.leftlayout.addWidget(self.sidebar)
        left.setLayout(self.leftlayout)
        
        #Scene menu setup
        self.rightlayout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        #self.addScene()
        self.rightlayout.addWidget(self.chapterLabel, alignment=Qt.AlignCenter)
        #self.rightlayout.addWidget(self.new, alignment=Qt.AlignCenter)
        right.setLayout(self.rightlayout)

        mainlayout.addWidget(left)
        mainlayout.addWidget(right, 5)
        windowlayout.addLayout(mainlayout, 6)
        central.setLayout(windowlayout)
        central.setMinimumSize(500, 550)
        self.setCentralWidget(central)

    def addScene(self, title = "", wordcount = 0):
        #Add a new scene widget
        print("appending scene: " + title)
        s = NewSceneWidget(self.index)
        self.scenes.append(s)
        s.new_scene.connect(self.saveToJson)
        s.dir = self.scenepath
        s.file = self.filepath
        self.index = self.index + 1

        if title != "":
            s.title.setText(str(s.index) + "     -     " + title)
            s.name = title
        if wordcount != 0:
            s.wordcount.setText("Words: " + str(wordcount))
    
        self.rightlayout.removeWidget(self.new)
        self.rightlayout.addWidget(s)
        self.rightlayout.addWidget(self.new, alignment=Qt.AlignCenter)


    def characterInfo(self):
        s = characterWindow()
        self.characters.append(s)
        s.show()
        
    def setFilepath(self, path):
        self.filepath = path
        file = open(path)
        self.chapter = json.load(file)
        for item in self.chapter:
            self.scenepath = item['folder']
            self.sidebar.setFilepath(self.scenepath)
            self.setProjectName(item['name'])
            self.setWindowTitle(item['name'])
        file.close()

    def setProjectName(self, name):
        self.projectLabel.setText(name)

    def populateScenes(self, path, name):
        print("Populating Scenes")
        print(len(self.scenes))
        self.rightlayout.removeWidget(self.new)
        for scene in self.scenes:
            #self.index = self.index - 1
            self.rightlayout.removeWidget(scene)
            print("removing widget")
        self.scenes.clear()
        self.index = 0

        self.chapterLabel.setText(name[1:] + "   -   Scenes")
        if name == "": return 1
        file = open(os.path.join(path, name + ".json"))
        self.filepath = os.path.join(path, name + ".json")
        chapter = json.load(file)
        if chapter ['scenes'] != "":
            for item in chapter['scenes']:
                self.addScene(item['title'], item['wordcount'])
        if len(self.scenes) == 0:
            pass
            self.rightlayout.addWidget(self.new, alignment=Qt.AlignCenter)
        file.close()
        pass

    def saveToJson(self, scene):
        found = False
        file = open(self.filepath)
        chapter = json.load(file)
        if "scenes" in chapter:
            for item in chapter['scenes']:
                if item['title'] == scene['title']:
                    item['body'] = scene['body']
                    item['wordcount'] = scene['wordcount']
                    found = True
                    break
            if found == False:
                chapter['scenes'].append(scene)
            with open(self.filepath, 'w') as f:
                json.dump(chapter, f)
                f.close()
            return
        for item in chapter:
            if "scenes" in item:
            #Need to change this later
                item['scenes'].append(scene)
        with open(self.filepath, 'w') as f:
            json.dump(chapter, f)
            f.close()
        file.close()
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChapterWindow()
    window.showMaximized()
    sys.exit(app.exec_())