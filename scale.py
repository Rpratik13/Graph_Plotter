from math import *
import wx
from wx.lib.masked import NumCtrl

class ScaleInputPopup(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        wx.PopupWindow.__init__(self, parent, style=wx.CLOSE_BOX )
        sxLabel = wx.StaticText(self, -1,
                           "Enter sx: ",
                           pos=(10,14))
        self.sxInput = NumCtrl(self, value=0.0, allowNegative=False, integerWidth=2, fractionWidth=2, pos=(75, 10), size=(100, -1))
        syLabel = wx.StaticText(self, -1,
                           "Enter sy: ",
                           pos=(10,44))
        self.syInput = NumCtrl(self, value=0.0, allowNegative=False, integerWidth=2, fractionWidth=2, pos=(75, 40), size=(100, -1))
        angleLabel = wx.StaticText(self, -1,
                           "Enter angle: ",
                           pos=(10,74))
        self.angleInput = NumCtrl(self, value=0.0, allowNegative=False, integerWidth=2, fractionWidth=2, pos=(75, 70), size=(100, -1))
        okBtn = wx.Button(self, -1, label='OK', pos=(10, 100), size=(100, 20))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(10, 130), size=(100, 20))
        self.SetSize((130, 170))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        sx = self.sxInput.GetValue()
        sy = self.syInput.GetValue()
        theta = self.angleInput.GetValue()
        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]
        self.parent.canvas.drawings.append(self.scale(points=self.parent.canvas.drawings[0], sx=sx, sy=sy, theta=theta))


        self.Show(False)
        self.parent.buttons[10] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[10] = True


    def matrixMultiply(self, A, B):
        prod = list()
        for i in range(3):
            row = list()
            sm = 0
            for j in range(3):
                sm += A[i][j] * B[j][0]
            row.append(sm)
            prod.append(row)
        return prod


    def scale(self, points, sx, sy, theta):
        theta = radians(theta)
        translated_points = list()
        scale_mat = [[sx * cos(theta) , -sy * sin(theta), 0],
                     [sx * sin(theta), sy * cos(theta), 0],
                     [0, 0, 1]]
        for point in points:
            translated = self.matrixMultiply(scale_mat, [[point[0]], [point[1]], [1]])
            translated_points.append([translated[0][0], translated[1][0]])
        return translated_points
