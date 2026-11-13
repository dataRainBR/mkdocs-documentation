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
repo_url: https://github.com/dataRainBR/mkdocs-documentation
repo_name: dataRainBR/mkdocs-documentation
edit_uri: edit/main/docs/
```

- **`repo_url`**: a URL do repositório. É esse valor que o Material usa para exibir o ícone do GitHub (ou GitLab/Bitbucket, dependendo do domínio) no cabeçalho do site, funcionando como um link direto para a página do projeto.
- **`repo_name`**: o texto exibido junto desse link no cabeçalho. Aqui usa o formato organização/repositório, mas poderia ser qualquer rótulo, como apenas o nome do projeto.
- **`edit_uri`**: o caminho relativo, anexado a `repo_url`, usado para montar o link "editar esta página" de cada arquivo. O valor `edit/main/docs/` instrui o MkDocs a montar URLs no formato `repo_url/edit/main/docs/<caminho-do-arquivo>.md` — ou seja, "editar", na branch `main`, dentro da pasta `docs/`. É exatamente essa a URL que o GitHub usa para abrir seu editor de arquivos online.

Ao usar este modelo em outro repositório, substitua a organização, o repositório e a branch pelos valores reais:

Confirme o nome da branch padrão e onde os arquivos Markdown estão localizados. Se a branch se chamar `master`, por exemplo, altere `edit_uri` para usar `edit/master/docs/`.

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

O plugin depende do histórico Git dos arquivos. Para conferir se o clone local tem histórico:

```text
git log --oneline -5
```

Se o checkout não incluir commits — por exemplo, um clone raso ou uma pasta ainda sem commits —, o plugin não terá datas históricas para exibir. A opção `fallback_to_build_date: true` permite usar a data do build como alternativa. No workflow deste projeto, `actions/checkout` usa `fetch-depth: 0` para disponibilizar o histórico completo.

## 5. GitHub Actions: o workflow real de CI/CD

Existe um workflow real em `.github/workflows/docs.yml`, e os valores de `repo_url`, `repo_name` e `edit_uri` no `mkdocs.yml` apontam para `dataRainBR/mkdocs-documentation`, na branch `main`. Esta seção apresenta o conteúdo desse workflow e explica, passo a passo, o que cada etapa faz.

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

      - name: Instalar TypeDoc
        run: npm install --global typedoc

      - name: Instalar o uv
        uses: astral-sh/setup-uv@v3

      - name: Instalar dependências Python
        run: uv sync

      - name: Instalar o Chromium do Playwright
        run: uv run playwright install --with-deps chromium

      - name: Gerar referências dos pacotes
        run: uv run python docs_preview.py --generate-references

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

1. **Clonar o repositório** (`actions/checkout@v4` com `fetch-depth: 0`) — baixa o histórico completo de commits, em vez do padrão `fetch-depth: 1` (apenas o commit mais recente). Assim, o `git-revision-date-localized` consegue calcular as datas reais de modificação e criação das páginas.

2. **Configurar Node.js** (`actions/setup-node@v4`) **e instalar TypeDoc** (`npm install --global typedoc`) — a diretiva `::: calcular-media` (handler `typescript` do `mkdocstrings`, usada na página [Exemplos de código](exemplos-codigo.md)) depende do TypeDoc. O runner do GitHub Actions também precisa ter o Node.js disponível para executar essa ferramenta.

3. **Instalar o `uv`** (`astral-sh/setup-uv@v3`) **e instalar as dependências Python** (`uv sync`) — preparam o ambiente Python do projeto a partir do `pyproject.toml`/`uv.lock`, da mesma forma que um desenvolvedor faria localmente ao rodar `uv sync` na própria máquina.

4. **Instalar o Chromium do Playwright** (`uv run playwright install --with-deps chromium`) — instala o navegador Chromium (e suas dependências de sistema) necessário para o plugin `exporter` do `mkdocs.yml`, que abre cada página renderizada em um navegador headless para gerar o PDF correspondente durante o build. Sem essa etapa, o build falharia ao tentar abrir um navegador que ainda não está instalado no runner.

5. **Gerar referências dos pacotes** (`uv run python docs_preview.py --generate-references`) — cria ou atualiza `docs/referencias.md` a partir do `pyproject.toml` (ou de `requirements.txt` como alternativa), antes que o MkDocs transforme as páginas em HTML.

6. **Buildar a documentação** (`uv run mkdocs build --strict`) — gera o site estático completo na pasta `site/`, já incluindo a página de referências atualizada. A flag `--strict` faz o build falhar (em vez de só avisar) caso exista qualquer referência quebrada, como um item de `nav` apontando para um arquivo inexistente — garantindo que um site incompleto nunca chegue a ser publicado.

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

## 6. MkDocs com GitHub Enterprise e repositórios privados

GitHub Enterprise tem duas opções de implantação, e é importante distingui-las:

- **GitHub Enterprise Cloud (GHEC)** é o serviço hospedado pelo GitHub em `github.com` ou no domínio de residência de dados da empresa. Ele permite publicar um GitHub Pages privado para uma organização Enterprise Cloud.
- **GitHub Enterprise Server (GHES)** é instalado e administrado pela própria empresa. O endereço da instância, o acesso de rede, as políticas de Actions, os runners e a disponibilidade de Pages dependem da configuração e da versão mantidas pelos administradores.

### 6.1 Apontar MkDocs para o GitHub Enterprise

No GitHub Enterprise Cloud padrão, os URLs do repositório usam `github.com`. No Enterprise Server, copie a URL HTTPS do repositório na instância da empresa. Use o mesmo host em `repo_url`; o `edit_uri` deve apontar para a branch e a pasta que contêm os Markdown:

```yaml
repo_url: https://github.empresa.example/ORGANIZACAO/REPOSITORIO
repo_name: ORGANIZACAO/REPOSITORIO
edit_uri: edit/main/docs/
```

Configure também `site_url` com o endereço que aparece nas configurações do GitHub Pages. Sites privados podem usar um subdomínio diferente do endereço público:

```yaml
site_url: https://SUBDOMINIO-PRIVADO.pages.github.io/
```

Confirme o formato do host e do caminho com a opção de clonar do repositório Enterprise e com a página **Settings → Pages** da instância. Em GHES, o administrador pode usar caminhos ou domínios próprios.

### 6.2 Construir e publicar a partir de um repositório privado

O workflow de MkDocs pode permanecer em `.github/workflows/docs.yml`. Para publicar com o workflow do GitHub Pages, ele precisa das permissões abaixo:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

`actions/checkout` usa por padrão o `GITHUB_TOKEN` para ler o próprio repositório privado. Não é necessário criar um token pessoal apenas para clonar o código do workflow. Se o build depender de outro repositório privado, use um GitHub App ou um token de acesso fino com somente a permissão de leitura necessária, guarde-o como secret e não o imprima nos logs:

```yaml
- name: Clonar dependência privada
  uses: actions/checkout@v4
  with:
    repository: ORGANIZACAO/DEPENDENCIA-PRIVADA
    token: {% raw %}${{ secrets.REPO_READ_TOKEN }}{% endraw %}
    path: dependencias/privadas
