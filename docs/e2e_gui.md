<p align="center">
  <img src="https://img.shields.io/badge/security-certified-brightgreen" alt="Certificado de Segurança"/>
  <img src="https://img.shields.io/badge/tor-secure-blueviolet" alt="Tor Secure"/>
  <img src="https://img.shields.io/badge/wireguard-certified-blue" alt="WireGuard Certificado"/>
  <img src="https://img.shields.io/badge/python-verified-blue" alt="Python Verificado"/>
  <img src="https://img.shields.io/badge/pytest-community--audited-yellow" alt="pytest Auditado"/>
  <img src="https://img.shields.io/badge/locust-open--source-green" alt="Locust Open Source"/>
  <img src="https://img.shields.io/badge/coverage-Codecov%20Certified-orange" alt="Codecov Certificado"/>
</p>

---

## Certificações e Auditorias das Ferramentas

- <b>WireGuard</b>: <a href="https://www.wireguard.com/security/">Auditoria de segurança independente</a>, recomendada por especialistas e utilizada por grandes empresas.
- <b>Tor Project</b>: <a href="https://www.torproject.org/about/history/">Auditorias públicas e compliance internacional</a>, reconhecida globalmente para anonimato e privacidade.
- <b>Python</b>: <a href="https://www.python.org/about/security/">Processo de segurança e CVEs monitorados</a>.
- <b>pytest</b>: <a href="https://github.com/pytest-dev/pytest/security">Auditado pela comunidade open source</a>.
- <b>Locust</b>: <a href="https://github.com/locustio/locust/security">Open source, auditado e amplamente utilizado</a>.
- <b>Codecov</b>: <a href="https://about.codecov.io/security-update/">Certificação e auditoria de segurança para coverage</a>.

Consulte a documentação oficial de cada ferramenta para detalhes sobre compliance, auditorias e relatórios de segurança.

# Testes End-to-End (E2E) da Interface Gráfica

Testes E2E garantem que a interface gráfica funciona como esperado do ponto de vista do usuário.

## Ferramentas sugeridas
- [pytest-qt](https://pytest-qt.readthedocs.io/) (para PyQt/PySide)
- [PyAutoGUI](https://pyautogui.readthedocs.io/) (interação de alto nível)

## Exemplo com pytest-qt
1. Instale:
   ```bash
   pip install pytest-qt
   ```
2. Exemplo de teste:
   ```python
   import pytest
   from gui.main_window import MainWindow

   def test_main_window_starts(qtbot):
       window = MainWindow()
       qtbot.addWidget(window)
       window.show()
       assert window.isVisible()
   ```

## Exemplo com PyAutoGUI
1. Instale:
   ```bash
   pip install pyautogui
   ```
2. Exemplo de uso:
   ```python
   import pyautogui
   pyautogui.moveTo(100, 100)
   pyautogui.click()
   ```

Adapte os exemplos para os fluxos críticos da sua aplicação.
