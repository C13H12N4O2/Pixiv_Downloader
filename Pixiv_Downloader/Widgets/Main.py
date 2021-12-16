from Libraries.Pixiv_Crawler import Pixiv
from Widgets.Labels.UserIconLabel import UserIconLabel
from PyQt6.QtCore import Qt, QThread
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
    self.download(uid)
    
  def changeIconImg(self, uid):
    res = self.pixiv.user_detail(uid, is_pc=True)
    url = res['body']['imageBig']
    
    img = self.pixiv.img_data(url)
    if self.isSame(img):
      return
      
    self.userIconLabel.img = img
    self.userIconLabel.isDefault = False
    self.userIconLabel.setLabel()
    
      
  def get_data(self, illust_detail):
    data = {
      'url': illust_detail['url_big'],
      'title': illust_detail['title'],
      'author': illust_detail['author_details']['user_name'],
      'bookmark': illust_detail['bookmark_user_total'],
      'description': '\n              '.join(str(illust_detail['meta']['twitter_card']['description']).split('\r\n'))
    }
    return data
    
    
  def getIllustsData(self, illust_ids):
    return [self.pixiv.illust_detail(illust_id, is_pc=True)['body']['illust_details'] for illust_id in illust_ids]
    
    
  def downloadIllusts(self, illust_detail):
      illust_data = self.get_data(illust_detail)
      
      self.pixiv.download(illust_data['url'])
    
    
  def download(self, uid):
    res = self.pixiv.user_illust(uid, is_pc=True)
    illust_ids = res['body']['illusts']
    illust_details = [self.pixiv.illust_detail(illust_id, is_pc=True)['body']['illust_details'] for illust_id in illust_ids]

    for illust_detail in illust_details:
      illust_data = self.get_data(illust_detail)

      self.pixiv.download(illust_data['url'])
    
  
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
