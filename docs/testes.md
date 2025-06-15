# 🧪 Testes e Cobertura

<p align="center">
  <img src="https://img.icons8.com/fluency/96/test-tube.png" alt="Testes" width="60"/>
</p>

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
