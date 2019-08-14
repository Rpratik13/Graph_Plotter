import wx
from wx.lib.masked import NumCtrl

class ClipInputPopup(wx.Frame):
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
                           "Enter min: ",
                           pos=(10,24))
        self.minxInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(90, 20), size=(100, -1))
        self.minyInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(150, 20), size=(100, -1))
        radiusLabel = wx.StaticText(self, -1,
                           "Enter max: ",
                           pos=(10,54))
        self.maxxInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(90, 50), size=(100, -1))
        self.maxyInput = NumCtrl(self, value=0.0, integerWidth=3, fractionWidth=2, pos=(150, 50), size=(100, -1))
        self.errorLabel = wx.StaticText(self, -1,
                                   "",
                                   pos=(90, 80))
        okBtn = wx.Button(self, -1, label='OK', pos=(10, 100), size=(100, 30))
        cancelBtn = wx.Button(self, -1, label='Cancel', pos=(120, 100), size=(100, 30))
        self.SetSize((230, 135))

        okBtn.Bind(wx.EVT_BUTTON, self.onOKClick)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def onOKClick(self, event):
        if self.minxInput.GetValue() < self.maxxInput.GetValue() and self.minyInput.GetValue() < self.maxyInput.GetValue():
            self.parent.canvas.min_x = self.minxInput.GetValue()
            self.parent.canvas.min_y = self.minyInput.GetValue()
            self.parent.canvas.max_x = self.maxxInput.GetValue()
            self.parent.canvas.max_y = self.maxyInput.GetValue()
            self.parent.canvas.draw()
            self.Show(False)
            self.parent.buttons[3] = True
        else:
            self.errorLabel.SetForegroundColour((255,0,0))
            self.errorLabel.SetLabel('Clipping Error')


    def onCancelClick(self, event):
        self.Show(False)
        self.parent.buttons[3] = True
