import sys
from Widgets.Main import Main
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication


class PixivDownloader(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__()
    self.initUI()
    
  
  def initUI(self):
    main = Main()
    self.setCentralWidget(main)
  
    self.setGeometry(300, 300, 300, 300)
    self.setWindowTitle("Pixiv Downloader")
    self.show()
    

if __name__ == '__main__':
  app = QApplication(sys.argv)
  pd = PixivDownloader()
  sys.exit(app.exec())
