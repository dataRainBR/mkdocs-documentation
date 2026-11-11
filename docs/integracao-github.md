# Integração com GitHub

## 1. O que significa "integrar" a documentação com o repositório

Até aqui, o Documentation_Site foi tratado como um artefato isolado: um site estático gerado a partir dos arquivos em `docs/`. O MkDocs Material, porém, sabe se conectar ao repositório Git/GitHub onde esses arquivos vivem, e usar essa conexão para acrescentar, automaticamente, três coisas em cada página do site:

1. Um **link (ou ícone) para o repositório** no topo do site, apontando para a página do projeto no GitHub.
2. **Botões de ação no topo de cada página**: um para abrir o arquivo Markdown daquela página direto no GitHub, pronto para edição (e eventual Pull Request), e outro para apenas visualizar o Markdown bruto no repositório.
3. A **data da última modificação** daquela página (e, opcionalmente, a data de criação), lida do histórico de commits do arquivo no Git.

Nenhuma dessas três coisas depende de hospedar o site no GitHub Pages especificamente — elas dependem apenas de o `mkdocs.yml` apontar para onde o repositório (ou pelo menos seu histórico Git local) está. As três próximas seções explicam, respectivamente, como cada uma é configurada neste projeto.

## 2. `repo_url`, `repo_name` e `edit_uri`

O `mkdocs.yml` deste projeto define:

```yaml
repo_url: https://github.com/seu-usuario/teste-mkdocks   # Placeholder — substitua pela URL real do seu repositório
repo_name: seu-usuario/teste-mkdocks
edit_uri: edit/main/docs/
```

- **`repo_url`**: a URL do repositório. É esse valor que o Material usa para exibir o ícone do GitHub (ou GitLab/Bitbucket, dependendo do domínio) no cabeçalho do site, funcionando como um link direto para a página do projeto.
- **`repo_name`**: o texto exibido junto desse link no cabeçalho. Aqui está configurado como `seu-usuario/teste-mkdocks`, no formato usuário/repositório, que é a convenção mais comum — mas poderia ser qualquer rótulo, como apenas o nome do projeto.
- **`edit_uri`**: o caminho relativo, anexado a `repo_url`, usado para montar o link "editar esta página" de cada arquivo. O valor `edit/main/docs/` instrui o MkDocs a montar URLs no formato `repo_url/edit/main/docs/<caminho-do-arquivo>.md` — ou seja, "editar", na branch `main`, dentro da pasta `docs/`. É exatamente essa a URL que o GitHub usa para abrir seu editor de arquivos online.

**Importante — isto é um placeholder.** A URL `https://github.com/seu-usuario/teste-mkdocks` não aponta para um repositório real. Este projeto, na máquina em que a documentação foi escrita, ainda não tem nenhum remote Git configurado:

```text
$ git remote -v
(nenhuma saída)
```

Ou seja, não existe hoje um "GitHub deste projeto" para apontar de verdade. Os valores de `repo_url`, `repo_name` e `edit_uri` foram preenchidos com um nome de exemplo (`seu-usuario/teste-mkdocks`) apenas para que a estrutura de configuração completa pudesse ser demonstrada e testada nesta página e no `mkdocs.yml`.

Antes de publicar o seu site, você deve:

1. Criar (ou identificar) o repositório real no GitHub que hospeda este projeto.
2. Substituir `seu-usuario/teste-mkdocks` em `repo_url` e `repo_name` pelo usuário/organização e nome reais desse repositório.
3. Confirmar que o nome da branch em `edit_uri` (`main`, no exemplo) corresponde à branch padrão real do seu repositório — se ela se chamar `master` ou outra coisa, `edit_uri` deve ser ajustado de acordo.

Enquanto esses valores continuarem como placeholder, os botões de edição/visualização descritos na próxima seção vão gerar links que não funcionam (apontam para um repositório inexistente). Isso não impede o `mkdocs build`, mas também não tem utilidade real até que a URL seja corrigida.

## 3. `theme.features`: `content.action.edit` e `content.action.view`

O `mkdocs.yml` também habilita, na seção `theme.features`:

```yaml
theme:
  features:
    - content.action.edit
    - content.action.view
```

Essas duas features controlam os botões/ícones exibidos no topo de **cada página** do site:

