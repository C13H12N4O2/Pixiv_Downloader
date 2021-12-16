from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):
  def __init__(self, *args, **kwargs):
    super(ProgressBar, self).__init__(*args, **kwargs)
    self.step = 0
    self.setMinimum(0)

  def increase(self):
    self.setValue(self.value() + 1)
