# Exportar a documentação MkDocs para PDF

O MkDocs gera o site em HTML. Para produzir PDFs com o mesmo conteúdo, este projeto usa o plugin [`mkdocs-exporter`](https://github.com/adrienbrignon/mkdocs-exporter), que renderiza as páginas com um navegador controlado pelo Playwright. O plugin pode criar um PDF por página e, opcionalmente, reunir as páginas em um único PDF.

Neste projeto, o plugin e o Playwright já estão declarados em `pyproject.toml`, e a exportação de PDFs individuais já está habilitada em `mkdocs.yml`. Para gerar um arquivo único com toda a documentação, também é necessário configurar o agregador, conforme o passo 3.

## 1. Como funciona a exportação

O processo é:

1. O MkDocs converte os arquivos Markdown em páginas HTML.
2. O `mkdocs-exporter` abre essas páginas em um navegador sem interface gráfica, usando Playwright.
3. O navegador imprime cada página em PDF.
4. Se o agregador estiver habilitado, o plugin reúne os PDFs das páginas em um documento.
5. Os arquivos resultantes ficam dentro da pasta de saída do site, normalmente `site/`.

O HTML continua sendo o site publicado; o PDF é um formato adicional para baixar ou distribuir.

## 2. Instalar as dependências

Em um projeto novo, instale o MkDocs, o plugin e o Playwright com o gerenciador de pacotes escolhido. Para um projeto que usa `uv`:

```powershell
uv add mkdocs mkdocs-exporter playwright
```

Neste repositório essas dependências já estão listadas em `pyproject.toml`. Para sincronizar o ambiente:

```powershell
uv sync
```

O Playwright precisa de um navegador instalado. No Windows, instale o Chromium:

```powershell
uv run playwright install chromium
```

No Ubuntu usado por uma GitHub Action, instale o Chromium e as dependências do sistema:

```yaml
- name: Instalar o Chromium do Playwright
  run: uv run playwright install --with-deps chromium
```

## 3. Habilitar PDFs individuais e o PDF completo

O plugin é configurado na lista `plugins` do `mkdocs.yml`. Mantenha os outros plugins do projeto e atualize a entrada existente de `exporter`; não crie uma segunda entrada `exporter`.

```yaml
plugins:
  # Mantenha aqui search, mkdocstrings e os demais plugins já usados.
  - exporter:
      formats:
        pdf:
          enabled: true
          aggregator:
            enabled: true
            output: documentacao-completa.pdf
```

Com `enabled: true`, o plugin também gera PDFs individuais para as páginas incluídas. O bloco `aggregator` combina essas páginas em `site/documentacao-completa.pdf` após o build.

Se estiver usando capas individuais e quiser controlar quais aparecem na combinação, configure `covers`:

```yaml
          aggregator:
            enabled: true
            output: documentacao-completa.pdf
            covers: limits
```

O modo `limits` mantém a capa inicial do primeiro documento e a capa final do último. Outras opções incluem `all`, `none`, `front`, `back` e `book`. Sem capas configuradas, deixe essa opção de fora.

Por padrão, todas as páginas são consideradas para exportação. Para excluir uma página específica, adicione front matter no início do arquivo Markdown:

```markdown
---
pdf: false
---

# Página que só deve aparecer no site HTML
```

## 4. Personalizar o layout de impressão

Crie uma folha de estilos para PDF. Ela é separada do CSS usado na tela e pode definir tamanho do papel, margens, paginação e comportamento de imagens e blocos de código.

Por exemplo, crie `docs/stylesheets/pdf.scss`:

```scss
@page {
  size: A4;
  margin: 18mm 15mm 20mm;

  @bottom-right {
    content: counter(page);
    color: #526B7A;
  }
}

@media print {
  h1,
  h2,
  h3 {
    break-after: avoid;
  }

  img,
  svg {
    max-width: 100%;
    height: auto;
  }

  table,
  blockquote {
    break-inside: avoid;
  }

  pre {
    white-space: pre-wrap;
    overflow-wrap: anywhere;
  }
}
```

Registre o arquivo na configuração do exportador:

```yaml
  - exporter:
      formats:
        pdf:
          enabled: true
          stylesheets:
            - docs/stylesheets/pdf.scss
          aggregator:
            enabled: true
            output: documentacao-completa.pdf
```

Se o YAML já tiver uma entrada de `exporter`, acrescente `stylesheets` dentro de `formats.pdf` nela. Teste o resultado com tabelas largas, imagens, diagramas e exemplos de código extensos; CSS de impressão pode exigir ajustes diferentes do CSS do site.

## 5. Adicionar uma capa opcional

O plugin aceita modelos HTML/Jinja para capas. Por exemplo, crie `docs/overrides/pdf-capa.html.j2`:

```html
<section class="pdf-cover">
  <h1>{{ config.site_name }}</h1>
  <p>{{ page.title }}</p>
</section>
```

Configure o modelo no mesmo bloco do PDF:

```yaml
  - exporter:
      formats:
        pdf:
          enabled: true
          covers:
            front: docs/overrides/pdf-capa.html.j2
          aggregator:
            enabled: true
            output: documentacao-completa.pdf
            covers: limits
```

Ajuste a aparência da capa na folha `pdf.scss`. Para uma documentação que não precisa de capa, omita `covers` e mantenha a configuração mais simples.

## 6. Gerar e conferir os arquivos localmente

Depois de instalar dependências e configurar o navegador, execute o build:

```powershell
uv run mkdocs build --strict
```

Confira se o site e o PDF completo foram gerados:

```powershell
Test-Path site\index.html
Test-Path site\documentacao-completa.pdf
Get-Item site\documentacao-completa.pdf | Select-Object Name, Length
```

Abra `site/documentacao-completa.pdf` em um leitor de PDF e confira:

- se as páginas aparecem na ordem da navegação;
- se caracteres acentuados, links, imagens e fontes estão corretos;
- se tabelas e blocos de código não ultrapassam as margens;
- se os diagramas estão legíveis e as quebras de página são adequadas.

Para documentos longos, prefira diagramas SVG ou imagens estáticas. Diagramas interativos, `iframe`s e conteúdo que depende de serviços externos podem não ser adequados para impressão.

## 7. Publicar o PDF com o GitHub Pages

O fluxo do GitHub Actions deve instalar o navegador, executar o build e publicar toda a pasta `site/`. Como o PDF agregado é criado dentro dessa pasta, ele acompanha o HTML no artefato do Pages.

O workflow deste projeto já possui passos para instalar Node.js e TypeDoc, sincronizar o `uv`, instalar Chromium, executar `mkdocs build --strict` e publicar `site/`. Portanto, depois de habilitar o agregador em `mkdocs.yml`, o PDF será incluído na publicação do Pages.

Além do PDF criado pelo agregador, este projeto gera pela Action um PDF completo com cabeçalho, faixa de rodapé e botão de download na documentação. Esse fluxo usa o conversor local e está documentado em [Conversão PDF local](conversao-pdf-local.md); o arquivo é publicado em `assets/documentacao-local.pdf` e também fica disponível nos artefatos da execução da Action.

Um fluxo mínimo para um projeto semelhante é:

```yaml
- name: Instalar dependências Python
  run: uv sync

- name: Instalar o Chromium do Playwright
  run: uv run playwright install --with-deps chromium

- name: Gerar o site e os PDFs
  run: uv run mkdocs build --strict

- name: Publicar o site, incluindo o PDF
  uses: actions/upload-pages-artifact@v3
  with:
    path: site
```

Após a publicação, o PDF fica disponível na raiz do site, por exemplo, em `https://<usuario>.github.io/<repositorio>/documentacao-completa.pdf`. Ajuste o endereço ao domínio e ao caminho configurados para o Pages.

## 8. Problemas comuns

### O build informa que não encontrou o navegador

Instale o Chromium na máquina local ou adicione o passo de instalação do Playwright ao workflow:

```powershell
uv run playwright install chromium
```

### O site é gerado, mas o PDF completo não aparece

Confirme se `aggregator.enabled` está dentro de `plugins → exporter → formats → pdf`, se o caminho `output` está correto e se o build terminou sem erros.

### Uma página não aparece no PDF

Verifique se ela tem front matter `pdf: false`. Essa opção desativa a exportação da página.

### Diagramas ou imagens ficam cortados

Use SVG ou PNG estático, limite a largura no CSS de impressão e evite depender de `iframe`s ou de JavaScript externo. Gere novamente o PDF após cada ajuste no estilo.

### O build falha antes de começar a exportação

O exportador depende de um build MkDocs bem-sucedido. Neste projeto, páginas TypeScript também requerem Node.js e o comando `typedoc`; o workflow configura essas dependências antes de executar MkDocs. Em outros projetos, resolva primeiro os erros do build HTML.

## Referências

- [MkDocs Exporter: geração de PDFs](https://adrienbrignon.github.io/mkdocs-exporter/configuration/generating-pdf-documents/)
- [MkDocs Exporter: agregar páginas em um PDF](https://adrienbrignon.github.io/mkdocs-exporter/configuration/generating-pdf-documents/#combining-pages-into-a-single-pdf-document)
- [Playwright: instalação de navegadores](https://playwright.dev/python/docs/browsers)
- [MkDocs: configuração](https://www.mkdocs.org/user-guide/configuration/)
