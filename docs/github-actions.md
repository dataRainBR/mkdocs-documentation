# GitHub Actions

GitHub Actions é a plataforma de automação integrada ao GitHub. Ela executa tarefas de integração contínua e entrega/publicação contínua (CI/CD), como validar, testar, compilar e publicar um projeto quando ocorrem eventos no repositório. Para aprender a versionar os arquivos de workflow e enviá-los ao GitHub, consulte [Git](git.md).

## 1. Como funciona

Um workflow é um processo descrito em YAML e salvo em `.github/workflows/`. Quando um evento configurado acontece, o GitHub inicia um ou mais jobs em runners. Cada job executa steps em sequência; um step pode executar um comando ou chamar uma action reutilizável.

| Conceito | Significado |
|---|---|
| Workflow | Automação completa definida em um arquivo `.yml` ou `.yaml`. |
| Evento (`on`) | Situação que inicia a automação, como `push`, `pull_request` ou `workflow_dispatch`. |
| Job | Conjunto de etapas executado em um runner. Jobs diferentes podem executar em paralelo ou depender de outro job. |
| Runner | Máquina hospedada pelo GitHub ou máquina própria que executa um job. |
| Step | Um comando `run` ou uma action `uses` executada dentro do job. |
| Action | Componente reutilizável chamado por uma etapa, por exemplo, para clonar o repositório. |

O ciclo típico é: evento → workflow → job → runner → steps → resultado e logs na aba **Actions**.

## 2. Onde criar o arquivo YAML

Crie um arquivo `.yml` ou `.yaml` dentro desta pasta do repositório:

```text
.github/
└── workflows/
    └── validar-documentacao.yml
```

Ao enviar esse arquivo ao GitHub, o workflow aparece na aba **Actions**. O conteúdo do arquivo especifica quando executar e quais tarefas realizar.

## 3. Exemplo: validar este projeto MkDocs

O workflow abaixo valida a documentação em pushes para `main`, em Pull Requests direcionados a `main` e quando iniciado manualmente. Como este projeto documenta TypeScript e exporta PDFs, o job também instala Node.js/TypeDoc e Chromium para Playwright.

Salve este conteúdo como `.github/workflows/validar-documentacao.yml`:

```yaml
name: Validar documentação

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Baixar o repositório
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Configurar Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "24"

      - name: Instalar TypeDoc
        run: npm install --global typedoc

      - name: Instalar uv
        uses: astral-sh/setup-uv@v3

      - name: Instalar dependências Python
        run: uv sync

      - name: Instalar Chromium do Playwright
        run: uv run playwright install --with-deps chromium

      - name: Atualizar referências de pacotes
        run: uv run python docs_preview.py --generate-references

      - name: Validar o build do MkDocs
        run: uv run mkdocs build --strict
```

O arquivo `.github/workflows/docs.yml` deste repositório já contém o workflow de build e publicação do Pages. Não crie outro workflow de build junto deste, a menos que queira executar ambos. O exemplo acima serve como modelo de validação; para publicar o site, adapte o workflow existente ou use o fluxo de deploy conforme [Integração com GitHub](integracao-github.md).

## 4. Como ler e adaptar o YAML

- `name` é o nome mostrado na aba **Actions**.
- `on` lista os eventos de início. `push` filtra branch; `pull_request` valida alterações propostas; `workflow_dispatch` habilita a execução manual.
- `permissions` concede ao token automático somente o acesso necessário. Para um build que apenas lê código, `contents: read` é suficiente.
- `jobs` define um ou mais jobs. Cada job escolhe um runner em `runs-on`.
- `steps` lista ações e comandos executados em sequência. `uses` chama uma action; `run` executa comandos no shell do runner.
- `fetch-depth: 0` baixa o histórico Git completo, útil para plugins que leem datas de commits.
- `--strict` faz o MkDocs falhar quando encontra avisos, como links internos inválidos.

