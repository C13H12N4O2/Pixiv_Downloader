from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class UserNameLabel(QLabel):
  def __init__(self, *args, **kwargs):
    super(UserNameLabel, self).__init__(*args, **kwargs)
    self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.setText("User Name")
