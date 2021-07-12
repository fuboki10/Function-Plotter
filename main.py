import re
import sys
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QFormLayout, \
    QHBoxLayout, QLabel, QMessageBox
from PySide2.QtGui import QIcon

matplotlib.use('Qt5Agg')  # Render to PySide/PyQt Canvas

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=600, height=600, dpi=72):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('f(x)')
        self.axes.set_title('function plotter')
        super(PlotCanvas, self).__init__(fig)

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Function Plotter")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        self.setIcon()

        self.function, self.min, self.max, self.button = self.createWidgets()

        self.canvas = PlotCanvas()

        self.layout = self.createLayout()
        self.setLayout(self.layout)

        self.regexCheck = re.compile('(?:[0-9-+*/^()x]?)+')

        self.show()

    def setIcon(self):
        appIcon = QIcon('icon.png')
        self.setWindowIcon(appIcon)

    def createWidgets(self):
        function = QLineEdit("5*x^3 + 2*x")
        function.setMaximumWidth(200)

        min = QLineEdit('0')
        min.setMaximumWidth(200)

        max = QLineEdit('100')
        max.setMaximumWidth(200)

        button = QPushButton("Plot")
        button.setMaximumWidth(100)
        button.clicked.connect(self.updatePlot)

        return function, min, max, button

    def createLayout(self):
        outerLayout = QVBoxLayout()
        topLayout = QFormLayout()

        topLayout.addRow('Function (x)', self.function)
        topLayout.addRow('min', self.min)
        topLayout.addRow('max', self.max)

        outerLayout.addLayout(topLayout)
        outerLayout.addWidget(self.button)
        outerLayout.addWidget(self.canvas)
        return outerLayout

    def updatePlot(self):
        # take the text and remove spaces
        f_x = self.function.text().replace(" ", "").replace("^", "**")
        result = self.regexCheck.match(f_x)

        if not result or result.group() != f_x or f_x.find(r'x{2,}') != -1 or f_x.find(r'*{3,}') != -1:
            QMessageBox.warning(self, 'Error', 'the function is not valid')
            return

        mn, mx = int(self.min.text()), int(self.max.text())

        if mn < 0:
            QMessageBox.warning(self, 'Error', 'min < 0')
            return

        if mn >= mx:
            QMessageBox.warning(self, 'Error', 'min >= max')
            return

        x = np.linspace(mn, mx)

        try:
            eqn = eval('lambda x : ' + f_x)
            y = eqn(x)
        except:
            QMessageBox.warning(self, 'Error', 'the function is not valid')
            return

        self.canvas.axes.cla()  # clear the canvas
        self.canvas.axes.plot(x, y)
        self.canvas.axes.set_xlabel('x')
        self.canvas.axes.set_ylabel('f(x)')
        self.canvas.axes.set_title('function plotter')
        self.canvas.draw()


if __name__ == '__main__':
    # Create QT App
    app = QApplication(sys.argv)
    # Create Window
    window = Window()
    # Run QT loop
    sys.exit(app.exec_())
