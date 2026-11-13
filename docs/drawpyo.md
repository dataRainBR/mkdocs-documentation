# Criar diagramas do Draw.io com Python e `drawpyo`

[`drawpyo`](https://github.com/MerrimanInd/drawpyo) é uma biblioteca Python para gerar arquivos de diagramas que podem ser abertos e editados no Draw.io (também chamado diagrams.net). O código cria o arquivo, a página, os elementos e as conexões; depois, o Draw.io pode exportar o resultado como SVG ou HTML.

Há dois tipos de recursos externos neste tutorial:

- **Bibliotecas `mxlibrary`**, como o arquivo `developer.xml` indicado aqui, são coleções de formas do Draw.io. O arquivo não é uma biblioteca Python nem um conjunto de ícones AWS.
- **Ícones SVG da AWS** são arquivos de imagem que podem ser incorporados aos elementos do diagrama. O exemplo AWS abaixo usa SVGs oficiais baixados do pacote da AWS.

## 1. Instalar e preparar o projeto

Crie um projeto Python e instale `drawpyo`:

```powershell
uv init diagramas-cloud
cd diagramas-cloud
uv add "drawpyo @ git+https://github.com/MerrimanInd/drawpyo.git@0.2.6"
```

A versão 0.2.6 ou posterior é necessária para carregar bibliotecas `mxlibrary` externas. Se essa versão já estiver disponível no PyPI, também é possível instalá-la com `uv add "drawpyo>=0.2.6"`; consulte as [releases](https://github.com/MerrimanInd/drawpyo/releases) para verificar a versão atual.

Crie uma pasta para scripts e outra para os arquivos gerados:

```powershell
New-Item -ItemType Directory -Force scripts, docs\assets\diagrams
```

## 2. Criar o primeiro diagrama

Um arquivo Draw.io pode ter uma ou mais páginas. Cada página contém objetos (formas) e arestas (conexões). Salve o exemplo como `scripts/primeiro_diagrama.py`:

```python
from pathlib import Path

import drawpyo

output_dir = Path("docs/assets/diagrams")
output_dir.mkdir(parents=True, exist_ok=True)

diagram = drawpyo.File()
diagram.file_path = str(output_dir.resolve())
diagram.file_name = "primeiro-diagrama.drawio"

page = drawpyo.Page(file=diagram)
page.name = "Fluxo inicial"

inicio = drawpyo.diagram.Object(
    page=page,
    value="Receber solicitação",
    position=(80, 120),
    width=160,
    height=60,
)
inicio.fillColor = "#E8F0FE"
inicio.strokeColor = "#3791A6"

processo = drawpyo.diagram.Object(
    page=page,
    value="Processar dados",
    position=(340, 120),
    width=160,
    height=60,
)
processo.fillColor = "#FFF4DD"
processo.strokeColor = "#F27507"

conexao = drawpyo.diagram.Edge(
    page=page,
    source=inicio,
    target=processo,
)
conexao.strokeColor = "#526B7A"
conexao.strokeWidth = 2

diagram.write()
print(f"Diagrama salvo em: {output_dir / diagram.file_name}")
```

Execute o script e abra o arquivo `.drawio` no Draw.io:

```powershell
uv run python scripts/primeiro_diagrama.py
```

Use `Object` para criar formas, defina `position`, `width` e `height` para controlar a geometria e conecte os objetos com `Edge`. Os códigos hexadecimais definem as cores de preenchimento e da borda.

## 3. Carregar a biblioteca externa `developer.xml`

O arquivo [`developer.xml`](https://raw.githubusercontent.com/jgraph/drawio-libs/refs/heads/main/libs/integration/developer.xml) é uma biblioteca do formato nativo do Draw.io, chamada `mxlibrary`. Ela contém símbolos relacionados a desenvolvimento e integração. O projeto `drawpyo` consegue carregá-la de uma URL ou de um arquivo local.

Para registrar e usar uma forma, acrescente o código abaixo depois de criar `diagram` e `page`:

```python
import drawpyo

developer_url = (
    "https://raw.githubusercontent.com/jgraph/drawio-libs/"
    "refs/heads/main/libs/integration/developer.xml"
)

drawpyo.register_mxlibrary("developer", developer_url)

ferramenta = drawpyo.diagram.object_from_library(
    page=page,
    library="developer",
    obj_name="App Developing",
    value="Desenvolvimento",
    position=(210, 240),
)

diagram.write()
```

Os nomes das formas dependem do conteúdo da biblioteca e precisam corresponder ao nome registrado nela. Liste os nomes disponíveis antes de escolher um:

```python
formas = drawpyo.load_mxlibrary(developer_url)
print("\n".join(list(formas)[:30]))
```

Para evitar depender da disponibilidade da URL e de alterações futuras no branch `main`, baixe uma cópia revisada da biblioteca para o projeto e registre o caminho local:

```python
drawpyo.register_mxlibrary(
    "developer",
    "assets/libraries/developer.xml",
)
```

> **Importante:** `developer.xml` não contém os ícones de serviços AWS. Para representar uma arquitetura AWS, use os SVGs oficiais na próxima etapa ou outra biblioteca AWS compatível com o formato `mxlibrary`.

## 4. Criar um diagrama AWS usando ícones SVG

### 4.1 Obter os ícones oficiais

Baixe o pacote atual em [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/). Extraia o pacote e copie apenas os SVGs necessários para `assets/aws/`. Neste exemplo, salve os arquivos selecionados com estes nomes:

```text
assets/
└── aws/
    ├── api-gateway.svg
    ├── lambda.svg
    └── dynamodb.svg
```

Os nomes são escolhas locais para o exemplo: copie o SVG equivalente no pacote e renomeie-o. A AWS atualiza os ícones periodicamente; consulte a página oficial para obter a versão mais recente e respeite os termos de uso e avisos incluídos no pacote.

### 4.2 Incorporar os SVGs no arquivo editável

O exemplo lê cada SVG local, codifica seus bytes em Base64 e os coloca no estilo `image` do Draw.io. Assim, os ícones ficam incorporados ao `.drawio`; o arquivo não depende de URLs de imagem externas quando for aberto em outra máquina.

Salve como `scripts/diagrama_aws.py`:

```python
import base64
from pathlib import Path

import drawpyo


def adicionar_icone_svg(page, caminho_svg, rotulo, posicao):
    svg_base64 = base64.b64encode(
        Path(caminho_svg).read_bytes()
    ).decode("ascii")

    icone = drawpyo.diagram.Object(page=page, value="")
    icone.position = posicao
    icone.width = 64
    icone.height = 64
    icone.apply_style_string(
        "shape=image;"
        "aspect=fixed;"
        "imageAspect=0;"
        "verticalLabelPosition=bottom;"
        "verticalAlign=top;"
        f"image=data:image/svg+xml,{svg_base64};"
    )

    legenda = drawpyo.diagram.Object(
        page=page,
        value=rotulo,
        position=(posicao[0] - 35, posicao[1] + 74),
        width=134,
        height=36,
    )
    legenda.text_format.align = "center"
    legenda.fillColor = "none"
    legenda.strokeColor = "none"

    return icone


output_dir = Path("docs/assets/diagrams")
output_dir.mkdir(parents=True, exist_ok=True)

diagram = drawpyo.File()
diagram.file_path = str(output_dir.resolve())
diagram.file_name = "aws-arquitetura.drawio"

page = drawpyo.Page(file=diagram)
page.name = "API, processamento e dados"

regiao = drawpyo.diagram.Object(
    page=page,
    value="AWS | us-east-1",
    position=(45, 70),
    width=570,
    height=210,
)
regiao.rounded = True
regiao.fillColor = "#F8F9FA"
regiao.strokeColor = "#879196"

api = adicionar_icone_svg(
    page,
    "assets/aws/api-gateway.svg",
    "Amazon API Gateway",
    (90, 145),
)
funcao = adicionar_icone_svg(
    page,
    "assets/aws/lambda.svg",
    "AWS Lambda",
    (275, 145),
)
banco = adicionar_icone_svg(
    page,
    "assets/aws/dynamodb.svg",
    "Amazon DynamoDB",
    (460, 145),
)

for origem, destino in ((api, funcao), (funcao, banco)):
    conexao = drawpyo.diagram.Edge(
        page=page,
        source=origem,
        target=destino,
    )
    conexao.strokeColor = "#545B64"
    conexao.strokeWidth = 2

diagram.write()
print(f"Diagrama AWS salvo em: {output_dir / diagram.file_name}")
```

Gere o arquivo e abra `docs/assets/diagrams/aws-arquitetura.drawio` no Draw.io:

```powershell
uv run python scripts/diagrama_aws.py
```

Se o Draw.io não renderizar um SVG, valide que o arquivo é um SVG independente e bem formado. Prefira os SVGs oficiais, sem scripts ou referências externas. Os dados Base64 aumentam o tamanho do arquivo; incorpore somente os ícones usados.

### 4.3 Gerar o fluxo usando as imagens do projeto

Este passo a passo monta o fluxo solicitado:

```text
user.png -> imagem1.png -> Api_gateway.png -> lambda.png -> s3.png
```

#### 4.3.1 Organizar as imagens e o script

Salve os cinco PNGs dentro de `docs/assets/`. Os nomes devem corresponder exatamente aos usados pelo script:

| Etapa | Arquivo de entrada |
|---|---|
| Usuário | `docs/assets/user.png` |
| Imagem enviada | `docs/assets/imagem1.png` |
| API Gateway | `docs/assets/Api_gateway.png` |
| Lambda | `docs/assets/lambda.png` |
| S3 | `docs/assets/s3.png` |

O diretório `docs/assets/diagrams/` receberá o diagrama gerado. O script cria esse diretório automaticamente; para criá-lo manualmente no PowerShell:

```powershell
New-Item -ItemType Directory -Force docs\assets\diagrams
```

Salve o script em `examples/diagrama_fluxo_imagens.py`, na raiz do repositório. A estrutura relevante fica assim:

```text
repositorio/
├── examples/
│   └── diagrama_fluxo_imagens.py
└── docs/
    └── assets/
        ├── user.png
        ├── imagem1.png
        ├── Api_gateway.png
        ├── lambda.png
        ├── s3.png
        └── diagrams/
            └── fluxo-imagens.drawio  (gerado pelo script)
```

O código resolve os caminhos a partir da localização do próprio script, portanto pode ser executado de outras pastas sem alterar os caminhos dos PNGs. Ele incorpora os bytes de cada imagem no `.drawio` em Base64, acrescenta uma legenda e cria uma seta para cada ligação:

```python
--8<-- "examples/diagrama_fluxo_imagens.py"
```

#### 4.3.2 Configurar a dependência do `uv`

As dependências do projeto ficam em `pyproject.toml`; o `uv.lock` registra as versões resolvidas. Não é necessário criar nem editar um `uv.toml` para adicionar `drawpyo`: ele é um arquivo de configuração do `uv`, não o manifesto de dependências. As configurações equivalentes também podem ficar na seção `[tool.uv]` do `pyproject.toml`. Consulte a documentação oficial do [`uv` sobre dependências](https://docs.astral.sh/uv/concepts/projects/dependencies/) e sobre [arquivos de configuração](https://docs.astral.sh/uv/concepts/configuration-files/).

Para manter `drawpyo` como dependência do repositório, execute na raiz:

```powershell
uv add "drawpyo @ git+https://github.com/MerrimanInd/drawpyo.git@0.2.6"
```

O comando atualiza `pyproject.toml` e `uv.lock`. Como a biblioteca vem de uma release do GitHub, o `uv` registra o nome da dependência em `[project].dependencies` e sua origem em `[tool.uv.sources]`:

```toml
[project]
dependencies = [
    # Preserve as demais dependências já existentes no projeto.
    "drawpyo",
]

[tool.uv.sources]
drawpyo = { git = "https://github.com/MerrimanInd/drawpyo.git", rev = "0.2.6" }
```

Não substitua as dependências nem outras configurações já existentes pelo exemplo; acrescente a dependência e a origem Git indicadas. A referência `rev = "0.2.6"` fixa a release que disponibiliza o suporte a bibliotecas `mxlibrary` descrito neste tutorial. Se não quiser adicionar a biblioteca ao projeto, use a execução temporária abaixo; ela não altera `pyproject.toml` nem `uv.lock`.

```powershell
uv run --no-project --with "drawpyo @ git+https://github.com/MerrimanInd/drawpyo.git@0.2.6" python examples/diagrama_fluxo_imagens.py
```

Se adicionou a dependência ao projeto, execute-o assim:

```powershell
uv run python examples/diagrama_fluxo_imagens.py
```

#### 4.3.3 Conferir e publicar o resultado

Ao terminar, o terminal informa o caminho do arquivo criado:

```text
docs/assets/diagrams/fluxo-imagens.drawio
```

O diagrama contém cinco imagens, cinco legendas e quatro conexões direcionais. Abra `docs/assets/diagrams/fluxo-imagens.drawio` no Draw.io para conferir ou ajustar o layout. Como os PNGs estão incorporados no arquivo, o diagrama continua abrindo mesmo se os arquivos de entrada forem movidos.

Para publicar uma versão estática na documentação, abra o `.drawio` no Draw.io e exporte como SVG para `docs/assets/diagrams/fluxo-imagens.svg`. Então, inclua a imagem na página:

```markdown
![Fluxo do usuário até o armazenamento S3](assets/diagrams/fluxo-imagens.svg)
```

O arquivo `.drawio` também pode ser compartilhado como fonte editável:

```markdown
[Baixar o diagrama editável](assets/diagrams/fluxo-imagens.drawio)
```

#### 4.3.4 O que foi adicionado ao repositório

Para reproduzir o exemplo em outra cópia do repositório, mantenha os cinco PNGs nos caminhos listados e o script em `examples/diagrama_fluxo_imagens.py`. Instale `drawpyo` como dependência do projeto conforme o passo anterior ou use o comando temporário com `uv run --no-project`. O `.drawio` é gerado pelo script e pode ser mantido no repositório como fonte editável.

Neste exemplo, foram adicionados o script e o diagrama gerado, e a documentação desta seção foi atualizada. Os PNGs de entrada já estão em `docs/assets/`. A execução temporária usada para gerar o exemplo não alterou `pyproject.toml` nem `uv.lock`; use `uv add` se quiser registrar a dependência permanentemente. A página `drawpyo.md` já está na navegação do `mkdocs.yml` e o diretório `docs/assets/` já é publicado pelo MkDocs, portanto não é preciso alterar a navegação nem a configuração do MkDocs. Inclua os cinco PNGs, o script e o `.drawio` no controle de versão para que outros usuários recebam todos os arquivos ao clonar o repositório.

## 5. Exportar para XML, SVG ou HTML

O arquivo `.drawio` gerado pelo `drawpyo` é a fonte editável do diagrama. Para criar formatos de publicação, instale o aplicativo desktop do Draw.io e use sua interface em **File → Export as** ou a linha de comando.

### Exportar XML

O comando abaixo gera um XML sem compressão, útil para inspecionar o modelo ou integrar com outras ferramentas:

```powershell
drawio --export --format xml --uncompressed `
  --output docs/assets/diagrams/aws-arquitetura.xml `
  docs/assets/diagrams/aws-arquitetura.drawio
```

O `.drawio` original já deve ser preservado como fonte editável; o XML exportado é uma representação adicional.

### Exportar SVG

SVG é vetorial e costuma ser a melhor opção para incorporar diagramas estáticos em documentação. Use `--embed-diagram` para incluir também os dados do diagrama no SVG e `--embed-svg-images` para incorporar imagens SVG:

```powershell
drawio --export --format svg --transparent `
  --embed-diagram --embed-svg-images `
  --output docs/assets/diagrams/aws-arquitetura.svg `
  docs/assets/diagrams/aws-arquitetura.drawio
```

### Exportar HTML interativo

O exportador HTML inclui um visualizador com zoom e opções de interação:

```powershell
drawio --export --format html `
  --output docs/assets/diagrams/aws-arquitetura.html `
  docs/assets/diagrams/aws-arquitetura.drawio
```

O HTML exportado carrega o visualizador JavaScript hospedado pelo Draw.io e precisa de conexão à internet. Verifique as opções antes de publicar diagramas internos ou confidenciais. No Windows, se `drawio` não estiver no `PATH`, substitua o comando pelo caminho do executável `draw.io.exe` instalado na máquina.

## 6. Incorporar o diagrama no MkDocs

Mantenha os arquivos que serão publicados dentro de `docs/`, por exemplo em `docs/assets/diagrams/`. O MkDocs copia os arquivos de imagem e diagramas para o site gerado.

### Mostrar SVG estático

Em qualquer página Markdown, use um caminho relativo para a imagem:

```markdown
![Arquitetura AWS: API Gateway, Lambda e DynamoDB](assets/diagrams/aws-arquitetura.svg)
```

O SVG continua nítido ao ampliar. Também é possível disponibilizar a fonte editável:

```markdown
[Baixar a fonte editável do Draw.io](assets/diagrams/aws-arquitetura.drawio)
```

### Incorporar o visualizador HTML

Para exibir o HTML interativo dentro de uma página, use um `iframe`. O exemplo abaixo é relativo a uma página Markdown na raiz de `docs/`; ajuste `../assets/` se a página estiver em uma subpasta:

```html
<iframe
  src="../assets/diagrams/aws-arquitetura.html"
  title="Diagrama interativo da arquitetura AWS"
  width="100%"
  height="620"
  loading="lazy"
  style="border: 0;">
</iframe>
```

Ou forneça um link para abrir o visualizador em uma página separada:

```markdown
[Abrir o diagrama AWS interativo](assets/diagrams/aws-arquitetura.html)
```

Para documentação pública, o SVG estático é mais simples e não depende de JavaScript externo. Use HTML interativo quando precisar de zoom ou das funções do visualizador e quando a conexão ao serviço Draw.io for permitida.

## 7. Resumo do fluxo de trabalho

1. Instale `drawpyo` 0.2.6 ou posterior para usar bibliotecas `mxlibrary` externas.
2. Crie `File`, `Page`, objetos e conexões em Python.
3. Use `register_mxlibrary` para bibliotecas Draw.io como `developer.xml`.
4. Baixe SVGs AWS oficiais e incorpore-os como `image` se precisar criar diagramas AWS pelo código.
5. Salve a fonte `.drawio` em `docs/assets/diagrams/`.
6. Exporte SVG para documentação estática ou HTML para um visualizador interativo.
7. Referencie o SVG ou o HTML na página MkDocs e teste com `uv run mkdocs serve`.

## Referências

- [Repositório e exemplos de `drawpyo`](https://github.com/MerrimanInd/drawpyo)
- [Documentação de bibliotecas de formas do `drawpyo`](https://merrimanind.github.io/drawpyo/usage/shape_libs/)
- [Biblioteca `developer.xml`](https://raw.githubusercontent.com/jgraph/drawio-libs/refs/heads/main/libs/integration/developer.xml)
- [Pacote oficial de ícones da AWS](https://aws.amazon.com/architecture/icons/)
- [Formatos de exportação do Draw.io](https://www.drawio.com/docs/manual/export/export-diagram/)
- [Exportar SVG](https://www.drawio.com/docs/manual/export/export-to-svg/)
- [Exportar HTML](https://www.drawio.com/docs/manual/export/export-to-html/)
- [Opções da linha de comando do Draw.io Desktop](https://github.com/jgraph/drawio-desktop/blob/dev/src/main/args.js)
