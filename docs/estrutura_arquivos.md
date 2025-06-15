# 📁 Estrutura de Arquivos do Projeto Darks

<p align="center">
  <img src="https://img.icons8.com/fluency/96/folder-invoices--v2.png" alt="Arquivos" width="60"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/security-certified-brightgreen" alt="Certificado de Segurança"/>
  <img src="https://img.shields.io/badge/tor-secure-blueviolet" alt="Tor Secure"/>
  <img src="https://img.shields.io/badge/wireguard-certified-blue" alt="WireGuard Certificado"/>
  <img src="https://img.shields.io/badge/python-verified-blue" alt="Python Verificado"/>
  <img src="https://img.shields.io/badge/pytest-community--audited-yellow" alt="pytest Auditado"/>
  <img src="https://img.shields.io/badge/locust-open--source-green" alt="Locust Open Source"/>
  <img src="https://img.shields.io/badge/coverage-Codecov%20Certified-orange" alt="Codecov Certificado"/>
  <img src="https://img.shields.io/badge/docker-official-blue" alt="Docker Official"/>
  <img src="https://img.shields.io/badge/safety-vuln--scan-green" alt="Safety Scan"/>
  <img src="https://img.shields.io/badge/pip--audit-vuln--scan-green" alt="pip-audit Scan"/>
  <img src="https://img.shields.io/badge/python--dotenv-secure-green" alt="python-dotenv Secure"/>
</p>

---

Abaixo está a arquitetura de arquivos e diretórios recomendada para o projeto Darks, separando claramente código-fonte, documentação, testes, configurações e recursos auxiliares.

```
Darks/
│
├── crypto/                # Módulos de criptografia e protocolos de segurança
│   └── security_protocols.py
│
├── gui/                   # Interface gráfica, lógica de usuário, monitoramento
│   ├── audit_log.py
│   ├── db_manager.py
│   ├── icons/             # Ícones e recursos visuais
│   ├── icons_helper.py
│   ├── kill_switch.py
│   ├── main_window.py
│   ├── network_monitor.py
│   ├── network_monitor_helpers.py
│   ├── privacy_config.py
│   ├── secure_dns.py
│   ├── tor_integration.py
│   └── ...
│
├── integrations/          # Integração com APIs externas (Django, DRF)
│   ├── api_base.py
│   ├── api_server.py
│   ├── django_settings.py
│   └── urls.py
│
├── proxies/               # Gerenciamento de proxies e proxychains
│   ├── proxies_list.json
│   ├── proxy_manager.py
│   ├── proxychain_manager.py
│   ├── proxychains.py
│   └── proxychains_config.json
│
├── ProxyList/             # Listas de proxies para uso rápido
│   ├── http.txt
│   ├── https.txt
│   ├── proxydump.txt
│   ├── socks4.txt
│   └── socks5.txt
│
├── wireguard/             # Gerenciamento e configuração do WireGuard
│   ├── install_wireguard.py
│   ├── manager.py
│   ├── wg_settings.json
│   └── wg_settings.py
│
├── docs/                  # Documentação profissional e manuais
│   ├── README.md
│   ├── instalacao.md
│   ├── arquitetura.md
│   ├── gui.md
│   ├── seguranca.md
│   ├── vpn.md
│   ├── proxy.md
│   ├── tor_dns.md
│   ├── api.md
│   ├── testes.md
│   ├── deploy.md
│   ├── faq.md
│   └── estrutura_arquivos.md
│
├── tests/                 # Testes unitários e de integração (dev only)
│   ├── test_all.py
│   └── __init__.py
│
├── requirements.txt       # Dependências do projeto
├── run_gui.py             # Inicializador da interface gráfica
├── README.md              # Visão geral do projeto
└── .gitignore             # Arquivos/pastas ignorados pelo git
```

## Observações
- **Não inclua**: `.env.example`, `.pytest_cache/`, `.vscode/`, `app.log`, `venv/`, `__pycache__/` na produção.
- **Mantenha**: Somente código-fonte, configs essenciais, documentação e testes (para dev).
- **Personalize**: Adicione novos módulos em subpastas conforme o crescimento do projeto.

---
<p align="center">
  <img src="https://img.icons8.com/fluency/48/folder-invoices--v2.png" alt="Arquivos"/>
  <b>Estrutura clara, escalável e pronta para equipes profissionais.</b>
</p>
