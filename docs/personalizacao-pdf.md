# Personalizar o PDF com Playwright e pypdf

Este guia explica como alterar o PDF completo gerado por `examples/expotr_to_pdf.py`: fluxo do código, estilos, cabeçalho, rodapé, paginação, tabelas, imagens, links, referências e metadados.

O conversor combina duas ferramentas com papéis diferentes:

- **Playwright com Chromium** transforma cada página HTML do MkDocs em PDF. É o Chromium que renderiza o texto, as tabelas, as imagens e o CSS.
- **pypdf** combina os PDFs temporários, acrescenta marcadores de navegação e grava os metadados do arquivo final.

Assim, o conteúdo e o layout são ajustados principalmente no Markdown e no CSS; o código Python controla a ordem, os templates de impressão e a montagem final. Para executar o fluxo completo, consulte também [Conversão local do site HTML para PDF](conversao-pdf-local.md).

## 1. Preparar e executar a conversão

Na raiz do projeto, instale as dependências, gere o HTML e converta-o:

```powershell
uv sync
uv run playwright install chromium
uv run mkdocs build
uv run python examples\expotr_to_pdf.py `
  --site-dir site `
  --output site\assets\documentacao-local.pdf
```

O script também pode ser chamado como função Python:

```python
from pathlib import Path

from examples.expotr_to_pdf import export_to_pdf

pdf_path = export_to_pdf(
    site_dir=Path("site"),
    output_pdf=Path("site/assets/documentacao-local.pdf"),
    mkdocs_config=Path("mkdocs.yml"),
    base_url="https://<usuario>.github.io/<repositorio>/",
)

print(f"PDF criado: {pdf_path}")
```

`base_url` é opcional se `site_url` já estiver configurado no `mkdocs.yml`; configure um dos dois para que links internos no PDF apontem ao endereço publicado. Neste repositório, `site_url` já aponta para o GitHub Pages do projeto.

| Argumento | Padrão | Uso |
|---|---|---|
| `--site-dir` | `site` | Diretório do HTML gerado pelo MkDocs. |
| `--output` | `site/assets/documentacao-local.pdf` | Caminho do PDF final. |
| `--config` | `mkdocs.yml` | Configuração de navegação, tema e `site_url`. |
| `--base-url` | Nenhum | URL pública usada para reescrever links internos. |

## 2. Como o código monta o documento

O ponto de entrada é `main()`, que interpreta os argumentos da linha de comando e chama `export_to_pdf()`. A função principal segue estas etapas:

1. Lê o `mkdocs.yml` com `_MkDocsConfigLoader`, que aceita as tags Python usadas pela configuração MkDocs.
2. Percorre o `nav` usando `_iter_nav()` e converte cada documento em um caminho HTML com `_html_path()`.
3. Procura em `docs_dir` outras páginas Markdown/HTML que o build gerou, mas que não estavam no `nav`.
4. Valida `site_url` ou `base_url` e prepara o logo e a imagem do rodapé como data URIs.
5. Inicia um servidor HTTP local temporário para que Chromium carregue as páginas e seus assets.
6. Para cada página, seleciona o modo de impressão, injeta `PRINT_STYLES`, espera as fontes e chama `page.pdf()`.
7. Usa `PdfReader` para abrir cada PDF temporário e `PdfWriter` para reuni-los na ordem definida.
8. Cria os marcadores de navegação, grava os metadados e fecha o servidor local.

As páginas do `nav` mantêm a ordem e os agrupamentos configurados. As páginas Markdown/HTML fora da navegação são acrescentadas ao final em ordem de caminho. `_source_title()` usa o primeiro título Markdown como nome do marcador; se não encontrar um título, deriva o nome do arquivo.

### Funções auxiliares

| Função | Responsabilidade |
|---|---|
| `_iter_nav()` | Percorre os níveis e títulos do `nav`. |
| `_html_path()` | Converte caminhos `.md` e `.html` para a rota HTML do site, respeitando `use_directory_urls`. |
| `_rewrite_internal_links()` | Reescreve links internos do HTML para `base_url` ou `site_url`. |
| `_image_data_uri()` | Lê uma imagem local e a codifica em Base64 para incorporá-la em um template. |
| `_logo_data_uri()` | Localiza o logo configurado em `theme.logo` dentro do site gerado. |
| `_header_footer_templates()` | Monta o HTML do cabeçalho e do rodapé impressos pelo Chromium. |
| `export_to_pdf()` | Renderiza páginas, combina os arquivos, cria marcadores e grava o PDF. |
| `main()` | Expõe a função por meio dos argumentos de linha de comando. |

`pypdf` não compõe o layout HTML: tabelas, diagramas, fontes e imagens do conteúdo são renderizados pelo Chromium. O pypdf entra depois, para manipular as páginas PDF já prontas.

## 3. Alterar o estilo de impressão

O CSS injetado está na constante `PRINT_STYLES` de `examples/expotr_to_pdf.py`. O estilo atual usa papel A4, fundo claro e margens reservadas ao cabeçalho e rodapé:

