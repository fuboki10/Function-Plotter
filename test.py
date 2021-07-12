import pytest

from PySide2 import QtCore
from PySide2 import QtWidgets

import main


@pytest.fixture
def app(qtbot):
    testApp = main.Window()
    qtbot.addWidget(testApp)

    return testApp

def testMinInputValidation(app, qtbot):
    app.min.setText('-1')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    messagebox = QtWidgets.QApplication.activeWindow()
    yes_button = messagebox.button(QtWidgets.QMessageBox.Ok)
    qtbot.mouseClick(yes_button, QtCore.Qt.LeftButton)

