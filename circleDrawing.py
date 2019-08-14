import wx
from wx.lib.masked import NumCtrl

class CircleInputPopup(wx.Frame):
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
        radiusLabel = wx.StaticText(self, -1,
                           "Enter radius: ",
                           pos=(10,54))
        self.radiusInput = NumCtrl(self, value=0.0, allowNegative = False, integerWidth=3, fractionWidth=2, pos=(90, 50), size=(100, -1))
        okBtn = wx.Button(self, -1, label='OK', pos=(10, 100), size=(100, 30))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(120, 100), size=(100, 30))
        self.SetSize((230, 135))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        xc = self.centerxInput.GetValue()
        yc = self.centeryInput.GetValue()
        radius = self.radiusInput.GetValue()
        self.parent.canvas.drawings = self.parent.canvas.drawings[:self.parent.canvas.num_of_plots]
        self.parent.canvas.drawings.append(self.circleDrawing(xc, yc, radius))

        self.Show(False)
        self.parent.buttons[2] = True
        self.parent.canvas.num_of_plots = min(9, len(self.parent.canvas.drawings))
        self.parent.canvas.draw()

    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[2] = True


    def circleDrawing(self, xc, yc, r):
        points = list()

        x = 0
        y = r
        points.append([x + xc, y + yc])
        points.append([-x + xc, y + yc])
        points.append([x + xc, -y + yc])
        points.append([-x + xc, -y + yc])
        points.append([y + xc, x + yc])
        points.append([-y + xc, x + yc])
        points.append([y + xc, -x + yc])
        points.append([-y + xc,-x + yc])
        p = 5 / 4 - r

        while x < y:
            x += 1
            if p < 0:
                points.append([x + xc, y + yc])
                points.append([-x + xc, y + yc])
                points.append([x + xc, -y + yc])
                points.append([-x + xc, -y + yc])
                points.append([y + xc, x + yc])
                points.append([-y + xc, x + yc])
                points.append([y + xc, -x + yc])
                points.append([-y + xc,-x + yc])

                p += 2 * x + 1
            else:
                y -= 1
                points.append([x + xc, y + yc])
                points.append([-x + xc, y + yc])
                points.append([x + xc, -y + yc])
                points.append([-x + xc, -y + yc])
                points.append([y + xc, x + yc])
                points.append([-y + xc, x + yc])
                points.append([y + xc, -x + yc])
                points.append([-y + xc,-x + yc])
                p += 2 * (x - y) + 1
        return points