- **`content.action.edit`**: adiciona um ícone de lápis que leva direto para a URL de edição daquele arquivo Markdown específico, montada a partir de `repo_url` + `edit_uri` + o caminho do arquivo dentro de `docs/`. Clicar nele abre o editor de arquivos do GitHub já na página certa, pronta para receber alterações e, a partir delas, abrir um Pull Request.
- **`content.action.view`**: adiciona um segundo ícone, de "ver código-fonte", que leva para a visualização do Markdown bruto daquela página no repositório (sem abrir o modo de edição) — útil para quem só quer confirmar o texto original antes de copiá-lo ou citá-lo.

Ambos os botões dependem inteiramente de `repo_url` e `edit_uri` estarem corretos: é esse par de valores que o Material usa para montar a URL exata de cada botão, para cada página, automaticamente — nenhuma configuração adicional por página é necessária.

## 4. `git-revision-date-localized`: data de última modificação

O `mkdocs.yml` configura o plugin `git-revision-date-localized` assim:

```yaml
plugins:
  - git-revision-date-localized:
      fallback_to_build_date: true
      enable_creation_date: true
      type: timeago
```

Esse plugin lê o histórico `git log` de cada arquivo em `docs/` e, a partir dele, insere na página:

- a **data da última modificação** do arquivo (sempre), obtida do commit mais recente que o alterou;
- a **data de criação** do arquivo (graças a `enable_creation_date: true`), obtida do commit mais antigo que o introduziu;
- ambas formatadas de forma relativa — "há 2 dias", "há 3 meses" — em vez de uma data absoluta, graças a `type: timeago`.

**Importante — este repositório ainda não tem nenhum commit.** Como já mostrado, `git log` neste projeto retorna:

```text
$ git log --oneline -5
fatal: your current branch 'master' does not have any commits yet
```

Sem nenhum commit, não existe histórico Git algum para o plugin consultar — nem para esta página, nem para nenhuma outra. Sem um ajuste, isso faria o `git-revision-date-localized` falhar e interromper o `mkdocs build` com um erro, já que ele não teria nenhuma data real para exibir.

É exatamente por isso que a opção `fallback_to_build_date: true` foi incluída na configuração. Com ela, nessa condição — arquivo sem histórico git —, o plugin não lança um erro fatal: em vez disso, ele usa a data e hora em que o `mkdocs build` está sendo executado como substituta (*fallback*) para a data de revisão/criação daquela página. O build continua normalmente, só que exibindo "a data de hoje" em todas as páginas, em vez da data real de cada alteração.

Assim que o repositório passar a ter commits reais — depois de um `git add .` seguido de `git commit`, por exemplo —, o plugin passa a encontrar histórico Git de verdade para cada arquivo, e as datas exibidas em cada página do site passam a refletir automaticamente o momento real da última alteração (e da criação) de cada arquivo, sem que nenhuma configuração adicional seja necessária.

## 5. GitHub Actions: o workflow real de CI/CD

O mesmo problema de "histórico Git insuficiente" descrito na seção anterior também pode acontecer durante um build automatizado em CI/CD — e, a partir de agora, ele não é mais apenas uma possibilidade teórica neste projeto. Existe um workflow real e funcional em `.github/workflows/docs.yml`, e os valores de `repo_url`, `repo_name` e `edit_uri` no `mkdocs.yml` (vistos na Seção 2) já não são mais placeholder: eles apontam para o repositório real `dataRainBR/mkdocs-documentation`, na branch `main`. Esta seção apresenta o conteúdo exato desse workflow e explica, passo a passo, o que cada etapa faz.

### 5.1 O arquivo `.github/workflows/docs.yml`

