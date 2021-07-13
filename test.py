import pytest

from PySide2 import QtCore
from PySide2 import QtWidgets

import main


def setToDefault(app):
    app.showError = False
    app.min.setText('0')
    app.max.setText('100')
    app.function.setText('x')

@pytest.fixture
def app(qtbot):
    app = main.Window()
    setToDefault(app)
    qtbot.addWidget(app)

    return app

def testNegativeMin(app, qtbot):
    app.min.setText('-1')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'Min must be greater than 0'

def testEmptyMin(app, qtbot):
    app.min.setText('')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'Please Enter min Value'

def testMinInputValidation(app, qtbot):
    app.min.setText('ss')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'Please Enter a valid min Value'

def testMaxSmallerThanMin(app, qtbot):
    app.min.setText('10')
    app.max.setText('9')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'Min must be smaller than Max'

def testNegativeMax(app, qtbot):
    app.max.setText('-1')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'Max must be greater than 0'

def testEmptyMax(app, qtbot):
    app.max.setText('')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'Please Enter max Value'

def testMaxInputValidation(app, qtbot):
    app.max.setText('ss')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'Please Enter a valid max Value'

def testEmptyFunction(app, qtbot):
    app.function.setText('')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'Please Enter the function'

def testFunctionInputValidation(app, qtbot):
    app.function.setText('y')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'The function is not valid'

    app.function.setText('x^^3')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'The function is not valid'

    app.function.setText('3*xxx')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == 'The function is not valid'

def testValidFunction1(app, qtbot):
    app.function.setText('x')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == ''

def testValidFunction2(app, qtbot):
    app.function.setText('5*x^3 + 2*x')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == ''

def testValidFunction3(app, qtbot):
    app.function.setText('(5*x^3)*x + 2*x^0')
    qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)

    assert app.errorMessage == ''