```css
@page {
  size: A4;
  margin: 26mm 15mm 25mm;
}

@media print {
  html, body, .md-main, .md-content {
    color: #132B40 !important;
    background: #FFFFFF !important;
    color-scheme: light;
  }

  h1, h2, h3 {
    break-after: avoid;
  }

  img, svg {
    max-width: 100%;
    height: auto;
  }

  pre {
    white-space: pre-wrap;
    overflow-wrap: anywhere;
  }
}
```

Para mudar a identidade visual, ajuste as cores, fontes, margens e seletores nessa constante. O CSS do tema e `docs/stylesheets/extra.css` também participa da impressão; `PRINT_STYLES` é aplicado por último e pode sobrescrever regras anteriores.

As opções de impressão do Chromium também influenciam o resultado:

```python
page.pdf(
    path=str(page_pdf),
    print_background=True,
    prefer_css_page_size=True,
    display_header_footer=True,
    header_template=header_template,
    footer_template=footer_template,
)
```

- `print_background=True` mantém cores e fundos.
- `prefer_css_page_size=True` respeita o tamanho definido em `@page`.
- `display_header_footer=True` ativa os templates repetidos em cada página física.

Se alterar a altura do cabeçalho ou rodapé, ajuste também as margens superior e inferior de `@page`, para evitar sobreposição com o conteúdo.

## 4. Cabeçalho e rodapé

O cabeçalho e o rodapé são HTML separado do conteúdo das páginas. A função `_header_footer_templates()` recebe as imagens já convertidas em data URIs:

```python
header_template, footer_template = _header_footer_templates(
    _logo_data_uri(site_path, config),
    _image_data_uri(site_path / "assets" / "footer.png"),
)
```

O logo vem de `theme.logo` no `mkdocs.yml` (neste projeto, `assets/logo.png`). O rodapé vem de `docs/assets/footer.png`, copiado pelo MkDocs para `site/assets/footer.png`. Como as imagens são codificadas em Base64, os templates não dependem de URLs externas.

Para alterar o texto, a largura do logo ou a faixa colorida, edite o HTML e o CSS inline em `_header_footer_templates()`. Exemplo de ajustes:

```html
<img src="{logo_data_uri}"
     style="width:38mm; max-height:12mm; object-fit:contain;">
<span>GUIA TÉCNICO DATA RAIN</span>
```

Para trocar a imagem do rodapé, mantenha o arquivo dentro de `docs/`, confirme que ele foi copiado para `site/` e passe seu caminho para `_image_data_uri()`. A função informa erro se a imagem não existir ou não for um formato reconhecido como imagem.

## 5. Controlar paginação e quebras

Use regras de impressão CSS para evitar títulos órfãos, controlar quebras e manter blocos relacionados juntos:

```css
h1, h2, h3 {
  break-after: avoid;
}

figure, blockquote, tr {
  break-inside: avoid;
}

.nova-pagina {
  break-before: page;
}
```

Em Markdown, aplique a classe diretamente ao título que deve começar uma nova página:

```markdown
## Próxima seção
{: .nova-pagina }
```

O Material for MkDocs e o Chromium podem dividir uma tabela ou um bloco muito alto mesmo com `break-inside: avoid`. Teste o PDF e prefira dividir tabelas extensas em partes menores.

Playwright fornece placeholders `pageNumber` e `totalPages` nos templates de cabeçalho/rodapé. Neste conversor, cada página HTML é impressa em um PDF temporário separado e só depois os arquivos são combinados; por isso, esses números reiniciam em cada documento de origem. Numeração contínua para o PDF combinado precisa ser adicionada após a combinação, por exemplo, com uma etapa de overlay de páginas usando pypdf.

## 6. Construir e estilizar tabelas

Tabelas são escritas em Markdown e renderizadas pelo Chromium. O exemplo abaixo usa a extensão de tabelas do MkDocs:

```markdown
| Etapa | Ferramenta | Resultado |
|---|---|---|
| 1 | MkDocs | HTML |
| 2 | Chromium | PDF de cada página |
| 3 | pypdf | PDF combinado |
```

Para controlar a aparência impressa, acrescente regras à `PRINT_STYLES`:

```css
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9pt;
}

thead {
  display: table-header-group;
}

th, td {
  border: 1px solid #D5E0E7;
  padding: 5px 7px;
  text-align: left;
  vertical-align: top;
}

th {
  color: #132B40;
  background: #EAF2F5;
}

tr {
  break-inside: avoid;
}
```

`thead { display: table-header-group; }` pede ao Chromium para repetir o cabeçalho quando uma tabela continua em outra página. Para uma tabela específica, adicione uma classe com `attr_list`:

```markdown
| Campo | Descrição |
|---|---|
| `site_dir` | Pasta do site HTML |
| `output_pdf` | Destino do PDF |
{: .tabela-configuracao }
```

E restrinja a regra:

```css
table.tabela-configuracao {
  font-size: 8pt;
}
```

O pypdf não cria células nem aplica estilos de tabela; ajuste as tabelas no Markdown/HTML e no CSS de impressão.

## 7. Inserir imagens e diagramas

