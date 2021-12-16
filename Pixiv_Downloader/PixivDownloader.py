import sys
from Widgets.Main import Main
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QApplication


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
    
    
  def closeEvent(self, event):
    reply = QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
    
    if reply == QMessageBox.StandardButton.Yes:
      event.accept()
    else:
      event.ignore()
    

if __name__ == '__main__':
  app = QApplication(sys.argv)
  pd = PixivDownloader()
  sys.exit(app.exec())
