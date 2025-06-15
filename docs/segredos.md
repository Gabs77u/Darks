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

# Proteção e Separação de Segredos em Produção

Nunca armazene segredos (senhas, tokens, chaves) diretamente no código-fonte.

## Boas práticas
- Use arquivos `.env` (não versionados) para variáveis sensíveis.
- Em produção, utilize soluções como Docker secrets, AWS Secrets Manager, HashiCorp Vault, etc.
- Defina variáveis de ambiente no sistema operacional ou orquestrador (ex: Docker Compose, Kubernetes).

## Exemplo de uso com python-dotenv
1. Instale:
   ```bash
   pip install python-dotenv
   ```
2. Crie um arquivo `.env`:
   ```env
   SECRET_KEY=valor_super_secreto
   DB_PASSWORD=senha_segura
   ```
3. Carregue no código:
   ```python
   from dotenv import load_dotenv
   import os
   load_dotenv()
   secret = os.getenv('SECRET_KEY')
   ```

## Docker secrets
- Armazene segredos em `/run/secrets/` e leia no código.

## Nunca faça commit de arquivos `.env` ou segredos!
