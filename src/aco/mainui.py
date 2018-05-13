#! /Users/vs/Documents/Projects/KPI/master-degree/.env/bin/python
import sys
import datetime
from os.path import expanduser

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QToolTip, QPushButton, QApplication,
    QFileDialog, QTextEdit
)
from PyQt5.QtGui import QFont, QIcon

from aco.graphs import Graph

# HOME_DIR = expanduser('~')
HOME_DIR = expanduser('./aco/accets')


class Signals(QObject):
    machine_list_loaded = pyqtSignal()
    graph_built = pyqtSignal()
    props_loaded = pyqtSignal()
    solved = pyqtSignal()
    graph_load = pyqtSignal()


class MainUI(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._G = None
        self._result = {}

        # connect signal handlers
        self.signals = Signals()
        self.signals.graph_built.connect(self.on_graph_built)
        self.signals.machine_list_loaded.connect(self.on_machine_list_loaded)
        self.signals.props_loaded.connect(self.on_props_loaded)
        self.signals.solved.connect(self.on_solved)
        self.signals.graph_load.connect(self.on_graph_load)

        # UI elements
        self.LoadMachineListBtn = None
        self.LoadOwnPropsBtn = None
        self.LoadRelPropsBtn = None
        self.BuildGraphBtn = None
        self.DumpGraphToFileBtn = None
        self.LoadGraphFromFileBtn = None
        self.ShowGraphBtn = None
        self.SolveBtn = None
        self.LogsText = None
        self.ResultText = None
        self.SaveResultToFileBtn = None
        self.ShowShortestPathBtn = None

        # initialize UI elements
        self.initUI()

    def initUI(self):
        self.LoadMachineListBtn = QPushButton('Завантажити список верстатів', self)
        self.LoadMachineListBtn.setIcon(QIcon('accets/ico/xlsx.png'))
        self.LoadMachineListBtn.resize(self.LoadMachineListBtn.sizeHint())
        self.LoadMachineListBtn.clicked.connect(self.load_machine_list)
        self.LoadMachineListBtn.setEnabled(True)

        self.LoadOwnPropsBtn = QPushButton('Завантажити характеристики верстатів', self)
        self.LoadOwnPropsBtn.setIcon(QIcon('accets/ico/xlsx.png'))
        self.LoadOwnPropsBtn.resize(self.LoadOwnPropsBtn.sizeHint())
        self.LoadOwnPropsBtn.clicked.connect(self.load_own_props)
        self.LoadOwnPropsBtn.setEnabled(False)

        self.ShowShortestPathBtn = QPushButton('Показати найкоротший шлях', self)
        self.ShowShortestPathBtn.setIcon(QIcon('accets/ico/result.png'))
        self.ShowShortestPathBtn.resize(self.ShowShortestPathBtn.sizeHint())
        self.ShowShortestPathBtn.clicked.connect(self.show_shortest_path)
        self.ShowShortestPathBtn.setEnabled(False)

        self.LoadRelPropsBtn = QPushButton('Завантажити відносні параметри', self)
        self.LoadRelPropsBtn.setIcon(QIcon('accets/ico/xlsx.png'))
        self.LoadRelPropsBtn.resize(self.LoadRelPropsBtn.sizeHint())
        self.LoadRelPropsBtn.clicked.connect(self.load_rel_props)
        self.LoadRelPropsBtn.setEnabled(False)

        self.BuildGraphBtn = QPushButton('Побудувати граф', self)
        self.BuildGraphBtn.setIcon(QIcon('accets/ico/build.png'))
        self.BuildGraphBtn.resize(self.BuildGraphBtn.sizeHint())
        self.BuildGraphBtn.clicked.connect(self.build_graph)
        self.BuildGraphBtn.setEnabled(False)

        self.DumpGraphToFileBtn = QPushButton('Зберегти граф', self)
        self.DumpGraphToFileBtn.setIcon(QIcon('accets/ico/dump.png'))
        self.DumpGraphToFileBtn.resize(self.DumpGraphToFileBtn.sizeHint())
        self.DumpGraphToFileBtn.clicked.connect(self.dump_graph)
        self.DumpGraphToFileBtn.setEnabled(False)

        self.LoadGraphFromFileBtn = QPushButton('Завантажити граф', self)
        self.LoadGraphFromFileBtn.setIcon(QIcon('accets/ico/load.png'))
        self.LoadGraphFromFileBtn.resize(self.LoadGraphFromFileBtn.sizeHint())
        self.LoadGraphFromFileBtn.clicked.connect(self.load_graph)

        self.ShowGraphBtn = QPushButton('Показати граф', self)
        self.ShowGraphBtn.setIcon(QIcon('accets/ico/show.png'))
        self.ShowGraphBtn.resize(self.ShowGraphBtn.sizeHint())
        self.ShowGraphBtn.clicked.connect(self.show_graph)
        self.ShowGraphBtn.setEnabled(False)

        self.SolveBtn = QPushButton('Знайти найкоротший шлях', self)
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

        self.SaveResultToFileBtn = QPushButton('Зберегти результати до файлу', self)
        self.SaveResultToFileBtn.setIcon(QIcon('accets/ico/result.ico'))
        self.SaveResultToFileBtn.resize(self.SaveResultToFileBtn.sizeHint())
        self.SaveResultToFileBtn.clicked.connect(self.save_result)
        self.SaveResultToFileBtn.setEnabled(False)

        # zero row
        self.LoadMachineListBtn.move(10, 10)

        # first row
        self.LoadOwnPropsBtn.move(10, 40)
        self.LoadRelPropsBtn.move(320, 40)

        # second row
        self.BuildGraphBtn.move(10, 70)
        self.DumpGraphToFileBtn.move(180, 70)
        self.LoadGraphFromFileBtn.move(330, 70)

        # third row
        self.ShowGraphBtn.move(10, 100)
        self.SolveBtn.move(160, 100)

        # fourth row
        self.SaveResultToFileBtn.move(10, 130)
        self.ShowShortestPathBtn.move(265, 130)

        # fifth row
        self.LogsText.move(10, 160)
        self.ResultText.move(460, 160)

        QToolTip.setFont(QFont('Arial', 14))

        self.setWindowTitle('ACO Tool')
        self.setFixedWidth(700)
        self.setFixedHeight(470)
        self.show()
        self.msg('Програма готова до роботи')

    def on_machine_list_loaded(self):
        self.LoadOwnPropsBtn.setEnabled(True)
        self.LoadRelPropsBtn.setEnabled(True)

    def on_graph_built(self):
        self.DumpGraphToFileBtn.setEnabled(True)
        self.ShowGraphBtn.setEnabled(True)
        self.SolveBtn.setEnabled(True)

    def on_props_loaded(self):
        self.BuildGraphBtn.setEnabled(True)

    def on_solved(self):
        self.SaveResultToFileBtn.setEnabled(True)
        self.ShowShortestPathBtn.setEnabled(True)

    def on_graph_load(self):
        self.LoadMachineListBtn.setEnabled(False)

    def load_machine_list(self):
        f, _ = QFileDialog.getOpenFileName(self, 'Open csv file', HOME_DIR)
        if f:
            self._G = Graph.initialize_complete_graph(f)
            self.signals.machine_list_loaded.emit()
            self.msg('Завантажено список верстатів')

    def load_own_props(self):
        f, _ = QFileDialog.getOpenFileName(self, 'Open csv file', HOME_DIR)
        if f:
            self._G.load_own_attrs(f)
            self.signals.props_loaded.emit()
            self.msg('Завантажено характеристики верстатів')

    def load_rel_props(self):
        f, _ = QFileDialog.getOpenFileName(self, 'Open csv file', HOME_DIR)
        if f:
            self._G.load_relative_properties(f)
            self.signals.props_loaded.emit()
            self.msg('Завантажено відносні параметри')

    def build_graph(self):
        self._G.calc_weight()
        self.signals.graph_built.emit()
        self.msg('Граф побудовано')

    def dump_graph(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save File', HOME_DIR + '/graph', '*.gz')
        saved_to = self._G.dump_to_file(filename)
        self.msg(f'Граф збережено до файлу {saved_to}')

    def load_graph(self):
        f, _ = QFileDialog.getOpenFileName(
            self, 'Open csv file', HOME_DIR, '*.gz')
        if f:
            self._G = Graph.load_from_file(f)
            self.signals.graph_built.emit()
            self.signals.graph_load.emit()
            self.msg('Граф завантажено')

    def show_graph(self):
        self._G.show_on_plot()

    def solve(self):
        solution = self._G.solution()
        self._result = {
            'alpha': solution.alpha,
            'beta': solution.beta,
            'distance': solution.distance,
            'path': [(e.start, e.end) for e in solution.path][:-1],
            'start': solution.start,
            'tour': solution.tour,
            'traveled': [(e.start, e.end) for e in solution.path],
            'unvisited': solution.unvisited,
            'visited': solution.visited
        }
        for key, val in self._result.items():
            self.ResultText.append(f'{key}: {val}')
        self.signals.solved.emit()
        self.msg('Найкоротший шлях знайдено')

    def save_result(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save File', HOME_DIR + '/result')
        with open(filename, 'w') as f:
            f.writelines([f'{k}: {v}\n' for k, v in self._result.items()])
        self.msg(f'Результати збережено до файлу {filename}')

    def show_shortest_path(self):
        G = Graph()
        for node in self._result.get('tour'):
            G.add_node(node)
        for edge in self._result.get('path'):
            G.add_edge(*edge)
        G.show_on_plot()

    def openFileDialog(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', HOME_DIR)
        if file_name[0]:
            with open(file_name[0], 'r') as f:
                self.msg(f.read())

    def msg(self, text):
        curr_date = datetime.datetime.now().replace(microsecond=0)
        self.LogsText.append(f'--> {text}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())
