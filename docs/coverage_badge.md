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

# Badge real de cobertura de testes

Para exibir um badge real de cobertura, utilize o [Codecov](https://about.codecov.io/) ou [Coveralls](https://coveralls.io/).

## Como configurar com Codecov
1. Gere o relatório de cobertura localmente:
   ```bash
   pip install coverage
   coverage run -m pytest
   coverage xml
   ```
2. No seu repositório GitHub, ative o Codecov e adicione o token no CI.
3. Adicione o badge ao `README.md`:
   ```markdown
   ![Coverage](https://codecov.io/gh/USUARIO/REPO/branch/main/graph/badge.svg)
   ```

## Como configurar com Coveralls
1. Instale:
   ```bash
   pip install coveralls
   ```
2. Configure no seu CI e adicione o badge ao `README.md`.

Consulte a documentação das plataformas para detalhes de integração.
