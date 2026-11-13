# GitHub CLI (`gh`)

O **GitHub CLI**, chamado pelo comando `gh`, permite trabalhar com repositórios, issues, pull requests e GitHub Actions pelo terminal. Ele complementa o Git: comandos como `git pull` e `git push` continuam sendo comandos Git, enquanto `gh` facilita operações que normalmente seriam feitas pela interface web do GitHub. Para um guia dedicado ao versionamento local, consulte [Git](git.md); para workflows e arquivos YAML, consulte [GitHub Actions](github-actions.md).

Neste capítulo, os comandos são apresentados no PowerShell e também funcionam, em geral, em terminais macOS e Linux. Não cole tokens ou senhas em comandos compartilhados, arquivos do projeto ou capturas de tela.

## 1. Criar uma conta no GitHub

Se você ainda não tem uma conta:

1. Acesse [github.com/signup](https://github.com/signup).
2. Informe seu e-mail, crie uma senha e escolha um nome de usuário.
3. Conclua a verificação solicitada e confirme o endereço de e-mail.
4. Ative a autenticação de dois fatores nas configurações de segurança da conta.

Criar uma conta é uma etapa feita no site; o `gh` não cria contas. Se o trabalho for em uma organização, peça acesso ao repositório antes de tentar enviar alterações.

## 2. Instalar o GitHub CLI

O GitHub CLI precisa estar instalado separadamente do Git. Se ainda não tiver Git, instale-o também: o `gh` usa o Git para operações com os arquivos e o histórico local.

### Windows

No PowerShell, com o gerenciador `winget` disponível:

```powershell
winget install --id GitHub.cli
```

Feche e reabra o terminal após a instalação e confira:

```powershell
gh --version
git --version
```

### macOS

Com o Homebrew:

```bash
brew install gh
```

### Linux e outros métodos

As instruções de instalação variam conforme a distribuição Linux e o gerenciador de pacotes. Consulte o guia oficial: [Instalar GitHub CLI](https://github.com/cli/cli#installation).

## 3. Autenticar e configurar o Git

No terminal, inicie o login:

```bash
gh auth login
```

Responda às perguntas interativas. Para uma conta comum, escolha `GitHub.com`, selecione HTTPS ou SSH e autentique pelo navegador quando solicitado. O fluxo pelo navegador evita que você precise copiar uma senha para o terminal.

Verifique o estado da autenticação:

```bash
gh auth status
```

Se escolheu HTTPS e quer que o Git use as credenciais gerenciadas pelo `gh`, execute:

```bash
gh auth setup-git
```

Configure o nome e o e-mail que serão gravados nos commits Git (use o e-mail que deseja associar aos commits):

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@example.com"
```

Essas configurações identificam os commits; elas não autenticam você no GitHub. A autenticação é feita pelo `gh auth login` (ou por uma chave SSH configurada).

## 4. Criar ou obter um repositório

### Clonar um repositório existente

```bash
gh repo clone ORGANIZACAO/REPOSITORIO
cd REPOSITORIO
```

Por exemplo:

```bash
gh repo clone dataRainBR/mkdocs-documentation
cd mkdocs-documentation
```

O comando baixa o repositório e configura o remote `origin`. Confira os remotes com:

```bash
git remote -v
```

### Criar um repositório

Para criar um repositório no GitHub e também conectar a pasta atual:

```bash
gh repo create NOME-DO-REPOSITORIO --public --source=. --remote=origin
```

Use `--private` em vez de `--public` para um repositório privado. Revise cuidadosamente os arquivos antes de publicar um repositório público.

Para criar o repositório e já enviar os commits locais:

```bash
gh repo create NOME-DO-REPOSITORIO --private --source=. --remote=origin --push
```

`--push` envia o histórico existente para o GitHub. Não o use sem conferir se a pasta e o conteúdo são os corretos.

## 5. Fluxo básico: atualizar, alterar e enviar

Um fluxo comum de colaboração é criar uma branch para cada alteração. Evite trabalhar diretamente na branch principal do projeto.

```bash
git switch main
git pull
git switch -c docs/novo-capitulo
```

- `git switch main` muda para a branch principal (ela pode se chamar `master` ou ter outro nome).
- `git pull` baixa e integra as alterações recentes da branch rastreada.
- `git switch -c ...` cria uma branch nova e muda para ela.

Depois de editar os arquivos, revise e registre as alterações:

```bash
git status
git diff
git add docs/
git commit -m "docs: adiciona capítulo sobre GitHub CLI"
```

`git add` prepara arquivos para o commit; `git commit` salva um ponto no histórico local. Ajuste o caminho após `git add` aos arquivos que você realmente deseja incluir.

Envie a branch ao GitHub:

```bash
git push -u origin docs/novo-capitulo
```

`-u` configura o acompanhamento da branch remota; nos próximos envios dessa mesma branch, normalmente basta `git push`. Para trazer depois novas alterações da branch atual, use `git pull`.

> **Git e `gh` têm papéis diferentes:** `git pull`, `git push`, `git add`, `git commit` e `git switch` trabalham com o repositório e seus arquivos. O `gh` autentica com o GitHub e opera recursos como repositórios, issues, pull requests e Actions.

## 6. Pull requests e merge

Depois do `git push`, abra um pull request (PR) para propor a integração das mudanças na branch principal:

```bash
gh pr create --base main --title "Adiciona capítulo sobre GitHub CLI" --body "Documenta instalação, autenticação, Git e GitHub Actions."
```

Se preferir responder às perguntas no terminal, use `gh pr create` sem argumentos. O PR pode ser revisado pela interface web ou pelo terminal.

Comandos úteis:

```bash
gh pr list
gh pr status
gh pr view
gh pr view 42
gh pr diff 42
gh pr checkout 42
```

Substitua `42` pelo número do PR. `gh pr checkout` baixa e muda para a branch do PR selecionado.

Após a revisão e a aprovação das verificações exigidas, faça o merge:

```bash
gh pr merge 42 --squash --delete-branch
```

`--squash` combina os commits do PR em um único commit; alternativas comuns são `--merge` e `--rebase`. A exclusão da branch local/remota é opcional. O repositório pode exigir aprovação, verificações bem-sucedidas ou uma fila de merge; nesse caso, respeite as regras configuradas. Para solicitar merge automático quando os requisitos forem satisfeitos:

```bash
gh pr merge 42 --auto --squash
```

Após o merge, atualize sua branch principal:

```bash
git switch main
git pull
```

## 7. Funcionalidades principais do `gh`

O `gh` tem comandos para as principais tarefas do GitHub. Alguns exemplos:

```bash
gh repo view
gh issue list
gh issue create
gh pr list
gh release list
gh workflow list
gh run list
```

Para consultar a ajuda de um grupo de comandos ou de uma operação:

```bash
gh help
gh help pr
gh help workflow run
```

Também é possível indicar outro repositório com `--repo ORGANIZACAO/REPOSITORIO` (ou `-R ORGANIZACAO/REPOSITORIO`) em comandos que aceitam essa opção.

## 8. GitHub Actions pelo terminal

GitHub Actions executa automações definidas em arquivos YAML dentro de `.github/workflows/`. Um workflow pode iniciar, por exemplo, ao enviar commits (`push`), abrir ou atualizar um pull request (`pull_request`) ou ser iniciado manualmente (`workflow_dispatch`).

### Consultar workflows e execuções

```bash
gh workflow list
gh workflow view docs.yml
gh run list
```

Para ver uma execução específica, incluindo seus passos e logs:

```bash
gh run view ID-DA-EXECUCAO
gh run view ID-DA-EXECUCAO --log
```

Para acompanhar uma execução em andamento até terminar:

```bash
gh run watch ID-DA-EXECUCAO
```

### Iniciar e reexecutar workflows

Para iniciar manualmente um workflow que declare `workflow_dispatch`:

```bash
gh workflow run docs.yml --ref main
```

O comando agenda a execução; não significa que ela já foi concluída. Consulte `gh run list` para obter o ID e use `gh run watch` para acompanhar o resultado.

Para reexecutar uma execução anterior:

```bash
gh run rerun ID-DA-EXECUCAO
```

Se o workflow não aparecer, confira se o arquivo existe em `.github/workflows/`, se está habilitado e se a branch selecionada contém a versão correta dele. Para a execução manual, o YAML precisa incluir o evento `workflow_dispatch`.

### Exemplo de workflow de documentação

Este exemplo valida a documentação deste projeto em cada push ou pull request. Ele instala as dependências Python e as ferramentas TypeScript e Chromium usadas pelo `mkdocs.yml`:

```yaml
name: Validar documentação

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Baixar o repositório
        uses: actions/checkout@v4

      - name: Configurar Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Instalar TypeDoc
        run: npm install --global typedoc

      - name: Instalar uv
        uses: astral-sh/setup-uv@v3

      - name: Instalar dependências Python
        run: uv sync

      - name: Instalar Chromium do Playwright
        run: uv run playwright install --with-deps chromium

      - name: Validar o build
        run: uv run mkdocs build --strict
```

O workflow de build e publicação deste projeto já está em `.github/workflows/docs.yml`; não crie outro arquivo com o mesmo nome. Use o exemplo para entender as etapas ou adaptar um workflow equivalente. O push ou a abertura/atualização de um PR dispara a execução; também é possível iniciá-la com `gh workflow run docs.yml --ref main`.

Este exemplo só faz o build e validação; ele não publica o site. Para publicar no GitHub Pages, configure o Pages e as permissões necessárias conforme [Integração com GitHub](integracao-github.md). O workflow de publicação deste projeto já está em `.github/workflows/docs.yml`.

### Segredos e permissões

- Guarde credenciais e chaves em **Settings → Secrets and variables → Actions**; nunca as escreva diretamente no YAML, no código ou em logs.
- Em workflows, dê ao `GITHUB_TOKEN` somente as permissões necessárias ao trabalho. A permissão de escrita não deve ser concedida sem necessidade.
- O `gh auth login` é para a sua sessão local. Nos workflows, prefira o `GITHUB_TOKEN` fornecido pelo GitHub, em vez de copiar para o workflow o token pessoal da sua conta.
- Ao usar workflows de terceiros ou ações externas, confira a origem, o código e as permissões antes de executá-los.

## 9. Referências oficiais

- [GitHub CLI: instalação](https://github.com/cli/cli#installation)
- [Manual do GitHub CLI](https://cli.github.com/manual/)
- [Autenticação com GitHub CLI](https://cli.github.com/manual/gh_auth_login)
- [Workflows do GitHub Actions pelo `gh`](https://cli.github.com/manual/gh_workflow)
- [Execuções do GitHub Actions pelo `gh`](https://cli.github.com/manual/gh_run)
- [GitHub Actions: entender workflows](https://docs.github.com/actions/writing-workflows)
