from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
from math import *

import wx
from wx.lib.masked import NumCtrl

class CosInputPopup(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        wx.PopupWindow.__init__(self, parent, style=wx.CLOSE_BOX )
        amplitudeLabel = wx.StaticText(self, -1,
                           "Enter amplitude: ",
                           pos=(10,14))
        self.amplitudeInput = NumCtrl(self, value=0.0, integerWidth=3,fractionWidth=2, pos=(120, 10), size=(100, -1))
        phaseLabel = wx.StaticText(self, -1,
                           "Enter phase: ",
                           pos=(10,44))
        self.phaseInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(120, 40), size=(100, -1))
        okBtn = wx.Button(self, -1, label='OK', pos=(10, 70), size=(100, 30))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(120, 70), size=(100, 30))
        self.SetSize((230, 110))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        amplitude = self.amplitudeInput.GetValue()
        phase = self.phaseInput.GetValue()

        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]

        self.parent.canvas.drawings.append(self.cosDrawing(amplitude, phase))
        self.Show(False)
        self.parent.buttons[5] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[5] = True


    def cosDrawing(self, amplitude, phase):
        points = list()
        y = 0
        while y <= 1:
            x = degrees(acos(y))
            points.append([(x + phase ), y * amplitude])
            points.append([(180 + phase - x), -y * amplitude])
            points.append([(180 + phase + x), -y * amplitude])
            points.append([(360 + phase - x), y * amplitude])
            y += 0.0005
        return points
