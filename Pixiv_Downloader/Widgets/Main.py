from Libraries.Pixiv_Crawler import Pixiv
from Model.Download import Download
from Widgets.Labels.UserIconLabel import UserIconLabel
from Widgets.ProgressBar.ProgressBar import ProgressBar
from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QWidget


class Main(QWidget):
  def __init__(self, *args, **kwargs):
    super(Main, self).__init__(*args, **kwargs)
    self.pixiv = Pixiv()
    self.initUI()
    
    
  def initUI(self):
    self.headerHLayout()
    self.infoVLayout()
    self.functionHLayout()
    self.setButton()
    self.progressBarHLayout()
  
    layout = QVBoxLayout()
    layout.addLayout(self.headerHLayout)
    layout.addLayout(self.infoVLayout)
    layout.addLayout(self.functionHLayout)
    layout.addLayout(self.progressBarHLayout)
    
    self.setLayout(layout)
    
    
  def setButton(self):
    self.downloadButton.clicked.connect(self.downloadClick)
    
    
  def downloadClick(self):
    uid = self.searchBar.text()
    if self.isEmpty(uid):
      return
    
    if self.progressBar.value() > 0:
      self.progressBar.setValue(0)
    
    self.changeUserInfo(uid)
    
    pool = QThreadPool.globalInstance()
    dl = Download(uid, self.pixiv, self.progressBar.increase, self.progressBar.setMaximum)
    pool.start(dl)
    
    
  def changeUserInfo(self, uid):
    res = self.pixiv.user_detail(uid, is_pc=True)
    name = res['body']['name']
    url = res['body']['imageBig']
    
    img = self.pixiv.img_data(url)
    if self.isSame(img):
      return
    
    self.userNameLabel.setText(name)
    self.userIconLabel.img = img
    self.userIconLabel.isDefault = False
    self.userIconLabel.setLabel()
    
  
  def isEmpty(self, str):
    return str == ""
    
    
  def isSame(self, img):
    return self.userIconLabel.img == img
    
  
  def headerHLayout(self):
    self.userIconLabel = UserIconLabel()
    
    self.headerHLayout = QHBoxLayout()
    self.headerHLayout.addStretch(10)
    self.headerHLayout.addWidget(self.userIconLabel)
    self.headerHLayout.addStretch(10)
    
    
  def infoVLayout(self):
    self.userNameLabel = QLabel("User Name")
    self.userNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    self.infoVLayout = QVBoxLayout()
    self.infoVLayout.addWidget(self.userNameLabel)
    
    
  def functionHLayout(self):
    self.downloadButton = QPushButton("Download")
    self.searchBar = QLineEdit()
  
    self.functionHLayout = QHBoxLayout()
    self.functionHLayout.addStretch(5)
    self.functionHLayout.addWidget(self.searchBar)
    self.functionHLayout.addWidget(self.downloadButton)
    self.functionHLayout.addStretch(5)
    
    
  def progressBarHLayout(self):
    self.progressBar = ProgressBar()
    self.progressBar.setGeometry(30, 40, 200, 25)
    
    self.progressBarHLayout = QHBoxLayout()
    self.progressBarHLayout.addWidget(self.progressBar)
