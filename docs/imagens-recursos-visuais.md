# Imagens e recursos visuais

Além de configurar o logo e o favicon do tema em [Identidade visual](personalizacao.md), também é possível inserir imagens diretamente no conteúdo das páginas Markdown. O [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) e seus plugins oferecem recursos para ampliar, dimensionar e legendar essas imagens.

Esta página cobre três formas de enriquecer imagens no Documentation_Site:

1. **Lightbox** com o plugin `mkdocs-glightbox`: zoom em tela cheia ao clicar em qualquer imagem.
2. **Legendas e alinhamento** com as extensões `attr_list` e `pymdownx.blocks.caption`.
3. **Otimização automática** de imagens com o recurso nativo `optimize` do tema Material.

## 1. Lightbox com `mkdocs-glightbox`

### Instalação

O plugin de lightbox não vem embutido no MkDocs nem no Material; é um pacote Python separado, instalado com:

```bash
uv add mkdocs-glightbox
```

### Configuração

Depois de instalado, basta registrá-lo na seção `plugins` do `mkdocs.yml`:

```yaml
plugins:
  - glightbox
```

Este projeto já tem exatamente essa entrada configurada (ver [Configuração do mkdocs.yml](configuracao-yaml.md)).

### O que o plugin faz

O `glightbox` atua no momento do `mkdocs build`: ele percorre o HTML gerado de **cada página** e envolve **toda imagem inserida via sintaxe Markdown** (`![alt](caminho)`) em um comportamento de lightbox — ou seja, ao clicar na imagem, ela se expande em uma camada de zoom sobre o restante da página, com suporte a navegação entre as imagens da mesma página e fechamento ao clicar fora ou pressionar <kbd>Esc</kbd>.

O ponto mais importante é que **isso acontece automaticamente para qualquer imagem Markdown**, sem exigir nenhuma marcação especial por imagem. Não é necessário envolver a imagem em um link, adicionar uma classe CSS ou qualquer atributo extra: basta que a imagem exista como `![alt](caminho)` em qualquer página do site, e o `glightbox` já cuida do resto durante o build.

### Exemplo: ampliar uma imagem

A imagem abaixo usa o arquivo DataRain `dataRain_Color-removebg-preview.png`, salvo em `docs/assets/`. Como ela está escrita com a sintaxe Markdown comum, o `glightbox` permite clicar nela para abrir a visualização ampliada:

![Logotipo DataRain](assets/dataRain_Color-removebg-preview.png){: width="500" }
/// caption
Logo DataRain exibido como imagem de conteúdo. Clique na imagem para ampliá-la.
///

### Como o lightbox funciona nas demais imagens

O mesmo comportamento se aplica automaticamente às demais imagens Markdown do site. Não é necessário envolver cada imagem em um link nem adicionar configurações especiais do `glightbox`.

## 2. Legendas e alinhamento com `attr_list` e `pymdownx.blocks.caption`

Duas extensões de Markdown já habilitadas neste projeto (ver `markdown_extensions` em [Configuração do mkdocs.yml](configuracao-yaml.md)) permitem controlar o tamanho, o alinhamento e a legenda de uma imagem diretamente no Markdown, sem recorrer a HTML bruto.

### `attr_list`: dimensionar e alinhar uma imagem

A extensão `attr_list` permite anexar atributos HTML — como `width`, `height`, `align` ou classes CSS — a praticamente qualquer elemento Markdown, escrevendo-os entre chaves `{: ... }` imediatamente após o elemento. Aplicada a uma imagem, a sintaxe é:

```markdown
![Logotipo DataRain](assets/dataRain_Color-removebg-preview.png){: width="300" align="right" }
```

Aqui:

- `![Logotipo DataRain](assets/dataRain_Color-removebg-preview.png)` é a sintaxe Markdown comum de imagem: o texto entre `[` e `]` é o texto alternativo (`alt`), e o texto entre `(` e `)` é o caminho do arquivo.
- `{: width="300" align="right" }` é o bloco de atributos do `attr_list`. Cada par `atributo="valor"` dentro das chaves é copiado para a tag `<img>` gerada. Neste exemplo, `width="300"` limita a largura da imagem a 300 pixels, e `align="right"` a alinha à direita do texto ao redor (fazendo o texto da página fluir ao lado dela, como em um documento tradicional).

O mesmo bloco de atributos funciona para qualquer outro elemento Markdown (parágrafos, cabeçalhos, links), não apenas imagens — mas aqui o uso mais comum é justamente controlar dimensão e alinhamento de imagens sem escrever HTML manualmente.

### `pymdownx.blocks.caption`: adicionar uma legenda

A extensão `pymdownx.blocks.caption` adiciona uma legenda visível abaixo de uma imagem (ou de outro bloco), usando a sintaxe de blocos `///` do pymdown-extensions:

```markdown
![Logotipo DataRain](assets/dataRain_Color-removebg-preview.png)
/// caption
Figura 1 — Logo DataRain inserido no conteúdo da página.
///
```

A leitura dessa sintaxe é:

- A primeira linha é a imagem comum, exatamente como antes.
- O bloco que começa em `/// caption` e termina no `///` de fechamento é um **bloco pymdownx** do tipo `caption`. Na linha de abertura, o texto logo depois de `///` (`caption`) identifica o tipo de bloco; todo o texto entre essa linha e o `///` final é o conteúdo da legenda.
- No HTML gerado, o pymdownx.blocks.caption associa automaticamente essa legenda à imagem (ou bloco) imediatamente anterior, renderizando-a como um elemento `<figcaption>` — o equivalente semântico de uma legenda de figura em HTML.

As duas extensões podem ser combinadas na mesma imagem: primeiro o `attr_list` para controlar tamanho/alinhamento, depois o bloco `/// caption ... ///` para a legenda.

## 3. Otimização automática de imagens com `optimize`

Além do lightbox e das legendas, o Material for MkDocs oferece um plugin nativo chamado `optimize`, que **não precisa ser instalado separadamente** (já vem embutido no pacote `mkdocs-material`, já declarado no `pyproject.toml` deste projeto — ver [Instalação](instalacao.md)). Ele é habilitado apenas adicionando uma entrada em `plugins`:

```yaml
plugins:
  - optimize
```

Quando habilitado, o `optimize` processa automaticamente, durante o `mkdocs build`, todas as imagens referenciadas dentro de `docs/`: ele comprime o arquivo original e pode gerar variantes otimizadas (por exemplo, em formato `.webp`), reduzindo o tamanho final dos arquivos de imagem servidos pelo Documentation_Site — sem que o autor do conteúdo precise rodar nenhuma ferramenta externa de compressão de imagens antes de salvar o arquivo em `docs/assets/`.

Este projeto não habilita `optimize` no `mkdocs.yml` atualmente. O recurso é opcional e deve ser ativado quando a otimização automática das imagens for necessária; para isso, acrescente `optimize` à lista de `plugins` e valide o resultado do build antes de publicar.
