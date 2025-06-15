# Darks: Plataforma de Segurança, Anonimato e Gerenciamento de VPN/Proxy

<p align="center">
  <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status"/>
  <img src="https://img.shields.io/badge/coverage-100%25-brightgreen" alt="Test Coverage"/>
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"/>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python Version"/>
</p>

<p align="center">
  <img src="https://img.icons8.com/fluency/96/lock-2.png" alt="Segurança" width="60"/>
  <img src="https://img.icons8.com/fluency/96/anonymous-mask.png" alt="Anonimato" width="60"/>
  <img src="https://img.icons8.com/fluency/96/vpn.png" alt="VPN" width="60"/>
  <img src="https://img.icons8.com/fluency/96/proxy.png" alt="Proxy" width="60"/>
  <img src="https://img.icons8.com/fluency/96/settings.png" alt="Configuração" width="60"/>
</p>

---

## ✨ Visão Geral
Darks é uma solução completa para privacidade, anonimato e segurança digital, integrando VPN (WireGuard/OpenVPN), gerenciamento avançado de proxies, criptografia, monitoramento de rede e interface gráfica profissional. O projeto é modular, seguro e pronto para produção, com foco em robustez, testes e facilidade de uso.

## 🚀 Funcionalidades Principais
- 🖥️ Interface gráfica (GUI) moderna e responsiva
- 🔒 Gerenciamento de múltiplos protocolos VPN (WireGuard, OpenVPN)
- 🌐 Gerenciamento e upload de listas de proxies (SOCKS5, HTTP, FTPS, SFTP)
- 🕵️ Integração com Tor e DNS seguro
- 📊 Painel de feedback visual para fluxos críticos (VPN, Proxy, Tor, Usuários, Configurações)
- 🛡️ Criptografia avançada de dados e logs
- 🔄 Exportação/importação segura de configurações
- 📝 Módulo de auditoria e logging detalhado
- 🔗 Integração com APIs externas (Django, DRF)
- ✅ Testes unitários e de integração com cobertura total

## 🏗️ Arquitetura do Projeto
- **gui/**: Interface gráfica, lógica de usuário, feedback visual, monitoramento
- **crypto/**: Criptografia, protocolos de segurança, utilitários de segurança
- **openvpn/**, **wireguard/**: Gerenciamento de VPNs, configurações, integração
- **proxies/**: Gerenciamento de proxies, proxychains, upload seguro
- **integrations/**: APIs externas, integração com Django/DRF
- **ProxyList/**: Listas de proxies para uso rápido
- **tests/**: Testes unitários e de integração (não vai para produção)

## 🛠️ Instalação
1. Clone o repositório e acesse a pasta do projeto:
   ```bash
   git clone <repo_url>
   cd Darks
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Instale o WireGuard e/ou OpenVPN conforme seu sistema:
   - [WireGuard](https://www.wireguard.com/install/)
   - [OpenVPN](https://openvpn.net/community-downloads/)
4. (Opcional) Instale o Tor:
   - [Tor Project](https://www.torproject.org/download/)

## 💻 Uso
- Execute a interface gráfica:
  ```bash
  python run_gui.py
  ```
- Para rodar a API Django:
  ```bash
  cd integrations
  python api_server.py
  ```

## 🔐 Segurança e Privacidade
- Todos os dados sensíveis são criptografados (AES, chaves seguras)
- Logs críticos são protegidos e podem ser desativados
- Configurações de privacidade avançadas (no_logs, exportação segura)
- Upload seguro de listas de proxy via SFTP/FTPS
- Integração com Tor e DNS seguro para anonimato

## 🧪 Testes
- Testes unitários e de integração em `tests/test_all.py`
- Execute todos os testes:
  ```bash
  pytest tests/test_all.py --maxfail=5 --disable-warnings -v
  ```
- Cobertura total dos módulos críticos (segurança, anonimato, integração, falhas, logs, banco de dados, exportação/importação)

## 📁 Estrutura de Diretórios
```
gui/         # Interface gráfica, lógica de usuário, monitoramento
crypto/      # Criptografia, protocolos de segurança
openvpn/     # Gerenciamento de VPNs OpenVPN
wireguard/   # Gerenciamento de VPNs WireGuard
proxies/     # Proxies, proxychains, upload seguro
integrations/# APIs externas, Django/DRF
ProxyList/   # Listas de proxies
tests/       # Testes unitários/integrados (apenas dev)
docs/        # Documentação profissional
requirements.txt
run_gui.py
README.md
```

## 🚚 Deploy e Produção
- **Remova arquivos não necessários para produção:**
  - `.env.example`, `.pytest_cache/`, `.vscode/`, `app.log`, `tests/`, `venv/`, todos os `__pycache__/`
- **Mantenha apenas:** código-fonte, configs essenciais, `requirements.txt`, `README.md`, `docs/`
- **Recomendações:**
  - Use ambiente virtual dedicado
  - Proteja as chaves e arquivos sensíveis
  - Configure variáveis de ambiente para produção

## 🤝 Contribuição
- Siga o padrão PEP8/Black
- Escreva testes para novas funcionalidades
- Documente métodos e módulos críticos
- Use branches para novas features/correções

## ❓ FAQ
- **WireGuard/Proxies não conectam:** Verifique permissões, firewall e configurações
- **Erros de dependência:** Reinstale o ambiente virtual e dependências
- **Logs não aparecem:** Verifique permissões de escrita e configurações de privacidade

## 📬 Suporte
- Para dúvidas, abra uma issue ou entre em contato com o mantenedor

---

<p align="center">
  <img src="https://img.icons8.com/fluency/48/checked-checkbox.png" alt="Pronto para produção"/>
  <b>Documentação gerada automaticamente para ambiente profissional e seguro.</b>
</p>
