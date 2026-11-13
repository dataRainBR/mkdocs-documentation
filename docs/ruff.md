# Ruff: analisar e formatar código Python

Ruff reúne duas ferramentas relacionadas, mas diferentes:

- **Linter**: analisa o código e aponta problemas, como imports não utilizados, erros comuns e divergências das regras selecionadas.
- **Formatador**: reescreve o código para aplicar um estilo consistente.

O linter é executado com `ruff check`; o formatador, com `ruff format`. Um não substitui o outro: formatar o código não corrige todos os problemas encontrados pelo linter.

## 1. Instalar Ruff com uv

No terminal, a partir da pasta que contém `pyproject.toml`, adicione Ruff ao grupo de desenvolvimento:

```bash
uv add --dev ruff
```

Confira a versão instalada:

```bash
uv run ruff --version
```

## 2. Executar o linter

Analise todos os arquivos Python nas pastas indicadas:

```bash
uv run ruff check src tests
```

Ruff informa o arquivo, a linha e o código da regra para cada problema. Para verificar uma regra específica, por exemplo imports não utilizados (`F401`):

```bash
uv run ruff check --select F401 src tests
```

Para tentar aplicar automaticamente as correções seguras:

```bash
uv run ruff check --fix src tests
```

Revise o diff depois de corrigir. Ruff pode oferecer correções não seguras com `--unsafe-fixes`; elas podem alterar o comportamento e devem ser avaliadas antes de aplicar:

```bash
uv run ruff check --fix --unsafe-fixes src tests
```

Para ver a explicação de uma regra:

```bash
uv run ruff rule F401
```

## 3. Formatar o código

Formate os arquivos Python:

```bash
uv run ruff format src tests
```

Para apenas verificar se já estão formatados — sem modificar os arquivos — use:

```bash
uv run ruff format --check src tests
```

Para visualizar as alterações propostas sem gravá-las:

```bash
uv run ruff format --diff src tests
```

`ruff format` grava as alterações; `ruff format --check` é apropriado para CI, pois retorna erro quando encontra arquivos que precisam ser formatados.

## 4. Configurar Ruff no `pyproject.toml`

Ruff lê sua configuração do mesmo `pyproject.toml` usado pelo uv:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"
extend-exclude = ["build", "dist", "htmlcov", "site"]

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

O que essas opções fazem:

- **`line-length`**: comprimento de linha usado pelo linter e pelo formatador.
- **`target-version`**: versão mínima do Python considerada na análise; `py312` corresponde ao Python 3.12.
- **`extend-exclude`**: complementa a lista de arquivos e diretórios ignorados.
- **`lint.select`**: escolhe os grupos de regras; `E` vem do pycodestyle, `F` do Pyflakes e `I` verifica a organização dos imports.
- **`format.quote-style`** e **`format.indent-style`**: definem o estilo de aspas e indentação.

O Ruff também aceita ajustes como `lint.ignore` para ignorar regras e `lint.per-file-ignores` para exceções restritas a certos arquivos. Prefira corrigir o código ou limitar a exceção ao arquivo necessário em vez de desativar uma regra para o projeto inteiro.

## 5. Integrar Ruff ao Taskipy

Depois de instalar Taskipy com `uv add --dev taskipy`, configure tarefas no mesmo TOML:

```toml
[tool.taskipy.tasks]
lint = "ruff check src tests"
lint_fix = "ruff check --fix src tests"
format = "ruff format src tests"
format_check = "ruff format --check src tests"
```

Execute as tarefas sem precisar lembrar todos os argumentos:

```bash
uv run task lint
uv run task lint_fix
uv run task format
uv run task format_check
```

Para verificações automáticas, use `lint` e `format_check`, que apenas analisam o código. Reserve `lint_fix` e `format` para quando quiser gravar as correções localmente.

## 6. Executar as verificações no GitHub Actions

O GitHub Actions pode usar as mesmas tarefas sem duplicar os comandos do projeto. No arquivo `.github/workflows/qualidade.yml`, depois de configurar checkout e uv:

```yaml
      - name: Instalar dependências
        run: uv sync --locked

      - name: Verificar lint
        run: uv run task lint

      - name: Conferir formatação
        run: uv run task format_check
```

Se um comando retornar erro, o job falha e os detalhes ficam nos logs da execução em **GitHub → Actions**. Consulte [Taskipy](taskipy.md) para o workflow completo.

## Referências oficiais

- [Documentação do Ruff](https://docs.astral.sh/ruff/)
- [Linter: regras e opções](https://docs.astral.sh/ruff/linter/)
- [Formatador](https://docs.astral.sh/ruff/formatter/)
- [Configurações disponíveis](https://docs.astral.sh/ruff/settings/)
- [Taskipy: executar Ruff com tarefas](taskipy.md)
