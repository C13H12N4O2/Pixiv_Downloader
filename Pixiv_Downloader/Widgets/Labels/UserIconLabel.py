from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QPen, QColor


class UserIconLabel(QLabel):
  def __init__(self, basePath, antialiasing=True, *args, **kwargs):
    super(UserIconLabel, self).__init__(*args, **kwargs)
    
    self.img = f'{basePath}/Resources/DefaultUserIcon.png'
    self.antialiasing = antialiasing
    self.isDefault = True
    
    self.setMaximumSize(170, 170)
    self.setMinimumSize(170, 170)
    self.radius = 85
    
    self.setLabel()
    
    
  def setLabel(self):
    target = QPixmap(self.size())
    target.fill(QColor("transparent"))
    
    self.setImage()
    
    painter = QPainter(target)
    painter.setPen(QPen(Qt.GlobalColor.black, 3))
    if self.antialiasing:
      painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
      painter.setRenderHint(QPainter.RenderHint.LosslessImageRendering, True)
      painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
      
    path = QPainterPath()
    path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius, Qt.SizeMode.AbsoluteSize)
        
    painter.drawPath(path)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, self.p)
    painter.end()
    self.setPixmap(target)
        
        
  def setImage(self):
    if self.isDefault:
      self.p = QPixmap(self.img).scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
    else:
      self.p = QPixmap()
      self.p.loadFromData(self.img)
    
    
  def isSame(self, img):
    return self.img == img
    
    
  def changeUserIcon(self, url):
    img = self.Util.getImageData(url)
    
    if self.isSame(img):
      return
    
    self.img = img
    self.isDefault = False
    self.setLabel()
