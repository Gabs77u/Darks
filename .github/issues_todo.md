# Issues do Projeto Darks

## 1. Documentação e Onboarding
- [ ] Atualizar todos os manuais em `docs/` após cada nova feature
- [ ] Adicionar exemplos visuais (prints, GIFs) nos manuais da GUI e deploy
- [ ] Criar um guia rápido de onboarding para novos desenvolvedores

## 2. Segurança
- [ ] Revisar e reforçar sanitização de todas as entradas do usuário (GUI e backend)
- [ ] Implementar verificação automática de integridade dos arquivos de configuração
- [ ] Adicionar testes de penetração automatizados (fuzzing, brute-force controlado)
- [ ] Garantir que logs sensíveis sejam sempre criptografados e nunca versionados

## 3. Automação e DevOps
- [ ] Adicionar pipeline CI/CD (GitHub Actions) para rodar testes e lint automaticamente
- [ ] Gerar badge de cobertura de testes no README principal
- [ ] Automatizar o deploy seguro (scripts de build, checklist de produção)

## 4. Experiência do Usuário (UX)
- [ ] Adicionar pop-ups de confirmação para todas as ações destrutivas na GUI
- [ ] Melhorar feedback visual para erros de conexão e falhas de autenticação
- [ ] Incluir modo escuro e acessibilidade na interface

## 5. Testes
- [ ] Garantir que todos os fluxos críticos tenham testes reais e de borda
- [ ] Adicionar testes de stress para múltiplas conexões simultâneas
- [ ] Documentar como rodar testes em ambiente CI

## 6. Performance e Escalabilidade
- [ ] Otimizar carregamento de listas grandes de proxies
- [ ] Implementar cache para configurações e logs acessados frequentemente
- [ ] Monitorar uso de memória e recursos em execuções prolongadas

## 7. Internacionalização
- [ ] Adicionar suporte a múltiplos idiomas na GUI e documentação

## 8. Licenciamento e Compliance
- [ ] Garantir que todos os arquivos de código tenham o cabeçalho da licença MIT
- [ ] Revisar dependências para evitar conflitos de licença

## 9. Integrações Futuras
- [ ] Planejar integração com outros protocolos de VPN e proxies
- [ ] Adicionar suporte a autenticação 2FA para acesso à interface

---
