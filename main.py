import re
import sys
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PySide2.QtGui import QIcon

matplotlib.use('Qt5Agg')  # Render to PySide/PyQt Canvas

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=600, height=600, dpi=72):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PlotCanvas, self).__init__(fig)

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Function Plotter")

        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        self.setIcon()

        self.function = QLineEdit("5*x^3 + 2*x")
        self.button = QPushButton("Enter")
        self.canvas = PlotCanvas()

        self.layout = self.createLayout()

        self.setLayout(self.layout)

        self.regexCheck = re.compile('(?:[0-9-+*/^()x]?)+')

        self.button.clicked.connect(self.updatePlot)

    def setIcon(self):
        appIcon = QIcon('icon.png')
        self.setWindowIcon(appIcon)

    def createLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.function)
        layout.addWidget(self.button)
        layout.addWidget(self.canvas)
        return layout

    def updatePlot(self):
        # take the text and remove spaces
        f_x = self.function.text().replace(" ", "").replace("^", "**")
        print(f_x)
        result = self.regexCheck.match(f_x)
        print(result)

        eqn = eval('lambda x : ' + f_x)
        mn, mx = 0, 100
        x = np.linspace(mn, mx)

        y = eqn(x)

        self.canvas.axes.cla()  # clear the canvas
        self.canvas.axes.plot(x, y)
        self.canvas.draw()


if __name__ == '__main__':
    # Create QT App
    app = QApplication(sys.argv)
    # Create And Show Window
    window = Window()
    window.show()
    # Run QT loop
    sys.exit(app.exec_())
