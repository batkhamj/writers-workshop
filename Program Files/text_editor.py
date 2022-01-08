from os import close
from PyQt5 import Qt, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import *
import sys

import WikiLookup
import NameGenerator
import SettingGenerator

class TextWindow(QWidget):
    def __init__(self):
        super().__init__()
        QWidget.__init__(self)
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        
        menubar = QMenuBar()
        self.statusBar = QStatusBar
        layout.addWidget(menubar,0,0)
        
        #add window title
        text = "Untitled"
        self.title = QLabel(text)
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.AlignCenter)
        #layout.addWidget(self.title)
       
        #FBFile = menubar.addMenu("File")
        ### FBFile menu options 
        #self.open_new_file_act = QAction("Open", self)
        #FBFile.addAction(self.open_new_file_act)
        #self.open_new_file_act.triggered.connect(self.open_new_file)

        #self.save_current_file_act = QAction("Save", self)
        #FBFile.addAction(self.save_current_file_act)
        #self.save_current_file_act.triggered.connect(self.save_current_file)
        
        self.file_path = None

        toolsMenu = menubar.addMenu("Tools")

        #creates the font options action that opens up a window that allows for changing the font,
        #changing the font size, bolding, underlining, striking, and other options depending on the font selected
        font_options = QAction("Font Options", self)
        font_options.triggered.connect(self.font_options)
        toolsMenu.addAction(font_options)

        #creates the font color sub-menu that when hovered over shows some colors to change the text to
        fontColor = toolsMenu.addMenu("Font Color")

        #creates the black action which changes the text's color to black
        black = QAction("Black", self)
        black.triggered.connect(self.black)
        fontColor.addAction(black)

        #creates the red action which changes the text's color to red
        red = QAction("Red", self)
        red.triggered.connect(self.red)
        fontColor.addAction(red)

        #creates the yellow action which changes the text's color to yellow
        yellow = QAction("Yellow", self)
        yellow.triggered.connect(self.yellow)
        fontColor.addAction(yellow)

        #creates the blue action which changes the text's color to blue
        blue = QAction("Blue", self)
        blue.triggered.connect(self.blue)
        fontColor.addAction(blue)

        #creates the green action which changes the text's color to green
        green = QAction("Green", self)
        green.triggered.connect(self.green)
        fontColor.addAction(green)

        #creates the highlight sub-menu where you can toggle highlighting on or off
        highlight = toolsMenu.addMenu("Highlight")
        
        #creates the on action which turns highlighting on
        highlight1 = QAction("On", self)
        highlight1.triggered.connect(self.highlight1)
        highlight.addAction(highlight1)

        #creates the off action which turns highlighting off
        highlight2 = QAction("Off", self)
        highlight2.triggered.connect(self.highlight2)
        highlight.addAction(highlight2)

        #find tool button added
        find = QAction("Find", self)
        find.triggered.connect(self.find)
        toolsMenu.addAction(find)

        #adds the button for the spell check
        spellCheck = QAction("Spell Check", self)
        spellCheck.triggered.connect(self.spellCheck)
        toolsMenu.addAction(spellCheck)

        #remove highlights tool button added
        remover = QAction("Remove Highlights", self)
        remover.triggered.connect(self.remover)
        toolsMenu.addAction(remover)

        #add words to the custom dictionary tool button
        adder = QAction("Add Word To Dictionary", self)
        adder.triggered.connect(self.adder)
        toolsMenu.addAction(adder)

        self.scrollable_text_area = QTextEdit()

        layout.addWidget(self.scrollable_text_area, 1, 0)

        #Add a Wiki Look up option

        #Set up the info box
        self.wiki_info = QTextEdit()
        self.wiki_info.setFont(QFont("Helvetica", 16))

        #set up title box
        self.wiki_title = QLabel()
        self.wiki_title.setFont(QFont("Times", 24))
        self.wiki_title.setText("No Search Available")
        self.wiki_title.setAlignment(QtCore.Qt.AlignCenter)

        #store related wiki search results
        self.relevant = [] 
        self.res_place = 0

        #allign widget and hide till activated
        layout.addWidget(self.wiki_info, 1, 1)
        layout.addWidget(self.wiki_title, 0, 1)
        self.wiki_info.setParent(self)
        self.wiki_info.hide()
        self.wiki_title.hide()

        wiki_check = QAction("Look up online", self)
        wiki_check.triggered.connect(self.check_wiki)
        toolsMenu.addAction(wiki_check)

        #Wikipedia switching actions -- checkout other results
        page_prev = QAction("Previous Result", self)
        page_prev.setShortcut(QKeySequence('CTRL + Left'))
        page_prev.triggered.connect(self.wiki_prev)

        page_next = QAction("Next Result", self)
        page_next.setShortcut(QKeySequence('CTRL + Right'))
        page_next.triggered.connect(self.wiki_next)

        close_wiki = QAction("Exit", self)
        close_wiki.setShortcut(QKeySequence('CTRL + Down'))
        close_wiki.triggered.connect(self.wiki_exit)

        #hidden menu for using wiki actions
        self.wm = QMenuBar()
        self.wm.addAction(page_prev)
        self.wm.addAction(page_next)
        self.wm.addAction(close_wiki)
        layout.addWidget(self.wm, 2, 1)
        self.wm.hide()

        #Undo and Redo is a built-in feature of QTextEdit
        self.scrollable_text_area.setUndoRedoEnabled(True)

        self.scrollable_text_area.textChanged.connect(self.WordCount)
        self.WordCount()

        #Inserts menu
        InsertsMenu = menubar.addMenu("Insert")
        GenNames = QAction("Names", self)
        GenNames.triggered.connect(self.Names_Box)
        InsertsMenu.addAction(GenNames)
        GenSetting = QAction("Setting", self)
        GenSetting.triggered.connect(self.SettingsBox)
        InsertsMenu.addAction(GenSetting)
        Image = QAction("Image", self)
        Image.triggered.connect(self.Insert_Image)
        InsertsMenu.addAction(Image)

    def WordCount(self):
        #Count the number of words in a document
        #May have to rework this implementation
        text = self.scrollable_text_area.toPlainText()
        count = 0
        words = text.split()
        for word in words:
            count = count + 1
            
        message = "Word Count : " + str(count)
        self.statusBar().showMessage(message)
        return str(count)

    def open_new_file(self):
        #Removed the filetype filter in QFileDialog
        self.file_path, filter_type = QFileDialog.getOpenFileName(self, "Open new file",
                "", "")
        if self.file_path:
            with open(self.file_path, "r") as f:
                file_contents = f.read()
                self.title.setText(self.file_path)
                self.scrollable_text_area.setText(file_contents)
        else:
            self.invalid_path_alert_message()

    #def save_current_file(self):
        #if not self.file_path:
            #new_file_path, filter_type = QFileDialog.getSaveFileName(self, "Save this file as...", "", "All files (*)")
            #if new_file_path:
                #self.file_path = new_file_path
            #else:
                #self.invalid_path_alert_message()
                #return False
        #So the solution for formatted text Ive seen is using Html filetype
        #file_contents = self.scrollable_text_area.toHtml()
        #with open(self.file_path, "w") as f:
            #f.write(file_contents)
        #self.title.setText(self.file_path)
    
    def invalid_path_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Invalid file")
        messageBox.setText("Selected filename or path is not valid. Please select a valid file.")
        messageBox.exec()
    
    #when font options is pressed, bring up the font menu and set the text to the selected options
    def font_options(self):
        font, ok = QFontDialog.getFont(self.scrollable_text_area.font(), self)
        if ok:
            #Make a cursor to get selected word
            cursor = self.scrollable_text_area.textCursor()
            
            #char format is used to change text selection
            format = QTextCharFormat()
            format.setFont(font)
            cursor.setCharFormat(format)
            self.scrollable_text_area.setTextCursor(cursor)

    #when black is pressed, set the text color to black
    def black(self):
        self.scrollable_text_area.setTextColor(QtGui.QColor("#000000"))

    #when red is pressed, set the text color to red
    def red(self):
        self.scrollable_text_area.setTextColor(QtGui.QColor("#FF0000"))

    #when yellow is pressed, set the text color to yellow
    def yellow(self):
        self.scrollable_text_area.setTextColor(QtGui.QColor("#FFFF00"))

    #when blue is pressed, set the text color to blue
    def blue(self):
        self.scrollable_text_area.setTextColor(QtGui.QColor("#0000FF"))

    #when green is pressed, set the text color to green
    def green(self):
        self.scrollable_text_area.setTextColor(QtGui.QColor("#00FF00"))

    #when highlight on is pressed, toggles the highlighter to on
    def highlight1(self):
        self.scrollable_text_area.setTextBackgroundColor(QtGui.QColor("#CCFF00"))

    #when highlight off is pressed, toggles the highlighter to off
    def highlight2(self):
        self.scrollable_text_area.setTextBackgroundColor(QtGui.QColor("#FFFFFF"))

    #brings up the child window and continues to find2 upon closing
    def find(self):
        self.findBox = searchWindow()
        self.findBox.text.connect(self.find2)
        self.findBox.show()

    #upon closing the child window the inputted text is transfered over
    @QtCore.pyqtSlot(str)
    def find2(self, word):
        #search word, set to lowercase so the search is not case sensitive
        input = word
        input = input.lower()

        #takes in the text file
        text = self.scrollable_text_area.toPlainText()
        words = text.split()

        #puts a cursor over the text file that goes down each word
        cursor = self.scrollable_text_area.textCursor()
        cursor.movePosition(1, 0, 1)
        cursor.movePosition(14, 1, 1)

        #blue highlight format for the found words
        highlight = QTextCharFormat()
        highlight.setBackground(QtGui.QColor("#30C5FF"))

        #for every word in the text file
        for i in words:
            i = i.lower()

            #if the current word matches the input
            if  i == input:
                #set the word within the text file to be highlighted
                cursor.setCharFormat(highlight)
            
            #moves to the next word within the text file
            cursor.movePosition(18, 0, 1)
            cursor.movePosition(5, 0, 1)
            cursor.movePosition(14, 1, 1)

    #spell cheker that highlights misspelled words
    def spellCheck(self):
        #converts everything in the text file to plain text
        text = self.scrollable_text_area.toPlainText()
        words = text.split()

        #puts a cursor over the text file that goes down each word
        cursor = self.scrollable_text_area.textCursor()
        cursor.movePosition(1, 0, 1)
        cursor.movePosition(14, 1, 1)

        #red highlight format for mispelled words
        highlight = QTextCharFormat()
        highlight.setBackground(QtGui.QColor("#FFCCCB"))

        #goes through every word in the text file
        for i in words:
            #if the word is found in a dictionary or has an uppercase, number, or symbol character found is set to 1
            found = 0

            #checks for capital letters
            for char in i:
                if char.isupper():
                    found = 1

            #checks for numbers or symbols
            if not i.isalnum() or i.isdigit():
                found = 1
            
            #goes through the dictionary file to check if the current word is present
            if found == 0:
                with open("dictionaries/dictionary.txt", "r") as file1:
                    for j in file1:
                        j = j.strip()
                        if i == j:
                            found = 1
                            break
            
            #goes through the custom dictionary file to check if the current word is present
            if found == 0:
                with open("dictionaries/custom_dictionary.txt", "r") as file2:
                    for k in file2:
                        if i == k:
                            found = 1
                            break
            
            #if the word was not found, mark it
            if found == 0:
                #set the word within the text file to be highlighted
                cursor.setCharFormat(highlight)

            #moves to the next word within the text file
            cursor.movePosition(18, 0, 1)
            cursor.movePosition(5, 0, 1)
            cursor.movePosition(14, 1, 1)

    def remover(self):
        #puts a cursor over the text file that goes down each word
        cursor = self.scrollable_text_area.textCursor()
        cursor.movePosition(1, 0, 1)
        cursor.movePosition(11, 1, 1)

        clear = QTextCharFormat()
        clear.setBackground(QtGui.QColor("#FFFFFF"))

        cursor.setCharFormat(clear)

    def adder(self):
        self.addWord = addWindow()
        self.addWord.show()
    
    #Function for Generated Names
    def Names_Box(self):
        box = QMessageBox()
        n = NameGenerator.NameGen
        names = []
        names = n.Generate_Names()

        box.setText("Generated Random Names")
        box.setInformativeText(str(names[0]+'\n'+names[1]+'\n'+names[2]+'\n'+names[3]+'\n'+
                        names[4]+'\n'+names[5]+'\n'+names[6]+'\n'+names[7]+'\n'))
        box.exec_()
    def SettingsBox(self):
        newBox = QMessageBox()
        s = SettingGenerator.SettingGenerator()
        newBox.setText("Generated Setting")
        newBox.setInformativeText(s)
        newBox.exec_()

    def Insert_Image(self):
        print('inserting image')

        cursor = QTextCursor(self.scrollable_text_area.document())
        cursor_position = cursor.position()
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Add Image to Document", "","All Files (*)", options=options)
        if fileName:
            cursor.insertImage(fileName)
    
    def check_wiki(self):
        #Make a cursor to get selected word
        cursor = self.scrollable_text_area.textCursor()

        #separate word that is selected to be looked up
        text = self.scrollable_text_area.toPlainText()
        string = text[cursor.selectionStart():cursor.selectionEnd()]

        #Searching an empty string removes wiki box
        if(string == ""):
            self.wiki_exit()
        else:
            #Call the find function and get the wikipedia info
            results, self.relevant, pg_title = WikiLookup.WikiInfo.find(self, string)

            #set search result
            self.wiki_info.setText(results)
            self.wiki_title.setText(pg_title)

            #activate modules
            self.wiki_info.show()
            self.wiki_title.show()
            self.wm.show()

    def wiki_prev(self):
        #variables for the last result
        scrap = []
        term = ""
        #search and change text if possible
        if self.res_place > 0:
            self.res_place -= 1
            term = self.relevant[self.res_place]
            
            p_res, scrap, p_title = WikiLookup.WikiInfo.find(self, term)

            self.wiki_info.setText(p_res)
            self.wiki_title.setText(p_title)

    def wiki_next(self):
        #variables to get next result
        scrap = []
        term = ""
        #iterate to next relevant article, search and change text if successful
        if self.res_place < len(self.relevant):
            self.res_place += 1
            term = self.relevant[self.res_place]
            
            n_res, scrap, n_title = WikiLookup.WikiInfo.find(self, term)

            self.wiki_info.setText(n_res)
            self.wiki_title.setText(n_title)

    def wiki_exit(self):
        self.wiki_title.hide()
        self.wiki_info.hide()
        self.wm.hide()