Um evento agendado, por exemplo, usa uma expressão cron em UTC:

```yaml
on:
  schedule:
    - cron: "0 9 * * 1"
```

O exemplo executa às 09:00 UTC toda segunda-feira. Consulte a documentação oficial para a sintaxe cron e os eventos disponíveis.

## 5. Publicar documentação no GitHub Pages

Para publicar o site gerado pelo MkDocs, o workflow precisa empacotar a pasta de saída e executar um job de deploy que dependa do build. O workflow real deste projeto já inclui estas etapas e as permissões correspondentes. A configuração usual é:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

No job de build, envie `site/` como artefato do Pages:

```yaml
- name: Enviar artefato do Pages
  uses: actions/upload-pages-artifact@v3
  with:
    path: site
```

Depois do build, um job de deploy dependente publica o artefato:

```yaml
deploy:
  needs: build
  runs-on: ubuntu-latest
  environment:
    name: github-pages
    url: {% raw %}${{ steps.deployment.outputs.page_url }}{% endraw %}
  steps:
    - name: Publicar no GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
```

No repositório, selecione **Settings → Pages → Build and deployment → Source → GitHub Actions**. A fonte e as permissões estão detalhadas na página [Integração com GitHub](integracao-github.md).

## 6. Segredos, permissões e repositórios privados

Não grave tokens, senhas ou chaves no YAML. Cadastre valores sensíveis em **Settings → Secrets and variables → Actions** e acesse-os como secrets no workflow:

```yaml
env:
  API_TOKEN: {% raw %}${{ secrets.API_TOKEN }}{% endraw %}
```

Para clonar o próprio repositório privado, `actions/checkout` usa por padrão o `GITHUB_TOKEN` do workflow. Se um job precisar ler outro repositório privado, use um token ou GitHub App com acesso mínimo, salvo como secret e passado apenas à etapa necessária.

```yaml
- name: Baixar um repositório privado adicional
  uses: actions/checkout@v4
  with:
    repository: ORGANIZACAO/REPOSITORIO-PRIVADO
    token: {% raw %}${{ secrets.REPO_READ_TOKEN }}{% endraw %}
    path: dependencias/privadas
```

Quem tem permissão de escrita no repositório pode alterar workflows e potencialmente usá-los para acessar secrets. Revise alterações de workflows, limite permissões do `GITHUB_TOKEN` e não disponibilize secrets a código não confiável de Pull Requests externos.

## 7. Acompanhar, iniciar e depurar execuções

Pela interface, abra a aba **Actions**, escolha o workflow e clique em uma execução para ver cada job, step e log. Se a execução falhar, comece pelo primeiro step vermelho e confira o comando e a mensagem de erro.

Pelo GitHub CLI:

```bash
gh auth status
gh workflow list
gh run list --workflow docs.yml
gh run view ID-DA-EXECUCAO --log
gh run watch ID-DA-EXECUCAO
```

Para iniciar manualmente um workflow que declara `workflow_dispatch`:

```bash
gh workflow run docs.yml --ref main
```

Para reexecutar uma execução anterior:

```bash
gh run rerun ID-DA-EXECUCAO
```

`gh run watch` acompanha a execução até ela terminar; `gh run view --log` mostra os logs. Uma execução agendada ou manual pode consumir recursos de Actions dependendo do plano, runner e tipo de repositório. Veja os limites e a cobrança na seção Enterprise de [Integração com GitHub](integracao-github.md).

## 8. Referências oficiais

- [Entender GitHub Actions](https://docs.github.com/actions/about-github-actions/understanding-github-actions)
- [Sintaxe dos workflows](https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax)
- [Eventos que iniciam workflows](https://docs.github.com/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [Usar secrets em GitHub Actions](https://docs.github.com/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)
- [Visualizar o histórico de execuções](https://docs.github.com/actions/how-tos/monitor-workflows/view-workflow-run-history)
