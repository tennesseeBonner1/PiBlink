
#Module that performs screenshots on pyqtgraph items (i.e. the stimulus graph).

#This file is originally from the pyqtgraph library and was called "ImageExporter.py".
#However, that file had a bug in it (see BEFORE and AFTER comments below) so I had to create this modified...
#instance of it in order to get it to work. All credit for this file goes to the author of the pyqtgraph library.

#Aside from the single bug fix, all instances of "ImageExporter" are now "GraphExporter", imports were fixed to point to...
#the correct locations and the captureItem function was added below for convenience. That's it.

from pyqtgraph.exporters.Exporter import Exporter
from pyqtgraph.parametertree import Parameter
from pyqtgraph.Qt import QtGui, QtCore, QtSvg, USE_PYSIDE
from pyqtgraph import functions as fn
import numpy as np

__all__ = ['GraphExporter']

#Returns a QPixMap type screenshot of item passed in as parameter with following type requirement...
#From PyQtGraph's Exporter.py: "[Parameter] can be an individual graphics item or a scene."
def captureItem(toCapture):
    #Create exporter object and pass it item to screenshot
    exporter = GraphExporter(toCapture)

    #Use exporter object to take screenshot and save result
    #toBytes specifies to return screenshot as QImage, rather than save it to a file or send it to the copy buffer
    #See source code for PyQtGraph's Exporter.py's export method for more information
    qImageResult = exporter.export(toBytes = True)

    #Convert screenshot from QImage to QPixMap and return it
    return QtGui.QPixmap.fromImage(qImageResult)

class GraphExporter(Exporter):
    Name = "Image File (PNG, TIF, JPG, ...)"
    allowCopy = True
    
    def __init__(self, item):
        Exporter.__init__(self, item)
        tr = self.getTargetRect()
        if isinstance(item, QtGui.QGraphicsItem):
            scene = item.scene()
        else:
            scene = item
        bgbrush = scene.views()[0].backgroundBrush()
        bg = bgbrush.color()
        if bgbrush.style() == QtCore.Qt.NoBrush:
            bg.setAlpha(0)
            
        self.params = Parameter(name='params', type='group', children=[
            {'name': 'width', 'type': 'int', 'value': tr.width(), 'limits': (0, None)},
            {'name': 'height', 'type': 'int', 'value': tr.height(), 'limits': (0, None)},
            {'name': 'antialias', 'type': 'bool', 'value': True},
            {'name': 'background', 'type': 'color', 'value': bg},
        ])
        self.params.param('width').sigValueChanged.connect(self.widthChanged)
        self.params.param('height').sigValueChanged.connect(self.heightChanged)
        
    def widthChanged(self):
        sr = self.getSourceRect()
        ar = float(sr.height()) / sr.width()
        self.params.param('height').setValue(self.params['width'] * ar, blockSignal=self.heightChanged)
        
    def heightChanged(self):
        sr = self.getSourceRect()
        ar = float(sr.width()) / sr.height()
        self.params.param('width').setValue(self.params['height'] * ar, blockSignal=self.widthChanged)
        
    def parameters(self):
        return self.params
    
    def export(self, fileName=None, toBytes=False, copy=False):
        if fileName is None and not toBytes and not copy:
            if USE_PYSIDE:
                filter = ["*."+str(f) for f in QtGui.QImageWriter.supportedImageFormats()]
            else:
                filter = ["*."+bytes(f).decode('utf-8') for f in QtGui.QImageWriter.supportedImageFormats()]
            preferred = ['*.png', '*.tif', '*.jpg']
            for p in preferred[::-1]:
                if p in filter:
                    filter.remove(p)
                    filter.insert(0, p)
            self.fileSaveDialog(filter=filter)
            return
            
        targetRect = QtCore.QRect(0, 0, self.params['width'], self.params['height'])
        sourceRect = self.getSourceRect()

        #self.png = QtGui.QImage(targetRect.size(), QtGui.QImage.Format_ARGB32)
        #self.png.fill(pyqtgraph.mkColor(self.params['background']))
        w, h = self.params['width'], self.params['height']
        if w == 0 or h == 0:
            raise Exception("Cannot export image with size=0 (requested export size is %dx%d)" % (w,h))
        
        #BEFORE
        #bg = np.empty((self.params['width'], self.params['height'], 4), dtype=np.ubyte)

        #AFTER
        bgSize = ((int(self.params['width']), int(self.params['height']), 4))
        bg = np.empty(bgSize, dtype=np.ubyte)

        #... I have no idea why that fixes it, I just guessed around and googled for 3 hours until it worked.
        #https://groups.google.com/forum/?nomobile=true#!topic/pyqtgraph/4jiAPUpLpF4
        #Above link led me on the right track to fixing it but for some reason I also had to declare bgSize separately?

        color = self.params['background']
        bg[:,:,0] = color.blue()
        bg[:,:,1] = color.green()
        bg[:,:,2] = color.red()
        bg[:,:,3] = color.alpha()
        self.png = fn.makeQImage(bg, alpha=True)
        
        ## set resolution of image:
        origTargetRect = self.getTargetRect()
        resolutionScale = targetRect.width() / origTargetRect.width()
        #self.png.setDotsPerMeterX(self.png.dotsPerMeterX() * resolutionScale)
        #self.png.setDotsPerMeterY(self.png.dotsPerMeterY() * resolutionScale)
        
        painter = QtGui.QPainter(self.png)
        #dtr = painter.deviceTransform()
        try:
            self.setExportMode(True, {'antialias': self.params['antialias'], 'background': self.params['background'], 'painter': painter, 'resolutionScale': resolutionScale})
            painter.setRenderHint(QtGui.QPainter.Antialiasing, self.params['antialias'])
            self.getScene().render(painter, QtCore.QRectF(targetRect), QtCore.QRectF(sourceRect))
        finally:
            self.setExportMode(False)
        painter.end()
        
        if copy:
            QtGui.QApplication.clipboard().setImage(self.png)
        elif toBytes:
            return self.png
        else:
            self.png.save(fileName)
        
GraphExporter.register()        
        

