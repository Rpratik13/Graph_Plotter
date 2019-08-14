import math
import wx
from wx.lib.masked import NumCtrl

class ShearInputPopup(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        wx.PopupWindow.__init__(self, parent, style=wx.CLOSE_BOX )
        self.rbox = wx.RadioBox(self,label = 'Shear Axis', pos = (50,10), choices = ['X-axis', 'Y-axis'], majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        sfLabel = wx.StaticText(self, -1,
                           "Enter Shear Factor: ",
                           pos=(10,74))
        self.sfInput = NumCtrl(self, value=0.0, integerWidth=2, fractionWidth=2, pos=(115, 75), size=(100, -1))
        refLabel = wx.StaticText(self, -1,
                           "Enter ref: ",
                           pos=(10,104))
        self.refInput = NumCtrl(self, value=0.0, integerWidth=2, fractionWidth=2, pos=(115, 105), size=(100, -1))

        okBtn = wx.Button(self, -1, label='OK', pos=(10, 140), size=(100, 30))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(120, 140), size=(100, 30))
        self.SetSize((230, 180))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        sf = self.sfInput.GetValue()
        ref = self.refInput.GetValue()
        selected = self.rbox.GetStringSelection()
        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]
        if selected == 'X-axis':
            self.parent.canvas.drawings.append(self.shear(points=self.parent.canvas.drawings[0], sf=sf, ref=ref, axis='x'))
        else:
            self.parent.canvas.drawings.append(self.shear(points=self.parent.canvas.drawings[0], sf=sf, ref=ref, axis='y'))

        self.Show(False)
        self.parent.buttons[12] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[12] = True


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


    def shear(self, points, sf, ref, axis):
        translated_points = list()
        if axis == 'x':
            shear_mat = [[1, sf, -sf * ref],
                         [0, 1, 0],
                         [0, 0, 1]]

        elif axis == 'y':
            shear_mat = [[1, 0, 0],
                         [sf, 1, -sf * ref],
                         [0, 0, 1]]

        for point in points:
            translated = self.matrixMultiply(shear_mat, [[point[0]], [point[1]], [1]])
            translated_points.append([translated[0][0], translated[1][0]])
        return translated_points
