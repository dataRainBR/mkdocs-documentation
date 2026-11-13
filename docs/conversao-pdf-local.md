# Conversão local do site HTML para PDF

Esta página ensina a converter toda a documentação HTML já gerada pelo MkDocs em um PDF único, mantendo a ordem da navegação, o estilo claro, imagens e diagramas estáticos. O script inclui cabeçalho com o logo DataRain, rodapé em todas as páginas e marcadores no PDF para as seções.

O conversor é útil quando você quer processar localmente o site pronto ou gerar um PDF com marcadores próprios. Para a geração integrada diretamente ao `mkdocs build`, veja também [Exportação para PDF](exportacao-para-pdf.md), que documenta o `mkdocs-exporter` e seu agregador.

<a class="md-button md-button--primary" href="../assets/documentacao-local.pdf" download>Baixar a documentação completa em PDF</a>

## 1. Como a conversão funciona

O arquivo `examples/expotr_to_pdf.py`:

1. Lê a ordem e os títulos de `nav` no `mkdocs.yml`.
2. Acrescenta as demais páginas Markdown e HTML encontradas em `docs_dir` que não estejam listadas em `nav`.
3. Abre as páginas HTML do diretório `site/` em Chromium por um servidor HTTP local.
4. Usa as folhas de estilo, imagens, fontes e diagramas já publicados no site gerado.
5. Imprime cada página em PDF com o estilo claro e junta os resultados.
6. Repete o cabeçalho e o rodapé em todas as páginas físicas e cria marcadores hierárquicos.
7. Grava o PDF em `site/assets/documentacao-local.pdf`, caminho usado pelo botão de download.

As páginas listadas em `nav` aparecem primeiro e mantêm sua ordem e agrupamento. Outras páginas Markdown/HTML que o MkDocs tenha gerado são acrescentadas depois, em ordem de caminho. O servidor HTTP é local e temporário; ele serve os arquivos durante a conversão e é encerrado ao final. O HTML original não é modificado.

## 2. Instalar os requisitos

O script utiliza Playwright para renderizar as páginas, PyYAML para ler a navegação e `pypdf` para combinar os PDFs. As três bibliotecas estão declaradas diretamente nas dependências deste projeto; Playwright já era usado pelo `mkdocs-exporter`.

Sincronize as dependências e instale o Chromium:

```powershell
uv sync
uv run playwright install chromium
```

Se estiver usando outro projeto, adicione as bibliotecas diretamente:

```powershell
uv add playwright pypdf pyyaml
uv run playwright install chromium
```

## 3. Gerar primeiro o site HTML

O conversor não compila Markdown: ele lê HTML que já foi gerado. Na raiz do projeto, execute:

```powershell
uv run mkdocs build
uv run python examples\expotr_to_pdf.py `
  --site-dir site `
  --output site\assets\documentacao-local.pdf
```

Confirme que o diretório e as páginas principais existem:

```powershell
Test-Path site\index.html
Get-ChildItem site -Filter *.html -Recurse | Select-Object -First 10 FullName
```

Se o build falhar, corrija os erros do MkDocs antes de executar a conversão.

## 4. Definir o endereço do site para os links internos

Links externos são preservados como links clicáveis no PDF. Para que links entre páginas apontem ao site publicado, configure `site_url` no `mkdocs.yml` ou informe `base_url` ao executar o script.

Exemplo de configuração — substitua pelo endereço real do seu site:

```yaml
site_url: https://<usuario>.github.io/<repositorio>/
```

Ou informe o endereço diretamente no comando. O `base_url` deve terminar com `/`:

```powershell
uv run python examples\expotr_to_pdf.py `
  --site-dir site `
  --output site\assets\documentacao-local.pdf `
  --config mkdocs.yml `
  --base-url "https://<usuario>.github.io/<repositorio>/"
```

Se o endereço não for informado, o script avisa que os links internos podem não apontar ao site publicado.

## 5. Executar a função Python diretamente

