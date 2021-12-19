from Cores.Runnable.DownloadRunnable import DownloadRunnable
from PyQt6.QtCore import QThreadPool


class Download(DownloadRunnable):
  def __init__(self, illust_id, *args, **kwargs):
    super(Download, self).__init__(*args, **kwargs)
    self.illust_id = illust_id
    
    
  def setDownload(self, illust_id):
    try:
      self.ugoiraDownload(illust_id)
    except:
      self.illustsDownload(illust_id)


  def ugoiraDownload(self, illust_id):
    metadata = self.pixiv.ugoira_metadata(illust_id, is_pc=True)['body']
    delay = [data['delay']/1000 for data in metadata['frames']]
    url = metadata['originalSrc']
    self.pixiv.download(url, delay)
    
    
  def illustsDownload(self, illust_id):
    illust_detail = self.pixiv.illust_pages(illust_id)['body']
    for data in illust_detail:
      url = data['urls']['original']
      self.pixiv.download(url)


  def run(self):
    self.setDownload(self.illust_id)
    self.signals.finished.emit()
