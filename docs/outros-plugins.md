# Outros plugins

## 1. Introdução

As páginas anteriores já cobriram imagens, diagramas, integração com GitHub e as extensões `pymdownx` de formatação de conteúdo. Esta página reúne um grupo de plugins complementares que não se encaixam diretamente em nenhum desses temas, mas que resolvem problemas comuns de qualquer site MkDocs em produção:

- **`macros`**: permite usar variáveis e lógica Jinja2 reutilizável dentro das páginas Markdown.
- **`hooks` (redirecionamentos nativos)**: resolve o problema de URLs antigas quebradas quando uma página é renomeada, sem depender de um pacote externo controverso.
- **`minify`**: reduz o tamanho do HTML gerado, sem alterar sua aparência.
- **`awesome-pages`**: permite organizar a navegação por pasta através de arquivos `.pages` — com uma ressalva importante para este projeto, explicada na seção 5.
- **`exporter`**: exporta páginas do site para PDF, reaproveitando o Playwright já usado na página [Preview com Playwright](playwright-preview.md).

Todos os cinco já estão instalados e configurados no `mkdocs.yml` real deste projeto. As seções a seguir explicam cada um, mostrando a configuração efetivamente usada.

## 2. Macros (`mkdocs-macros-plugin`)

### Instalação

```bash
uv add mkdocs-macros-plugin
```

### Configuração

```yaml
plugins:
  - macros:
      module_name: macros_mkdocs
```

### O que ele faz

O `mkdocs-macros-plugin` transforma cada página Markdown em um template Jinja2 antes de renderizá-la. Isso significa que, além do Markdown comum, é possível usar variáveis e expressões entre chaves duplas — a mesma sintaxe `{% raw %}{{ ... }}{% endraw %}` do Jinja2 — diretamente no texto da página.

> As ocorrências de chaves duplas mostradas nesta seção estão envolvidas por um recurso do próprio Jinja2 que bloqueia sua substituição (sem gerar nenhuma marcação visível no texto renderizado), para que apareçam como sintaxe literal nesta página, em vez de serem interpretadas e substituídas pelo `mkdocs-macros-plugin` durante o build.

Duas fontes de variáveis costumam ser usadas:

- **Variáveis automáticas do próprio MkDocs**, como `{% raw %}{{ page.title }}{% endraw %}` (o título da página atual) ou `{% raw %}{{ config.site_name }}{% endraw %}` (o `site_name` definido no `mkdocs.yml`), disponíveis sem nenhuma configuração extra.
- **Variáveis customizadas**, definidas pelo autor do site em um arquivo Python que declara uma função `define_env(env)`. Essa função recebe um objeto `env` e registra variáveis dentro de `env.variables`. Por convenção, o plugin procura esse arquivo em `main.py` na raiz do projeto — mas neste projeto `main.py` já é a aplicação real (`def main(): print(...)`), e não um módulo de macros. Por isso a configuração acima usa explicitamente a opção `module_name: macros_mkdocs`, apontando para um arquivo dedicado, `macros_mkdocs.py`, em vez de deixar o plugin tentar importar `main.py` como se fosse seu módulo de macros:

```python
# macros_mkdocs.py
def define_env(env):
    env.variables["minha_variavel"] = "valor"
```

Depois de registrada, a variável pode ser usada em **qualquer página Markdown** do site:

```markdown
{% raw %}O valor configurado é: {{ minha_variavel }}{% endraw %}
```

No momento do `mkdocs build`, o plugin substitui `{% raw %}{{ minha_variavel }}{% endraw %}` pelo texto `valor` antes de o Markdown ser convertido em HTML. O mesmo mecanismo também permite registrar macros (funções Jinja2 chamáveis, via `env.macro`), não apenas variáveis simples — úteis para gerar trechos repetitivos de conteúdo a partir de uma única definição central, em vez de copiar o mesmo texto em várias páginas.

## 3. Redirecionamentos sem dependência externa (`hooks`)

### Por que o `mkdocs-redirects` foi evitado

A escolha natural para redirecionar URLs antigas de página costuma ser o pacote `mkdocs-redirects`. Esse pacote, porém, passou a declarar o `properdocs` como dependência a partir da versão 1.2.3. O `properdocs` é um fork/continuação concorrente do próprio MkDocs, criado após uma disputa de governança no projeto original.

Para deixar claro: o `properdocs` **não é malware** nem um pacote malicioso. O problema não é de segurança — é de escopo e de risco de manutenção. Este projeto já usa o MkDocs original diretamente (`mkdocs`, `mkdocs-material`) e não tem motivo para trazer, como dependência transitiva de um plugin de redirecionamento, um fork inteiro e concorrente da própria ferramenta de documentação que o projeto usa. É uma dependência desnecessária para a funcionalidade desejada, e controversa o suficiente para ser evitada.

### A alternativa: `hooks` nativo do MkDocs

