# uv: gerenciar projetos e dependências Python

[`uv`](https://docs.astral.sh/uv/) é uma ferramenta para instalar e gerenciar versões do Python, criar projetos, resolver dependências e executar comandos dentro de ambientes virtuais. Em um projeto, o `pyproject.toml` descreve as dependências e configurações; o `uv.lock` registra a resolução exata usada para reproduzir o ambiente.

## 1. Instalar o uv

No Windows, instale pelo WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

Ou use o instalador oficial no PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

No macOS ou Linux, o instalador oficial é:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Feche e reabra o terminal e confirme a instalação:

```powershell
uv --version
```

Se o comando não for reconhecido, confirme se o diretório de instalação do `uv` está no `PATH` e abra um novo terminal. A instalação e as opções por sistema estão na documentação oficial de [instalação do uv](https://docs.astral.sh/uv/getting-started/installation/).

## 2. Criar um projeto com `uv init`

Crie uma pasta de projeto e inicialize nela:

```bash
uv init meu-projeto
cd meu-projeto
```

No template padrão atual para aplicação empacotada, o `uv init` cria arquivos semelhantes a estes:

```text
meu-projeto/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── src/
    └── meu_projeto/
        └── __init__.py
```

- `.python-version` indica a versão padrão do Python para o projeto.
- `pyproject.toml` contém os metadados e as dependências.
- `src/meu_projeto/` é o pacote Python inicial. O sublinhado substitui o hífen do nome da distribuição.
- `.gitignore` exclui arquivos gerados, como `.venv`.
- `README.md` é o ponto de partida para a descrição do projeto.

O template pode variar conforme a versão do `uv` e as opções do comando. Para um script simples sem sistema de build, use `uv init --no-package meu-script`; esse modelo cria `main.py` em vez do pacote em `src/`. Para uma biblioteca distribuível, use `uv init --lib minha-biblioteca`.

O `uv init` não precisa criar o ambiente e o lockfile imediatamente. `uv lock`, `uv run` ou `uv sync` podem criar o `uv.lock`; já a pasta `.venv` é criada quando `uv run` ou `uv sync` prepara o ambiente. `uv lock` sozinho não cria nem instala um ambiente virtual. Depois desses comandos, a estrutura pode incluir:

```text
meu-projeto/
├── .venv/       # Ambiente virtual local; não deve ir para o Git
└── uv.lock      # Versões resolvidas; deve ser versionado
```

## 3. Executar comandos e scripts

`uv run` prepara ou sincroniza o ambiente do projeto antes de executar um comando. Assim, não é necessário ativar `.venv` manualmente:

```bash
uv run python --version
uv run python main.py
```

Para executar uma ferramenta instalada como dependência do projeto:

```bash
uv run pytest
```

Para sincronizar o ambiente explicitamente, por exemplo para que o editor encontre o interpretador e as dependências:

```bash
uv sync
```

O ambiente do projeto fica em `.venv/`, ao lado de `pyproject.toml`. Use `uv add` para dependências persistentes; evite instalar pacotes de projeto manualmente dentro de `.venv`, pois uma sincronização posterior pode removê-los.

## 4. Configurar o `pyproject.toml`

`pyproject.toml` é o arquivo TOML padrão para metadados e configurações de projetos Python. O bloco `[project]` segue o padrão PEP 621; o `uv` também reconhece configurações próprias em `[tool.uv]`.

Exemplo de metadados, dependência de execução e grupos:

```toml
[project]
name = "meu-projeto"
version = "0.1.0"
description = "Descrição do projeto"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "httpx>=0.27,<1",
]

[dependency-groups]
dev = [
    "pytest>=8",
    "ruff>=0.11",
]
docs = [
    "mkdocs>=1.6",
]

[project.optional-dependencies]
postgres = [
    "psycopg[binary]>=3.2",
]
```

O significado das seções:

- **`[project]`**: nome, versão, Python compatível e dependências necessárias para executar o projeto.
- **`dependencies`**: dependências obrigatórias de execução; são consideradas ao instalar o projeto e ao publicar uma distribuição.
- **`[dependency-groups]`**: ferramentas e bibliotecas locais de desenvolvimento, como testes, lint e documentação.
- **`[project.optional-dependencies]`**: recursos opcionais publicados como *extras*, que podem ser instalados por quem consome a biblioteca.
- **`[tool.uv]`**: opções específicas do `uv`, como fontes Git, índices ou grupos padrão.
- **`[build-system]`**: backend usado para empacotar o projeto. O template de `uv init` normalmente o configura; não é necessário alterá-lo para apenas adicionar dependências.

Você pode editar o TOML manualmente, mas os comandos `uv add` e `uv remove` ajudam a manter o arquivo e o lockfile sincronizados.

## 5. Adicionar e remover dependências

Adicione uma dependência necessária em execução:

```bash
uv add httpx
```

Isso acrescenta a dependência a `[project].dependencies`, atualiza `uv.lock` e sincroniza o ambiente. Para removê-la:

```bash
uv remove httpx
```

Para fixar uma faixa de versões, informe o requisito:

```bash
uv add "httpx>=0.27,<1"
```

Para executar uma ferramenta sem registrá-la permanentemente no projeto, use `uvx` (atalho para executar uma ferramenta em um ambiente isolado):

```bash
uvx ruff --version
```

## 6. Separar dependências de desenvolvimento e produção

Use **`project.dependencies`** para bibliotecas necessárias ao funcionamento do aplicativo e **`dependency-groups.dev`** para ferramentas de desenvolvimento, testes e lint. O grupo `dev` é local: não é publicado nos requisitos da distribuição.

Comandos equivalentes para gerenciar essas listas:

```bash
uv add fastapi
uv add --dev pytest ruff
uv add --group docs mkdocs
```

O resultado fica separado no `pyproject.toml`:

```toml
[project]
dependencies = [
    "fastapi>=0.115",
]

[dependency-groups]
dev = [
    "pytest>=8",
    "ruff>=0.11",
]
docs = [
    "mkdocs>=1.6",
]
```

Comportamento dos comandos de sincronização:

```bash
uv sync                  # dependências de execução + grupo dev (padrão)
uv sync --no-dev         # dependências de execução, sem o grupo dev
uv sync --locked --no-dev  # produção/CI: não altera o lockfile
uv sync --group docs     # inclui o grupo docs além dos grupos padrão
```

Por padrão, `uv sync` inclui o grupo `dev`. `--no-dev` o exclui; a opção `--locked` falha se `pyproject.toml` e `uv.lock` não estiverem sincronizados, em vez de atualizar o lockfile silenciosamente. `uv sync` também faz uma sincronização exata e pode remover pacotes que foram instalados manualmente, mas não estão declarados.

Use `[project.optional-dependencies]` quando o recurso opcional deve ser oferecido aos consumidores da biblioteca como *extra*:

```bash
uv add --optional postgres "psycopg[binary]>=3.2"
uv sync --extra postgres
```

Extras não são instalados por padrão. Diferentemente do grupo `dev`, eles fazem parte dos metadados publicados do projeto.

## 7. O que é `uv.lock` e como atualizá-lo

`uv.lock` é o lockfile gerenciado pelo `uv`. Enquanto `pyproject.toml` declara requisitos e faixas aceitáveis, o lockfile registra a resolução exata das dependências diretas e transitivas, as fontes dos pacotes e as condições por plataforma/Python. O formato é universal para que o mesmo arquivo possa orientar instalações em diferentes sistemas compatíveis.

O lockfile é criado ou atualizado por `uv lock`, `uv add`, `uv remove` e também automaticamente durante comandos de projeto como `uv run` e `uv sync`. **Não edite `uv.lock` manualmente**; altere o `pyproject.toml` ou use os comandos do `uv`.

Comandos úteis:

```bash
uv lock --check                    # verifica se o lockfile corresponde ao projeto
uv lock                            # resolve e atualiza o lockfile
uv lock --upgrade                  # atualiza pacotes dentro dos requisitos declarados
uv lock --upgrade-package httpx    # atualiza apenas um pacote
uv sync --locked                   # instala sem modificar um lockfile desatualizado
```

Versione `uv.lock` junto com `pyproject.toml` para que desenvolvimento, CI e implantação usem a mesma resolução. Não versione `.venv/`.

## 8. Interpretar a estrutura deste repositório

O `pyproject.toml` deste tutorial declara os pacotes do site em `[project].dependencies`; a origem Git e a revisão fixada de `griffe-typedoc` ficam em `[tool.uv.sources]`. O `uv.lock` contém a resolução exata de todos eles. Como as ferramentas MkDocs fazem parte da tarefa principal deste repositório, elas estão declaradas como dependências do projeto, e não como grupo `dev`.

Para instalar o ambiente documentado, clone o repositório e execute:

```bash
uv sync
```

Isso lê os requisitos do TOML e as versões do lockfile; não é necessário repetir uma série de comandos `uv add` pacote por pacote.

## 9. Comandos principais

| Comando | Uso |
|---|---|
| `uv init` | Cria a estrutura inicial de um projeto. |
| `uv add pacote` | Adiciona uma dependência de execução. |
| `uv add --dev pacote` | Adiciona uma dependência ao grupo de desenvolvimento. |
| `uv remove pacote` | Remove uma dependência. |
| `uv sync` | Sincroniza o ambiente com o projeto e o lockfile. |
| `uv run comando` | Executa um comando dentro do ambiente do projeto. |
| `uv lock` | Resolve e atualiza o lockfile. |
| `uv tree` | Mostra a árvore de dependências. |
| `uv python install 3.12` | Instala uma versão gerenciada do Python. |
| `uv python pin 3.12` | Define a versão padrão do projeto em `.python-version`. |
| `uv build` | Constrói os arquivos de distribuição em `dist/`. |

## Referências oficiais

- [Instalação do uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Criar projetos com `uv init`](https://docs.astral.sh/uv/concepts/projects/init/)
- [Trabalhar em projetos](https://docs.astral.sh/uv/guides/projects/)
- [Configurar dependências](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [Lockfile e sincronização](https://docs.astral.sh/uv/concepts/projects/sync/)
- [Estrutura do projeto e arquivos](https://docs.astral.sh/uv/concepts/projects/layout/)
