import math
import wx
from wx.lib.masked import NumCtrl

class TranslateInputPopup(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        wx.PopupWindow.__init__(self, parent, style=wx.CLOSE_BOX )
        txLabel = wx.StaticText(self, -1,
                           "Enter tx: ",
                           pos=(10,14))
        self.txInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(55, 10), size=(100, -1))
        tyLabel = wx.StaticText(self, -1,
                           "Enter ty: ",
                           pos=(10,44))
        self.tyInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(55, 40), size=(100, -1))

        okBtn = wx.Button(self, -1, label='OK', pos=(10, 70), size=(100, 20))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(10, 100), size=(100, 20))
        self.SetSize((130, 140))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        tx = self.txInput.GetValue()
        ty = self.tyInput.GetValue()
        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]
        self.parent.canvas.drawings.append(self.translate(points=self.parent.canvas.drawings[0], tx=tx, ty=ty))


        self.Show(False)
        self.parent.buttons[9] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[9] = True


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


    def translate(self, points, tx, ty):
        translated_points = list()
        translate_mat = [[1, 0, tx],
                         [0, 1, ty],
                         [0, 0, 1]]
        for point in points:
            translated = self.matrixMultiply(translate_mat, [[point[0]], [point[1]], [1]])
            translated_points.append([translated[0][0], translated[1][0]])
        return translated_points
