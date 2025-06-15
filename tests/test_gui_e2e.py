import pytest
from gui.main_window import MainWindow


def test_main_window_starts(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    assert window.isVisible()
