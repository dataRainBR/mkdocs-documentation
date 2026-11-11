# Personalização

Depois de configurar a navegação, os plugins e as extensões do `mkdocs.yml` (ver [Configuração do mkdocs.yml](configuracao-yaml.md)), chegou a hora de ajustar a aparência do site. O tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) é altamente customizável através da seção `theme` do `mkdocs.yml`: é ali que configuramos a fonte do texto, a paleta de cores, o logo e o favicon.

Todas as opções descritas nesta página já estão aplicadas no `mkdocs.yml` real deste projeto, reproduzido abaixo:

```yaml
theme:
  name: material
  logo: assets/logo.png
  favicon: assets/favicon.png
  font:
    text: Roboto
    code: Roboto Mono
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: "Mudar para modo escuro"
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: "Mudar para modo claro"
```

Vamos entender cada parte, uma por uma.

## 1. Fontes (`theme.font`)

O Material for MkDocs usa o [Google Fonts](https://fonts.google.com/) para carregar as fontes do site. A chave `theme.font` aceita duas subchaves:

- `text`: a fonte usada no corpo do texto (títulos, parágrafos, menu, etc.).
- `code`: a fonte monoespaçada usada nos blocos de código.

No `mkdocs.yml` deste projeto, a configuração é:

```yaml
theme:
  font:
    text: Roboto
    code: Roboto Mono
```

Isso significa que todo o texto normal das páginas é renderizado com a fonte **Roboto**, e todo trecho de código (inline ou em bloco) usa a fonte monoespaçada **Roboto Mono**.

### Passo a passo para trocar a fonte

1. Escolha um nome de fonte disponível no [Google Fonts](https://fonts.google.com/). O Material for MkDocs busca a fonte diretamente pelo nome, sem necessidade de baixar arquivos manualmente. Alguns exemplos de fontes suportadas: `Roboto`, `Open Sans`, `Lato`, `Fira Sans`, `Noto Sans`, `Inter`, `Merriweather` (serifada) e, para código, `Roboto Mono`, `Fira Code`, `Source Code Pro`, `JetBrains Mono`.
2. Edite as chaves `theme.font.text` e/ou `theme.font.code` no `mkdocs.yml`, substituindo o valor pelo nome exato da fonte escolhida (respeitando maiúsculas/minúsculas e espaços, por exemplo `"Fira Sans"`).
3. Salve o arquivo e execute `uv run mkdocs serve` para visualizar a mudança: o MkDocs recarrega a página automaticamente e já exibe a nova fonte.

!!! note "Desativar fontes do Google"
    Se o site precisar funcionar sem acesso à internet para carregar fontes externas (ex.: ambientes totalmente offline), é possível definir `theme.font: false` no `mkdocs.yml`. Nesse caso, o Material usa as fontes padrão do sistema do visitante.

## 2. Paleta de cores (`theme.palette`)

A chave `theme.palette` controla as cores do tema e também o alternador de modo claro/escuro. Ela pode receber um único objeto (uma cor fixa) ou, como neste projeto, uma **lista** com duas variantes: uma para modo claro e outra para modo escuro.

```yaml
theme:
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: "Mudar para modo escuro"
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: "Mudar para modo claro"
```

Cada item dessa lista tem os seguintes campos:

- **`media`**: uma media query CSS que detecta a preferência de tema do sistema operacional do visitante. `"(prefers-color-scheme: light)"` casa com sistemas configurados para modo claro, e `"(prefers-color-scheme: dark)"` com modo escuro. Assim, o site já abre no modo preferido do usuário, sem exigir nenhum clique.
- **`scheme`**: o esquema de cores base do Material. `default` é o esquema claro (fundo branco, texto escuro); `slate` é o esquema escuro (fundo escuro, texto claro). Essas são as duas únicas opções de `scheme` disponíveis — a variação de cor em si vem de `primary`/`accent`.
- **`primary`**: a cor principal do tema, usada no cabeçalho, na barra de navegação lateral e em outros elementos de destaque. Aceita qualquer cor da [paleta do Material Design](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/#primary-color), como `red`, `pink`, `purple`, `deep purple`, `indigo`, `blue`, `teal`, `green`, `orange`, `brown`, entre outras.
- **`accent`**: a cor de destaque usada em links, botões e elementos interativos ao passar o mouse. Também aceita qualquer cor da mesma paleta.
- **`toggle`**: define o botão que permite ao visitante alternar manualmente entre os modos claro e escuro, mesmo que o sistema já tenha detectado uma preferência via `media`. Tem duas subchaves:
    - `icon`: o ícone exibido no botão, referenciando um dos ícones embutidos do Material (prefixo `material/...`). Aqui, `material/brightness-7` representa um "sol" (ação de ir para o modo escuro) e `material/brightness-4` representa uma "lua" (ação de voltar ao modo claro).
    - `name`: o texto acessível (tooltip) exibido ao passar o mouse sobre o botão — por isso está em português no projeto ("Mudar para modo escuro" / "Mudar para modo claro").

### Passo a passo para trocar a cor primária

Por exemplo, para trocar a cor primária de `indigo` para `teal`:

1. Abra o `mkdocs.yml` e localize a seção `theme.palette`.
2. Em **cada** variante da lista (tanto a de `media: light` quanto a de `media: dark`), troque o valor de `primary: indigo` para `primary: teal`. É importante alterar as duas variantes, a menos que você queira cores diferentes no modo claro e no modo escuro.
3. Opcionalmente, troque também `accent: indigo` para outra cor de destaque, como `accent: orange`, se quiser que os links e botões tenham uma cor diferente da cor principal.
4. Salve o arquivo e execute `uv run mkdocs serve` (ou recarregue a página, se o servidor já estiver rodando) para ver a nova cor aplicada imediatamente.

!!! tip "Lista completa de cores"
    A lista oficial e atualizada de valores aceitos para `primary` e `accent` está na documentação do Material: [Changing the colors](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/).

## 3. Modos claro e escuro

A seção anterior mostrou que `theme.palette` é uma lista com duas variantes, uma para `media: "(prefers-color-scheme: light)"` e outra para `media: "(prefers-color-scheme: dark)"`. É justamente essa lista, reproduzida de forma resumida a seguir, que faz o site suportar modo claro e modo escuro:

```yaml
theme:
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: "Mudar para modo escuro"
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: "Mudar para modo claro"
```

Esse comportamento combina três mecanismos, que trabalham juntos:

- **Detecção automática.** Cada entrada de `theme.palette` tem uma `media` query (`"(prefers-color-scheme: light)"` ou `"(prefers-color-scheme: dark)"`), que é a forma padrão do navegador de expor a preferência de tema já configurada no sistema operacional do visitante. Por isso, na primeira visita ao site — antes de qualquer clique —, a página já é renderizada no modo correspondente a essa preferência do sistema, sem exigir nenhuma ação do visitante.
- **Botão de alternância manual.** Cada variante também define um `toggle`, com um `icon` (o ícone do botão) e um `name` (o texto do tooltip exibido ao passar o mouse). Esse `toggle` cria um botão no cabeçalho do site que permite ao visitante trocar manualmente de modo, mesmo que o sistema operacional já tenha indicado uma preferência diferente. No `mkdocs.yml` deste projeto, o botão mostra o ícone de sol (`material/brightness-7`, "Mudar para modo escuro") quando o site está no modo claro, e o ícone de lua (`material/brightness-4`, "Mudar para modo claro") quando está no modo escuro.
- **Persistência da escolha entre visitas.** Quando o visitante usa o botão de alternância manual, o tema Material salva essa escolha no `localStorage` do navegador. Em visitas futuras, o site abre direto no modo escolhido anteriormente, em vez de voltar a detectar a preferência via `prefers-color-scheme` a cada carregamento de página — e isso continua valendo até que o `localStorage` seja limpo ou até que um navegador ou dispositivo diferente seja usado, momento em que a detecção automática volta a valer como ponto de partida.

## 4. Logo (`theme.logo`)

A chave `theme.logo` define a imagem exibida no canto superior esquerdo do site, substituindo o ícone padrão do tema. No `mkdocs.yml` deste projeto:

```yaml
theme:
  logo: assets/logo.png
```

Um ponto importante: esse caminho é **relativo à pasta `docs/`**, e não à raiz do projeto. Ou seja, `assets/logo.png` aponta para o arquivo `docs/assets/logo.png` — o MkDocs sempre resolve os caminhos de recursos do tema a partir do `docs_dir` configurado (ver [Configuração do mkdocs.yml](configuracao-yaml.md)).

### Passo a passo para adicionar um logo

1. Crie ou obtenha uma imagem para o logo (formatos comuns: `.png`, `.svg` ou `.jpg`). O Material recomenda uma imagem quadrada ou com fundo transparente, para encaixar bem no cabeçalho.
2. Salve essa imagem dentro da pasta `docs/assets/`, por exemplo como `docs/assets/logo.png`.
3. No `mkdocs.yml`, defina `theme.logo` apontando para esse arquivo **a partir de `docs/`**: `theme.logo: assets/logo.png`.
4. Execute `uv run mkdocs build` (ou `uv run mkdocs serve`) e verifique no cabeçalho do site que a nova imagem substituiu o ícone padrão.

## 5. Favicon (`theme.favicon`)

A chave `theme.favicon` segue exatamente a mesma lógica do logo, mas define o ícone exibido na aba do navegador. No `mkdocs.yml` deste projeto:

```yaml
theme:
  favicon: assets/favicon.png
```

Assim como `theme.logo`, o caminho de `theme.favicon` também é relativo à pasta `docs/`, portanto `assets/favicon.png` corresponde ao arquivo `docs/assets/favicon.png`.

### Passo a passo para adicionar um favicon

1. Crie ou obtenha uma imagem pequena e quadrada (formatos aceitos: `.png`, `.ico`, `.svg`, `.gif`; o tamanho usual é algo como 32×32 ou 48×48 pixels).
2. Salve essa imagem em `docs/assets/`, por exemplo como `docs/assets/favicon.png` (ou `docs/assets/favicon.ico`).
3. No `mkdocs.yml`, defina `theme.favicon` apontando para esse arquivo a partir de `docs/`: `theme.favicon: assets/favicon.png`.
4. Execute `uv run mkdocs build` (ou `uv run mkdocs serve`) e confirme, na aba do navegador, que o ícone foi atualizado.

## 6. Convenção de pasta: `docs/assets/`

Tanto o logo quanto o favicon (e, de forma geral, qualquer imagem ou recurso estático usado nas páginas do tutorial) devem ficar guardados na subpasta `docs/assets/`. Essa é a convenção adotada neste projeto: manter todos os arquivos binários de personalização em um único lugar, separado dos arquivos Markdown de conteúdo, facilitando tanto a organização quanto a referência por caminhos relativos (`assets/logo.png`, `assets/favicon.png`, etc.).

## 7. Observação importante: este projeto ainda não tem imagens reais

Vale destacar: no momento, a pasta `docs/assets/` deste projeto **não contém nenhum arquivo de imagem binário real** — apenas um `README.md` explicando a convenção da pasta. Ou seja, os caminhos `assets/logo.png` e `assets/favicon.png` configurados no `mkdocs.yml` ainda **não correspondem a arquivos existentes**.

Isso não é um problema para o funcionamento do site: o MkDocs e o tema Material **não falham o build** por causa disso. Quando `theme.logo` ou `theme.favicon` apontam para um arquivo que não existe, o Material simplesmente ignora a configuração e continua usando o ícone padrão do tema (o logo-livro do Material e o favicon padrão do MkDocs) até que uma imagem real seja adicionada.

Portanto, você pode seguir todo este tutorial normalmente, sem precisar criar nenhuma imagem agora. Quando quiser personalizar visualmente o site com uma identidade própria, basta seguir os passos a passo das seções 4 e 5 acima: salvar os arquivos reais em `docs/assets/logo.png` e `docs/assets/favicon.png`, e o site passará a exibi-los automaticamente.
