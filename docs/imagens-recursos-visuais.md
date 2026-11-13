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

Duas extensões de Markdown já habilitadas neste projeto (ver `markdown_extensions` em [Configuração do mkdocs.yml](configuracao-yaml.md)) permitem controlar o tamanho, classes de posicionamento e a legenda de uma imagem diretamente no Markdown.

### `attr_list`: dimensionar e adicionar classes a uma imagem

A extensão `attr_list` permite anexar atributos HTML — como `width`, `height` ou classes CSS — a praticamente qualquer elemento Markdown, escrevendo-os entre chaves `{: ... }` imediatamente após o elemento. Aplicada a uma imagem, a sintaxe é:

```markdown
![Logotipo DataRain](assets/dataRain_Color-removebg-preview.png){: width="300" align="right" }
```

Aqui:

- `![Logotipo DataRain](assets/dataRain_Color-removebg-preview.png)` é a sintaxe Markdown comum de imagem: o texto entre `[` e `]` é o texto alternativo (`alt`), e o texto entre `(` e `)` é o caminho do arquivo.
- `{: width="300" align="right" }` é o bloco de atributos do `attr_list`. Neste exemplo, `width="300"` define a largura e `align="right"` usa o alinhamento legado de imagens do HTML.

O atributo HTML `align` é mantido por compatibilidade, mas é legado. Para novas páginas, prefira as classes CSS `.image-left`, `.image-right` e `.image-center` documentadas a seguir; elas permitem controlar margens e comportamento responsivo.

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

As duas extensões podem ser combinadas na mesma imagem: primeiro o `attr_list` para controlar tamanho e classe, depois o bloco `/// caption ... ///` para a legenda.

## 3. Grades e posicionamento de imagens

O projeto carrega `docs/stylesheets/extra.css` por meio de `extra_css` em `mkdocs.yml`. As classes desta seção são incluídas nesse arquivo e podem ser reutilizadas em outras páginas. Coloque os arquivos de imagem dentro de `docs/` e use caminhos relativos, como `assets/logo.png`.

### Criar uma grade responsiva

Uma grade organiza várias imagens lado a lado e ajusta o número de colunas conforme a largura disponível. O HTML abaixo usa `markdown="1"` para que as imagens e as legendas continuem sendo escritas em Markdown; a extensão `md_in_html` já está habilitada neste projeto.

Código para copiar para uma página Markdown:

````markdown
<div class="image-grid" markdown="1">

![Logo compacto](assets/logo.png)
/// caption
Versão compacta do logotipo.
///

![Logo horizontal](assets/dataRain_Color-removebg-preview.png)
/// caption
Versão horizontal do logotipo.
///

</div>
````

Resultado na página:

<div class="image-grid" markdown="1">

![Logo compacto](assets/logo.png)
/// caption
Versão compacta do logotipo.
///

![Logo horizontal](assets/dataRain_Color-removebg-preview.png)
/// caption
Versão horizontal do logotipo.
///

</div>

O CSS correspondente, já adicionado a `docs/stylesheets/extra.css`, usa `auto-fit` para criar quantas colunas couberem. O valor `14rem` define a largura mínima aproximada de cada cartão; aumente-o para exibir menos colunas ou reduza-o para exibir mais:

```css
.md-typeset .image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 14rem), 1fr));
  gap: 1rem;
  align-items: start;
  margin: 1.5rem 0;
}

.md-typeset .image-grid figure {
  min-width: 0;
  margin: 0;
}

.md-typeset .image-grid img {
  display: block;
  width: 100%;
  height: auto;
}

.md-typeset .image-grid figcaption {
  margin-top: 0.4rem;
  text-align: center;
}
```

Se precisar de exatamente três colunas em telas grandes, substitua a declaração de `grid-template-columns` por `repeat(3, minmax(0, 1fr))` e acrescente regras de media query para reduzir a quantidade em telas menores:

