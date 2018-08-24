from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
def newIcon(icon):
    return QIcon('./icon/' + icon+'.png')
def newAction(parent,text,slot=None,shortcut=None,icon=None,
              tip=None,statustip=None,checkable=False,enabled=True):
    a = QAction(text, parent)
    if icon is not None:
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if statustip is not None:
        a.setStatusTip(statustip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    return a
def addActions(widget, actions):
    for action in actions:
        if action is None:
            widget.addSeparator()
        elif isinstance(action, QMenu):
            widget.addMenu(action)
        else:
            widget.addAction(action)
def newWidgetAction(parent,widget):
    action=QWidgetAction(parent)
    action.setDefaultWidget(widget)
    return action
def read(filename,default=None):
    try:
        with open(filename,'rb')as f:
            return f.read()
    except:
        return default

