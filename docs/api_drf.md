# Documentação de API - Integração Django/DRF

Esta documentação detalha os principais endpoints expostos para integração de terceiros via Django REST Framework.

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

## Endpoints Disponíveis

### Exemplo: /api/v1/usuarios/
- **GET**: Lista todos os usuários.
- **POST**: Cria um novo usuário.

#### Parâmetros de exemplo
- `username` (string)
- `email` (string)

#### Respostas
- 200 OK: Lista de usuários.
- 201 Created: Usuário criado.

### Exemplo: /api/v1/tokens/
- **POST**: Gera um token de autenticação.

#### Parâmetros de exemplo
- `username` (string)
- `password` (string)

#### Respostas
- 200 OK: Token JWT.

## Autenticação
A autenticação é feita via JWT. Inclua o token no header `Authorization: Bearer <token>`.

## Observações
- Consulte o código em `integrations/api_server.py` para detalhes de implementação.
- Para customizações, siga o padrão de ViewSets do DRF.

> **Nota:** Esta documentação é um ponto de partida. Recomenda-se expandir conforme a API evoluir.
