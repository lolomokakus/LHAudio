import sys
import datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import *
import lhaudio
import os

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        promptWidth = 275
        self.fileList = []
        self.outputFile = ""
        self.inputFile = ""
        self.outputDir = ""

        monoFont = QFont()
        monoFont.setFamily("Monospace")
        monoFont.setPointSize(10)

        self.inputLabel = QLabel("Input file(s):", self)
        self.inputLabel.move(22, 20)

        self.inputFileList = QListWidget(self)
        self.inputFileList.resize(398, 200)
        self.inputFileList.move(20, 41)

        self.inputFileButton = QPushButton("Add", self)
        self.inputFileButton.clicked.connect(self.selectFile)
        self.inputFileButton.move(335, 245)

        self.listDeleteButton = QPushButton("Remove", self)
        self.listDeleteButton.move(250, 245)
        self.listDeleteButton.clicked.connect(self.listDelete)

        self.listClearButton = QPushButton("Clear", self)
        self.listClearButton.move(20, 245)
        self.listClearButton.clicked.connect(self.listClear)

        self.outputLabel = QLabel("Output directory:", self)
        self.outputLabel.move(22, 290)

        self.outputDirPrompt = QLineEdit(self)
        self.outputDirPrompt.setReadOnly(True)
        self.outputDirPrompt.setFixedWidth(promptWidth)
        self.outputDirPrompt.move(20, 310)

        self.outputDirButton = QPushButton("Select directory", self)
        self.outputDirButton.clicked.connect(self.selectDir)
        self.outputDirButton.move(promptWidth + 21, 310)

        self.modeLabel = QLabel("Select mode:", self)
        self.modeLabel.move(22, 360)

        self.encodeRadio = QRadioButton("Encode", self)
        self.encodeRadio.toggle()
        self.encodeRadio.move(20, 382)
        self.decodeRadio = QRadioButton("Decode", self)
        self.decodeRadio.move(110, 382)

        self.quitButton = QPushButton("Quit", self)
        self.quitButton.clicked.connect(self.close)
        self.quitButton.move(249, 375)
        self.startButton = QPushButton("Execute", self)
        self.startButton.move(334, 375)
        self.startButton.clicked.connect(self.execute)

        self.terminalLabel = QLabel("Terminal output:", self)
        self.terminalLabel.move(442, 20)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)
        
        self.terminalWindow = QTextEdit(self)
        self.terminalWindow.setReadOnly(True)
        self.terminalWindow.setFont(monoFont)
        self.terminalWindow.resize(398, 200)
        self.terminalWindow.move(440, 41)

        self.setFixedSize(860, 425)
        self.setWindowTitle("LHAudioQT")

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def selectFile(self):
        selectedFile = QFileDialog.getOpenFileName(self)

        if selectedFile != "":
            self.fileList.append(selectedFile)
            self.inputFileList.addItem(selectedFile)

    def selectDir(self):
        selectedDir = QFileDialog.getExistingDirectory(self)

        now = datetime.datetime.now()
        self.outputFile = str(selectedDir) + os.sep + "lhaudio-" + now.strftime("%Y-%m-%d_%H:%M:%S") + ".wav"

        self.outputDir = str(selectedDir)

        self.outputDirPrompt.setText(selectedDir)

    def listDelete(self):
        for selectedItem in self.inputFileList.selectedItems():
            self.fileList.remove(self.inputFileList.currentItem().text())
            self.inputFileList.takeItem(self.inputFileList.row(selectedItem))

    def listClear(self):
        self.inputFileList.clear()
        self.fileList = []

    def execute(self):
        if self.encodeRadio.isChecked() == True:
            if len(self.fileList) >= 1 and len(self.outputFile) >= 1:
                lhaudio.encode(self.fileList, self.outputFile)

                self.listClear()

            else:
                print("Select valid input file(s) and output directory")

        elif self.decodeRadio.isChecked() == True:
            if len(self.fileList) == 1:
                if len(self.outputDir) >= 1:
                    lhaudio.decode(self.fileList[0], self.outputDir)

                    self.listClear()

                else:
                    print("Choose a valid output directory")

            else:
                print("You need to decode one file")

        else:
            print("Uh oh, select mode")

    def normalOutputWritten(self, text):
        cursor = self.terminalWindow.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.terminalWindow.setTextCursor(cursor)
        self.terminalWindow.ensureCursorVisible()

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

def main(args):
    app = QApplication(args)
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
