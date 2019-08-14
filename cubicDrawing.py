import wx
from wx.lib.masked import NumCtrl
import numpy as np

class CubicInputPopup(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        wx.PopupWindow.__init__(self, parent, style=wx.CLOSE_BOX )
        aLabel = wx.StaticText(self, -1,
                           "Enter a: ",
                           pos=(10,14))
        self.aInput = NumCtrl(self, value=0.0, integerWidth=2, fractionWidth=2, pos=(55, 10), size=(100, -1))
        bLabel = wx.StaticText(self, -1,
                           "Enter b: ",
                           pos=(10,44))
        self.bInput = NumCtrl(self, value=0.0, integerWidth=2, fractionWidth=2, pos=(55, 40), size=(100, -1))
        cLabel = wx.StaticText(self, -1,
                           "Enter c: ",
                           pos=(10,74))
        self.cInput = NumCtrl(self, value=0.0, integerWidth=2, fractionWidth=2, pos=(55, 70), size=(100, -1))
        dLabel = wx.StaticText(self, -1,
                           "Enter d: ",
                           pos=(10,104))
        self.dInput = NumCtrl(self, value=0.0, integerWidth=2, fractionWidth=2, pos=(55, 100), size=(100, -1))
        okBtn = wx.Button(self, -1, label='OK', pos=(10, 130), size=(100, 20))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(10, 160), size=(100, 20))
        self.SetSize((120, 190))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        a = self.aInput.GetValue()
        b = self.bInput.GetValue()
        c = self.cInput.GetValue()
        d = self.dInput.GetValue()

        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]
        if a == 0 and b == 0:
            self.parent.canvas.drawings.append(self.lineDrawing(c, d))
        elif a == 0:
            self.parent.canvas.drawings.append(self.quadraticDrawing(b, c, d))
        else:
            self.parent.canvas.drawings.append(self.cubicDrawing(a, b, c, d))

        self.Show(False)
        self.parent.buttons[11] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[11] = True


    def cubicDrawing(self, a, b, c, d):
        points = list()
        for y in range(-1000, 1001):
            roots = list(np.roots([a, b, c, d - y]))
            for x in roots:
                if x.imag == 0:
                    points.append([x.real, y])
        return points


    def quadraticDrawing(self, a, b, c):
        points = list()
        for x in range(-1000, 1001):
            if b ** 2 - 4 * a * (c - x) >= 0:
                x1 = (-b + (b ** 2 - 4 * a * (c - x)) ** 0.5) / 2 * a
                x2 = (-b - (b ** 2 - 4 * a * (c - x)) ** 0.5) / 2 * a
                points.append([x1, x])
                points.append([x2, x])
        return points


    def lineDrawing(self, m, c):
        points = list()
        if m > 0:
            if m != float('inf'):
                start = [-1000, -1000 * m + c]
                end = [1000, 1000 * m + c]
            else:
                start = [c, -1000]
                end = [c, 1000]

        else:
            if m != float('-inf'):
                start = [1000, 1000 * m + c]
                end = [-1000, -1000 * m + c]
            else:
                start = [c,  1000]
                end = [c, -1000]
        x = start[0]
        y = start[1]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if abs(dx) > abs(dy):
            stepsize = abs(dx)
        else:
            stepsize = abs(dy)
        if stepsize != float('inf') and stepsize != float('-inf'):
            x_inc = dx / stepsize
            y_inc = dy / stepsize
        else:
            x_inc = 0
            if stepsize == float('inf'):
                y_inc = 1
            else:
                y_inc = -1
        for _ in range(round(stepsize) // 1):
            points.append([x, y])
            x += x_inc
            y += y_inc
            points.append([x, y])
        return points
