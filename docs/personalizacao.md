# Identidade visual

Esta página documenta a identidade visual DataRain aplicada ao site com [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/): paletas para os modos claro e escuro, alternador de tema, cores de interface, tipografia, logo e favicon. As cores detalhadas e os estilos de componentes estão em `docs/stylesheets/extra.css`; a configuração do tema e os recursos de imagem ficam no `mkdocs.yml` e em `docs/assets/`.

Todas as opções descritas nesta página já estão aplicadas no `mkdocs.yml` real deste projeto, reproduzido abaixo:

```yaml
theme:
  name: material
  logo: assets/logo.png
  favicon: assets/datarain-logo.ico
  font:
    text: Roboto
    code: Roboto Mono
  palette:
    - scheme: default
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-sunny
        name: "Ativar modo escuro"
    - scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-night
        name: "Ativar modo claro"
  features:
    - navigation.instant
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - navigation.footer
    - navigation.indexes
    - content.code.copy
    - content.code.annotate
    - content.tabs.link
    - search.suggest
    - search.highlight

extra_css:
  - stylesheets/extra.css
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

## 2. Paleta de cores e identidade DataRain

A paleta usa azul-petróleo e azul-marinho como cores institucionais, laranja para chamadas e interações, e tons claros para fundos e textos. Os valores de `primary` e `accent` são `custom`; as cores reais são definidas em `docs/stylesheets/extra.css`.

| Uso | Modo claro (`default`) | Modo escuro (`slate`) |
|---|---|---|
| Cor principal | `#3791A6` | `#132B40` |
| Destaque | `#F27507` | `#F27507` |
| Fundo | `#FFFFFF` | `#132B40` |
| Texto principal | `#132B40` | `#F2F2F2` |
| Fundo de código | `#F2F2F2` | `#0D1E2C` |
| Rodapé | `#132B40` | `#0D1E2C` |

O CSS também configura botões, links, seleção de texto, abas e admonitions. Para alterar a identidade visual, edite as variáveis nos seletores `[data-md-color-scheme="default"]` e `[data-md-color-scheme="slate"]` e confira os dois modos no navegador.

## 3. Seletor de tema claro e escuro

O `theme.palette` define o esquema claro `default` e o escuro `slate`, além dos ícones e rótulos acessíveis do alternador:

```yaml
theme:
  palette:
    - scheme: default
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-sunny
        name: Ativar modo escuro
    - scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-night
        name: Ativar modo claro
```

O botão com o ícone de sol ativa o modo escuro; o botão com a lua ativa o modo claro. O tema Material persiste a escolha no armazenamento local do navegador. Como o esquema claro é o primeiro da lista, ele é usado quando ainda não existe uma preferência salva.

## 4. Logo (`theme.logo`)

A chave `theme.logo` define a imagem exibida no canto superior esquerdo do site, substituindo o ícone padrão do tema. No `mkdocs.yml` deste projeto:

```yaml
theme:
  logo: assets/logo.png
```

Um ponto importante: esse caminho é **relativo à pasta `docs/`**, e não à raiz do projeto. Ou seja, `assets/logo.png` aponta para o arquivo `docs/assets/logo.png` — o MkDocs sempre resolve os caminhos de recursos do tema a partir do `docs_dir` configurado (ver [Configuração do mkdocs.yml](configuracao-yaml.md)).

### Passo a passo para adicionar um logo

1. Use uma imagem de logo em formato `.png` ou `.svg`, preferencialmente com fundo transparente.
2. Salve-a em `docs/assets/` e defina `theme.logo` com o caminho relativo a `docs/`.
3. Neste projeto, o logo DataRain fornecido em ICO foi convertido para `docs/assets/logo.png` para uso no cabeçalho.
4. Execute `uv run mkdocs build` (ou `uv run mkdocs serve`) e verifique a imagem no cabeçalho.

## 5. Favicon (`theme.favicon`)

A chave `theme.favicon` segue exatamente a mesma lógica do logo, mas define o ícone exibido na aba do navegador. No `mkdocs.yml` deste projeto:

```yaml
theme:
  favicon: assets/datarain-logo.ico
```

Assim como `theme.logo`, o caminho de `theme.favicon` também é relativo à pasta `docs/`, portanto `assets/datarain-logo.ico` corresponde ao arquivo `docs/assets/datarain-logo.ico`.

### Passo a passo para adicionar um favicon

1. Crie ou obtenha uma imagem pequena para a aba do navegador (formatos aceitos incluem `.png`, `.ico`, `.svg` e `.gif`).
2. Salve a imagem em `docs/assets/`.
3. No `mkdocs.yml`, defina `theme.favicon` apontando para esse arquivo a partir de `docs/`.
4. Execute `uv run mkdocs build` (ou `uv run mkdocs serve`) e confirme, na aba do navegador, que o ícone foi atualizado.

## 6. Convenção de pasta: `docs/assets/`

Tanto o logo quanto o favicon (e, de forma geral, qualquer imagem ou recurso estático usado nas páginas do tutorial) devem ficar guardados na subpasta `docs/assets/`. Neste projeto, `assets/logo.png` fornece o logo do cabeçalho e `assets/datarain-logo.ico` o favicon.

## 7. Folha de estilos personalizada

O `mkdocs.yml` carrega `docs/stylesheets/extra.css` por meio da opção `extra_css`. Esse arquivo centraliza as cores para os esquemas `default` e `slate`, além dos estilos dos botões, links, código, abas, seleção de texto e caixas informativas.

Os estilos das caixas seguem as categorias de admonition: note e success usam azul-petróleo; tip e important usam laranja; warning usa laranja-avermelhado. Os títulos das caixas recebem peso de fonte maior para facilitar a leitura.
