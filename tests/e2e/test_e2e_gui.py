import pytest
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow


@pytest.mark.usefixtures("mock_backend")
def test_main_window_starts(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    assert window.isVisible()
    if hasattr(window, "log_view"):
        window.log_view._skip_log = True


@pytest.mark.usefixtures("mock_backend")
def test_iniciar_vpn(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    if hasattr(window, "log_view"):
        window.log_view._skip_log = True
    btn = window.findChild(QPushButton, "btnStartVPN")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.LeftButton)
    # Checar status após clique


@pytest.mark.usefixtures("mock_backend")
def test_configurar_proxy(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    if hasattr(window, "log_view"):
        window.log_view._skip_log = True
    btn = window.findChild(QPushButton, "btnConfigProxy")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.LeftButton)


@pytest.mark.usefixtures("mock_backend")
def test_verificar_logs(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    if hasattr(window, "log_view"):
        window.log_view._skip_log = True
    btn = window.findChild(QPushButton, "btnLogs")
    assert btn is not None
    qtbot.mouseClick(btn, Qt.LeftButton)
