from multiprocessing.pool import ThreadPool
from PyQt6.QtCore import QRunnable


class Download(QRunnable):
  def __init__(self, uid, pixiv, increase, setMaximum, *args, **kwargs):
    super(Download, self).__init__(*args, **kwargs)
    self.uid = uid
    self.pixiv = pixiv
    self.increase = increase
    self.setMaximum = setMaximum
    
    
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
    self.increase()


  def run(self):
    res = self.pixiv.user_illust(self.uid, is_pc=True)
    illust_ids = res['body']['illusts']
    self.setMaximum(len(illust_ids) - 1)
    
    results = ThreadPool(10).imap_unordered(self.illustDownload, (illust_id for illust_id in illust_ids))
    for r in results:
      r

