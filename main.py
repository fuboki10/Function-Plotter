import sys

import numpy as np

# f_x = input('Enter equation f(x) eg., 5*x^3 + 2*x\n').replace('^', '**')

# eqn = eval('lambda x : ' + f_x)

# print(eqn(3))

# mn, mx = 0, 100

# x = np.linspace(mn, mx)

# y = eqn(x)

# plt.plot(x, y)
# plt.show()


from PySide2.QtWidgets import QApplication, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Function Plotter")

        self.setMinimumWidth(600)
        self.setMinimumHeight(400)


app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec_())