O script também pode ser importado e usado em outro código Python:

```python
from pathlib import Path

from examples.expotr_to_pdf import export_to_pdf

arquivo_pdf = export_to_pdf(
    site_dir=Path("site"),
    output_pdf=Path("site/assets/documentacao-local.pdf"),
    mkdocs_config=Path("mkdocs.yml"),
    base_url="https://<usuario>.github.io/<repositorio>/",
)

print(f"PDF criado em: {arquivo_pdf}")
```

Os parâmetros são:

| Parâmetro | Finalidade |
|---|---|
| `site_dir` | Pasta do site HTML gerado; por padrão, `site/`. |
| `output_pdf` | Destino do PDF; por padrão, `site/assets/documentacao-local.pdf`. |
| `mkdocs_config` | Caminho para o `mkdocs.yml`, usado para ler a navegação e `site_url`. |
| `base_url` | Endereço publicado usado para reescrever links internos; opcional se `site_url` estiver configurado. |

O `nav` do `mkdocs.yml` precisa estar definido para o script manter a ordem e os agrupamentos. Todas as páginas Markdown/HTML geradas sob `docs_dir` são convertidas; páginas não listadas em `nav` entram no final. Arquivos estáticos, como CSS e imagens, são recursos das páginas e não viram páginas independentes.

## 6. Disponibilizar o botão de download

O botão no início desta página usa um link relativo para `assets/documentacao-local.pdf` e o atributo HTML `download`. O caminho relativo também funciona quando o GitHub Pages publica o site em uma subpasta do domínio. O PDF precisa existir nesse caminho no site publicado; por isso, o comando acima grava o arquivo em `site/assets/` depois do build.

No Chrome/Chromium, clicar no botão normalmente baixa o arquivo. O navegador ainda pode abri-lo se as preferências do usuário determinarem esse comportamento. O link direto continua disponível para baixar ou abrir o PDF.

## 7. Gerar e publicar com GitHub Actions

O workflow `.github/workflows/docs.yml` executa os passos nesta ordem:

1. Instala as dependências do projeto e o Chromium do Playwright.
2. Executa `mkdocs build --strict` para gerar o HTML e copiar os assets para `site/`.
3. Executa `examples/expotr_to_pdf.py` e grava o PDF em `site/assets/documentacao-local.pdf`.
4. Disponibiliza o PDF como artefato para download na execução da Action por 30 dias.
5. Envia toda a pasta `site/` como artefato do GitHub Pages; o HTML, as imagens e o PDF são publicados juntos.

Para configurar a publicação, abra o repositório no GitHub e vá a **Settings → Pages → Build and deployment → Source**. Selecione **GitHub Actions**. Depois, envie as alterações para a branch `main` ou execute o workflow manualmente pela aba **Actions**. Aguarde a execução terminar com sucesso e abra a URL publicada pelo job; o botão da página **Conversão PDF local** baixa o arquivo gerado naquela execução. Para baixar diretamente da execução, abra o resumo do job e selecione o artefato `documentacao-completa-pdf` em **Artifacts**.

O PDF não precisa ser regenerado nem commitado em cada alteração: a Action o gera durante o build e publica o resultado. Para testá-lo localmente, use os comandos do passo 3 e abra `site/assets/documentacao-local.pdf`. Se quiser versionar uma cópia no repositório, copie a saída local para `docs/assets/documentacao-local.pdf` e inclua essa alteração no commit.

## 8. Preservar imagens, diagramas, estilos e referências

O script serve a pasta inteira do site gerado durante a renderização. Por isso, caminhos relativos de CSS, imagens e diagramas estáticos continuam disponíveis ao navegador. Verifique se os arquivos usados estão dentro de `docs/` antes do build, para que sejam copiados para `site/`.

