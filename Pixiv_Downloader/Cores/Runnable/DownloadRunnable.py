from Libraries.Pixiv_Crawler import Pixiv
from Model.DownloadSignals import DownloadSignals
from PyQt6.QtCore import QRunnable


class DownloadRunnable(QRunnable):
  def __init__(self, *args, **kwargs):
    super(DownloadRunnable, self).__init__(*args, **kwargs)
    self.pixiv = Pixiv()
    self.signals = DownloadSignals()
