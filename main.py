import wx
from wx.lib.masked import NumCtrl
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from circleDrawing import *
from clipping import *
from cosDrawing import *
from cubicDrawing import *
from ellipseDrawing import *
from lineDrawing import *
from polyDrawing import *
from rectangleDrawing import *
from reflect import *
from rotate import *
from quadraticDrawing import *
from scale import *
from shear import *
from sinDrawing import *
from translate import *

class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        self.drawings = list()
        self.num_of_plots = 0
        self.min_x = -50
        self.max_x = 50
        self.min_y = -50
        self.max_y = 50

        self.parent = parent
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(700, 700))
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        glClearColor(0, 0, 0, 0)
        self.Bind(wx.EVT_PAINT, self.OnDraw)

    def setColor(self, num):
        if num == 0:
            glColor(0, 1, 0, 0)
        elif num == 1:
            glColor(0, 0, 1, 0)
        elif num == 2:
            glColor(142 / 255, 68 / 255, 173 / 255, 0)
        elif num == 3:
            glColor(241 / 255, 196 / 255, 15 / 255, 0)
        elif num == 4:
            glColor(211 / 255, 84 / 255, 0, 0)
        elif num == 5:
            glColor(125 / 255, 206 / 255, 160 / 255, 0)
        elif num == 6:
            glColor(1, 51 / 255, 218 / 255, 0)
        elif num == 7:
            glColor(51 / 255, 79 / 255, 1, 0)
        elif num == 8:
            glColor(117 / 255, 185 / 255, 136 / 255, 0)

    def OnDraw(self, event):
        dc = wx.PaintDC(self)
        glClear(GL_COLOR_BUFFER_BIT)
        self.createLabels()

        glBegin(GL_POINTS)
        self.drawAxes()
        glEnd()
        self.SwapBuffers()

    def labels(self, font, value, x, y):
        glRasterPos2f(x, y)
        text = str(int(value))
        for ch in text :
            glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

    def createLabels(self):
        glColor(1, 1, 1, 0)
        countx = -1
        county = -1
        midx = (self.min_x + self.max_x) / 2
        midy = (self.min_y + self.max_y) / 2
        diffx = abs(self.max_x) - abs(midx)
        diffy = abs(self.max_y) - abs(midy)
        for i in range(-1000, 1001):
            if self.min_x <= i <= self.max_x and self.min_y <= 0 <= self.max_y:
                countx += 1
                if countx == int(round(diffx / 10)):
                    if i >= 0:
                        self.labels(GLUT_BITMAP_9_BY_15, round(i), (i - midx) / diffx, (0 - midy) / diffy)
                    else:
                        self.labels(GLUT_BITMAP_9_BY_15, round(i), (i - midx - 1) / diffx, (0 - midy) / diffy)
                    countx = 0
                    glBegin(GL_LINES)
                    glColor(1, 0, 0, 0)
                    glVertex2f((i - midx) / diffx, (0 - midy + (self.max_y - self.min_y) / 200) / diffy)
                    glVertex2f((i - midx) / diffx, (0 - midy - (self.max_y - self.min_y) / 200) / diffy)
                    glColor(1, 1, 1, 0)
                    glEnd()

            if self.min_x <= 0 <= self.max_x and self.min_y <= i <= self.max_y:
                county += 1
                if county == int(round(diffy / 10)):
                    if i >= 0:
                        self.labels(GLUT_BITMAP_9_BY_15, round(i), (0 - midx) / diffx, (i - midy) / diffy)
                    else:
                        self.labels(GLUT_BITMAP_9_BY_15, round(i), (0 - midx) / diffx, (i - midy) / diffy)
                    county = 0
                    glBegin(GL_LINES)
                    glColor(1, 0, 0, 0)
                    glVertex2f((0 - midx + (self.max_x - self.min_x) / 200) / diffx, (i - midy) / diffy)
                    glVertex2f((0 - midx - (self.max_x - self.min_x) / 200) / diffx, (i - midy) / diffy)
                    glColor(1, 1, 1, 0)
                    glEnd()


    def drawAxes(self):
        glColor(1, 0, 0, 0)
        midx = (self.min_x + self.max_x) / 2
        midy = (self.min_y + self.max_y) / 2
        diffx = abs(self.max_x) - abs(midx)
        diffy = abs(self.max_y) - abs(midy)
        for i in range(-1000, 1001):
            if self.min_x <= i <= self.max_x and self.min_y <= 0 <= self.max_y:
                glVertex2f((i - midx) / diffx, (0 - midy) / diffy)
            if self.min_x <= 0 <= self.max_x and self.min_y <= i <= self.max_y:
                glVertex2f((0 - midx) / diffx, (i - midy) / diffy)

    def draw(self):
        midx = (self.min_x + self.max_x) / 2
        midy = (self.min_y + self.max_y) / 2
        diffx = abs(self.max_x) - abs(midx)
        diffy = abs(self.max_y) - abs(midy)

        self.clear(clearList=False)
        glBegin(GL_POINTS)

        self.drawAxes()
        if self.num_of_plots > 1:
            self.parent.rotateBtn.Disable()
            self.parent.reflectBtn.Disable()
            self.parent.translateBtn.Disable()
            self.parent.scaleBtn.Disable()
            self.parent.shearBtn.Disable()
        else:
            self.parent.rotateBtn.Enable()
            self.parent.reflectBtn.Enable()
            self.parent.translateBtn.Enable()
            self.parent.scaleBtn.Enable()
            self.parent.shearBtn.Enable()

        if len(self.drawings) == 10:
            self.drawings = self.drawings[1:]
        count = 0
        for drawing in self.drawings[:self.num_of_plots]:
            self.setColor(count)
            for point in drawing:
                if self.min_x <= point[0] <= self.max_x and self.min_y <= point[1] <= self.max_y:
                    glVertex2f((point[0] - midx) / diffx, (point[1] - midy) / diffy)
            count += 1
        glEnd()
        self.parent.canvas.createLabels()
        self.SwapBuffers()


    def clear(self, clearList):
        if clearList:
            self.drawings = list()
        glClear(GL_COLOR_BUFFER_BIT)
        self.SwapBuffers()
        glClear(GL_COLOR_BUFFER_BIT)
        self.SwapBuffers()
        glBegin(GL_POINTS)
        self.parent.canvas.drawAxes()
        glEnd()
        self.parent.canvas.createLabels()
        self.SwapBuffers()

    def clip(self):
        gluOrtho2D(self.min_x, self.max_x, self.min_y, self.max_y)
        self.clear(clearList=False)
        self.draw()




class MyPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self.buttons = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("#626D58")
        self.canvas = OpenGLCanvas(self)

        self.lineBtn = wx.Button(self, -1, label='Line', pos=(710, 10), size=(70, 30))
        self.lineBtn.Bind(wx.EVT_BUTTON, self.onLinePopup)
        self.lineWindow = LineInputPopup(self)

        self.quadBtn = wx.Button(self, -1, label='Quadratic', pos=(710, 50), size=(70, 30))
        self.quadBtn.Bind(wx.EVT_BUTTON, self.onQuadPopup)
        self.quadWindow = QuadInputPopup(self)

        self.cubicBtn = wx.Button(self, -1, label='Cubic', pos=(710, 90), size=(70, 30))
        self.cubicBtn.Bind(wx.EVT_BUTTON, self.onCubicPopup)
        self.cubicWindow = CubicInputPopup(self)

        self.polyBtn = wx.Button(self, -1, label='Poly', pos=(710, 130), size=(70, 30))
        self.polyBtn.Bind(wx.EVT_BUTTON, self.onPolyPopup)
        self.polyWindow = PolyInputPopup(self)

        self.circleBtn = wx.Button(self, -1, label='Circle', pos=(710, 170), size=(70, 30))
        self.circleBtn.Bind(wx.EVT_BUTTON, self.onCirclePopup)
        self.circleWindow = CircleInputPopup(self)

        self.ellipseBtn = wx.Button(self, -1, label='Ellipse', pos=(710, 210), size=(70, 30))
        self.ellipseBtn.Bind(wx.EVT_BUTTON, self.onEllipsePopup)
        self.ellipseWindow = EllipseInputPopup(self)

        self.rectBtn = wx.Button(self, -1, label='Rectangle', pos=(710, 250), size=(70, 30))
        self.rectBtn.Bind(wx.EVT_BUTTON, self.onRectanglePopup)
        self.rectWindow = RectangleInputPopup(self)

        self.rotateBtn = wx.Button(self, -1, label='Rotate', pos=(710, 290), size=(70, 30))
        self.rotateBtn.Bind(wx.EVT_BUTTON, self.onRotatePopup)
        self.rotateWindow = RotateInputPopup(self)

        self.reflectBtn = wx.Button(self, -1, label='Reflect', pos=(710, 330), size=(70, 30))
        self.reflectBtn.Bind(wx.EVT_BUTTON, self.onReflectPopup)
        self.reflectWindow = ReflectInputPopup(self)

        self.translateBtn = wx.Button(self, -1, label='Translate', pos=(710, 370), size=(70, 30))
        self.translateBtn.Bind(wx.EVT_BUTTON, self.onTranslatePopup)
        self.translateWindow = TranslateInputPopup(self)

        self.scaleBtn = wx.Button(self, -1, label='Scale', pos=(710, 410), size=(70, 30))
        self.scaleBtn.Bind(wx.EVT_BUTTON, self.onScalePopup)
        self.scaleWindow = ScaleInputPopup(self)

        self.shearBtn = wx.Button(self, -1, label='Shear', pos=(710, 450), size=(70, 30))
        self.shearBtn.Bind(wx.EVT_BUTTON, self.onShearPopup)
        self.shearWindow = ShearInputPopup(self)

        self.sinBtn = wx.Button(self, -1, label='Sin', pos=(710, 490), size=(70, 30))
        self.sinBtn.Bind(wx.EVT_BUTTON, self.onSinPopup)
        self.sinWindow = SinInputPopup(self)

        self.cosBtn = wx.Button(self, -1, label='Cos', pos=(710, 530), size=(70, 30))
        self.cosBtn.Bind(wx.EVT_BUTTON, self.onCosPopup)
        self.cosWindow = CosInputPopup(self)

        self.clipBtn = wx.Button(self, -1, label='Clip', pos=(710, 570), size=(70, 30))
        self.clipBtn.Bind(wx.EVT_BUTTON, self.onClipPopup)
        self.clipWindow = ClipInputPopup(self)

        self.backBtn = wx.Button(self, -1, label='<-', pos=(710, 610), size=(30, 30))
        self.backBtn.Bind(wx.EVT_BUTTON, self.goBack)
        self.forwardBtn = wx.Button(self, -1, label='->', pos=(750, 610), size=(30, 30))
        self.forwardBtn.Bind(wx.EVT_BUTTON, self.goForward)

        self.clearBtn = wx.Button(self, -1, label='Clear', pos=(710, 650), size=(70, 30))
        self.clearBtn.Bind(wx.EVT_BUTTON, self.clearScreen)


    def enableDisable(self, num):
        for i in range(len(self.buttons)):
            if i != num:
                self.buttons[i] = True

        if num != 0:
            self.lineWindow.Show(False)
        if num != 1:
            self.quadWindow.Show(False)
        if num != 2:
            self.circleWindow.Show(False)
        if num != 3:
            self.clipWindow.Show(False)
        if num != 4:
            self.sinWindow.Show(False)
        if num != 5:
            self.cosWindow.Show(False)
        if num != 6:
            self.ellipseWindow.Show(False)
        if num != 7:
            self.rotateWindow.Show(False)
        if num != 8:
            self.reflectWindow.Show(False)
        if num != 9:
            self.translateWindow.Show(False)
        if num != 10:
            self.scaleWindow.Show(False)
        if num != 11:
            self.cubicWindow.Show(False)
        if num != 12:
            self.shearWindow.Show(False)
        if num != 13:
            self.rectWindow.Show(False)
        if num != 14:
            self.polyWindow.Show(False)


    def onLinePopup(self, event):
        if self.buttons[0]:
            self.enableDisable(0)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.lineWindow.SetPosition((pos[0] - 250, pos[1]))
            self.lineWindow.Show(True)
            self.buttons[0] = False
        else:
            self.lineWindow.Show(False)
            self.buttons[0] = True


    def onQuadPopup(self, event):
        if self.buttons[1]:
            self.enableDisable(1)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.quadWindow.SetPosition((pos[0] - 150, pos[1]))
            self.quadWindow.Show(True)
            self.buttons[1] = False
        else:
            self.quadWindow.Show(False)
            self.buttons[1] = True


    def onCirclePopup(self, event):
        if self.buttons[2]:
            self.enableDisable(2)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.circleWindow.SetPosition((pos[0] - 250, pos[1]))
            self.circleWindow.Show(True)
            self.buttons[2] = False
        else:
            self.circleWindow.Show(False)
            self.buttons[2] = True

    def onEllipsePopup(self, event):
        if self.buttons[6]:
            self.enableDisable(6)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.ellipseWindow.SetPosition((pos[0] - 250, pos[1]))
            self.ellipseWindow.Show(True)
            self.buttons[6] = False
        else:
            self.ellipseWindow.Show(False)
            self.buttons[6] = True

    def onCubicPopup(self, event):
        if self.buttons[11]:
            self.enableDisable(11)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.cubicWindow.SetPosition((pos[0] - 150, pos[1]))
            self.cubicWindow.Show(True)
            self.buttons[11] = False
        else:
            self.cubicWindow.Show(False)
            self.buttons[11] = True

    def onPolyPopup(self, event):
        if self.buttons[14]:
            self.enableDisable(14)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.polyWindow.SetPosition((pos[0] - 250, pos[1]))
            self.polyWindow.errorLabel.SetLabel('')
            self.polyWindow.Show(True)
            self.buttons[14] = False
        else:
            self.polyWindow.Show(False)
            self.buttons[14] = True

    def onRectanglePopup(self, event):
        if self.buttons[13]:
            self.enableDisable(13)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.rectWindow.SetPosition((pos[0] - 250, pos[1]))
            self.rectWindow.errorLabel.SetLabel('')
            self.rectWindow.Show(True)
            self.buttons[13] = False
        else:
            self.rectWindow.Show(False)
            self.buttons[13] = True

    def onRotatePopup(self, event):
        if self.buttons[7]:
            self.enableDisable(7)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.rotateWindow.SetPosition((pos[0] - 250, pos[1]))
            self.rotateWindow.Show(True)
            self.buttons[7] = False
        else:
            self.rotateWindow.Show(False)
            self.buttons[7] = True

    def onReflectPopup(self, event):
        if self.buttons[8]:
            self.enableDisable(8)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.reflectWindow.SetPosition((pos[0] - 250, pos[1]))
            self.reflectWindow.Show(True)
            self.buttons[8] = False
        else:
            self.reflectWindow.Show(False)
            self.buttons[8] = True

    def onTranslatePopup(self, event):
        if self.buttons[9]:
            self.enableDisable(9)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.translateWindow.SetPosition((pos[0] - 150, pos[1]))
            self.translateWindow.Show(True)
            self.buttons[9] = False
        else:
            self.translateWindow.Show(False)
            self.buttons[9] = True

    def onScalePopup(self, event):
        if self.buttons[10]:
            self.enableDisable(10)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.scaleWindow.SetPosition((pos[0] - 150, pos[1]))
            self.scaleWindow.Show(True)
            self.buttons[10] = False
        else:
            self.scaleWindow.Show(False)
            self.buttons[10] = True

    def onShearPopup(self, event):
        if self.buttons[12]:
            self.enableDisable(12)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.shearWindow.SetPosition((pos[0] - 250, pos[1]))
            self.shearWindow.Show(True)
            self.buttons[12] = False
        else:
            self.shearWindow.Show(False)
            self.buttons[12] = True

    def onSinPopup(self, event):
        if self.buttons[4]:
            self.enableDisable(4)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.sinWindow.SetPosition((pos[0] - 250, pos[1]))
            self.sinWindow.Show(True)
            self.buttons[4] = False
        else:
            self.sinWindow.Show(False)
            self.buttons[4] = True

    def onCosPopup(self, event):
        if self.buttons[5]:
            self.enableDisable(5)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.cosWindow.SetPosition((pos[0] - 250, pos[1]))
            self.cosWindow.Show(True)
            self.buttons[5] = False
        else:
            self.cosWindow.Show(False)
            self.buttons[5] = True

    def onClipPopup(self, event):
        if self.buttons[3]:
            self.enableDisable(3)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.clipWindow.SetPosition((pos[0] - 250, pos[1]))
            self.clipWindow.errorLabel.SetLabel('')
            self.clipWindow.Show(True)
            self.buttons[3] = False
        else:
            self.clipWindow.Show(False)
            self.buttons[3] = True


    def goBack(self, event):
        self.canvas.num_of_plots = max(0, self.canvas.num_of_plots - 1)
        self.canvas.draw()

    def goForward(self, event):
        self.canvas.num_of_plots = min(len(self.canvas.drawings), self.canvas.num_of_plots + 1)
        self.canvas.draw()

    def clearScreen(self, event):
        self.enableDisable(-1)
        self.canvas.clear(clearList=True)

class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (800, 735)
        wx.Frame.__init__(self, None, title='Plotter', size=self.size, style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        self.SetIcon(wx.Icon("images/window_icon.png"))
        self.panel = MyPanel(self)
        self.SetPosition((0, 0))
        self.SetMinSize(self.size)
        self.SetMaxSize(self.size)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
