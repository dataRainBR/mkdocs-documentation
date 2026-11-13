# Playwright: automação de navegadores

Playwright é uma biblioteca para controlar navegadores reais por código. Com Python, ela pode abrir páginas, preencher formulários, verificar conteúdo, tirar capturas de tela, baixar arquivos e gerar PDFs. Também é usada para testes automatizados de ponta a ponta (*end-to-end*).

Este projeto já declara o pacote Python `playwright` no `pyproject.toml`. O script [Preview com Playwright](playwright-preview.md) o usa para abrir a documentação local no Chromium, e o plugin `mkdocs-exporter` o usa para gerar PDFs. Esta página apresenta os conceitos e exemplos para outros projetos.

## 1. Instalar a biblioteca e o Chromium

O Playwright é composto por duas partes: a biblioteca Python e os navegadores que ela controla. Instale ambas:

```bash
uv add playwright
uv run playwright install chromium
```

O primeiro comando registra o pacote no projeto; o segundo baixa o Chromium compatível com a versão instalada do Playwright. Em um projeto que usa `pip`, ative o ambiente virtual e execute:

```bash
python -m pip install playwright
playwright install chromium
```

Depois de atualizar a versão do Playwright, execute novamente `playwright install chromium`: cada versão da biblioteca espera versões específicas dos binários dos navegadores. Para instalar Firefox ou WebKit, troque `chromium` pelo navegador desejado.

Em Linux, especialmente em integração contínua, instale também as dependências de sistema necessárias:

```bash
uv run playwright install --with-deps chromium
```

