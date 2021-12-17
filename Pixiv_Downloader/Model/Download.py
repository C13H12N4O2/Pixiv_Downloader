from multiprocessing.pool import ThreadPool
from PyQt6.QtCore import QRunnable


class Download(QRunnable):
  def __init__(self, uid, pixiv, increase, setMaximum, *args, **kwargs):
    super(Download, self).__init__(*args, **kwargs)
    self.uid = uid
    self.pixiv = pixiv
    self.increase = increase
    self.setMaximum = setMaximum
    
    
  def setDownload(self, illust_id):
    delay = None
    try:
      self.ugoiraDownload(illust_id)
    except:
      self.illustsDownload(illust_id)


  def ugoiraDownload(self, illust_id):
    metadata = self.pixiv.ugoira_metadata(illust_id, is_pc=True)
    delay = [data['delay']/1000 for data in metadata['body']['frames']]
    url = metadata['body']['originalSrc']
    self.pixiv.download(url, delay)
    self.increase()
    
    
  def illustsDownload(self, illust_id):
    illust_detail = self.pixiv.illust_pages(illust_id)['body']
    for data in illust_detail:
      url = data['urls']['original']
      self.pixiv.download(url)
    self.increase()


  def run(self):
    res = self.pixiv.user_illust(self.uid, is_pc=True)
    illust_ids = res['body']['illusts']
    self.setMaximum(len(illust_ids) - 1)
    
    results = ThreadPool(10).imap_unordered(self.setDownload, (illust_id for illust_id in illust_ids))
    (r for r in results)