```css
.md-typeset .image-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

@media screen and (max-width: 50em) {
  .md-typeset .image-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media screen and (max-width: 35em) {
  .md-typeset .image-grid {
    grid-template-columns: 1fr;
  }
}
```

### Centralizar ou alinhar a imagem à esquerda ou à direita

Para centralizar uma imagem, aplique a classe `.image-center` e defina uma largura. A imagem permanece dentro da largura da página:

```markdown
![Logotipo centralizado](assets/logo.png){: width="300" .image-center}
```

Prévia:

![Logotipo centralizado](assets/logo.png){: width="300" .image-center}

Para deixar o texto fluir ao lado da imagem, use `.image-left` ou `.image-right`. Depois do trecho que deve contornar a imagem, insira o elemento de limpeza para que o conteúdo seguinte volte a ocupar a largura inteira:

Imagem à esquerda:

```markdown
![Logotipo à esquerda](assets/logo.png){: width="220" .image-left}
```

Imagem à direita, seguida de uma limpeza para o próximo conteúdo:

````markdown
![Logotipo à direita](assets/logo.png){: width="220" .image-right}

Este parágrafo flui ao lado da imagem. O alinhamento à direita funciona bem para ilustrações pequenas acompanhadas por um texto curto. Para uma galeria de várias imagens, prefira a grade responsiva em vez de floats.

<div class="image-clear"></div>

Este parágrafo começa abaixo da imagem, sem continuar ao lado dela.
````

Prévia do alinhamento à direita:

![Logotipo à direita](assets/logo.png){: width="220" .image-right}

Este texto ocupa o espaço ao lado da imagem. O exemplo é curto para deixar visível o efeito do alinhamento.

<div class="image-clear"></div>

As classes de posicionamento são implementadas assim:

```css
.md-typeset img.image-center {
  display: block;
  float: none;
  max-width: 100%;
  height: auto;
  margin: 1rem auto;
}

.md-typeset img.image-left,
.md-typeset img.image-right {
  max-width: 45%;
  height: auto;
}

.md-typeset img.image-left {
  float: left;
  margin: 0 1rem 0.75rem 0;
}

.md-typeset img.image-right {
  float: right;
  margin: 0 0 0.75rem 1rem;
}

.md-typeset .image-clear {
  clear: both;
}

@media screen and (max-width: 40em) {
  .md-typeset img.image-left,
  .md-typeset img.image-right {
    display: block;
    float: none;
    max-width: 100%;
    margin: 1rem auto;
  }
}
```

As mesmas regras já estão em `extra.css`; não é necessário copiá-las novamente nesse projeto. Se levar os exemplos para outro projeto MkDocs, copie o CSS para a folha de estilos do tema e confirme que ela está referenciada em `extra_css`.

## 4. Otimização automática de imagens com `optimize`

Além do lightbox e das legendas, o Material for MkDocs oferece um plugin nativo chamado `optimize`, que **não precisa ser instalado separadamente** (já vem embutido no pacote `mkdocs-material`, já declarado no `pyproject.toml` deste projeto — ver [Instalação](instalacao.md)). Ele é habilitado apenas adicionando uma entrada em `plugins`:

```yaml
plugins:
  - optimize
```

Quando habilitado, o `optimize` processa automaticamente, durante o `mkdocs build`, todas as imagens referenciadas dentro de `docs/`: ele comprime o arquivo original e pode gerar variantes otimizadas (por exemplo, em formato `.webp`), reduzindo o tamanho final dos arquivos de imagem servidos pelo Documentation_Site — sem que o autor do conteúdo precise rodar nenhuma ferramenta externa de compressão de imagens antes de salvar o arquivo em `docs/assets/`.

Este projeto não habilita `optimize` no `mkdocs.yml` atualmente. O recurso é opcional e deve ser ativado quando a otimização automática das imagens for necessária; para isso, acrescente `optimize` à lista de `plugins` e valide o resultado do build antes de publicar.