#Child window that pops up and takes in the word to find
class searchWindow(QWidget):

    text = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        #window size and title
        self.setGeometry(500, 500, 320, 120)
        self.setWindowTitle("Find")
        
        #small text box for inputting search word
        self.textbox = QTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 30)
        
        #button to close and send the inputted text
        self.button = QPushButton("OK", self)
        self.button.move(20, 70)
        self.button.clicked.connect(self.toText)

    #upon closing the window, the inputted string is converted to plaintext and emitted to be taken in by the parent window
    def toText(self):
        word = self.textbox.toPlainText()
        self.text.emit(word)
        self.close()
        
#window for adding words to the custom dictionary
class addWindow(QWidget):
    def __init__(self):
        super().__init__()

        #window size and title
        self.setGeometry(500, 500, 320, 120)
        self.setWindowTitle("Add Word")
        
        #small text box for inputting words you want to add
        self.textbox = QTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 30)
        
        #button to add the inputted text
        self.button = QPushButton("Add", self)
        self.button.move(20, 70)
        self.button.clicked.connect(self.addWord)

    def addWord(self):
        #converts the text to a string and sets it to lowercase
        text = self.textbox.toPlainText()
        text = text.lower()

        #does not add the word if there are multiple words put in the text box
        if len(text.split()) > 1:
            popup = QMessageBox()
            popup.setText("Word Not Added: Multiple Words Entered")
            popup.exec_()
            return

        #does not add the word if the word contains a symbol or number
        if not text.isalnum() or text.isdigit():
            popup = QMessageBox()
            popup.setText("Word Not Added: Includes symbol/number")
            popup.exec_()
            return

        #makes sure the word does not already exist within the given dictionary
        with open("dictionaries/dictionary.txt", "r") as file1:
                    for j in file1:
                        j = j.strip()
                        if text == j:
                            popup = QMessageBox()
                            popup.setText("Word Not Added: Already In Dictionary")
                            popup.exec_()
                            return

        #makes sure the word does not already exist within the custom dictionary
        with open("dictionaries/custom_dictionary.txt", "r") as file2:
                    for k in file2:
                        if text == k:
                            popup = QMessageBox()
                            popup.setText("Word Not Added: Already In Custom Dictionary")
                            popup.exec_()
                            return

        #enters the word into the custom dictionary txt file   
        file = open("dictionaries/custom_dictionary.txt", "a")
        file.write("\n")
        file.write(text)
        file.close()

        #gives a popup letting the user know the word was added
        popup = QMessageBox()
        popup.setText("Word Added")
        popup.exec_()
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = TextWindow()
    screen.showMaximized()
    sys.exit(app.exec_())