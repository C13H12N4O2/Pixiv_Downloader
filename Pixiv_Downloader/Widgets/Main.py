from multiprocessing.pool import ThreadPool
from Libraries.Pixiv_Crawler import Pixiv
from Widgets.Labels.UserIconLabel import UserIconLabel
from PyQt6.QtCore import Qt, QRunnable, QThreadPool
from PyQt6.QtWidgets import QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget


class Main(QWidget):
  def __init__(self, *args, **kwargs):
    super(Main, self).__init__(*args, **kwargs)
    self.pixiv = Pixiv()
    self.initUI()
    
    
  def initUI(self):
    self.headerHLayout()
    self.functionHLayout()
    self.setButton()
  
    layout = QVBoxLayout()
    layout.addLayout(self.headerHLayout)
    layout.addLayout(self.functionHLayout)
    self.setLayout(layout)
    
    
  def setButton(self):
    self.downloadButton.clicked.connect(self.downloadClick)
    
    
  def downloadClick(self):
    uid = self.searchBar.text()
    if self.isEmpty(uid):
      return
    
    self.changeIconImg(uid)
    
    pool = QThreadPool.globalInstance()
    dl = Download(uid, self.pixiv)
    pool.start(dl)
    
    
  def changeIconImg(self, uid):
    res = self.pixiv.user_detail(uid, is_pc=True)
    url = res['body']['imageBig']
    
    img = self.pixiv.img_data(url)
    if self.isSame(img):
      return
      
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
    
    
  def functionHLayout(self):
    self.downloadButton = QPushButton("Download")
    self.searchBar = QLineEdit()
  
    self.functionHLayout = QHBoxLayout()
    self.functionHLayout.addStretch(5)
    self.functionHLayout.addWidget(self.searchBar)
    self.functionHLayout.addWidget(self.downloadButton)
    self.functionHLayout.addStretch(5)


class Download(QRunnable):
  def __init__(self, uid, pixiv, *args, **kwargs):
    super(Download, self).__init__(*args, **kwargs)
    self.uid = uid
    self.pixiv = pixiv
    
    
  def illustDownload(self, illust_id):
    delay = None
    try:
      metadata = self.pixiv.ugoira_metadata(illust_id, is_pc=True)
      delay = [data['delay']/1000 for data in metadata['body']['frames']]
      url = metadata['body']['originalSrc']
    except:
      illust_detail = self.pixiv.illust_detail(illust_id, is_pc=True)['body']['illust_details']
      url = illust_detail['url_big']
    self.pixiv.download(url, delay)


  def run(self):
    res = self.pixiv.user_illust(self.uid, is_pc=True)
    illust_ids = res['body']['illusts']
    
    results = ThreadPool(10).imap_unordered(self.illustDownload, (illust_id for illust_id in illust_ids))
    for r in results:
      r
