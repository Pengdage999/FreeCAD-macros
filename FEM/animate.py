#forum.freecadweb.org/viewtopic.php?t=2159
#
# bits taken from:
#./Mod/Fem/femguiobjects/_ViewProviderFemResultMechanical.py:

import sys
import math
#sys.path.append('/usr/lib/freecad/lib')
#sys.path.append('/usr/share/freecad/')
#sys.path.append('/usr/lib/freecad-python2/lib')
import FreeCAD, FreeCADGui, time
import pysideuic
import PySide
from PySide import QtGui
from PySide import QtCore
from PyQt4 import uic

'''
see:
https://github.com/FreeCAD/FreeCAD-macros

Macro description

CamelCase macro name
Please follow the CamelCase.FCMacro convention for the macro name (other associated files except the macro icon don't need to follow this convention). Please don't start your macro name with Macro or FC or similar (we already know it's a macro for FreeCAD).

Macro name specifics
Also, if possible, start the macro name with the type of object it's working on, e.g. use ViewRotation instead of RotateView, so that all macros related to View will be together when sorting alphabetically.

Macro metadata

    __Name__ = ''
    __Comment__ = ''
    __Author__ = ''
    __Version__ = ''
    __Date__ = ''
    __License__ = ''
    __Web__ = ''
    __Wiki__ = ''
    __Icon__ = ''
    __Help__ = ''
    __Status__ = ''
    __Requires__ = ''
    __Communication__ = ''
    __Files__ = ''
'''
'''
items in the widget window:
startEndButton
amplitude
factor
steps
steps/second is codes as frames/second
loops

'''

class mac():
    def __init__(self): 
        self.startAnimate = False
        self.UI = "animate.ui"
        self.console = FreeCAD.Console
        self.inc = 1

        self.f,self.w = FreeCAD.Gui.PySideUic.loadUiType(self.UI)
        self.form = self.f()
        self.widget = self.w()
        self.form.setupUi(self.widget)
        self.widget.show()
#        print "f and w: ", self.f, self.w
        self.myConnect()
        self.messageBox()

    def myConnect(self):
#        print "myConnect" 
        QtCore.QObject.connect(self.form.startEndButton, QtCore.SIGNAL("clicked()"),         \
      lambda dummy="", name='startEndButton': self.valueChanged(self, dummy, name))
        QtCore.QObject.connect(self.form.amplitude,QtCore.SIGNAL("valueChanged(int)"),         \
      lambda dummy="", name='amplitude': self.valueChanged(self, dummy, name))
        QtCore.QObject.connect(self.form.factor,QtCore.SIGNAL("valueChanged(double)"),         \
      lambda dummy="", name='factor': self.valueChanged(self, dummy, name))
        QtCore.QObject.connect(self.form.steps,QtCore.SIGNAL("valueChanged(int)"),         \
      lambda dummy="", name='steps': self.valueChanged(self, dummy, name))
        QtCore.QObject.connect(self.form.frames,QtCore.SIGNAL("valueChanged(int)"),         \
      lambda dummy="", name='frames': self.valueChanged(self, dummy, name))
        QtCore.QObject.connect(self.form.loops, QtCore.SIGNAL("valueChanged(int)"),         \
      lambda dummy="", name='loops': self.valueChanged(self, dummy, name))

    def printV(self):
        print "amplitude: ",   self.form.amplitude.value()
        print "factor: ",   self.form.factor.value()
        print "steps: ",   self.form.steps.value()
        print "frames: ",   self.form.frames.value()
        print "loops: ",   self.form.loops.value()

    def valueChanged(self, dummy, value, myType):
# value - the value of the thing
# myType - the char string

# the only actions are:
        if myType == "startEndButton":
            if not self.startAnimate:
                self.startAnimate = True
                self.myInternalAnimate()
            else:
              self.startAnimate = False
# set the amplitude
        elif myType == "amplitude":
         if self.inc == 0:
           self.form.factor.setValue(self.form.amplitude.value())
         self.inc = 1 - self.inc
# set the factor
        elif myType == "factor":
         if self.inc == 0:
            self.form.amplitude.setValue(int(self.form.factor.value()))
         self.inc = 1 - self.inc
        else:
            pass
        self.widget.update()
        return

    def messageBox(self):
            box = QtGui.QMessageBox()
            box.setWindowTitle('No Results')
            box.setText("Select a case and select a displacement type, e.g. Abs")
            box.setInformativeText("Tick the displacement radio button")
            box.setStandardButtons(QtGui.QMessageBox.Ok)
            box.setDefaultButton(QtGui.QMessageBox.Save)
            self.box = box

    def myAnimate(self):
        self.startAnimate = True
        self.myInternalAnimate()

    def myInternalAnimate(self):
        if not self.startAnimate: return
        try:
            mesh_obj = FreeCAD.FEM_dialog["result_obj"]
            mesh_obj.Mesh.ViewObject.applyDisplacement(math.sin(0.0) * self.form.factor.value())
            self.form.startEndButton.setText("Stop Animation");
        except:
#            "no results"
            result = self.box.exec_()
            self.startAnimate = False
            return
            pass
        prevFactor = FreeCAD.FEM_dialog["disp_factor"]
        numberFrames = self.form.frames.value()
        steps = self.form.steps.value()
        loops = self.form.loops.value()
        inc = math.pi/steps*2.

        done = False
        for lo in range(0, loops):
           for st in range(0,steps):
# self.form.factor.value(): this is the value of the scale factor.
                 mesh_obj.Mesh.ViewObject.applyDisplacement(math.sin(inc*st) * self.form.factor.value())
                 FreeCADGui.updateGui()
                 if not self.startAnimate:
                     done = True
                     break
                 time.sleep(1./numberFrames) # modify the time here
           if done: break 
        self.form.startEndButton.setText("Start Animation");
        self.startAnimate = False

#---------------------------------------------------------------------------------

if __name__ == '__main__':
  b = mac()