# 🚚 Deploy e Produção

<p align="center">
  <img src="https://img.icons8.com/fluency/96/deployment.png" alt="Deploy" width="60"/>
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

## Checklist de Deploy
- Remova arquivos temporários: `.env.example`, `.pytest_cache/`, `.vscode/`, `app.log`, `venv/`, todos os `__pycache__/`
- Mantenha apenas código-fonte, configs essenciais, `requirements.txt`, `README.md` e `docs/`
- Proteja arquivos sensíveis e chaves
- Configure variáveis de ambiente para produção

## Recomendações
- Use ambiente virtual dedicado
- Revise permissões de arquivos
- Ative logs apenas se necessário
- Teste o sistema em ambiente isolado antes do deploy final

<p align="center">
  <img src="https://img.icons8.com/fluency/48/rocket.png" alt="Deploy"/>
  <b>Deploy seguro, limpo e pronto para produção.</b>
</p>