Em vez do `mkdocs-redirects`, este projeto usa a funcionalidade `hooks`, nativa do próprio MkDocs desde a versão 1.4 e documentada oficialmente em [mkdocs.org/user-guide/configuration/#hooks](https://www.mkdocs.org/user-guide/configuration/#hooks). Essa funcionalidade permite registrar um ou mais scripts Python locais como handlers dos eventos internos do MkDocs (como `on_post_build`), **sem instalar nenhum pacote adicional do PyPI** — o script é só um arquivo `.py` do próprio repositório.

A configuração, no `mkdocs.yml` deste projeto, é:

```yaml
hooks:
  - hooks/redirects.py
```

### O script `hooks/redirects.py`

O conteúdo real do arquivo, na raiz do projeto, é:

```python
"""hooks/redirects.py — Native_Redirect_Hook.

Gera páginas de redirecionamento HTML (meta refresh) para caminhos antigos
de página, sem depender do pacote `mkdocs-redirects` (nem, por
consequência, do pacote `properdocs`). Referenciado na opção `hooks` do
mkdocs.yml.

Documentação oficial da funcionalidade `hooks` do MkDocs (disponível desde a
versão 1.4, sem exigir nenhum pacote PyPI adicional):
https://www.mkdocs.org/user-guide/configuration/#hooks
"""

import os

# Mapeamento de caminho antigo (relativo a docs_dir) -> caminho atual.
REDIRECTS = {
    "preview.md": "playwright-preview.md",
}


def _write_redirect_html(target_path: str, destination_url: str) -> None:
    """Escreve um arquivo HTML de redirecionamento em `target_path`."""
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    content = (
        "<!DOCTYPE html>\n"
        "<html lang=\"pt-BR\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        f"  <meta http-equiv=\"refresh\" content=\"0; url={destination_url}\">\n"
        f"  <link rel=\"canonical\" href=\"{destination_url}\">\n"
        "  <title>Redirecionando...</title>\n"
        "</head>\n"
        "<body>\n"
        f"  Redirecionando para <a href=\"{destination_url}\">{destination_url}</a>...\n"
        "</body>\n"
        "</html>\n"
    )
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)


def on_post_build(config, **kwargs):
    """Evento `on_post_build` do MkDocs: gera uma página de
    redirecionamento para cada entrada de REDIRECTS, dentro de
    `config["site_dir"]`."""
    site_dir = config["site_dir"]
    for old_path, new_path in REDIRECTS.items():
        old_slug = old_path.rsplit(".", 1)[0]
        new_slug = new_path.rsplit(".", 1)[0]
        target_html = os.path.join(site_dir, old_slug, "index.html")
        destination_url = f"../{new_slug}/"
        _write_redirect_html(target_html, destination_url)
```

Duas peças merecem atenção:

- **O dicionário `REDIRECTS`** é o único lugar que precisa ser editado para adicionar um novo redirecionamento: cada chave é o caminho antigo de uma página (relativo a `docs_dir`), e cada valor é o caminho atual correspondente.
- **A função `on_post_build(config, **kwargs)`** corresponde a um evento do ciclo de vida do MkDocs, disparado **depois** que o site inteiro já foi escrito em disco, dentro da pasta `site/` (`config["site_dir"]`). Ou seja, quando esse evento dispara, todas as páginas reais (incluindo `playwright-preview.md` já convertida em `site/playwright-preview/index.html`) já existem. A função aproveita exatamente esse momento para escrever um arquivo HTML **extra**, que não corresponde a nenhuma página Markdown real, contendo apenas uma tag `<meta http-equiv="refresh" content="0; url=...">` — a técnica padrão de redirecionamento automático em páginas HTML estáticas, sem exigir um servidor com lógica de redirecionamento.

### O exemplo configurado

O mapeamento ativo hoje é:

```python
REDIRECTS = {
    "preview.md": "playwright-preview.md",
}
```

Isso simula uma situação comum em sites de documentação reais: a página hoje chamada "Preview com Playwright" (`playwright-preview.md`) já teve, no passado, um nome mais curto, `preview.md`. Qualquer link antigo — em um favorito salvo, em outro site, em um resultado de busca já indexado — que ainda aponte para `.../preview/` continua funcionando: ao acessá-lo, o visitante é redirecionado automaticamente para `.../playwright-preview/`, a URL atual da página real, sem receber um erro 404.

## 4. Minificação (`mkdocs-minify-plugin`)

### Instalação

```bash
uv add mkdocs-minify-plugin
```

### Configuração

```yaml
plugins:
  - minify:
      minify_html: true
```

### O que ele faz

O `mkdocs-minify-plugin` processa o HTML já gerado por cada página do site e remove tudo que é irrelevante para a renderização no navegador: espaços em branco redundantes entre tags, quebras de linha de formatação, comentários HTML e outras sobras de indentação que só existem para facilitar a leitura do código-fonte. Com `minify_html: true`, essa limpeza é aplicada a todo arquivo `.html` do site gerado.

O resultado visual da página **não muda em nada** — é o mesmo HTML, semanticamente idêntico, só mais compacto como texto. O benefício é puramente de tamanho de arquivo: páginas menores para transferir, o que reduz (ainda que de forma modesta, em sites deste porte) o tempo de carregamento e o consumo de banda de quem acessa a documentação publicada.

## 5. Organização automática de navegação (`mkdocs-awesome-pages-plugin`)

### Instalação

```bash
uv add mkdocs-awesome-pages-plugin
```

### Configuração

```yaml
plugins:
  - awesome-pages
```

### O que ele faz, e por que não tem efeito neste projeto

O `mkdocs-awesome-pages-plugin` permite controlar a navegação do site a pasta por pasta, sem precisar listar cada página manualmente na seção `nav` do `mkdocs.yml`. Isso é feito através de arquivos chamados `.pages`, colocados dentro de cada pasta de `docs_dir`, com opções como:

- `title`: o título exibido para aquela pasta/seção na navegação.
- `nav`: a ordem e os rótulos das páginas daquela pasta (pode reordenar, renomear ou omitir arquivos).
- `collapse`: se a seção deve iniciar recolhida no menu lateral.

Para ser honesto sobre o comportamento real neste projeto: **o `awesome-pages` não tem efeito nenhum sobre a navegação deste site específico.** Isso não é um bug nem uma configuração incompleta — é o comportamento documentado oficialmente pelo próprio plugin: ele não faz nada quando o `mkdocs.yml` já define uma seção `nav` explícita. Como este projeto declara, desde a Tarefa 1.1, uma seção `nav` completa e manual (as treze entradas visíveis em `mkdocs.yml`, da página "Início" até "Outros plugins"), o `awesome-pages` permanece instalado e habilitado, mas inativo na prática: a navegação real é inteiramente determinada pelo `nav` explícito, não por arquivos `.pages`.

O plugin continua configurado aqui porque faz parte do catálogo de plugins do ecossistema coberto por esta página — e porque pode ser útil no futuro, caso o `nav` explícito seja removido. Para quem quiser usar o plugin de verdade, em um projeto **sem** `nav` explícito, um arquivo `.pages` de referência se pareceria com isto:

```yaml
title: Minha Seção
nav:
  - Visão geral: index.md
  - ...
collapse: true
```

Colocado dentro de uma subpasta de `docs_dir`, esse arquivo faria o `awesome-pages` renomear a seção correspondente para "Minha Seção" na navegação, definir "Visão geral" (`index.md`) como primeira entrada, preencher o restante com `...` (um atalho do próprio plugin para "todas as outras páginas da pasta, em ordem alfabética") e exibir a seção inicialmente recolhida no menu lateral.

## 6. Exportação para PDF (`mkdocs-exporter`)

### Instalação

```bash
uv add mkdocs-exporter
```

### Configuração

A configuração real usada neste projeto, em `mkdocs.yml`:

```yaml
plugins:
  - exporter:
      formats:
        pdf:
          enabled: true
```

### O que ele faz

O `mkdocs-exporter` exporta cada página do site (ou a documentação inteira) como um arquivo PDF. A parte interessante de como ele faz isso: em vez de tentar converter o Markdown ou o HTML diretamente em PDF por conta própria, ele abre a própria página já publicada em um **navegador headless controlado via Playwright** e manda esse navegador renderizar a página exatamente como um visitante humano a veria — com o CSS do tema Material aplicado, com diagramas Mermaid já desenhados, com sintaxe de código já destacada — e só então converte essa renderização final em PDF.

Isso significa que o PDF gerado não é uma reinterpretação simplificada do conteúdo: é, literalmente, uma cópia fiel e impressa da página como ela existe no site.

Vale destacar explicitamente: o `mkdocs-exporter` **não traz uma dependência nova de automação de navegador**. Ele reaproveita o mesmíssimo pacote `playwright`, já instalado neste projeto desde a página [Preview com Playwright](playwright-preview.md), onde é usado pelo Preview_Script (`docs_preview.py`) para abrir o site buildado localmente. O `mkdocs-exporter` apenas dá um segundo uso a uma ferramenta que já estava presente: no Preview_Script, o Playwright abre o navegador para que um humano veja a página; no `mkdocs-exporter`, o Playwright abre o navegador para capturar a página e congelá-la em PDF — a mesma tecnologia de automação, dois propósitos diferentes.

### Como usar

Depois de um `mkdocs build` (ou `mkdocs serve`) com esse plugin habilitado, cada página do site passa a exibir um botão/link "Download as PDF" próximo ao topo. Clicar nesse botão baixa um arquivo PDF contendo apenas aquela página específica, já convertida — sem precisar rodar nenhum comando adicional manualmente para gerar o PDF daquela página.
