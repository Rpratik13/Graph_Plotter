from math import *
import wx
from wx.lib.masked import NumCtrl

class ReflectInputPopup(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        wx.PopupWindow.__init__(self, parent, style=wx.CLOSE_BOX )
        self.rbox = wx.RadioBox(self,label = 'About', pos = (2,10), choices = ['X-axis', 'Y-axis', 'Origin', 'Line'], majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        slopeLabel = wx.StaticText(self, -1,
                           "Enter slope (m): ",
                           pos=(10,70))
        self.slopeInput = NumCtrl(self, value=0.0, integerWidth=3,fractionWidth=2, pos=(120, 70), size=(100, -1))
        cLabel = wx.StaticText(self, -1,
                           "Enter y-intercept (c): ",
                           pos=(10,100))
        self.cInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(120, 100), size=(100, -1))
        okBtn = wx.Button(self, -1, label='OK', pos=(10, 130), size=(100, 30))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(120, 130), size=(100, 30))
        self.SetSize((230, 170))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        selected = self.rbox.GetStringSelection()
        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]

        if selected == 'X-axis':
            self.parent.canvas.drawings.append(self.reflect(points=self.parent.canvas.drawings[0], m=0, c=0, about='x'))
        elif selected == 'Y-axis':
            self.parent.canvas.drawings.append(self.reflect(points=self.parent.canvas.drawings[0], m=0, c=0, about='y'))
        elif selected == 'Origin':
            self.parent.canvas.drawings.append(self.reflect(points=self.parent.canvas.drawings[0], m=0, c=0, about='origin'))
        else:
            slope = min(100, self.slopeInput.GetValue())
            c = self.cInput.GetValue()
            self.parent.canvas.drawings.append(self.reflect(points=self.parent.canvas.drawings[0], m=slope, c=c, about='line'))


        self.Show(False)
        self.parent.buttons[8] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[8] = True


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

    def reflect(self, points, m, c, about):
        translated_points = list()
        if about == 'x':
            reflect_mat = [[1, 0, 0],
                           [0, -1, 0],
                           [0, 0, 1]]

        elif about == 'y':
            reflect_mat = [[-1, 0, 0],
                           [0, 1, 0],
                           [0, 0, 1]]

        elif about == 'origin':
            reflect_mat = [[-1, 0, 0],
                           [0, -1, 0],
                           [0, 0, 1]]

        else:
            reflect_mat = [[cos(2 * atan(m)), sin(2 * atan(m)), -c * sin(2 * atan(m))],
                           [sin(2 * atan(m)), -cos(2 * atan(m)), c * 2 * (cos(atan(m)) ** 2)],
                           [0, 0, 1]]
        for point in points:
            translated = self.matrixMultiply(reflect_mat, [[point[0]], [point[1]], [1]])
            translated_points.append([translated[0][0], translated[1][0]])
        return translated_points
