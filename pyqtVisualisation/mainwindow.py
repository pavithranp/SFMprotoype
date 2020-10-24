from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import *
import pygame

MAX_IMAGE_DIM = 1920
ccd_width = 9.96  # mm for nokia 7 plus
focal_length = 36  # mm from image properties
cam_focalLength = MAX_IMAGE_DIM * focal_length / ccd_width


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = glWidget(self)
        # self.button = QPushButton('Test', self)
        self.widget.setFocusPolicy(Qt.StrongFocus)
        mainLayout = QHBoxLayout()

        mainLayout.addWidget(self.widget)
        # mainLayout.addWidget(self.button)
        self.setLayout(mainLayout)


class glWidget(QGLWidget):

    def __init__(self, parent):
        self.zoom = -5
        self.camera = [0, 0]

        self.action_keymap = {
            'a': [0, -1],
            'd': [0, 1],
            'w': [1, 0],
            's': [-1, 0],
        }
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)

    def image_load(self, lox, loy, loz, picture, rotate, zoom=0.5):
        self.read_texture(picture)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glRotated(rotate, 0.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f((-1 * zoom) + lox, (-1 * zoom) + loy, -(1 * zoom) + loz)
        glTexCoord2f(1.0, 0.0)
        glVertex3f((1 * zoom) + lox, (-1 * zoom) + loy, -(1 * zoom) + loz)
        glTexCoord2f(1.0, 1.0)
        glVertex3f((1 * zoom) + lox, (1 * zoom) + loy, -(1 * zoom) + loz)
        glTexCoord2f(0.0, 1.0)
        glVertex3f((-1 * zoom) + lox, (1 * zoom) + loy, -(1 * zoom) + loz)
        glEnd()
        self.camera_frustum(lox, loy, loz, zoom)
        glPopMatrix()

    def camera_frustum(self, lox, loy, loz, zoom):
        glBegin(GL_LINES)
        # glVertex3f(-0.1 + lox, -0.1 + loy, loz)
        # glVertex3f(0.1 + lox, -0.1 + loy, loz)
        # glVertex3f(0.1 + lox, 0.1 + loy, loz)
        # glVertex3f(-0.1 + lox, 0.1 + loy, loz)
        #
        # glVertex3f(-0.1 + lox, -0.1 + loy, loz)
        # glVertex3f(-0.1 + lox, 0.1 + loy, loz)
        # glVertex3f(0.1 + lox, -0.1 + loy, loz)
        # glVertex3f(0.1 + lox, 0.1 + loy, loz)

        glVertex3f(-(1 * zoom) + lox, -(1 * zoom) + loy, -(1 * zoom) + loz)
        glVertex3f(lox, loy, loz)

        glVertex3f(-(1 * zoom) + lox, (1 * zoom) + loy, -(1 * zoom) + loz)
        glVertex3f(lox, loy, loz)

        glVertex3f((1 * zoom) + lox, (1 * zoom) + loy, -(1 * zoom) + loz)
        glVertex3f(lox, loy, loz)

        glVertex3f((1 * zoom) + lox, -(1 * zoom) + loy, -(1 * zoom) + loz)
        glVertex3f(lox, loy, loz)

        glEnd()

    def keyPressEvent(self, event):
        try:
            self.camera = self.action_keymap.get(event.text())
            if event.text() in self.action_keymap.keys():
                glRotate(self.camera[0], 1, 0, 0)
                glRotate(self.camera[1], 0, 1, 0)
                self.update()
        except:
            pass

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.image_load(-1, 0, 0, "../reconstruction/mon_r.jpg", -20)
        self.image_load(1, 0, 0, "../reconstruction/mon_l.jpg", 20)
        glFlush()

    def initializeGL(self):
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 1.33, 0.1, 100.0)

        glTranslatef(0.0, 0.0, -10)
        glMatrixMode(GL_MODELVIEW)

    def resizeGL(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width / height
        glViewport(0, 0, width, height)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            glTranslate(0, 0, 1)
        else:
            glTranslate(0, 0, -1)
        self.update()

    def read_texture(self, picture):
        textureSurface = pygame.image.load(picture)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glEnable(GL_TEXTURE_2D)
        tex_id = glGenTextures(1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        return tex_id


if __name__ == '__main__':
    app = QApplication(['Reconstruction'])
    window = MainWindow()
    window.show()
    app.exec_()