Guarde as imagens de conteúdo em `docs/assets/` para que o MkDocs as copie para `site/assets/`. Em uma página Markdown na raiz de `docs/`, use:

```markdown
![Diagrama da arquitetura](assets/arquitetura.svg){ width="90%" }
```

O projeto habilita `attr_list`, então a largura pode ser ajustada por imagem. Também é possível aplicar uma classe e controlar o alinhamento pelo CSS:

```markdown
![Fluxo de dados](assets/fluxo.png){ .diagrama-pdf }
```

```css
img.diagrama-pdf {
  display: block;
  max-width: 85%;
  margin: 8mm auto;
}
```

Chromium incorpora a imagem na impressão quando ela é carregada pela página. Prefira SVG ou PNG para diagramas; arquivos editáveis, como `.drawio`, podem ser links para download, mas não são renderizados como imagem automaticamente. Se um recurso depender de JavaScript remoto ou de um `iframe`, exporte também uma versão estática para o PDF.

## 8. Links, referências e marcadores

Links externos continuam clicáveis. Para links entre páginas, configure `site_url` no `mkdocs.yml` ou informe `--base-url`:

```yaml
site_url: https://<usuario>.github.io/<repositorio>/
```

```powershell
uv run python examples\expotr_to_pdf.py `
  --base-url "https://<usuario>.github.io/<repositorio>/"
```

O endereço deve incluir o caminho do repositório, se o Pages publicar em uma subpasta, e terminar com `/`. Sem um endereço canônico, o conversor emite um aviso e os links internos do PDF podem apontar ao servidor local temporário. Os links internos são direcionados ao site publicado; não são convertidos em destinos internos entre páginas do PDF.

Referências Markdown também são renderizadas como links. Exemplo de referência nomeada:

```markdown
Consulte a documentação do [Playwright][playwright] e do [pypdf][pypdf].

[playwright]: https://playwright.dev/python/
[pypdf]: https://pypdf.readthedocs.io/
```

Os marcadores laterais do PDF são diferentes dos links: `PdfWriter.add_outline_item()` cria a navegação hierárquica com base nos grupos e títulos do `nav` do MkDocs. Cada página Markdown recebe um marcador e aponta para a primeira página física gerada para ela.

## 9. Alterar metadados e usar pypdf

O código atual grava o título no final de `export_to_pdf()`:

```python
writer.add_metadata({"/Title": "Documentação MkDocs"})
```

Para personalizar as propriedades exibidas pelo leitor de PDF, inclua outras chaves, com a barra inicial:

```python
writer.add_metadata(
    {
        "/Title": "Manual de Integração",
        "/Author": "DataRain",
        "/Subject": "Documentação técnica",
        "/Keywords": "MkDocs, Chromium, PDF",
    }
)
```

O trecho de combinação usa `PdfReader` para ler cada arquivo temporário e `PdfWriter` para acrescentar suas páginas:

```python
writer = PdfWriter()

for page_pdf in temporary_pdfs:
    for page in PdfReader(page_pdf).pages:
        writer.add_page(page)
```

Para combinar também um PDF externo em um script separado, use `append()` e grave em outro caminho:

```python
from pypdf import PdfWriter

writer = PdfWriter()
writer.append("site/assets/documentacao-local.pdf")
writer.append("docs/assets/anexo.pdf")

with open("site/assets/documentacao-com-anexo.pdf", "wb") as output:
    writer.write(output)
```

Os marcadores atuais são criados depois de cada grupo de páginas, usando `add_outline_item()`. Para alterar os títulos, edite os nomes produzidos pelo `nav` ou a chamada a `writer.add_outline_item()`; para anexar documentos extras e manter a navegação, crie também marcadores para as páginas adicionadas.

## 10. Checklist para validar alterações

Depois de editar estilo, templates ou código:

```powershell
uv run mkdocs build
uv run python examples\expotr_to_pdf.py `
  --output site\assets\documentacao-local.pdf
```

Confira propriedades básicas do PDF com pypdf:

```powershell
uv run python -c "from pypdf import PdfReader; p=PdfReader('site/assets/documentacao-local.pdf'); print('Páginas:', len(p.pages)); print('Marcadores:', len(p.outline)); print('Metadados:', p.metadata)"
```

Abra o arquivo e verifique visualmente:

- se logo e rodapé aparecem em todas as páginas;
- se o conteúdo não invade as margens;
- se tabelas repetem cabeçalho e não ficam cortadas;
- se imagens e diagramas estão legíveis;
- se marcadores, links externos e links para o site publicado funcionam;
- se metadados e acentuação estão corretos.

## Referências

- [pypdf: documentação oficial](https://pypdf.readthedocs.io/en/stable/)
- [pypdf: combinar documentos](https://pypdf.readthedocs.io/en/stable/user/merging-pdfs.html)
- [Playwright: `page.pdf()`](https://playwright.dev/python/docs/api/class-page#page-pdf)
- [Playwright: templates de cabeçalho e rodapé](https://playwright.dev/python/docs/api/class-page#page-pdf)
- [MkDocs: navegação `nav`](https://www.mkdocs.org/user-guide/configuration/#nav)
