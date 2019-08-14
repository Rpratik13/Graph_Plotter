import math
import wx
from wx.lib.masked import NumCtrl

class RotateInputPopup(wx.Frame):
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
        thetaLabel = wx.StaticText(self, -1,
                           "Enter angle: ",
                           pos=(10,54))
        self.thetaInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(90, 50), size=(100, -1))

        okBtn = wx.Button(self, -1, label='OK', pos=(10, 110), size=(100, 30))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(120, 110), size=(100, 30))
        self.SetSize((230, 145))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        xc = self.centerxInput.GetValue()
        yc = self.centeryInput.GetValue()
        theta = self.thetaInput.GetValue()
        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]
        self.parent.canvas.drawings.append(self.rotate(xc, yc, theta, self.parent.canvas.drawings[0]))

        self.Show(False)
        self.parent.buttons[7] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[7] = True


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

    def rotate(self, xc, yc, theta, points):
        translated_points = list()
        theta = math.radians(theta)
        rotate_mat = [[math.cos(theta), -math.sin(theta), -xc * math.cos(theta) + yc * math.sin(theta) + xc],
                      [math.sin(theta), math.cos(theta), -xc * math.sin(theta) - yc * math.cos(theta) + yc],
                      [0, 0, 1]]
        for point in points:
            translated = self.matrixMultiply(rotate_mat, [[point[0]], [point[1]], [1]])
            translated_points.append([translated[0][0], translated[1][0]])
        return translated_points
