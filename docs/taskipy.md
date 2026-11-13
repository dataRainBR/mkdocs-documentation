# Taskipy: automatizar tarefas do projeto

Taskipy é um executor de tarefas para projetos Python. Você cadastra comandos com nomes curtos no `pyproject.toml` e os executa de forma consistente no terminal e no GitHub Actions. Por exemplo, uma tarefa chamada `test` pode executar o pytest, e outra chamada `lint` pode executar o Ruff.

Neste tutorial, os comandos usam [`uv`](uv.md) para instalar dependências e executar tarefas no ambiente do projeto.

## 1. Instalar Taskipy com uv

Abra o terminal na pasta que contém `pyproject.toml` e adicione Taskipy ao grupo de desenvolvimento:

```bash
uv add --dev taskipy
```

O comando atualiza `pyproject.toml` e `uv.lock`. Confirme a instalação:

```bash
uv run task --help
```

Taskipy é uma ferramenta de desenvolvimento, não uma dependência necessária para a aplicação funcionar em produção.

## 2. Criar uma tarefa no `pyproject.toml`

As tarefas são declaradas em `[tool.taskipy.tasks]`. Cada chave vira o nome de uma tarefa e o valor é o comando executado:

```toml
[tool.taskipy.tasks]
hello = "python -c \"print('Olá, Taskipy!')\""
```

Execute-a dentro do ambiente gerenciado pelo uv:

```bash
uv run task hello
```

Para listar as tarefas configuradas:

```bash
uv run task --list
```

Taskipy não substitui `uv run`: o uv seleciona o ambiente virtual e o Taskipy escolhe qual comando executar nesse ambiente.

## 3. Integrar Taskipy, Ruff e pytest

Instale as ferramentas usadas nos exemplos:

```bash
uv add --dev taskipy ruff pytest pytest-cov
```

Adicione tarefas para formatação, lint, testes e cobertura:

```toml
[tool.taskipy.tasks]
lint = "ruff check src tests"
format = "ruff format src tests"
format_check = "ruff format --check src tests"
test = "pytest -q"
coverage = "pytest --cov=meu_pacote --cov-report=term-missing --cov-report=html"
check = "task lint && task format_check && task test"
```

Substitua `src` e `tests` pelos diretórios usados no seu projeto. Troque `meu_pacote` pelo nome importável do pacote Python — normalmente com sublinhados, mesmo que o nome de distribuição use hífens.

Agora é possível executar cada etapa separadamente:

```bash
uv run task lint
uv run task format
uv run task test
uv run task coverage
```

Ou executar as verificações de uma só vez:

```bash
uv run task check
```

O comando `check` chama as tarefas na ordem indicada. Se uma etapa falhar, o processo termina com erro, o que também faz o GitHub Actions marcar a execução como falha.

## 4. Passar argumentos e criar tarefas compostas

Argumentos escritos depois do nome da tarefa são encaminhados ao comando configurado. Por exemplo, para selecionar um subconjunto de testes:

```bash
uv run task test -k cadastro
```

Uma tarefa composta pode chamar outras tarefas. No exemplo anterior, `check` combina lint, conferência de formatação e testes com `&&`; se uma etapa falhar, as seguintes não são executadas.

Taskipy também reconhece tarefas `pre_<nome>` e `post_<nome>` como ganchos antes e depois de uma tarefa. Use-os quando essa dependência fizer sentido para o fluxo; para verificações explícitas de CI, uma tarefa composta como `check` costuma ser mais fácil de entender.

## 5. Executar as tarefas no GitHub Actions

Crie `.github/workflows/qualidade.yml`. O workflow abaixo instala uv, sincroniza o ambiente usando o lockfile e executa as tarefas definidas no TOML:

```yaml
name: Qualidade do código

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  qualidade:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Instalar uv
        uses: astral-sh/setup-uv@v9
        with:
          enable-cache: true

      - name: Instalar dependências
        run: uv sync --locked

      - name: Executar verificações
        run: uv run task check
```

Versione `pyproject.toml` e `uv.lock`. A opção `--locked` faz o job falhar se os arquivos não estiverem sincronizados, em vez de alterar o lockfile durante o CI. Depois de enviar o workflow ao GitHub, acompanhe o resultado na aba **Actions** do repositório.

## Referências oficiais

- [Taskipy no GitHub: instalação, tarefas, argumentos e hooks](https://github.com/taskipy/taskipy)
- [uv em GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/)
- [Ruff: linter e formatador](ruff.md)
- [pytest: testes e cobertura](pytest.md)
