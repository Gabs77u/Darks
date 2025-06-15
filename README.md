# Darks: Plataforma de Segurança, Anonimato e Gerenciamento de VPN/Proxy

<p align="center">
  <img src="https://img.shields.io/github/workflow/status/USUARIO/REPO/CI" alt="Build Status"/>
  <img src="https://codecov.io/gh/USUARIO/REPO/branch/main/graph/badge.svg" alt="Coverage"/>
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
Darks é uma solução completa para privacidade, anonimato e segurança digital, integrando VPN (WireGuard), gerenciamento avançado de proxies, criptografia, monitoramento de rede e interface gráfica profissional. Modular, seguro e pronto para produção.

## 🚀 Funcionalidades
- 🖥️ Interface gráfica (GUI) moderna
- 🔒 VPN WireGuard
- 🌐 Proxies (SOCKS5, HTTP, FTPS, SFTP)
- 🕵️ Tor e DNS seguro
- 📊 Painel visual de status
- 🛡️ Criptografia avançada
- 🔄 Exportação/importação segura
- 📝 Auditoria e logging
- 🔗 Integração com APIs externas
- ✅ Testes unitários, integração e E2E

## 📦 Estrutura do Projeto
- `gui/`: Interface gráfica
- `crypto/`: Criptografia
- `wireguard/`: VPN WireGuard
- `proxies/`: Proxies e proxychains
- `integrations/`: APIs externas
- `ProxyList/`: Listas de proxies
- `tests/`: Testes unitários, integração e E2E
- `docs/`: Documentação detalhada

## 🛠️ Instalação
```bash
# Clone o repositório
 git clone <repo_url>
 cd Darks
# Instale as dependências
 pip install -r requirements.txt
# Instale o WireGuard (https://www.wireguard.com/install/)
# (Opcional) Instale o Tor (https://www.torproject.org/download/)
```

## 💻 Uso
```bash
python run_gui.py
```
Para rodar a API Django:
```bash
cd integrations
python api_server.py
```

## 🔐 Segurança e Produção
- [Proteção de segredos e .env](docs/segredos.md)
- [Permissões mínimas de arquivos](docs/permissoes_arquivos.md)
- [SCA: análise de dependências](docs/sca.md)
- [Troubleshooting de escalabilidade](docs/troubleshooting_escalabilidade.md)
- [Exemplo de configuração segura](.env.example)

## 🧪 Testes e Qualidade
- [Estrutura de testes granularizada](docs/estrutura_testes.md)
- [Benchmarks de performance](docs/benchmarks.md)
- [Testes de carga e stress](docs/stress_load_tests.md)
- [Testes E2E da interface gráfica](docs/e2e_gui.md)
- [Badge real de coverage: como configurar](docs/coverage_badge.md)

### Executando todos os testes
```bash
pytest tests/
```

## 📁 Estrutura de Diretórios
```
gui/         # Interface gráfica
crypto/      # Criptografia
wireguard/   # VPN WireGuard
proxies/     # Proxies
integrations/# APIs externas
ProxyList/   # Listas de proxies
tests/       # Testes
```

## 🚚 Deploy
- Remova arquivos não necessários para produção: `.env.example`, `.pytest_cache/`, `.vscode/`, `tests/`, etc.
- Mantenha apenas código-fonte, configs essenciais, `requirements.txt`, `README.md`, `docs/`
- Use ambiente virtual dedicado e proteja arquivos sensíveis

## 🤝 Contribuição
- Siga PEP8/Black
- Escreva testes para novas funcionalidades
- Documente métodos e módulos críticos
- Use branches para features/correções

## ❓ FAQ e Suporte
- [FAQ](docs/faq.md)
- Para dúvidas, abra uma issue ou entre em contato

---

<p align="center">
  <img src="https://img.icons8.com/fluency/48/checked-checkbox.png" alt="Pronto para produção"/>
  <b>Documentação profissional, badges reais e pronta para produção.</b>
</p>
