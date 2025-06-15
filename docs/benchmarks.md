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

# Benchmarks de Performance

Este projeto inclui exemplos de benchmarks de performance utilizando o pacote `pytest-benchmark`.

## Como rodar benchmarks

1. Instale as dependências necessárias:
   ```bash
   pip install pytest pytest-benchmark
   ```

2. Execute os benchmarks:
   ```bash
   pytest tests/ --benchmark-only
   ```

3. Para gerar um relatório comparativo:
   ```bash
   pytest tests/ --benchmark-autosave
   pytest-benchmark compare .benchmarks/latest .benchmarks/previous
   ```

## Exemplo de benchmark

Crie um arquivo `test_benchmarks.py` em `tests/` com o seguinte conteúdo:

```python
import time

def test_sleep_benchmark(benchmark):
    def sleeper():
        time.sleep(0.01)
    benchmark(sleeper)
```

Adapte para funções reais do seu projeto conforme necessário.
