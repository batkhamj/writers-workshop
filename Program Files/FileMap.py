import sys, os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class File_Map(QMainWindow):
    def __init__(self):
        super().__init__()

        #open the data folder and get files to map
        file_path = os.path.abspath('Program Files/data')
        files =os.listdir(file_path)

        #only save json files
        to_map = []

        for file in files:
            if '.json' in file:
                to_map.append(file)

        print(files)
        print(to_map)

        

app = QApplication(sys.argv)
w = File_Map()
w.show()
app.exec()