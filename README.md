# alabio

To start our program, run the executable file named "Writer's Workshop.exe"
or alternatively run the file named "launchWindow.py" within the "Program Files" folder.
The launch menu allows you to create projects by clicking "Add Project"
The project files are created within the /data folder
(The main menu does not have scrolling functionality yet, and creating too many projects will cause them to not display
in the window correctly)

After creating a project, you can click on the project's card to bring up the scene menu.
This window allows you to create chapters and scenes within the project.  Clicking the "New Chapter" button on the left column allows you to create a new chapter within the project.  When you create a chapter, the right column is updated so that you can create scenes within the chapter.  Clicking the "open" button on a given scene will open the
scene editor.  The scene can be given a name in the top bar, and content in the lower area.

The chapter menu also allows you to open the character editor, which allows you to enter fields of information about a character.  The character editor has full save and load functionality, and saves its content to a folder within /data.

Within the scene editor, there are several options:
"File" has two options within it that are pretty self explanatory: "Open" and "Save".
"Open" opens up a preexisting file from your own file directory and displays the text within on the text editor.
"Save" saves whatever has been typed out into a file.

"Tools" has six options within it: "Font Options", "Font Color", "Highlight", "Find", "Spell Check", and "Remove Highlight".
"Font Options" when selected brings up a small window that allows the user to change the font, change the font size, underline, strike, and other options depending on selected font.
"Font Color" is a submenu that brings up five colors (black, red, yellow, blue, green) that when selected changes the font's color to the one selected.
"Highlight" is a submenu with two options, on and off, that respectively turn on or off highlighting for the background of the text.
"Find" when selected opens a child window that takes in a words (though it will only work with one word) and highlights all occurances of the inputted word.
"Spell Check" when selected highlights all words not in the dictionary or custom dictionary and not containing uppercase, numeric, or symbol character.
"Remove Highlight" does exactly what it says and removes all highlights from the document. This helps in clearing highights from find and spellcheck

"Insert" contains a random generator for character names, a setting name for the author, and an option to add an image to the page. 

"Tools" menu has new option called "Look up online" it allows you to search a selected word and bring up the wikipedia summary for the selection. A tool bar controls results and allows you to close the window.

Dependencies:
pip install wikipedia
