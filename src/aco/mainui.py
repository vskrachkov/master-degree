import sys
import datetime
from os.path import expanduser

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QToolTip, QPushButton, QApplication,
    QFileDialog, QTextEdit
)
from PyQt5.QtGui import QFont, QIcon

HOME_DIR = expanduser('~')


class Signals(QObject):
    graph_built = pyqtSignal()
    props_loaded = pyqtSignal()
    solved = pyqtSignal()


class MainUI(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # connect signal handlers
        self.signals = Signals()
        self.signals.graph_built.connect(self.on_graph_built)
        self.signals.props_loaded.connect(self.on_props_loaded)
        self.signals.solved.connect(self.on_solved)

        # UI elements
        self.LoadOwnPropsBtn = None
        self.LoadRelPropsBtn = None
        self.BuildGraphBtn = None
        self.DumpGraphToFileBtn = None
        self.LoadGraphFromFileBtn = None
        self.ShowGraphBtn = None
        self.ShowResultPathBtn = None
        self.SolveBtn = None
        self.LogsText = None
        self.ResultText = None
        self.SaveResultToFileBtn = None

        # initialize UI elements
        self.initUI()

    def initUI(self):
        self.LoadOwnPropsBtn = QPushButton('Load own properties from file', self)
        self.LoadOwnPropsBtn.setIcon(QIcon('accets/ico/xlsx.png'))
        self.LoadOwnPropsBtn.resize(self.LoadOwnPropsBtn.sizeHint())
        self.LoadOwnPropsBtn.clicked.connect(self.load_own_props)

        self.LoadRelPropsBtn = QPushButton('Load related properties from file', self)
        self.LoadRelPropsBtn.setIcon(QIcon('accets/ico/xlsx.png'))
        self.LoadRelPropsBtn.resize(self.LoadRelPropsBtn.sizeHint())
        self.LoadRelPropsBtn.clicked.connect(self.load_rel_props)

        self.BuildGraphBtn = QPushButton('Build graph', self)
        self.BuildGraphBtn.setIcon(QIcon('accets/ico/build.png'))
        self.BuildGraphBtn.resize(self.BuildGraphBtn.sizeHint())
        self.BuildGraphBtn.clicked.connect(self.build_graph)
        self.BuildGraphBtn.setEnabled(False)

        self.DumpGraphToFileBtn = QPushButton('Dump graph to file', self)
        self.DumpGraphToFileBtn.setIcon(QIcon('accets/ico/dump.png'))
        self.DumpGraphToFileBtn.resize(self.DumpGraphToFileBtn.sizeHint())
        self.DumpGraphToFileBtn.clicked.connect(self.dump_graph)
        self.DumpGraphToFileBtn.setEnabled(False)

        self.LoadGraphFromFileBtn = QPushButton('Load graph from file', self)
        self.LoadGraphFromFileBtn.setIcon(QIcon('accets/ico/load.png'))
        self.LoadGraphFromFileBtn.resize(self.LoadGraphFromFileBtn.sizeHint())
        self.LoadGraphFromFileBtn.clicked.connect(self.load_graph)

        self.ShowGraphBtn = QPushButton('Show graph', self)
        self.ShowGraphBtn.setIcon(QIcon('accets/ico/show.png'))
        self.ShowGraphBtn.resize(self.ShowGraphBtn.sizeHint())
        self.ShowGraphBtn.clicked.connect(self.show_graph)
        self.ShowGraphBtn.setEnabled(False)

        self.SolveBtn = QPushButton('Find the shortest path on the graph', self)
        self.SolveBtn.setIcon(QIcon('accets/ico/solve.png'))
        self.SolveBtn.resize(self.SolveBtn.sizeHint())
        self.SolveBtn.clicked.connect(self.solve)
        self.SolveBtn.setEnabled(False)

        self.LogsText = QTextEdit(self)
        self.LogsText.setReadOnly(True)
        self.LogsText.setFixedHeight(300)
        self.LogsText.setFixedWidth(450)
        self.LogsText.resize(self.LogsText.sizeHint())

        self.ResultText = QTextEdit(self)
        self.ResultText.setReadOnly(True)
        self.ResultText.setFixedHeight(300)
        self.ResultText.setFixedWidth(230)
        self.ResultText.resize(self.ResultText.sizeHint())

        self.SaveResultToFileBtn = QPushButton('Save results to file', self)
        self.SaveResultToFileBtn.setIcon(QIcon('accets/ico/xlsx.png'))
        self.SaveResultToFileBtn.resize(self.SaveResultToFileBtn.sizeHint())
        self.SaveResultToFileBtn.clicked.connect(self.save_result)
        self.SaveResultToFileBtn.setEnabled(False)

        self.ShowResultPathBtn = QPushButton('Show the shortest path')
        self.ShowResultPathBtn.setIcon(QIcon('accets/ico/xlsx.png'))
        self.ShowResultPathBtn.resize(self.ShowResultPathBtn.sizeHint())
        self.ShowResultPathBtn.clicked.connect(self.show_result)
        self.ShowResultPathBtn.setEnabled(False)

        # first row
        self.LoadOwnPropsBtn.move(10, 10)
        self.LoadRelPropsBtn.move(250, 10)

        # second row
        self.BuildGraphBtn.move(10, 40)
        self.DumpGraphToFileBtn.move(140, 40)
        self.LoadGraphFromFileBtn.move(310, 40)

        # third row
        self.ShowGraphBtn.move(10, 70)
        self.SolveBtn.move(140, 70)

        # fourth row
        self.SaveResultToFileBtn.move(10, 100)

        # fifth row
        self.LogsText.move(10, 130)
        self.ResultText.move(460, 130)

        QToolTip.setFont(QFont('Arial', 14))

        self.msg('before button creation')

        self.setWindowTitle('ACO Tool')
        self.setFixedWidth(700)
        self.setFixedHeight(440)
        self.show()

    def on_graph_built(self):
        self.DumpGraphToFileBtn.setEnabled(True)
        self.ShowGraphBtn.setEnabled(True)
        self.SolveBtn.setEnabled(True)

    def on_props_loaded(self):
        self.BuildGraphBtn.setEnabled(True)

    def on_solved(self):
        self.SaveResultToFileBtn.setEnabled(True)

    def load_own_props(self):
        self.msg('Load own props')
        self.signals.props_loaded.emit()

    def load_rel_props(self):
        self.msg('Load related props')
        self.signals.props_loaded.emit()

    def build_graph(self):
        self.signals.graph_built.emit()

    def dump_graph(self):
        pass

    def load_graph(self):
        pass

    def show_graph(self):
        pass

    def solve(self):
        self.signals.solved.emit()

    def save_result(self):
        pass

    def show_result(self):
        pass

    def openFileDialog(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', HOME_DIR)
        if file_name[0]:
            with open(file_name[0], 'r') as f:
                self.msg(f.read())

    def msg(self, text):
        curr_date = datetime.datetime.now().replace(microsecond=0)
        self.LogsText.append(f'{curr_date}: {text}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())