```

Além do YAML, confirme que Actions está habilitado para a organização e que as políticas Enterprise permitem as actions utilizadas, incluindo `actions/checkout`, `actions/upload-pages-artifact` e `actions/deploy-pages`. Em GHES, o administrador também precisa disponibilizar runners e acesso de rede aos repositórios e dependências do build.

Para publicar o site:

1. Abra **Settings → Pages → Build and deployment** no repositório.
2. Selecione **GitHub Actions** como fonte de publicação.
3. Quando o plano e a organização permitirem, configure a visibilidade do site como **Private** em **Settings → Pages**.
4. Envie uma alteração ou inicie o workflow manualmente e confira o job `deploy` na aba **Actions**.

**Atenção à visibilidade:** um repositório privado não torna automaticamente o site Pages privado. Um site publicado como público pode ser acessado por qualquer pessoa, mesmo que o código-fonte esteja em um repositório privado. A publicação privada do Pages está disponível no **GitHub Enterprise Cloud**; nesse modo, o site fica acessível somente a pessoas com acesso de leitura ao repositório. Não publique dados confidenciais no site, nos artefatos ou nos logs do workflow.

No GitHub Enterprise Server, não presuma que as opções de publicação privada do Enterprise Cloud estejam disponíveis. Confirme com o administrador a política de Pages, a URL interna e o modelo de autenticação aceito pela instalação.

### 6.3 Custos e limites

O GitHub Enterprise é um plano pago. A cobrança exata pode depender do contrato, da quantidade de usuários e dos produtos habilitados; consulte a página de preços e a área de faturamento do seu Enterprise. A documentação oficial de cobrança do Actions registra as cotas atuais de compute e armazenamento:

| Item do GitHub Enterprise Cloud | Referência oficial consultada em novembro de 2026 |
|---|---|
| Assinatura Enterprise | A página pública de preços lista atualmente **US$ 21 por usuário/mês** para Enterprise. Contratos empresariais podem ter condições diferentes; confira a [página de preços do GitHub](https://github.com/pricing) e o contrato da organização. |
| Compute incluído do Actions | A documentação de cobrança lista US$ 300 de uso de compute incluído por ciclo, aproximadamente 50.000 minutos em runner Linux padrão. A página de preços também apresenta 50.000 minutos mensais para Enterprise. |
| Armazenamento de artefatos | A documentação de cobrança lista 50 GB compartilhados com o armazenamento do GitHub Packages. |
| Cache do Actions | 10 GB por repositório incluídos; uso acima da franquia pode ser cobrado conforme a configuração e o uso. |
| Pages privado | Requer uma organização no GitHub Enterprise Cloud; o custo da assinatura Enterprise se aplica. |

O uso de runners hospedados pelo GitHub em repositórios privados ou internos pode consumir o compute incluído; após a franquia, o uso adicional é cobrado se houver faturamento habilitado. Os custos são atribuídos ao proprietário do repositório. A documentação atual também informa que runners self-hosted não geram cobrança de uso do Actions, mas a infraestrutura, operação e manutenção dessas máquinas continuam sendo responsabilidade da empresa. O uso padrão de runners para GitHub Pages é indicado como gratuito pela documentação de cobrança.

No GitHub Enterprise Server, licenciamento, infraestrutura e cobrança dependem do contrato e da instalação; a tabela do GitHub Enterprise Cloud não deve ser aplicada automaticamente ao GHES.

Consulte sempre os valores vigentes antes de estimar o orçamento:

- [Preços do GitHub](https://github.com/pricing)
- [Cobrança do GitHub Actions e cotas por plano](https://docs.github.com/billing/concepts/product-billing/github-actions)
- [Calculadora de preços do Actions](https://github.com/pricing/calculator?feature=actions)
- [Ver uso e faturamento dos produtos](https://docs.github.com/billing/how-tos/products/view-productlicense-use)
- [GitHub Enterprise Cloud](https://docs.github.com/enterprise-cloud@latest/admin/overview/about-github-enterprise-cloud)
- [Publicar um site GitHub Pages privado](https://docs.github.com/enterprise-cloud@latest/pages/getting-started-with-github-pages/about-privately-published-github-pages-sites)
- [Configurar uma fonte de publicação do Pages](https://docs.github.com/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

Para instruções de colaboração e versionamento, veja [Git](git.md). Para configurar e acompanhar automações, veja [GitHub Actions](github-actions.md).
