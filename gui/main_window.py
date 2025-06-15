from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QLineEdit,
    QHBoxLayout,
    QScrollArea,
    QSpacerItem,
    QSizePolicy,
    QGridLayout,
    QDialog,
    QFormLayout,
    QCheckBox,
    QTabWidget,
    QComboBox,
    QTextEdit,
    QStackedWidget,
    QListWidget,
    QListWidgetItem,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from wireguard.manager import WireGuardManager
from openvpn.manager import OpenVPNManager
from proxies.proxy_manager import ProxyManager, validate_proxy_config, ProxyChain
from proxies.proxychain_manager import (
    generate_random_chain,
    set_active_proxychain,
    load_proxychain_config,
    save_proxychain_config,
    load_proxies_list,
    save_proxies_list,
    add_proxy,
    remove_proxy,
    list_proxies,
    save_chain,
    load_chain,
    list_chains,
    test_all_chains,
    validate_chain,
    reorder_chain,
    update_proxies_from_scraper,
)
from gui.db_manager import DBManager, DB_PATH
from gui.privacy_config import (
    load_config,
    save_config,
    backup_config,
    reset_config,
    validate_privacy_config,
)
from gui.kill_switch import enable_kill_switch, disable_kill_switch
from gui.secure_dns import set_secure_dns
from gui.tor_integration import start_tor
from openvpn.settings import (
    load_ovpn_settings,
    save_ovpn_settings,
    get_presets,
    validate_ovpn_settings,
    default_ovpn_settings,
)
from wireguard.wg_settings import (
    load_wg_settings,
    save_wg_settings,
    validate_wg_settings,
    default_wg_settings,
)
from gui.network_monitor_helpers import (
    get_network_stats,
    get_connections,
    get_vpn_status,
    get_tor_status,
    get_proxy_status,
    update_traffic_history,
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import os
import webbrowser
from gui.icons_helper import get_icon
import logging
import traceback
from PyQt5.QtWidgets import QAction
import json
import pandas as pd
import platform
from crypto.security_protocols import (
    AESCipher,
    SSHManager,
    ftps_upload,
    generate_self_signed_cert,
    generate_secure_random_bytes,
)
from gui.audit_log import log_audit_event
import threading
import time
import socket
import psutil
from PyQt5.QtCore import pyqtSignal, QObject


class LogHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)


class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Usuários")
        self.setStyleSheet("background-color: #181c24; color: #f5f6fa;")
        self.setWindowIcon(get_icon("user"))
        layout = QVBoxLayout(self)

        btn_add = QPushButton("Adicionar Usuário")
        btn_add.setIcon(get_icon("add"))
        btn_add.setStyleSheet(
            """QPushButton {background-color: #263238; color: #00e676; border-radius: 8px; padding: 10px;} QPushButton:hover {background-color: #37474f;}"""
        )
        layout.addWidget(btn_add)

        self.setLayout(layout)


class ProxyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Proxies")
        self.setStyleSheet("background-color: #181c24; color: #f5f6fa;")
        self.setWindowIcon(get_icon("proxy"))
        layout = QVBoxLayout(self)

        btn_multi = QPushButton("Ativar Multi-Hop")
        btn_multi.setIcon(get_icon("proxy"))
        btn_multi.setStyleSheet(
            """QPushButton {background-color: #7c4dff; color: #fff; border-radius: 8px; padding: 10px;} QPushButton:hover {background-color: #512da8;}"""
        )
        layout.addWidget(btn_multi)

        btn_proxychains = QPushButton("Gerenciar ProxyChains")
        btn_proxychains.setIcon(get_icon("chain"))
        btn_proxychains.setStyleSheet(
            """QPushButton {background-color: #00e676; color: #181c24; border-radius: 8px; padding: 10px;} QPushButton:hover {background-color: #00bfae;}"""
        )
        layout.addWidget(btn_proxychains)

        self.setLayout(layout)


class ApiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Painel de Integrações/API")
        self.setStyleSheet("background-color: #181c24; color: #f5f6fa;")
        self.setWindowIcon(get_icon("api"))
        layout = QVBoxLayout(self)

        btn_open = QPushButton("Abrir Documentação API")
        btn_open.setIcon(get_icon("api"))
        btn_open.setStyleSheet(
            """QPushButton {background-color: #ff9100; color: #222; border-radius: 8px; padding: 10px;} QPushButton:hover {background-color: #ffab40;}"""
        )
        layout.addWidget(btn_open)

        self.setLayout(layout)


class KeyManagerDialog(QDialog):
    def __init__(self, key_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Chave de Criptografia")
        self.setStyleSheet("background-color: #181c24; color: #f5f6fa;")
        self.setWindowIcon(get_icon("settings"))
        layout = QVBoxLayout(self)
        self.key_path = key_path
        self.key_label = QLabel("Caminho da chave: " + key_path)
        self.key_label.setStyleSheet("color: #ffd600;")
        layout.addWidget(self.key_label)
        btn_show = QPushButton("Exibir Chave")
        btn_show.setStyleSheet(
            "background-color: #263238; color: #00e676; border-radius: 8px; padding: 10px;"
        )
        btn_show.clicked.connect(self.show_key)
        layout.addWidget(btn_show)
        btn_regen = QPushButton("Regenerar Chave")
        btn_regen.setStyleSheet(
            "background-color: #263238; color: #ff1744; border-radius: 8px; padding: 10px;"
        )
        btn_regen.clicked.connect(self.regen_key)
        layout.addWidget(btn_regen)
        self.setLayout(layout)

    def show_key(self):
        try:
            if os.path.exists(self.key_path):
                with open(self.key_path, "rb") as f:
                    key = f.read()
                QMessageBox.information(self, "Chave", key.hex())
            else:
                QMessageBox.warning(self, "Chave", "Chave não encontrada.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exibir chave: {e}")

    def regen_key(self):
        try:
            key = generate_secure_random_bytes(32)
            with open(self.key_path, "wb") as f:
                f.write(key)
            QMessageBox.information(self, "Chave", "Chave regenerada com sucesso.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao regenerar chave: {e}")


class ConfigBackupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Backup/Restauração de Configuração Criptografada")
        self.setStyleSheet("background-color: #181c24; color: #f5f6fa;")
        self.setWindowIcon(get_icon("settings"))
        layout = QVBoxLayout(self)
        btn_export = QPushButton("Exportar Configuração Criptografada")
        btn_export.setStyleSheet(
            "background-color: #263238; color: #00e676; border-radius: 8px; padding: 10px;"
        )
        btn_export.clicked.connect(self.export_config)
        layout.addWidget(btn_export)
        btn_import = QPushButton("Importar Configuração Criptografada")
        btn_import.setStyleSheet(
            "background-color: #263238; color: #ffd600; border-radius: 8px; padding: 10px;"
        )
        btn_import.clicked.connect(self.import_config)
        layout.addWidget(btn_import)
        self.setLayout(layout)

    def export_config(self):
        from gui.privacy_config import export_encrypted_config

        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar Configuração", "", "Arquivo Criptografado (*.enc)"
        )
        if path:
            try:
                if export_encrypted_config(path):
                    QMessageBox.information(
                        self, "Exportação", "Configuração exportada com sucesso!"
                    )
                else:
                    QMessageBox.warning(
                        self, "Exportação", "Falha ao exportar configuração."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, "Erro", f"Erro ao exportar configuração: {e}"
                )

    def import_config(self):
        from gui.privacy_config import import_encrypted_config

        path, _ = QFileDialog.getOpenFileName(
            self, "Importar Configuração", "", "Arquivo Criptografado (*.enc)"
        )
        if path:
            try:
                if import_encrypted_config(path):
                    QMessageBox.information(
                        self,
                        "Importação",
                        "Configuração importada e validada com sucesso!",
                    )
                else:
                    QMessageBox.warning(
                        self, "Importação", "Falha ao importar ou validar configuração."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, "Erro", f"Erro ao importar configuração: {e}"
                )


class DBBackupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Backup/Restauração do Banco de Dados Criptografado")
        self.setStyleSheet("background-color: #181c24; color: #f5f6fa;")
        self.setWindowIcon(get_icon("settings"))
        layout = QVBoxLayout(self)
        btn_export = QPushButton("Exportar Banco de Dados Criptografado")
        btn_export.setStyleSheet(
            "background-color: #263238; color: #00e676; border-radius: 8px; padding: 10px;"
        )
        btn_export.clicked.connect(self.export_db)
        layout.addWidget(btn_export)
        btn_import = QPushButton("Importar Banco de Dados Criptografado")
        btn_import.setStyleSheet(
            "background-color: #263238; color: #ffd600; border-radius: 8px; padding: 10px;"
        )
        btn_import.clicked.connect(self.import_db)
        layout.addWidget(btn_import)
        self.setLayout(layout)

    def export_db(self):
        from gui.db_manager import export_encrypted_db

        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar Banco de Dados", "", "Banco Criptografado (*.enc)"
        )
        if path:
            try:
                if export_encrypted_db(path):
                    QMessageBox.information(
                        self, "Exportação", "Banco de dados exportado com sucesso!"
                    )
                else:
                    QMessageBox.warning(
                        self, "Exportação", "Falha ao exportar banco de dados."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, "Erro", f"Erro ao exportar banco de dados: {e}"
                )

    def import_db(self):
        from gui.db_manager import import_encrypted_db

        path, _ = QFileDialog.getOpenFileName(
            self, "Importar Banco de Dados", "", "Banco Criptografado (*.enc)"
        )
        if path:
            try:
                if import_encrypted_db(path):
                    QMessageBox.information(
                        self,
                        "Importação",
                        "Banco de dados importado e validado com sucesso!",
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Importação",
                        "Falha ao importar ou validar banco de dados.",
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, "Erro", f"Erro ao importar banco de dados: {e}"
                )


class AuditLogDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Logs de Auditoria Criptografados")
        self.setStyleSheet("background-color: #181c24; color: #f5f6fa;")
        self.setWindowIcon(get_icon("search"))
        layout = QVBoxLayout(self)
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("background-color: #222; color: #00e676;")
        layout.addWidget(self.log_view)
        btn_refresh = QPushButton("Atualizar Logs")
        btn_refresh.setStyleSheet(
            "background-color: #263238; color: #ffd600; border-radius: 8px; padding: 10px;"
        )
        btn_refresh.clicked.connect(self.load_logs)
        layout.addWidget(btn_refresh)
        self.setLayout(layout)
        self.load_logs()

    def load_logs(self):
        from gui.privacy_config import get_or_create_key, AESCipher

        key = get_or_create_key()
        aes = AESCipher(key)
        log_path = os.path.join(os.path.dirname(__file__), "audit.log.enc")
        if os.path.exists(log_path):
            try:
                with open(log_path, "rb") as f:
                    encrypted = f.read()
                data = aes.decrypt(encrypted)
                self.log_view.setPlainText(data.decode())
            except Exception:
                self.log_view.setPlainText("Falha ao decifrar os logs.")
        else:
            self.log_view.setPlainText("Nenhum log encontrado.")


class NetworkMonitorBackend(QObject):
    update_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def monitor_loop(self):
        while self.running:
            stats = self.get_full_network_stats()
            self.update_signal.emit(stats)
            time.sleep(2)

    def get_full_network_stats(self):
        devices = self.get_connected_devices()
        ips = self.detect_ips()
        ids = self.detect_ids()
        return {
            "devices": devices,
            "ips": ips,
            "ids": ids,
            "network": get_network_stats(),
        }

    def get_connected_devices(self):
        devices = []
        try:
            for conn in psutil.net_connections(kind="inet"):
                if conn.raddr:
                    devices.append(
                        {
                            "local": f"{conn.laddr.ip}:{conn.laddr.port}",
                            "remote": f"{conn.raddr.ip}:{conn.raddr.port}",
                            "status": conn.status,
                        }
                    )
        except Exception:
            pass
        return devices

    def detect_ips(self):
        # Simulação de IPS (pode ser expandido com scapy/snort)
        alerts = []
        for conn in psutil.net_connections(kind="inet"):
            if (
                conn.status == "ESTABLISHED"
                and conn.raddr
                and conn.raddr.ip not in ["127.0.0.1", "::1"]
            ):
                alerts.append(
                    {"type": "IPS", "desc": f"Conexão ativa detectada: {conn.raddr.ip}"}
                )
        return alerts

    def detect_ids(self):
        # Simulação de IDS (pode ser expandido com regras reais)
        alerts = []
        for conn in psutil.net_connections(kind="inet"):
            if (
                conn.status == "LISTEN"
                and conn.laddr
                and conn.laddr.ip not in ["127.0.0.1", "::1"]
            ):
                alerts.append(
                    {
                        "type": "IDS",
                        "desc": f"Serviço escutando: {conn.laddr.ip}:{conn.laddr.port}",
                    }
                )
        return alerts


class NetworkMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #181c24; color: #e0f7fa;")
        layout = QVBoxLayout(self)
        self.devices_label = QLabel("Dispositivos conectados:")
        self.devices_label.setStyleSheet("color: #ffd600; font-weight: bold;")
        layout.addWidget(self.devices_label)
        self.devices_list = QListWidget()
        self.devices_list.setStyleSheet("background-color: #222; color: #00e676;")
        layout.addWidget(self.devices_list)
        self.ips_label = QLabel("Alertas IPS:")
        self.ips_label.setStyleSheet("color: #ff1744; font-weight: bold;")
        layout.addWidget(self.ips_label)
        self.ips_list = QListWidget()
        self.ips_list.setStyleSheet("background-color: #222; color: #ff1744;")
        layout.addWidget(self.ips_list)
        self.ids_label = QLabel("Alertas IDS:")
        self.ids_label.setStyleSheet("color: #ffd600; font-weight: bold;")
        layout.addWidget(self.ids_label)
        self.ids_list = QListWidget()
        self.ids_list.setStyleSheet("background-color: #222; color: #ffd600;")
        layout.addWidget(self.ids_list)
        self.network_label = QLabel("Resumo da Rede:")
        self.network_label.setStyleSheet("color: #00e676; font-weight: bold;")
        layout.addWidget(self.network_label)
        self.network_text = QTextEdit()
        self.network_text.setReadOnly(True)
        self.network_text.setStyleSheet("background-color: #222; color: #b2ebf2;")
        layout.addWidget(self.network_text)
        self.setLayout(layout)

    def update_monitor(self, stats):
        self.devices_list.clear()
        for d in stats.get("devices", []):
            self.devices_list.addItem(
                f"Local: {d['local']} | Remoto: {d['remote']} | Status: {d['status']}"
            )
        self.ips_list.clear()
        for alert in stats.get("ips", []):
            self.ips_list.addItem(alert["desc"])
        self.ids_list.clear()
        for alert in stats.get("ids", []):
            self.ids_list.addItem(alert["desc"])
        self.network_text.setPlainText(
            json.dumps(stats.get("network", {}), indent=2, ensure_ascii=False)
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darks VPN - Futurista")
        self.setGeometry(100, 100, 1100, 700)
        self.setStyleSheet("background-color: #181c24; color: #e0f7fa;")
        self.config_path = None
        self.interface_name = None
        self.proxy_manager = ProxyManager()
        self.current_proxy = None
        self.selected_protocol = "WireGuard"
        self.init_db()
        self.init_ui()
        self.setup_logging()
        self.setup_menu()
        self.init_network_monitor()
        log_audit_event("Aplicação iniciada")

    def init_db(self):
        self.db = DBManager.create_and_populate_db()

    def init_ui(self):
        main_layout = QHBoxLayout()
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(180)
        self.sidebar.setStyleSheet(
            """QListWidget {background: #1a2332; color: #b2ebf2; border: none; font-size: 16px;} QListWidget::item:selected {background: #263859; color: #00e676;}"""
        )
        for name, icon in [
            ("Painel VPN", get_icon("vpn")),
            ("Proxies", get_icon("proxy")),
            ("Tor", get_icon("tor")),
            ("Usuários", get_icon("user")),
            ("Configurações", get_icon("settings")),
            ("Logs", get_icon("network")),
            (
                "Monitor de Rede",
                get_icon("network"),
            ),  # Adicionado item para o monitor de rede
        ]:
            item = QListWidgetItem(icon, name)
            self.sidebar.addItem(item)
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.change_panel)
        main_layout.addWidget(self.sidebar)
        # Painéis centrais
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_vpn_panel())
        self.stack.addWidget(self.create_proxy_panel())
        self.stack.addWidget(self.create_tor_panel())
        self.stack.addWidget(self.create_users_panel())
        self.stack.addWidget(self.create_settings_panel())
        self.stack.addWidget(self.create_logs_panel())
        self.stack.addWidget(
            self.create_network_dashboard()
        )  # Adicionado painel de rede
        main_layout.addWidget(self.stack)
        # Widget central
        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def change_panel(self, idx):
        self.stack.setCurrentIndex(idx)

    def create_vpn_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(24)
        # Status animado
        self.vpn_status_label = QLabel("Status: Desconectado")
        self.vpn_status_label.setAlignment(Qt.AlignCenter)
        self.vpn_status_label.setStyleSheet(
            """
            font-size: 24px;
            color: #00e6ff;
            font-family: "Segoe UI", "Consolas", monospace;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f2027, stop:1 #2c5364);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 10px;
        """
        )
        layout.addWidget(self.vpn_status_label)
        # Protocolo
        proto_layout = QHBoxLayout()
        proto_label = QLabel("Protocolo:")
        proto_label.setStyleSheet("font-size: 18px; color: #b2ebf2;")
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["WireGuard", "OpenVPN"])
        self.protocol_combo.setStyleSheet(
            """
            background: #222b3a;
            color: #00e6ff;
            font-size: 18px;
            border-radius: 8px;
            padding: 6px;
        """
        )
        self.protocol_combo.currentTextChanged.connect(self.set_protocol)
        proto_layout.addWidget(proto_label)
        proto_layout.addWidget(self.protocol_combo)
        proto_layout.addStretch()
        layout.addLayout(proto_layout)
        # IP e interface
        self.ip_label = QLabel("IP: ---")
        self.ip_label.setStyleSheet(
            "font-size: 18px; color: #b2ebf2; background: #181c24; border-radius: 8px; padding: 6px;"
        )
        layout.addWidget(self.ip_label)
        # Botões
        btn_layout = QHBoxLayout()
        self.vpn_connect_btn = QPushButton("Conectar")
        self.vpn_connect_btn.setIcon(get_icon("connect"))
        self.vpn_connect_btn.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00e6ff, stop:1 #2979ff);
                color: #181c24;
                font-weight: bold;
                border-radius: 12px;
                padding: 16px;
                font-size: 18px;
            }
            QPushButton:hover {
                background: #00b8d4;
                color: #fff;
            }
        """
        )
        self.vpn_connect_btn.clicked.connect(self.connect_vpn)
        btn_layout.addWidget(self.vpn_connect_btn)
        self.vpn_disconnect_btn = QPushButton("Desconectar")
        self.vpn_disconnect_btn.setIcon(get_icon("disconnect"))
        self.vpn_disconnect_btn.setStyleSheet(
            """
            QPushButton {
                background: #263859;
                color: #fff;
                font-weight: bold;
                border-radius: 12px;
                padding: 16px;
                font-size: 18px;
            }
            QPushButton:hover {
                background: #c0392b;
                color: #fff;
            }
        """
        )
        self.vpn_disconnect_btn.clicked.connect(self.disconnect_vpn)
        btn_layout.addWidget(self.vpn_disconnect_btn)
        layout.addLayout(btn_layout)
        # Configuração rápida
        config_btn = QPushButton("Configurações WireGuard")
        config_btn.setIcon(get_icon("settings"))
        config_btn.setStyleSheet(
            """
            QPushButton {
                background: #1a2332;
                color: #00b8d4;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #263859;
                color: #fff;
            }
        """
        )
        config_btn.clicked.connect(self.open_wg_settings)
        layout.addWidget(config_btn)
        # Botão de configurações OpenVPN
        config_ovpn_btn = QPushButton("Configurações OpenVPN")
        config_ovpn_btn.setIcon(get_icon("settings"))
        config_ovpn_btn.setStyleSheet(
            """
            QPushButton {
                background: #1a2332;
                color: #ff9100;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #263859;
                color: #fff;
            }
        """
        )
        config_ovpn_btn.clicked.connect(self.open_ovpn_settings)
        layout.addWidget(config_ovpn_btn)
        panel.setLayout(layout)
        return panel

    def create_proxy_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(24)
        # Status
        self.proxy_status_label = QLabel("Proxy: Nenhum")
        self.proxy_status_label.setAlignment(Qt.AlignCenter)
        self.proxy_status_label.setStyleSheet(
            """
            font-size: 20px;
            color: #2979ff;
            font-family: "Segoe UI", "Consolas", monospace;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #232526, stop:1 #414345);
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
        """
        )
        layout.addWidget(self.proxy_status_label)
        # Botões
        btn_layout = QHBoxLayout()
        self.proxy_generate_btn = QPushButton("Gerar Proxy Aleatório")
        self.proxy_generate_btn.setIcon(get_icon("proxy"))
        self.proxy_generate_btn.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2979ff, stop:1 #00e6ff);
                color: #fff;
                border-radius: 10px;
                padding: 14px;
                font-size: 17px;
            }
            QPushButton:hover {
                background: #00b8d4;
                color: #fff;
            }
        """
        )
        self.proxy_generate_btn.clicked.connect(self.generate_proxy)
        btn_layout.addWidget(self.proxy_generate_btn)
        self.proxy_multi_btn = QPushButton("Ativar Multi-Hop")
        self.proxy_multi_btn.setIcon(get_icon("proxy_on"))
        self.proxy_multi_btn.setStyleSheet(
            """
            QPushButton {
                background: #263859;
                color: #00e676;
                border-radius: 10px;
                padding: 14px;
                font-size: 17px;
            }
            QPushButton:hover {
                background: #2979ff;
                color: #fff;
            }
        """
        )
        self.proxy_multi_btn.clicked.connect(self.toggle_multi_hop)
        btn_layout.addWidget(self.proxy_multi_btn)
        layout.addLayout(btn_layout)
        # Lista de proxies ativos
        self.proxy_list = QListWidget()
        self.proxy_list.setStyleSheet("background-color: #222; color: #00e676;")
        layout.addWidget(self.proxy_list)
        panel.setLayout(layout)
        return panel

    def create_tor_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(24)
        # Status
        self.tor_status_label = QLabel("Tor: Desativado")
        self.tor_status_label.setAlignment(Qt.AlignCenter)
        self.tor_status_label.setStyleSheet(
            """
            font-size: 20px;
            color: #00b8d4;
            font-family: "Segoe UI", "Consolas", monospace;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #232526, stop:1 #414345);
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
        """
        )
        layout.addWidget(self.tor_status_label)
        # Botão ativar/desativar
        self.tor_toggle_btn = QPushButton("Ativar Tor")
        self.tor_toggle_btn.setIcon(get_icon("tor"))
        self.tor_toggle_btn.setStyleSheet(
            """
            QPushButton {
                background: #263859;
                color: #00e676;
                border-radius: 10px;
                padding: 14px;
                font-size: 17px;
            }
            QPushButton:hover {
                background: #2979ff;
                color: #fff;
            }
        """
        )
        self.tor_toggle_btn.clicked.connect(self.toggle_tor)
        layout.addWidget(self.tor_toggle_btn)
        # Botão de configurações avançadas do Tor
        self.tor_settings_btn = QPushButton("Configurações Tor")
        self.tor_settings_btn.setIcon(get_icon("settings"))
        self.tor_settings_btn.setStyleSheet(
            """
            QPushButton {
                background: #1a2332;
                color: #ffab40;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #263859;
                color: #fff;
            }
        """
        )
        self.tor_settings_btn.clicked.connect(self.open_tor_settings)
        layout.addWidget(self.tor_settings_btn)
        # Logs do Tor
        self.tor_log = QTextEdit()
        self.tor_log.setReadOnly(True)
        self.tor_log.setStyleSheet(
            """
            background: #111;
            color: #00e6ff;
            font-family: monospace;
            border-radius: 8px;
            font-size: 15px;
        """
        )
        self.tor_log.setFixedHeight(120)
        layout.addWidget(self.tor_log)
        panel.setLayout(layout)
        return panel

    def open_tor_settings(self):
        from gui.privacy_config import load_config, save_config

        config = load_config()
        dialog = QDialog(self)
        dialog.setWindowTitle("Configurações Avançadas do Tor")
        layout = QFormLayout(dialog)
        tor_enabled_cb = QCheckBox("Ativar integração com Tor")
        tor_enabled_cb.setChecked(config.get("tor_enabled", False))
        layout.addRow(tor_enabled_cb)
        save_btn = QPushButton("Salvar")

        def save_tor():
            try:
                config["tor_enabled"] = tor_enabled_cb.isChecked()
                save_config(config)
                logging.info("Configurações Tor salvas.")
                self.show_feedback("Configurações", "Configurações Tor salvas!", success=True)
                dialog.accept()
            except Exception as e:
                self.show_feedback("Erro", "Falha ao salvar configurações Tor.", str(e), success=False)

        save_btn.clicked.connect(save_tor)
        layout.addRow(save_btn)
        dialog.setLayout(layout)
        dialog.exec_()

    def create_logs_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(18)
        title = QLabel("Logs e Atividades em Tempo Real")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            """
            font-size: 22px;
            color: #ffd600;
            font-family: "Segoe UI", "Consolas", monospace;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #232526, stop:1 #414345);
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
        """
        )
        layout.addWidget(title)
        self.realtime_log = QTextEdit()
        self.realtime_log.setReadOnly(True)
        self.realtime_log.setStyleSheet(
            "background: #111; color: #ffd600; font-family: monospace; border-radius: 8px; font-size: 15px;"
        )
        layout.addWidget(self.realtime_log)
        panel.setLayout(layout)
        # Handler de log para atualizar em tempo real
        handler = LogHandler(self.realtime_log)
        logging.getLogger().addHandler(handler)
        return panel

    def create_network_dashboard(self):
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        import matplotlib.pyplot as plt
        import numpy as np
        from gui.network_monitor_helpers import (
            update_traffic_history,
            get_network_stats,
            get_vpn_status,
            get_tor_status,
            get_proxy_status,
            get_connections,
        )

        panel = QWidget()
        layout = QVBoxLayout()
        title = QLabel("Monitor de Rede")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            """
            font-size: 22px;
            color: #00b8d4;
            font-family: "Segoe UI", "Consolas", monospace;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #232526, stop:1 #414345);
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
        """
        )
        layout.addWidget(title)
        # Gráfico animado de tráfego
        self.fig, self.ax = plt.subplots(facecolor="#181c24")
        self.canvas = FigureCanvas(self.fig)
        self.ax.set_facecolor("#181c24")
        self.ax.tick_params(colors="#b2ebf2")
        self.ax.spines["bottom"].set_color("#00e676")
        self.ax.spines["top"].set_color("#00e676")
        self.ax.spines["right"].set_color("#00e676")
        self.ax.spines["left"].set_color("#00e676")
        (self.traffic_sent,) = self.ax.plot(
            [0] * 60, color="#00e676", linewidth=2, label="Enviados (KB/s)"
        )
        (self.traffic_recv,) = self.ax.plot(
            [0] * 60, color="#2979ff", linewidth=2, label="Recebidos (KB/s)"
        )
        self.ax.set_ylim(0, 100 * 1024)
        self.ax.set_title("Tráfego de Rede", color="#b2ebf2")
        self.ax.legend(facecolor="#181c24", edgecolor="#00e676", labelcolor="#b2ebf2")
        layout.addWidget(self.canvas)
        # Gráfico de conexões
        self.conn_fig, self.conn_ax = plt.subplots(facecolor="#181c24")
        self.conn_canvas = FigureCanvas(self.conn_fig)
        self.conn_ax.set_facecolor("#181c24")
        self.conn_ax.tick_params(colors="#b2ebf2")
        self.conn_ax.set_title("Conexões Ativas", color="#b2ebf2")
        layout.addWidget(self.conn_canvas)
        # Gráfico de interfaces de rede
        self.if_fig, self.if_ax = plt.subplots(facecolor="#181c24")
        self.if_canvas = FigureCanvas(self.if_fig)
        self.if_ax.set_facecolor("#181c24")
        self.if_ax.tick_params(colors="#b2ebf2")
        self.if_ax.set_title("Uso das Interfaces", color="#b2ebf2")
        layout.addWidget(self.if_canvas)
        # Status VPN, Tor, Proxy
        status_layout = QHBoxLayout()
        self.vpn_status = QLabel("VPN: ---")
        self.vpn_status.setStyleSheet(
            "font-size: 16px; color: #00e676; background: #181c24; border-radius: 8px; padding: 8px;"
        )
        status_layout.addWidget(self.vpn_status)
        self.tor_status = QLabel("Tor: ---")
        self.tor_status.setStyleSheet(
            "font-size: 16px; color: #00b8d4; background: #181c24; border-radius: 8px; padding: 8px;"
        )
        status_layout.addWidget(self.tor_status)
        self.proxy_status = QLabel("Proxy: ---")
        self.proxy_status.setStyleSheet(
            "font-size: 16px; color: #2979ff; background: #181c24; border-radius: 8px; padding: 8px;"
        )
        status_layout.addWidget(self.proxy_status)
        layout.addLayout(status_layout)
        # Atualização animada
        self.dashboard_timer = QTimer()

        def update_dashboard():
            # Tráfego
            t, sent, recv = update_traffic_history()
            self.traffic_sent.set_ydata(sent + [0] * (60 - len(sent)))
            self.traffic_recv.set_ydata(recv + [0] * (60 - len(recv)))
            self.canvas.draw()
            # Conexões
            conns = get_connections()
            types = [c["type"] for c in conns]
            self.conn_ax.clear()
            self.conn_ax.set_facecolor("#181c24")
            self.conn_ax.set_title("Conexões Ativas", color="#b2ebf2")
            self.conn_ax.hist(types, bins=[0, 1, 2], color="#00e676", rwidth=0.8)
            self.conn_canvas.draw()
            # Interfaces de rede
            stats = get_network_stats()
            self.if_ax.clear()
            self.if_ax.set_facecolor("#181c24")
            self.if_ax.set_title("Uso das Interfaces", color="#b2ebf2")
            names = list(stats.keys())
            speeds = [stats[n]["speed"] for n in names]
            up = [stats[n]["bytes_sent"] for n in names]
            down = [stats[n]["bytes_recv"] for n in names]
            x = np.arange(len(names))
            self.if_ax.bar(x - 0.2, up, width=0.4, color="#00e676", label="Enviados")
            self.if_ax.bar(x + 0.2, down, width=0.4, color="#2979ff", label="Recebidos")
            self.if_ax.set_xticks(x)
            self.if_ax.set_xticklabels(names, rotation=30, color="#b2ebf2")
            self.if_ax.legend(
                facecolor="#181c24", edgecolor="#00e676", labelcolor="#b2ebf2"
            )
            self.if_canvas.draw()
            # Status
            vpn, iface = get_vpn_status()
            self.vpn_status.setText(
                f'VPN: {"Ativa" if vpn else "Inativa"} {iface or ""}'
            )
            self.tor_status.setText(
                f'Tor: {"Ativo" if get_tor_status() else "Inativo"}'
            )
            self.proxy_status.setText(
                f'Proxy: {"Ativo" if get_proxy_status() else "Inativo"}'
            )

        self.dashboard_timer.timeout.connect(update_dashboard)
        self.dashboard_timer.start(1000)
        panel.setLayout(layout)
        return panel

    def _placeholder_panel(self, text):
        w = QWidget()
        l = QVBoxLayout()
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 22px; color: #b2ebf2;")
        l.addWidget(lbl)
        w.setLayout(l)
        return w

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        handler = LogHandler(self.log_widget)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)

    def setup_menu(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Ajuda")
        about_action = QAction("Sobre", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        export_config_action = QAction("Exportar Configuração", self)
        export_config_action.triggered.connect(self.export_config)
        help_menu.addAction(export_config_action)
        import_config_action = QAction("Importar Configuração", self)
        import_config_action.triggered.connect(self.import_config)
        help_menu.addAction(import_config_action)
        export_users_action = QAction("Exportar Usuários", self)
        export_users_action.triggered.connect(self.export_users)
        help_menu.addAction(export_users_action)
        import_users_action = QAction("Importar Usuários", self)
        import_users_action.triggered.connect(self.import_users)
        help_menu.addAction(import_users_action)
        export_logs_action = QAction("Exportar Logs", self)
        export_logs_action.triggered.connect(self.export_logs)
        help_menu.addAction(export_logs_action)
        reset_action = QAction("Resetar Sistema", self)
        reset_action.triggered.connect(self.reset_all)
        help_menu.addAction(reset_action)
        proxy_menu = menubar.addMenu("Proxy")
        custom_proxy_action = QAction("Criar ProxyChain Personalizado", self)
        custom_proxy_action.triggered.connect(self.open_proxy_chain_dialog)
        proxy_menu.addAction(custom_proxy_action)
        proxychain_action = QAction("Testar ProxyChain", self)
        proxychain_action.triggered.connect(self.open_proxy_chain_dialog)
        help_menu.addAction(proxychain_action)
        update_proxies_action = QAction("Atualizar Proxies Reais", self)
        update_proxies_action.triggered.connect(self.update_proxies_from_scraper_action)
        help_menu.addAction(update_proxies_action)

    def show_about(self):
        QMessageBox.information(
            self, "Sobre", "VPN Python WireGuard\nVersão 1.0\nDesenvolvido por SeuNome"
        )

    def closeEvent(self, event):
        logging.info("Aplicação finalizada.")
        event.accept()

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        err = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logging.error(f"Exceção não tratada: {err}")
        QMessageBox.critical(
            self,
            "Erro Crítico",
            "Ocorreu um erro inesperado. Veja app.log para detalhes.",
        )

    def select_config(self):
        QMessageBox.information(
            self,
            "Configuração",
            "Agora a configuração é feita pelo menu Configurações WireGuard.",
        )

    def get_interface_name(self, config_path):
        # Nome da interface = nome do arquivo sem extensão
        return os.path.splitext(os.path.basename(config_path))[0]

    def set_protocol(self, protocol):
        self.selected_protocol = protocol

    def connect_vpn(self):
        config = load_config()
        if not self.config_path:
            self.show_feedback('Atenção', 'Selecione um arquivo de configuração primeiro!', success=False)
            return
        try:
            if self.selected_protocol == "WireGuard":
                if platform.system() == "Windows" and not os.path.exists("C:/Program Files/WireGuard/wg.exe"):
                    self.show_feedback('Erro', 'WireGuard não está instalado no Windows!', success=False)
                    return
                set_secure_dns()
                enable_kill_switch()
                start_tor()
                ok, msg = WireGuardManager.start_tunnel(self.config_path)
                if ok:
                    self.show_feedback('VPN', 'Conectado com sucesso!', msg, success=True)
                else:
                    self.show_feedback('Erro VPN', 'Falha ao conectar WireGuard.', msg, success=False)
                self.status_label.setText("Status: Conectado" if ok else f"Erro: {msg}")
            elif self.selected_protocol == "OpenVPN":
                ok, msg = OpenVPNManager.start_tunnel(self.config_path)
                if ok:
                    self.show_feedback('VPN', 'Conectado com sucesso (OpenVPN)!', msg, success=True)
                else:
                    self.show_feedback('Erro VPN', 'Falha ao conectar OpenVPN.', msg, success=False)
                self.status_label.setText("Status: Conectado (OpenVPN)" if ok else f"Erro: {msg}")
        except Exception as e:
            self.show_feedback('Erro Crítico', 'Erro inesperado ao conectar VPN.', str(e), success=False)

    def disconnect_vpn(self):
        if not self.config_path:
            self.show_feedback('Atenção', 'Selecione um arquivo de configuração primeiro!', success=False)
            return
        try:
            if self.selected_protocol == "WireGuard":
                disable_kill_switch()
                ok, msg = WireGuardManager.stop_tunnel(self.config_path)
                if ok:
                    self.show_feedback('VPN', 'Desconectado com sucesso!', msg, success=True)
                else:
                    self.show_feedback('Erro VPN', 'Falha ao desconectar WireGuard.', msg, success=False)
                self.status_label.setText("Status: Desconectado" if ok else f"Erro: {msg}")
            elif self.selected_protocol == "OpenVPN":
                ok, msg = OpenVPNManager.stop_tunnel()
                if ok:
                    self.show_feedback('VPN', 'Desconectado com sucesso (OpenVPN)!', msg, success=True)
                else:
                    self.show_feedback('Erro VPN', 'Falha ao desconectar OpenVPN.', msg, success=False)
                self.status_label.setText("Status: Desconectado (OpenVPN)" if ok else f"Erro: {msg}")
        except Exception as e:
            self.show_feedback('Erro Crítico', 'Erro inesperado ao desconectar VPN.', str(e), success=False)

    def generate_proxy(self):
        config = load_config()
        if not hasattr(self.proxy_manager, "start_random_proxy"):
            self.show_feedback('Erro', 'ProxyManager não implementa proxy real. Função placeholder.', success=False)
            return
        try:
            if config.get("multi_hop", False):
                proxies = self.proxy_manager.start_multi_hop(hops=2)
                for p in proxies:
                    errors = validate_proxy_config(p)
                    if errors:
                        self.show_feedback('Erro de Validação', 'Proxy inválido.', "\n".join(errors), success=False)
                        return
                self.current_proxy = proxies
                msg = "\n".join([
                    f"Proxy: {p['host']}:{p['port']} ({p.get('country','')})" for p in proxies
                ])
                self.proxy_label.setText(f"Multi-Hop: {msg}")
                logging.info(f"Proxies multi-hop gerados: {msg}")
                self.show_feedback('Proxies Multi-Hop', 'Proxies multi-hop gerados com sucesso!', msg, success=True)
            else:
                proxy = self.proxy_manager.start_random_proxy()
                errors = validate_proxy_config(proxy)
                if errors:
                    self.show_feedback('Erro de Validação', 'Proxy inválido.', "\n".join(errors), success=False)
                    return
                self.current_proxy = proxy
                self.proxy_label.setText(
                    f"Proxy: {proxy['host']}:{proxy['port']} ({proxy.get('country','')})"
                )
                logging.info(f"Proxy gerado: {proxy}")
                self.show_feedback('Proxy Gerado', 'Proxy SOCKS5 rodando!', f"{proxy['host']}:{proxy['port']} ({proxy.get('country','')})", success=True)
        except Exception as e:
            logging.error(f"Erro ao gerar proxy: {e}")
            self.show_feedback('Erro', 'Falha ao gerar proxy.', str(e), success=False)

    def open_api_panel(self):
        dlg = ApiDialog(self)
        dlg.exec_()

    def list_users(self):
        dlg = UserDialog(self)
        dlg.exec_()

    def add_user(self):
        usuario, ok = QInputDialog.getText(self, "Novo Usuário", "Nome do usuário:")
        if ok and usuario:
            user = {
                "usuario": usuario,
                "vpn_status": "desconectado",
                "proxy_host": "127.0.0.1",
                "proxy_port": 50000,
                "tipo_proxy": "SOCKS5",
            }
            errors = DBManager.validate_user(user)
            if errors:
                self.show_feedback("Erro de Validação", "Dados inválidos para usuário.", "\n".join(errors), success=False)
                return
            try:
                df = DBManager.add_user(usuario, "desconectado", "127.0.0.1", 50000, "SOCKS5")
                logging.info(f"Usuário adicionado: {usuario}")
                self.show_feedback("Usuário Adicionado", f"Usuário {usuario} adicionado com sucesso!", success=True)
                log_audit_event(f"Usuário adicionado: {usuario}")
            except Exception as e:
                self.show_feedback("Erro", "Falha ao adicionar usuário.", str(e), success=False)

    def remove_user(self):
        user_id, ok = QInputDialog.getInt(self, "Remover Usuário", "ID do usuário:")
        if ok:
            if user_id <= 0:
                self.show_feedback("Erro", "ID inválido!", success=False)
                return
            try:
                df = DBManager.remove_user(user_id)
                logging.info(f"Usuário removido: {user_id}")
                self.show_feedback("Usuário Removido", f"Usuário ID {user_id} removido.", success=True)
                log_audit_event(f"Usuário removido: {user_id}")
            except Exception as e:
                self.show_feedback("Erro", "Falha ao remover usuário.", str(e), success=False)

    def edit_user(self):
        user_id, ok = QInputDialog.getInt(self, "Editar Usuário", "ID do usuário:")
        if not ok or user_id <= 0:
            self.show_feedback("Erro", "ID inválido!", success=False)
            return
        usuario, ok1 = QInputDialog.getText(self, "Editar Usuário", "Novo nome (deixe vazio para não alterar):")
        status, ok2 = QInputDialog.getText(self, "Editar Usuário", "Novo status (conectado/desconectado):")
        host, ok3 = QInputDialog.getText(self, "Editar Usuário", "Novo host (deixe vazio para não alterar):")
        port, ok4 = QInputDialog.getInt(self, "Editar Usuário", "Nova porta (0 para não alterar):")
        tipo, ok5 = QInputDialog.getText(self, "Editar Usuário", "Novo tipo de proxy (deixe vazio para não alterar):")
        if any([ok1, ok2, ok3, ok4, ok5]):
            port_val = port if port != 0 else None
            user = {
                "usuario": usuario or "user",
                "vpn_status": status or "desconectado",
                "proxy_host": host or "127.0.0.1",
                "proxy_port": port_val or 50000,
                "tipo_proxy": tipo or "SOCKS5",
            }
            errors = DBManager.validate_user(user)
            if errors:
                self.show_feedback("Erro de Validação", "Dados inválidos para usuário.", "\n".join(errors), success=False)
                return
            try:
                df = DBManager.edit_user(
                    user_id,
                    usuario or None,
                    status or None,
                    host or None,
                    port_val,
                    tipo or None,
                )
                logging.info(f"Usuário editado: {user_id}")
                self.show_feedback("Usuário Editado", f"Usuário ID {user_id} editado.", success=True)
            except Exception as e:
                self.show_feedback("Erro", "Falha ao editar usuário.", str(e), success=False)

    def export_config(self):
        from gui.privacy_config import export_encrypted_config
        path, _ = QFileDialog.getSaveFileName(self, 'Exportar Configuração', '', 'Arquivo Criptografado (*.enc)')
        if path:
            try:
                if export_encrypted_config(path):
                    self.show_feedback('Exportação', 'Configuração exportada com sucesso!', success=True)
                else:
                    self.show_feedback('Exportação', 'Falha ao exportar configuração.', success=False)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao exportar configuração.', str(e), success=False)

    def import_config(self):
        from gui.privacy_config import import_encrypted_config
        path, _ = QFileDialog.getOpenFileName(self, 'Importar Configuração', '', 'Arquivo Criptografado (*.enc)')
        if path:
            try:
                if import_encrypted_config(path):
                    self.show_feedback('Importação', 'Configuração importada e validada com sucesso!', success=True)
                else:
                    self.show_feedback('Importação', 'Falha ao importar ou validar configuração.', success=False)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao importar configuração.', str(e), success=False)

    def export_users(self):
        from gui.db_manager import save_encrypted_db, DBManager
        path, _ = QFileDialog.getSaveFileName(self, 'Exportar Usuários', '', 'Banco Criptografado (*.enc)')
        if path:
            try:
                df = DBManager.load_db()
                save_encrypted_db(df)
                self.show_feedback('Exportação', 'Usuários exportados com sucesso!', success=True)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao exportar usuários.', str(e), success=False)

    def import_users(self):
        from gui.db_manager import import_encrypted_db
        path, _ = QFileDialog.getOpenFileName(self, 'Importar Usuários', '', 'Banco Criptografado (*.enc)')
        if path:
            try:
                if import_encrypted_db(path):
                    self.show_feedback('Importação', 'Usuários importados e validados com sucesso!', success=True)
                else:
                    self.show_feedback('Importação', 'Falha ao importar ou validar usuários.', success=False)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao importar usuários.', str(e), success=False)

    def export_logs(self):
        from gui.audit_log import log_audit_event
        path, _ = QFileDialog.getSaveFileName(self, 'Exportar Logs', '', 'Logs Criptografados (*.enc)')
        if path:
            try:
                # Simplesmente copia o arquivo de log criptografado
                import shutil
                log_path = os.path.join(os.path.dirname(__file__), 'audit.log.enc')
                shutil.copy(log_path, path)
                self.show_feedback('Exportação', 'Logs exportados com sucesso!', success=True)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao exportar logs.', str(e), success=False)

    def reset_all(self):
        from gui.privacy_config import reset_config
        try:
            reset_config()
            self.show_feedback('Reset', 'Sistema resetado para o padrão!', success=True)
        except Exception as e:
            self.show_feedback('Erro', 'Erro ao resetar sistema.', str(e), success=False)

    def open_key_manager(self):
        from gui.privacy_config import KEY_PATH

        log_audit_event("Acesso ao gerenciamento de chave de criptografia")
        dlg = KeyManagerDialog(KEY_PATH, self)
        dlg.exec_()

    def open_config_backup(self):
        log_audit_event("Acesso ao backup/restauração de configuração")
        dlg = ConfigBackupDialog(self)
        dlg.exec_()

    def open_db_backup(self):
        log_audit_event("Acesso ao backup/restauração do banco de dados")
        dlg = DBBackupDialog(self)
        dlg.exec_()

    def open_audit_logs(self):
        log_audit_event("Acesso aos logs de auditoria")
        dlg = AuditLogDialog(self)
        dlg.exec_()

    def toggle_tor(self):
        from gui.privacy_config import load_config, save_config

        config = load_config()
        tor_enabled = config.get("tor_enabled", False)
        config["tor_enabled"] = not tor_enabled
        save_config(config)
        if config["tor_enabled"]:
            from gui.tor_integration import start_tor

            start_tor()
            self.tor_status_label.setText("Tor: Ativado")
            self.tor_toggle_btn.setText("Desativar Tor")
            self.tor_toggle_btn.setIcon(get_icon("tor_on"))
        else:
            self.tor_status_label.setText("Tor: Desativado")
            self.tor_toggle_btn.setText("Ativar Tor")
            self.tor_toggle_btn.setIcon(get_icon("tor_off"))

    def open_proxy_chain_dialog(self):
        dialog = ProxyDialog(self)
        dialog.exec_()

    def update_proxies_from_scraper_action(self):
        try:
            update_proxies_from_scraper()
            QMessageBox.information(self, "Proxies", "Proxies atualizados com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar proxies: {e}")

    def init_network_monitor(self):
        # Inicialização básica do monitor de rede (pode ser expandido conforme necessário)
        pass

    def toggle_multi_hop(self):
        config = load_config()
        multi_hop_enabled = config.get("multi_hop", False)
        config["multi_hop"] = not multi_hop_enabled
        save_config(config)
        if config["multi_hop"]:
            self.proxy_multi_btn.setText("Desativar Multi-Hop")
            self.proxy_multi_btn.setIcon(get_icon("proxy_off"))
            QMessageBox.information(self, "Multi-Hop", "Multi-Hop ativado.")
        else:
            self.proxy_multi_btn.setText("Ativar Multi-Hop")
            self.proxy_multi_btn.setIcon(get_icon("proxy_on"))
            QMessageBox.information(self, "Multi-Hop", "Multi-Hop desativado.")

class FeedbackPanel(QDialog):
    def __init__(self, title, message, details=None, success=True, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet(
            f"background-color: {'#263238' if success else '#c0392b'}; color: #f5f6fa; border-radius: 12px;"
        )
        layout = QVBoxLayout(self)
        label = QLabel(message)
        label.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(label)
        if details:
            details_box = QTextEdit()
            details_box.setReadOnly(True)
            details_box.setPlainText(details)
            details_box.setStyleSheet('background: #181c24; color: #ffd600; border-radius: 8px;')
            layout.addWidget(details_box)
        btn = QPushButton('OK')
        btn.clicked.connect(self.accept)
        btn.setStyleSheet('background: #00e676; color: #181c24; border-radius: 8px; padding: 8px;')
        layout.addWidget(btn)
        self.setLayout(layout)

    def show_feedback(self, title, message, details=None, success=True):
        dlg = FeedbackPanel(title, message, details, success, self)
        dlg.exec_()

    # Exemplo de uso nos métodos críticos:
    def connect_vpn(self):
        config = load_config()
        if not self.config_path:
            self.show_feedback('Atenção', 'Selecione um arquivo de configuração primeiro!', success=False)
            return
        try:
            if self.selected_protocol == "WireGuard":
                if platform.system() == "Windows" and not os.path.exists("C:/Program Files/WireGuard/wg.exe"):
                    self.show_feedback('Erro', 'WireGuard não está instalado no Windows!', success=False)
                    return
                set_secure_dns()
                enable_kill_switch()
                start_tor()
                ok, msg = WireGuardManager.start_tunnel(self.config_path)
                if ok:
                    self.show_feedback('VPN', 'Conectado com sucesso!', msg, success=True)
                else:
                    self.show_feedback('Erro VPN', 'Falha ao conectar WireGuard.', msg, success=False)
                self.status_label.setText("Status: Conectado" if ok else f"Erro: {msg}")
            elif self.selected_protocol == "OpenVPN":
                ok, msg = OpenVPNManager.start_tunnel(self.config_path)
                if ok:
                    self.show_feedback('VPN', 'Conectado com sucesso (OpenVPN)!', msg, success=True)
                else:
                    self.show_feedback('Erro VPN', 'Falha ao conectar OpenVPN.', msg, success=False)
                self.status_label.setText("Status: Conectado (OpenVPN)" if ok else f"Erro: {msg}")
        except Exception as e:
            self.show_feedback('Erro Crítico', 'Erro inesperado ao conectar VPN.', str(e), success=False)

    def disconnect_vpn(self):
        if not self.config_path:
            self.show_feedback('Atenção', 'Selecione um arquivo de configuração primeiro!', success=False)
            return
        try:
            if self.selected_protocol == "WireGuard":
                disable_kill_switch()
                ok, msg = WireGuardManager.stop_tunnel(self.config_path)
                if ok:
                    self.show_feedback('VPN', 'Desconectado com sucesso!', msg, success=True)
                else:
                    self.show_feedback('Erro VPN', 'Falha ao desconectar WireGuard.', msg, success=False)
                self.status_label.setText("Status: Desconectado" if ok else f"Erro: {msg}")
            elif self.selected_protocol == "OpenVPN":
                ok, msg = OpenVPNManager.stop_tunnel()
                if ok:
                    self.show_feedback('VPN', 'Desconectado com sucesso (OpenVPN)!', msg, success=True)
                else:
                    self.show_feedback('Erro VPN', 'Falha ao desconectar OpenVPN.', msg, success=False)
                self.status_label.setText("Status: Desconectado (OpenVPN)" if ok else f"Erro: {msg}")
        except Exception as e:
            self.show_feedback('Erro Crítico', 'Erro inesperado ao desconectar VPN.', str(e), success=False)

    def generate_proxy(self):
        config = load_config()
        if not hasattr(self.proxy_manager, "start_random_proxy"):
            self.show_feedback('Erro', 'ProxyManager não implementa proxy real. Função placeholder.', success=False)
            return
        try:
            if config.get("multi_hop", False):
                proxies = self.proxy_manager.start_multi_hop(hops=2)
                for p in proxies:
                    errors = validate_proxy_config(p)
                    if errors:
                        self.show_feedback('Erro de Validação', 'Proxy inválido.', "\n".join(errors), success=False)
                        return
                self.current_proxy = proxies
                msg = "\n".join([
                    f"Proxy: {p['host']}:{p['port']} ({p.get('country','')})" for p in proxies
                ])
                self.proxy_label.setText(f"Multi-Hop: {msg}")
                logging.info(f"Proxies multi-hop gerados: {msg}")
                self.show_feedback('Proxies Multi-Hop', 'Proxies multi-hop gerados com sucesso!', msg, success=True)
            else:
                proxy = self.proxy_manager.start_random_proxy()
                errors = validate_proxy_config(proxy)
                if errors:
                    self.show_feedback('Erro de Validação', 'Proxy inválido.', "\n".join(errors), success=False)
                    return
                self.current_proxy = proxy
                self.proxy_label.setText(
                    f"Proxy: {proxy['host']}:{proxy['port']} ({proxy.get('country','')})"
                )
                logging.info(f"Proxy gerado: {proxy}")
                self.show_feedback('Proxy Gerado', 'Proxy SOCKS5 rodando!', f"{proxy['host']}:{proxy['port']} ({proxy.get('country','')})", success=True)
        except Exception as e:
            logging.error(f"Erro ao gerar proxy: {e}")
            self.show_feedback('Erro', 'Falha ao gerar proxy.', str(e), success=False)

    def open_api_panel(self):
        dlg = ApiDialog(self)
        dlg.exec_()

    def list_users(self):
        dlg = UserDialog(self)
        dlg.exec_()

    def add_user(self):
        usuario, ok = QInputDialog.getText(self, "Novo Usuário", "Nome do usuário:")
        if ok and usuario:
            user = {
                "usuario": usuario,
                "vpn_status": "desconectado",
                "proxy_host": "127.0.0.1",
                "proxy_port": 50000,
                "tipo_proxy": "SOCKS5",
            }
            errors = DBManager.validate_user(user)
            if errors:
                self.show_feedback("Erro de Validação", "Dados inválidos para usuário.", "\n".join(errors), success=False)
                return
            try:
                df = DBManager.add_user(usuario, "desconectado", "127.0.0.1", 50000, "SOCKS5")
                logging.info(f"Usuário adicionado: {usuario}")
                self.show_feedback("Usuário Adicionado", f"Usuário {usuario} adicionado com sucesso!", success=True)
                log_audit_event(f"Usuário adicionado: {usuario}")
            except Exception as e:
                self.show_feedback("Erro", "Falha ao adicionar usuário.", str(e), success=False)

    def remove_user(self):
        user_id, ok = QInputDialog.getInt(self, "Remover Usuário", "ID do usuário:")
        if ok:
            if user_id <= 0:
                self.show_feedback("Erro", "ID inválido!", success=False)
                return
            try:
                df = DBManager.remove_user(user_id)
                logging.info(f"Usuário removido: {user_id}")
                self.show_feedback("Usuário Removido", f"Usuário ID {user_id} removido.", success=True)
                log_audit_event(f"Usuário removido: {user_id}")
            except Exception as e:
                self.show_feedback("Erro", "Falha ao remover usuário.", str(e), success=False)

    def edit_user(self):
        user_id, ok = QInputDialog.getInt(self, "Editar Usuário", "ID do usuário:")
        if not ok or user_id <= 0:
            self.show_feedback("Erro", "ID inválido!", success=False)
            return
        usuario, ok1 = QInputDialog.getText(self, "Editar Usuário", "Novo nome (deixe vazio para não alterar):")
        status, ok2 = QInputDialog.getText(self, "Editar Usuário", "Novo status (conectado/desconectado):")
        host, ok3 = QInputDialog.getText(self, "Editar Usuário", "Novo host (deixe vazio para não alterar):")
        port, ok4 = QInputDialog.getInt(self, "Editar Usuário", "Nova porta (0 para não alterar):")
        tipo, ok5 = QInputDialog.getText(self, "Editar Usuário", "Novo tipo de proxy (deixe vazio para não alterar):")
        if any([ok1, ok2, ok3, ok4, ok5]):
            port_val = port if port != 0 else None
            user = {
                "usuario": usuario or "user",
                "vpn_status": status or "desconectado",
                "proxy_host": host or "127.0.0.1",
                "proxy_port": port_val or 50000,
                "tipo_proxy": tipo or "SOCKS5",
            }
            errors = DBManager.validate_user(user)
            if errors:
                self.show_feedback("Erro de Validação", "Dados inválidos para usuário.", "\n".join(errors), success=False)
                return
            try:
                df = DBManager.edit_user(
                    user_id,
                    usuario or None,
                    status or None,
                    host or None,
                    port_val,
                    tipo or None,
                )
                logging.info(f"Usuário editado: {user_id}")
                self.show_feedback("Usuário Editado", f"Usuário ID {user_id} editado.", success=True)
            except Exception as e:
                self.show_feedback("Erro", "Falha ao editar usuário.", str(e), success=False)

    def export_config(self):
        from gui.privacy_config import export_encrypted_config
        path, _ = QFileDialog.getSaveFileName(self, 'Exportar Configuração', '', 'Arquivo Criptografado (*.enc)')
        if path:
            try:
                if export_encrypted_config(path):
                    self.show_feedback('Exportação', 'Configuração exportada com sucesso!', success=True)
                else:
                    self.show_feedback('Exportação', 'Falha ao exportar configuração.', success=False)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao exportar configuração.', str(e), success=False)

    def import_config(self):
        from gui.privacy_config import import_encrypted_config
        path, _ = QFileDialog.getOpenFileName(self, 'Importar Configuração', '', 'Arquivo Criptografado (*.enc)')
        if path:
            try:
                if import_encrypted_config(path):
                    self.show_feedback('Importação', 'Configuração importada e validada com sucesso!', success=True)
                else:
                    self.show_feedback('Importação', 'Falha ao importar ou validar configuração.', success=False)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao importar configuração.', str(e), success=False)

    def export_users(self):
        from gui.db_manager import save_encrypted_db, DBManager
        path, _ = QFileDialog.getSaveFileName(self, 'Exportar Usuários', '', 'Banco Criptografado (*.enc)')
        if path:
            try:
                df = DBManager.load_db()
                save_encrypted_db(df)
                self.show_feedback('Exportação', 'Usuários exportados com sucesso!', success=True)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao exportar usuários.', str(e), success=False)

    def import_users(self):
        from gui.db_manager import import_encrypted_db
        path, _ = QFileDialog.getOpenFileName(self, 'Importar Usuários', '', 'Banco Criptografado (*.enc)')
        if path:
            try:
                if import_encrypted_db(path):
                    self.show_feedback('Importação', 'Usuários importados e validados com sucesso!', success=True)
                else:
                    self.show_feedback('Importação', 'Falha ao importar ou validar usuários.', success=False)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao importar usuários.', str(e), success=False)

    def export_logs(self):
        from gui.audit_log import log_audit_event
        path, _ = QFileDialog.getSaveFileName(self, 'Exportar Logs', '', 'Logs Criptografados (*.enc)')
        if path:
            try:
                # Simplesmente copia o arquivo de log criptografado
                import shutil
                log_path = os.path.join(os.path.dirname(__file__), 'audit.log.enc')
                shutil.copy(log_path, path)
                self.show_feedback('Exportação', 'Logs exportados com sucesso!', success=True)
            except Exception as e:
                self.show_feedback('Erro', 'Erro ao exportar logs.', str(e), success=False)

    def reset_all(self):
        from gui.privacy_config import reset_config
        try:
            reset_config()
            self.show_feedback('Reset', 'Sistema resetado para o padrão!', success=True)
        except Exception as e:
            self.show_feedback('Erro', 'Erro ao resetar sistema.', str(e), success=False)

    def open_key_manager(self):
        from gui.privacy_config import KEY_PATH

        log_audit_event("Acesso ao gerenciamento de chave de criptografia")
        dlg = KeyManagerDialog(KEY_PATH, self)
        dlg.exec_()

    def open_config_backup(self):
        log_audit_event("Acesso ao backup/restauração de configuração")
        dlg = ConfigBackupDialog(self)
        dlg.exec_()

    def open_db_backup(self):
        log_audit_event("Acesso ao backup/restauração do banco de dados")
        dlg = DBBackupDialog(self)
        dlg.exec_()

    def open_audit_logs(self):
        log_audit_event("Acesso aos logs de auditoria")
        dlg = AuditLogDialog(self)
        dlg.exec_()

    def toggle_tor(self):
        from gui.privacy_config import load_config, save_config

        config = load_config()
        tor_enabled = config.get("tor_enabled", False)
        config["tor_enabled"] = not tor_enabled
        save_config(config)
        if config["tor_enabled"]:
            from gui.tor_integration import start_tor

            start_tor()
            self.tor_status_label.setText("Tor: Ativado")
            self.tor_toggle_btn.setText("Desativar Tor")
            self.tor_toggle_btn.setIcon(get_icon("tor_on"))
        else:
            self.tor_status_label.setText("Tor: Desativado")
            self.tor_toggle_btn.setText("Ativar Tor")
            self.tor_toggle_btn.setIcon(get_icon("tor_off"))

    def open_proxy_chain_dialog(self):
        dialog = ProxyDialog(self)
        dialog.exec_()

    def update_proxies_from_scraper_action(self):
        try:
            update_proxies_from_scraper()
            QMessageBox.information(self, "Proxies", "Proxies atualizados com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar proxies: {e}")

    def init_network_monitor(self):
        # Inicialização básica do monitor de rede (pode ser expandido conforme necessário)
        pass

    def toggle_multi_hop(self):
        config = load_config()
        multi_hop_enabled = config.get("multi_hop", False)
        config["multi_hop"] = not multi_hop_enabled
        save_config(config)
        if config["multi_hop"]:
            self.proxy_multi_btn.setText("Desativar Multi-Hop")
            self.proxy_multi_btn.setIcon(get_icon("proxy_off"))
            QMessageBox.information(self, "Multi-Hop", "Multi-Hop ativado.")
        else:
            self.proxy_multi_btn.setText("Ativar Multi-Hop")
            self.proxy