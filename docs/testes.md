# 🧪 Testes e Cobertura

<p align="center">
  <img src="https://img.icons8.com/fluency/96/test-tube.png" alt="Testes" width="60"/>
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

## Estrutura
- Testes organizados por módulo em subpastas de `tests/`
- Cobertura de 100% dos módulos críticos
- Testes de segurança, anonimato, integração, falhas, logs, banco de dados, exportação/importação
- Testes E2E em `tests/e2e/` (pytest-qt, pytest-playwright)

## Como Executar
```bash
pytest --cov=gui --cov=crypto --cov=wireguard --cov=proxies --cov=integrations --cov-report=term --cov-report=html
```

## Boas Práticas
- Escreva testes para cada nova funcionalidade
- Use dados reais e cenários de borda
- Revise resultados e logs após cada execução
- Use mocks e fixtures para dependências externas
- Garanta que todos os testes passem antes do pull request