- **Imagens e SVGs:** são carregados pelo Chromium e incorporados visualmente nas páginas do PDF.
- **Diagramas:** prefira imagens SVG/PNG exportadas. Um `.drawio` pode continuar disponível como link para download, mas não é uma imagem renderizada.
- **Links externos:** continuam clicáveis no PDF.
- **Links entre páginas:** são reescritos para `base_url` ou para o `site_url` do projeto.
- **Referências e ordem:** os PDFs são combinados seguindo o `nav`; os marcadores refletem os grupos e títulos da navegação.
- **JavaScript e iframes:** conteúdo remoto ou interativo pode não estar pronto para impressão; prefira uma exportação estática do diagrama para o PDF.

O Chromium aplica o modo de impressão e as regras `@media print` das páginas. O script força o esquema claro do Material, usa as cores de identidade visual DataRain, oculta a navegação do site e expande a área principal.

## 9. Cabeçalho e rodapé DataRain

O conversor lê o logo configurado em `theme.logo` no `mkdocs.yml`. Neste projeto, o caminho aponta para `assets/logo.png`, que é copiado para `site/assets/logo.png` durante o build. O logo é incorporado ao PDF como imagem, então não depende de acesso externo.

O cabeçalho é repetido em todas as páginas físicas e contém o logo DataRain. Para o rodapé, o script incorpora `docs/assets/footer.png`, que o MkDocs copia para `site/assets/footer.png`. Mantenha esse arquivo nesse caminho. O esquema claro usa fundo branco, texto azul-marinho e o teal/laranja da paleta clara do tema:

```yaml
theme:
  name: material
  logo: assets/logo.png
  palette:
    - scheme: default
      primary: custom
      accent: custom
```

O cabeçalho/rodapé e a folha de estilos estão definidos em `examples/expotr_to_pdf.py`. O tamanho do papel está configurado como A4, com margens reservadas para que o conteúdo não fique sob o logo ou a faixa do rodapé.

## 10. Conferir o PDF

Depois da execução, valide a existência e o tamanho do arquivo:

```powershell
Test-Path site\assets\documentacao-local.pdf
Get-Item site\assets\documentacao-local.pdf | Select-Object Name, Length
```

Abra o PDF e confira:

1. A ordem das páginas e os marcadores correspondem ao `nav`.
2. Imagens e diagramas não foram cortados.
3. Tabelas e blocos de código respeitam as margens.
4. Links externos e internos abrem os destinos esperados.
5. A acentuação e a paginação estão corretas.

## 11. Problemas comuns

### O script não encontra `site/` ou uma página HTML

Gere o site antes de converter e confirme que todos os documentos do `nav` foram incluídos no build:

```powershell
uv run mkdocs build
```

### O Chromium não está instalado

Instale o navegador usado pelo Playwright:

```powershell
uv run playwright install chromium
```

### O PDF não tem marcadores ou está fora de ordem

Confirme que `mkdocs.yml` tem uma seção `nav` válida e que as páginas listadas existem no HTML gerado. Páginas fora de `nav` aparecem após as páginas navegadas, ordenadas por caminho.

### O cabeçalho não mostra o logo DataRain

Confirme que `theme.logo` aponta para uma imagem dentro do site gerado e que o arquivo existe, por exemplo, `site/assets/logo.png`. Verifique também se `docs/assets/footer.png` foi copiado para `site/assets/footer.png`.

### Links internos não apontam para o site publicado

Configure `site_url` no `mkdocs.yml` ou passe o endereço completo ao parâmetro `--base-url`. Isso também é importante para sites GitHub Pages publicados em uma subpasta do domínio.

### Diagramas interativos não aparecem

Converta-os para SVG ou PNG e inclua a imagem na documentação antes de executar `mkdocs build`. Iframes e recursos dependentes de serviços remotos não são garantidos no PDF.

## Referências

- [Playwright para Python: geração de PDF](https://playwright.dev/python/docs/api/class-page#page-pdf)
- [pypdf: combinar documentos](https://pypdf.readthedocs.io/en/stable/user/merging-pdfs.html)
- [MkDocs: configuração da navegação](https://www.mkdocs.org/user-guide/configuration/#nav)
