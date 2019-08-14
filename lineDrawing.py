import wx
from wx.lib.masked import NumCtrl

class LineInputPopup(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        wx.PopupWindow.__init__(self, parent, style=wx.CLOSE_BOX )
        slopeLabel = wx.StaticText(self, -1,
                           "Enter slope (m): ",
                           pos=(10,14))
        self.slopeInput = NumCtrl(self, value=0.0, integerWidth=3,fractionWidth=2, pos=(120, 10), size=(100, -1))
        cLabel = wx.StaticText(self, -1,
                           "Enter y-intercept (c): ",
                           pos=(10,44))
        self.cInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(120, 40), size=(100, -1))
        okBtn = wx.Button(self, -1, label='OK', pos=(10, 70), size=(100, 30))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(120, 70), size=(100, 30))
        self.SetSize((230, 110))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        m = min(100, self.slopeInput.GetValue())
        c = self.cInput.GetValue()

        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]
        if m == 999.99:
            self.parent.canvas.drawings.append(self.lineDrawing(float('inf'), c))
        elif m == -999.99:
            self.parent.canvas.drawings.append(self.lineDrawing(float('-inf'), c))
        else:
            self.parent.canvas.drawings.append(self.lineDrawing(m, c))
        self.Show(False)
        self.parent.buttons[0] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[0] = True


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
