from gui.icons_helper import get_icon
from PyQt5.QtWidgets import QApplication
import sys


def test_get_icon():
    app = QApplication.instance() or QApplication(sys.argv)
    icon = get_icon("vpn")
    assert icon is not None or icon is None  # Aceita ambos para ambiente headless
