import sys
import datetime
from os.path import expanduser
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QFileDialog,
                             QTextEdit, )
from PyQt5.QtGui import QFont, QIcon

HOME_DIR = expanduser('~')


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.__prev_log_date = None
        self.initUI()

    def initUI(self):
        self.logsText = QTextEdit(self)
        self.logsText.setReadOnly(True)
        self.logsText.setFixedHeight(380)
        self.logsText.setFixedWidth(480)
        self.logsText.resize(self.logsText.sizeHint())
        self.logsText.move(10, 100)

        QToolTip.setFont(QFont('Arial', 14))

        self.log('before button creation')

        showGraphButton = QPushButton('Show graph', self)
        showGraphButton.setToolTip('Show graph')
        showGraphButton.resize(showGraphButton.sizeHint())
        showGraphButton.move(10, 10)
        showGraphButton.clicked.connect(self.draw_graph)

        self.log('button created')

        openFileButton = QPushButton('Open file', self)
        openFileButton.setToolTip('Open file')
        openFileButton.setShortcut('Ctrl+O')
        openFileButton.setIcon(QIcon('accets/ico/xlsx.png'))
        openFileButton.resize(openFileButton.sizeHint())
        openFileButton.move(10, 40)
        openFileButton.clicked.connect(self.openFileDialog)

        self.setWindowTitle('ACO Tool')
        self.setFixedWidth(500)
        self.setFixedHeight(500)
        self.show()

    def openFileDialog(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', HOME_DIR)
        if file_name[0]:
            with open(file_name[0], 'r') as f:
                self.log(f.read())

    def log(self, text):
        prev_date = self.__prev_log_date
        curr_date = datetime.datetime.now()
        delta = curr_date - prev_date if prev_date \
            else datetime.timedelta(seconds=0)
        self.logsText.append(f'{curr_date}:({delta.total_seconds()} sec) {text}')
        self.__prev_log_date = curr_date

    def draw_graph(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
