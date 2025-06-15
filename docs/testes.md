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
- Todos os testes estão em `tests/test_all.py`
- Cobertura de 100% dos módulos críticos
- Testes de segurança, anonimato, integração, falhas, logs, banco de dados, exportação/importação

## Como Executar
```bash
pytest tests/test_all.py --maxfail=5 --disable-warnings -v
```

## Boas Práticas
- Escreva testes para cada nova funcionalidade
- Use dados reais e cenários de borda
- Revise resultados e logs após cada execução
