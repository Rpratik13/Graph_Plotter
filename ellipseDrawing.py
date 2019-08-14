from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys


import wx
from wx.lib.masked import NumCtrl

class EllipseInputPopup(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        wx.PopupWindow.__init__(self, parent, style=wx.CLOSE_BOX )
        xLabel = wx.StaticText(self, -1,
                           "X",
                           pos=(120,5))
        yLabel = wx.StaticText(self, -1,
                           "Y",
                           pos=(180,5))
        centerLabel = wx.StaticText(self, -1,
                           "Enter center: ",
                           pos=(10,24))
        self.centerxInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(90, 20), size=(100, -1))
        self.centeryInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(150, 20), size=(100, -1))
        rxLabel = wx.StaticText(self, -1,
                           "Enter rx: ",
                           pos=(10,54))
        self.rxInput = NumCtrl(self, value=0.0, allowNegative = False, integerWidth=3, fractionWidth=2, pos=(90, 50), size=(100, -1))
        ryLabel = wx.StaticText(self, -1,
                           "Enter ry: ",
                           pos=(10,84))
        self.ryInput = NumCtrl(self, value=0.0, allowNegative = False, integerWidth=3, fractionWidth=2, pos=(90, 80), size=(100, -1))
        okBtn = wx.Button(self, -1, label='OK', pos=(10, 110), size=(100, 30))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(120, 110), size=(100, 30))
        self.SetSize((230, 145))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        xc = self.centerxInput.GetValue()
        yc = self.centeryInput.GetValue()
        rx = self.rxInput.GetValue()
        ry = self.ryInput.GetValue()
        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]
        self.parent.canvas.drawings.append(self.ellipseDrawing(xc, yc, rx, ry))

        self.Show(False)
        self.parent.buttons[6] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[6] = True


    def ellipseDrawing(self, xc, yc, rx, ry):
        points = list()
        x = 0
        y = ry
        p = (ry ** 2) - (rx ** 2) * ry + (rx ** 2) / 4


        points.append([(x + xc), (y + yc)])
        points.append([(-x + xc), (y + yc)])
        points.append([(x + xc), (-y + yc)])
        points.append([(-x + xc), (-y + yc)])

        while x * (ry ** 2) < y * (rx ** 2):
            x += 1
            if p < 0:
                p += 2 * (ry ** 2) * x + (ry ** 2)
            else:
                y -= 1
                p += 2 * (ry ** 2) * x + (ry ** 2) - 2 * (rx ** 2) * y

            points.append([(x + xc), (y + yc)])
            points.append([(-x + xc), (y + yc)])
            points.append([(x + xc), (-y + yc)])
            points.append([(-x + xc), (-y + yc)])

        p = (ry ** 2) * (x ** 2) + (ry ** 2) * (x + 1 / 4) + (rx ** 2) * ((y - 1) ** 2) - (rx * ry) ** 2

        while y != 0:
            y -= 1
            if p < 0:
                x += 1
                p += -2 * (rx ** 2) * y + 2 * (rx ** 2) * x + (rx ** 2)
            else:
                p += -2 * (rx ** 2) * y + (rx ** 2)

            points.append([(x + xc), (y + yc)])
            points.append([(-x + xc), (y + yc)])
            points.append([(x + xc), (-y + yc)])
            points.append([(-x + xc), (-y + yc)])
        return points
