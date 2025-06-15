# Estrutura recomendada para testes

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

Para maior granularidade e organização, recomenda-se separar os testes por módulo.

## Exemplo de estrutura
```
tests/
    test_all.py           # Testes gerais
    test_benchmarks.py    # Benchmarks
    test_gui/
        test_main_window.py
        test_audit_log.py
    test_crypto/
        test_security_protocols.py
    test_integrations/
        test_api_server.py
    test_wireguard/
        test_wireguard_protocols.py
    test_proxies/
        test_http_proxies.py
    ...
```

## Como criar
- Crie subpastas em `tests/` para cada módulo.
- Nomeie os arquivos como `test_<nome_do_modulo>.py`.
- Use `pytest` para rodar todos os testes:
  ```bash
  pytest tests/
  ```

Adapte conforme a evolução do projeto.

## Estrutura de testes granularizada

Os testes agora estão organizados por módulo em subpastas de `tests/`:

- `test_gui/` — testes da interface gráfica
- `test_crypto/` — testes de criptografia
- `test_integrations/` — testes de integrações
- `test_wireguard/` — testes do Wireguard
- `test_proxies/` — testes de proxies

Adicione novos arquivos conforme surgirem novos módulos.
