import re
import sys
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QMessageBox
from PySide2.QtGui import QIcon

matplotlib.use('Qt5Agg')  # Render to PySide/PyQt Canvas

POINTS_NUMBER = 20
WIDTH = 600
HEIGHT = 600


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=WIDTH, height=HEIGHT, dpi=72):
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

        self.errorMessage = ""
        self.showError = True
        self.errorMessageBox = QMessageBox

        self.setIcon()

        self.createWidgets()

        self.layout = self.createLayout()
        self.setLayout(self.layout)

        self.regexCheck = re.compile('(?:[0-9-+*/^()x]?)+')

        self.show()

    def setIcon(self):
        appIcon = QIcon('icon.png')
        self.setWindowIcon(appIcon)

    def createWidgets(self):
        self.function = QLineEdit()
        self.function.setPlaceholderText('5*x^3 + 2*x')
        self.function.setMaximumWidth(200)

        self.min = QLineEdit()
        self.min.setPlaceholderText('0')
        self.min.setMaximumWidth(200)

        self.max = QLineEdit()
        self.max.setPlaceholderText('100')
        self.max.setMaximumWidth(200)

        self.button = QPushButton('Plot')
        self.button.setMaximumWidth(100)
        self.button.clicked.connect(self.updatePlot)

        self.canvas = PlotCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)

    def createLayout(self):
        outerLayout = QVBoxLayout()
        topLayout = QFormLayout()

        topLayout.addRow('Function (x)', self.function)
        topLayout.addRow('min', self.min)
        topLayout.addRow('max', self.max)

        outerLayout.addLayout(topLayout)
        outerLayout.addWidget(self.button)
        outerLayout.addWidget(self.toolbar)
        outerLayout.addWidget(self.canvas)
        return outerLayout

    def createError(self, err):
        self.errorMessage = err
        if self.showError:
            self.errorMessageBox.warning(self, 'Error', self.errorMessage)

    def validateInput(self, f_x, mn, mx):
        result = self.regexCheck.match(f_x)

        if f_x == "":
            self.createError('Please Enter the function')
            return False

        if not result or result.group() != f_x or f_x.find(r'x{2,}') != -1 or f_x.find(r'*{3,}') != -1:
            self.createError('The function is not valid')
            return False

        if mn == "":
            self.createError('Please Enter min Value')
            return False

        if mx == "":
            self.createError('Please Enter max Value')
            return False

        try:
            mn = float(mn)
        except ValueError:
            self.createError('Please Enter a valid min Value')
            return False

        try:
            mx = float(mx)
        except ValueError:
            self.createError('Please Enter a valid max Value')
            return False

        if mn < 0:
            self.createError('Min must be greater than 0')
            return False

        if mx < 0:
            self.createError('Max must be greater than 0')
            return False

        if mn >= mx:
            self.createError('Min must be smaller than Max')
            return False

        return True

    def plot(self, x, y):
        self.errorMessage = ""  # Remove Error
        self.canvas.axes.cla()  # clear the canvas
        self.canvas.axes.plot(x, y)
        self.canvas.axes.set_xlabel('x')
        self.canvas.axes.set_ylabel('f(x)')
        self.canvas.axes.set_title('function plotter')
        self.canvas.draw()

    def updatePlot(self):
        # take the text and remove spacees
        f_x = self.function.text().replace(" ", "").replace("^", "**")
        mn, mx = self.min.text(), self.max.text()

        if not self.validateInput(f_x, mn, mx):
            return

        x = np.linspace(float(mn), float(mx), POINTS_NUMBER)

        try:
            eqn = eval('lambda x : ' + f_x)
            y = eqn(x)
        except:
            return self.createError('The function is not valid')

        self.plot(x, y)


if __name__ == '__main__':
    # Create QT App
    app = QApplication(sys.argv)
    # Create Window
    window = Window()
    # Run QT loop
    sys.exit(app.exec_())