```yaml
name: Build e publica a documentação

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Clonar o repositório
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Configurar Node.js (necessário para o TypeDoc)
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Instalar TypeScript e TypeDoc
        run: npm install --global typescript typedoc

      - name: Gerar as declarações TypeScript (.d.ts)
        run: tsc -p src/calcular-media/tsconfig.json

      - name: Instalar o uv
        uses: astral-sh/setup-uv@v3

      - name: Instalar dependências Python
        run: uv sync

      - name: Instalar o Chromium do Playwright
        run: uv run playwright install --with-deps chromium

      - name: Buildar a documentação
        run: uv run mkdocs build --strict

      - name: Publicar artefato do GitHub Pages
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

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

O workflow dispara automaticamente a cada `push` na branch `main`, e também pode ser disparado manualmente a qualquer momento através do `workflow_dispatch`, direto na aba "Actions" do GitHub.

### 5.2 Passo a passo do job `build`

1. **Clonar o repositório** (`actions/checkout@v4` com `fetch-depth: 0`) — baixa o histórico completo de commits, em vez do padrão `fetch-depth: 1` (apenas o commit mais recente). Esse histórico completo é exatamente o que falta na Seção 4 quando o `git-revision-date-localized` cai no `fallback_to_build_date`: aqui, como o repositório real terá um histórico de commits de verdade (diferente da máquina local em que esta documentação foi escrita, que não tinha nenhum commit), o plugin consegue calcular as datas reais de última modificação e criação de cada página, sem recorrer ao fallback.

2. **Configurar Node.js** (`actions/setup-node@v4`) **e instalar TypeScript/TypeDoc** (`npm install --global typescript typedoc`) — este é um ponto importante: o ambiente local onde esta spec foi desenvolvida não tem Node.js instalado, o que impedia de validar, de ponta a ponta, a diretiva `::: calcular-media` (handler `typescript` do `mkdocstrings`, usada na página [Exemplos de código](exemplos-codigo.md)). O runner do GitHub Actions, por outro lado, **já vem com Node.js disponível**, e esta etapa ainda instala globalmente os pacotes `typescript` e `typedoc`. Com isso, o ambiente de CI tem tudo que falta localmente para que o handler TypeScript funcione de verdade.

3. **Gerar as declarações TypeScript** (`tsc -p src/calcular-media/tsconfig.json`) — compila o pacote `calcular-media` usando a configuração de `src/calcular-media/tsconfig.json`, produzindo o arquivo `src/calcular-media/src/index.d.ts`. É esse arquivo `.d.ts` que o handler `typescript` do `mkdocstrings` lê durante o build do MkDocs para montar a documentação da diretiva `::: calcular-media` — e ele precisa existir *antes* da etapa de build, o que é garantido pela ordem das etapas neste workflow.

4. **Instalar o `uv`** (`astral-sh/setup-uv@v3`) **e instalar as dependências Python** (`uv sync`) — preparam o ambiente Python do projeto a partir do `pyproject.toml`/`uv.lock`, da mesma forma que um desenvolvedor faria localmente ao rodar `uv sync` na própria máquina.

5. **Instalar o Chromium do Playwright** (`uv run playwright install --with-deps chromium`) — instala o navegador Chromium (e suas dependências de sistema) necessário para o plugin `exporter` do `mkdocs.yml`, que abre cada página renderizada em um navegador headless para gerar o PDF correspondente durante o build. Sem essa etapa, o build falharia ao tentar abrir um navegador que ainda não está instalado no runner.

6. **Buildar a documentação** (`uv run mkdocs build --strict`) — gera o site estático completo na pasta `site/`. A flag `--strict` faz o build falhar (em vez de só avisar) caso exista qualquer referência quebrada, como um item de `nav` apontando para um arquivo inexistente — garantindo que um site incompleto nunca chegue a ser publicado.

7. **Publicar artefato do GitHub Pages** (`actions/upload-pages-artifact@v3`, apontando para `site`) — empacota o conteúdo da pasta `site/`, já gerada pela etapa anterior, como um artefato de build do GitHub Actions, pronto para ser consumido pelo job `deploy` a seguir.

### 5.3 O job `deploy`

O job `deploy` depende do `build` através de `needs: build`, ou seja, só começa a executar se todas as etapas do `build` tiverem sido concluídas com sucesso. Ele usa o ambiente especial `github-pages` do GitHub — que expõe a URL publicada do site em `steps.deployment.outputs.page_url` — e publica o artefato gerado pelo job `build` através de `actions/deploy-pages@v4`.

Essa é, atualmente, a forma oficialmente recomendada pelo GitHub para publicar um site no GitHub Pages a partir de um workflow, substituindo o método mais antigo de fazer commit do site estático gerado em uma branch dedicada (normalmente chamada `gh-pages`). Com `actions/deploy-pages`, não existe uma branch extra para manter sincronizada: o artefato é publicado diretamente a partir do build.

### 5.4 As `permissions` do workflow

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

Essas três permissões controlam o que o token automático do workflow (`GITHUB_TOKEN`, gerado pelo próprio GitHub a cada execução) está autorizado a fazer:

- **`contents: read`**: permite ao workflow ler o código do repositório — necessário para a etapa de checkout.
- **`pages: write`**: autoriza o workflow a publicar conteúdo no GitHub Pages.
- **`id-token: write`**: permite que o job `deploy` obtenha um token OIDC de curta duração, usado internamente por `actions/deploy-pages` para autenticar a publicação.

Com essas três permissões declaradas, o workflow publica no GitHub Pages usando apenas o `GITHUB_TOKEN` automático — sem que você precise criar, configurar ou armazenar nenhum secret ou token de acesso pessoal manualmente no repositório.

### 5.5 Configuração necessária no GitHub

As etapas acima cobrem tudo o que acontece *dentro* do workflow, mas existe um passo manual que precisa ser feito uma única vez, fora dele, direto no site do GitHub:

No repositório `dataRainBR/mkdocs-documentation`, acesse **Settings → Pages → Build and deployment → Source** e selecione a opção **"GitHub Actions"** — em vez da opção padrão **"Deploy from a branch"**.

Sem essa configuração manual, o GitHub Pages não tem como aceitar o artefato publicado por `actions/deploy-pages`, mesmo que o workflow esteja configurado corretamente: a opção padrão ("Deploy from a branch") espera que o conteúdo do site seja enviado por commit a uma branch específica, não por um artefato de build.

### 5.6 Acessar a documentação publicada

Depois de selecionar **GitHub Actions** como fonte do Pages, envie as alterações para a branch `main`. O evento `push` configurado em `.github/workflows/docs.yml` inicia automaticamente o workflow de build e publicação:

```bash
git add .
git commit -m "docs: atualiza documentação"
git push origin main
```

Antes de enviar, confira `git status` e revise as alterações para garantir que apenas os arquivos desejados serão publicados. Se o primeiro push ocorreu **antes** de configurar o Pages, a alteração da fonte, por si só, não inicia uma nova execução: faça um novo push para `main` ou dispare o workflow manualmente, conforme descrito abaixo.

#### Pela interface do GitHub

1. Abra o repositório no GitHub e selecione a aba **Actions**.
2. Na lista de workflows, escolha **Build e publica a documentação**.
3. Abra a execução mais recente da branch `main`. Verifique se os jobs `build` e `deploy` terminaram com sucesso (indicados como concluídos).
4. Quando a publicação terminar, abra **Settings → Pages**. Na seção do GitHub Pages, use o endereço do site exibido para acessar a documentação.
5. Se o endereço ainda não aparecer, confirme em **Settings → Pages → Build and deployment** se a fonte está como **GitHub Actions**, e confira os detalhes e logs da execução na aba **Actions**.

Também é possível abrir a execução e acompanhar o job `deploy`; o ambiente `github-pages` pode exibir o endereço publicado como link da implantação.

#### Pelo terminal com `gh`

Autentique-se no repositório e confira as execuções recentes:

```bash
gh auth status
gh workflow list
gh run list --workflow docs.yml --branch main
```

Copie o ID da execução mais recente e acompanhe até concluir:

```bash
gh run watch ID-DA-EXECUCAO
gh run view ID-DA-EXECUCAO
```

Para abrir os detalhes da execução no navegador:

```bash
gh run view ID-DA-EXECUCAO --web
```

Depois de uma execução bem-sucedida, consulte pelo `gh` o endereço configurado no GitHub Pages:

```bash
gh api repos/dataRainBR/mkdocs-documentation/pages --jq .html_url
```

O comando imprime a URL do site; abra-a no navegador. Se a consulta retornar erro ou ainda não houver URL, confirme a configuração em **Settings → Pages** e verifique se o job `deploy` concluiu com sucesso.

Se precisar iniciar uma execução sem fazer um novo push, o workflow também pode ser iniciado manualmente porque declara `workflow_dispatch`:

```bash
gh workflow run docs.yml --ref main
gh run list --workflow docs.yml --branch main
```

O primeiro comando agenda a execução; o segundo permite localizar o ID para acompanhá-la com `gh run watch`. A publicação só estará disponível quando o build e o deploy terminarem com sucesso.

!!! note
    Adicionar um remote git ao repositório local, com `git remote add origin https://github.com/dataRainBR/mkdocs-documentation.git`, é uma ação segura e reversível: ela apenas registra, no `.git/config` local, um endereço de referência, sem enviar nenhum dado ao repositório remoto por si só. Já o commit e o push do código para esse repositório real — a etapa que de fato dispara o workflow descrito nesta seção e torna o site publicável — é uma decisão que depende de você revisar e confirmar o conteúdo a ser publicado, e deve ser executada separadamente, por fora da geração automática desta documentação.