`--with-deps` instala bibliotecas do sistema e é voltado a ambientes Linux; no Windows e macOS, normalmente basta instalar o navegador com `playwright install chromium`. Consulte a documentação oficial de [instalação de navegadores](https://playwright.dev/python/docs/browsers) para requisitos atualizados.

## 2. Iniciar e configurar o Chromium

Por padrão, `playwright.chromium.launch()` usa o Chromium baixado pelo próprio Playwright. `headless=True` executa sem janela — ideal para CI e geração de PDFs — e `headless=False` abre uma janela visível para depuração:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    try:
        page = browser.new_page(
            viewport={"width": 1366, "height": 768},
            device_scale_factor=1,
        )
        page.goto("https://example.com", wait_until="domcontentloaded")
        print(page.title())
    finally:
        browser.close()
```

O navegador é o processo do Chromium; uma **página** corresponde a uma aba. Para manter cookies e configurações isolados entre sessões, crie um contexto e uma página dentro dele:

```python
context = browser.new_context(
    viewport={"width": 1280, "height": 800},
    locale="pt-BR",
)
page = context.new_page()
```

Feche o contexto quando terminar (`context.close()`) e, por fim, feche o navegador. Se precisar usar o Google Chrome ou o Microsoft Edge instalado na máquina, configure `channel="chrome"` ou `channel="msedge"` em `launch()`. Para a maioria dos casos, prefira o Chromium gerenciado pelo Playwright; não é necessário apontar manualmente para o executável.

```python
browser = playwright.chromium.launch(channel="chrome", headless=True)
```

## 3. Navegar, interagir e validar uma página

Use localizadores semânticos, como `get_by_role` e `get_by_label`. As ações e asserções do Playwright aguardam automaticamente que o elemento esteja pronto, evitando pausas arbitrárias com `time.sleep()`:

```python
from playwright.sync_api import expect, sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()

    page.goto("https://playwright.dev/python/docs/intro")
    expect(
        page.get_by_role("heading", name="Installation")
    ).to_be_visible()

    browser.close()
```

Para interagir com formulários, localize o campo pelo rótulo e o botão pela função e pelo nome:

```python
page.get_by_label("E-mail").fill("pessoa@example.com")
page.get_by_label("Senha").fill("senha-de-teste")
page.get_by_role("button", name="Entrar").click()
expect(page.get_by_text("Bem-vindo")).to_be_visible()
```

Prefira `get_by_role`, `get_by_label` e outros localizadores voltados ao usuário. Eles tornam os testes mais próximos da forma como uma pessoa usa o site e menos dependentes da estrutura interna do HTML.

## 4. Capturas de tela e depuração visual

Uma captura pode incluir a área visível ou a página inteira. Crie a pasta de destino antes de salvar:

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

Path("capturas").mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    page.screenshot(path="capturas/pagina-inteira.png", full_page=True)
    browser.close()
```

Para abrir o navegador e observar as ações durante o desenvolvimento, use `headless=False`. Também é possível desacelerar as ações:

```python
browser = playwright.chromium.launch(headless=False, slow_mo=250)
```

`slow_mo` é útil para depuração interativa; remova-o em testes normais e em CI. Para gerar código de automação interativamente a partir dos cliques no navegador, use o gravador do Playwright:

```bash
uv run playwright codegen https://example.com
```

## 5. Downloads e emulação de dispositivos

Para downloads, aguarde o evento antes de clicar; assim o script captura o arquivo iniciado pela ação:

```python
from pathlib import Path

Path("downloads").mkdir(exist_ok=True)

with page.expect_download() as download_event:
    page.get_by_role("link", name="Baixar relatório").click()

download = download_event.value
download.save_as(Path("downloads") / download.suggested_filename)
```

Playwright também pode configurar um contexto com parâmetros de um dispositivo móvel:

```python
device = playwright.devices["iPhone 13"]
context = browser.new_context(**device)
page = context.new_page()
page.goto("https://example.com")
```

Isso emula características como viewport, user agent e densidade de pixels. Use-o para verificar layouts responsivos; a emulação não substitui testes em aparelhos físicos quando o comportamento do hardware é relevante.

## 6. Gerar PDF com Chromium

O método `page.pdf()` imprime a página atual para PDF e está disponível no Chromium em modo headless. Por padrão, ele usa estilos de impressão; `print_background=True` inclui cores e imagens de fundo:

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

Path("exportados").mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com", wait_until="load")
    page.evaluate("document.fonts.ready")
    page.pdf(
        path="exportados/pagina.pdf",
        format="A4",
        print_background=True,
        prefer_css_page_size=True,
    )
    browser.close()
```

`prefer_css_page_size=True` permite que regras CSS `@page` determinem o tamanho e as margens quando existirem. Se precisar da aparência de tela em vez de estilos de impressão, configure `page.emulate_media(media="screen")` antes de chamar `page.pdf()`.

### PDF da documentação MkDocs neste projeto

Não é necessário criar um script próprio para exportar cada página deste site. O `mkdocs-exporter` já está configurado no `mkdocs.yml` e usa o Playwright para renderizar as páginas com o tema e então gerar PDFs. Após instalar o Chromium e executar o build, o plugin disponibiliza a exportação nas páginas. Veja a configuração e o uso na página [Plugins](outros-plugins.md).

Para configurar a mesma integração em outro projeto MkDocs, habilite o plugin no `mkdocs.yml` e gere o site:

````yaml
plugins:
  - search
  - exporter:
      formats:
        pdf:
          enabled: true
````

```bash
uv run playwright install chromium
uv run mkdocs build
```

O Playwright também abre o site local no script [Preview com Playwright](playwright-preview.md). Para executar o fluxo completo de preview, incluindo build e servidor HTTP, use `uv run docs_preview.py`; para exportar páginas, use o recurso do `mkdocs-exporter`.

## 7. API síncrona e assíncrona

Os exemplos acima usam a API síncrona (`playwright.sync_api`), que costuma ser mais simples para scripts pequenos. Em aplicações assíncronas, use a API `async_api` e aguarde cada operação:

```python
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        print(await page.title())
        await browser.close()


asyncio.run(main())
```

Não misture chamadas síncronas e assíncronas na mesma sessão do Playwright.

## 8. Boas práticas e diagnóstico

- **Instale o navegador compatível:** se o erro indicar que o executável não foi encontrado, execute `uv run playwright install chromium`. Repita após atualizar o pacote.
- **Em CI, use headless:** não abra uma janela com `headless=False` em um runner sem ambiente gráfico.
- **Aguarde condições, não tempos fixos:** use `expect(locator).to_be_visible()`, `locator.wait_for()` ou eventos específicos em vez de `sleep`.
- **Feche os recursos:** feche páginas/contextos e o navegador mesmo quando ocorrer uma exceção, usando `try/finally` ou o fluxo de limpeza adequado ao script.
- **Investigue falhas com rastreamento:** grave traces do contexto e abra-os com o visualizador do Playwright:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.goto("https://example.com")
    context.tracing.stop(path="trace.zip")
    browser.close()
```

```bash
uv run playwright show-trace trace.zip
```

O trace pode incluir capturas de tela, snapshots do DOM e fontes; evite compartilhá-lo se contiver dados privados de usuários.

## Referências oficiais

- [Playwright para Python](https://playwright.dev/python/)
- [Instalação de navegadores](https://playwright.dev/python/docs/browsers)
- [Localizadores](https://playwright.dev/python/docs/locators)
- [Capturas de tela](https://playwright.dev/python/docs/screenshots)
- [Gerar PDFs com `page.pdf()`](https://playwright.dev/python/docs/api/class-page#page-pdf)
