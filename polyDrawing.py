import wx
from wx.lib.masked import NumCtrl
import numpy as np

class PolyInputPopup(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        wx.PopupWindow.__init__(self, parent, style=wx.CLOSE_BOX )
        coeffLabel = wx.StaticText(self, -1,
                           "Enter coefficients: ",
                           pos=(10,14))
        self.coeffInput = wx.TextCtrl(self, pos=(110, 10), size=(100, -1), style = wx.TE_MULTILINE)
        self.errorLabel = wx.StaticText(self, -1,
                                   "",
                                   pos=(90, 60))
        okBtn = wx.Button(self, -1, label='OK', pos=(10, 80), size=(100, 20))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(120, 80), size=(100, 20))
        self.SetSize((230, 120))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def isfloat(self, num):
        try:
            num = float(num)
            return True
        except:
            return False

    def onOKClick(self, event):
        coeff = self.coeffInput.GetValue().split(',')
        if len(coeff) == 1 and coeff[0] == '':
            self.errorLabel.SetForegroundColour((255,0,0))
            self.errorLabel.SetLabel('Input Error')
        else:
            coeff_num = list()

            for i in coeff:
                if not self.isfloat(i.strip()):
                    self.errorLabel.SetForegroundColour((255,0,0))
                    self.errorLabel.SetLabel('Input Error')
                    break
                else:
                    coeff_num.append(float(i))
            else:
                self.errorLabel.SetLabel('')
                self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]
                if len(coeff_num) == 1:
                    self.parent.canvas.drawings.append(self.lineDrawing(0, coeff_num[0]))
                else:
                    self.parent.canvas.drawings.append(self.polyDrawing(coeff_num))
                self.Show(False)
                self.parent.buttons[14] = True
                self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
                self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.errorLabel.SetLabel('')
        self.parent.buttons[14] = True


    def polyDrawing(self, coeff):
        points = list()
        last = coeff[-1]
        for y in range(-1000, 1001):
            coeff[-1] = last - y
            roots = list(np.roots(coeff))
            for x in roots:
                if x.imag == 0:
                    points.append([x.real, y])
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
