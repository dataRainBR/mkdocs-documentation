# Exemplos do notebook

O arquivo `mkdocks.ipynb`, na raiz do projeto, funciona como um **roteiro de anotações**: um notebook Jupyter com os títulos das etapas que foram seguidas para colocar este site MkDocs no ar, na ordem em que aconteceram. Ele não contém explicações completas nem o detalhe de cada comando, apenas lembretes curtos como "Instalando Mkdocks", "fazendo o build" ou "Executando o mkdocks para visualizar no browser".

Esta página pega esse roteiro e o transforma em um passo a passo completo, em prosa e com os comandos reais de terminal, para que você consiga reproduzir o mesmo fluxo do início ao fim. Em vez de copiar literalmente as anotações do notebook, cada etapa abaixo é explicada com suas próprias palavras e aponta para a página do tutorial onde o assunto é tratado em profundidade.

## 1. Instalação dos pacotes

A primeira anotação do notebook é "Instalando Mkdocks". Antes de qualquer configuração ou conteúdo, é preciso ter os pacotes do MkDocs disponíveis no ambiente do projeto. Isso inclui o próprio MkDocs, o tema Material e os handlers do `mkdocstrings` usados para gerar documentação a partir do código-fonte.

```bash
uv add mkdocs mkdocs-material "mkdocstrings[python]" mkdocstrings-typescript
```

Esse é o mesmo comando detalhado, pacote por pacote, na página [Instalação](instalacao.md). Se você ainda não leu essa página, vale a pena revisá-la antes de seguir, pois ela explica por que o `mkdocstrings[python]` precisa de aspas e para que serve o handler de TypeScript.

## 2. Inicialização do projeto

A segunda anotação, "Inicializando um novo projeto", corresponde ao comando que cria a estrutura mínima de um site MkDocs:

```bash
uv run mkdocs new .
```

Esse comando pede ao MkDocs para inicializar um projeto na pasta atual (o `.` indica "aqui mesmo"). Quando executado em uma pasta vazia, ele cria dois elementos:

- um arquivo `mkdocs.yml` mínimo, apenas com um `site_name` padrão;
- uma pasta `docs/` contendo um único arquivo `index.md` de exemplo, com um texto de boas-vindas genérico.

Neste projeto específico, porém, esse ponto de partida automático não é mais o que você vai encontrar ao rodar o comando: tanto o `mkdocs.yml` quanto o conteúdo de `docs/` já foram criados e customizados manualmente nas etapas anteriores deste tutorial (navegação com as seis páginas, tema Material configurado, plugins de `mkdocstrings`, etc.). Ou seja, `uv run mkdocs new .` é o comando que *daria o pontapé inicial* em um projeto novo do zero; aqui ele serve apenas como referência histórica do que originou a estrutura do projeto, e não precisa ser executado novamente.

## 3. Build do site

A anotação "fazendo o build" se refere à geração do site estático a partir da configuração e do conteúdo já existentes:

```bash
uv run mkdocs build
```

Esse comando lê o `mkdocs.yml` da raiz do projeto, processa cada arquivo Markdown listado em `nav` dentro da pasta `docs/` (aplicando o tema, os plugins e as extensões configuradas) e grava o resultado como um conjunto de arquivos HTML, CSS e JavaScript prontos na pasta `site/`. É esse conteúdo de `site/` que, de fato, constitui o site de documentação publicável: nada nessa pasta precisa ser editado à mão, pois ela é recriada do zero a cada execução do `build`.

## 4. Visualização local

A anotação "executando o mkdocs para visualizar a documentação html" descreve o comando usado para conferir o resultado enquanto o conteúdo ainda está sendo escrito:

```bash
uv run mkdocs serve
```

Diferente do `build`, o `serve` não apenas gera os arquivos: ele também sobe um servidor web local, normalmente disponível em `http://127.0.0.1:8000`, e fica em execução observando os arquivos do projeto. Qualquer alteração salva em `mkdocs.yml` ou em algum arquivo dentro de `docs/` é detectada automaticamente, o site é reconstruído em segundo plano e a página aberta no navegador é recarregada sozinha. Esse é o comando mais usado durante a escrita da documentação, já que permite ver o resultado de cada mudança quase em tempo real, sem precisar rodar `build` e abrir o arquivo manualmente a cada edição.

## 5. Configuração do `mkdocs.yml`

A anotação "Configurando o Yaml" corresponde ao trabalho de definir, dentro do `mkdocs.yml`, tudo o que controla o comportamento do site: a lista de páginas em `nav`, o tema em `theme`, os plugins em `plugins` (incluindo os handlers do `mkdocstrings` para Python e TypeScript) e as extensões de Markdown em `markdown_extensions`.

Esse trabalho de configuração é explicado seção por seção, com os trechos de YAML reais usados neste projeto, na página [Configuração do mkdocs.yml](configuracao-yaml.md).

## 6. Personalizações visuais

A anotação "Personalizações" corresponde aos ajustes feitos sobre o tema Material depois que a configuração básica já estava funcionando: escolha de fontes (`theme.font`), paleta de cores com variantes clara e escura (`theme.palette`), logo (`theme.logo`) e favicon (`theme.favicon`).

Esses ajustes, incluindo onde guardar os arquivos de imagem usados por eles, são detalhados na página [Identidade visual](personalizacao.md).

## 7. Visualizando no navegador

A última anotação do notebook, "Executando o mkdocks para visualizar no browser", fecha o roteiro: depois de configurar e personalizar o site, falta apenas abri-lo em um navegador para conferir o resultado final. Existem duas formas de fazer isso:

**Opção recomendada — usando `mkdocs serve` novamente:**

```bash
uv run mkdocs serve
```

Com o servidor local em execução, basta abrir `http://127.0.0.1:8000` no navegador. Essa é a forma mais simples e também a mais indicada quando você ainda pode estar fazendo ajustes no conteúdo, já que o recarregamento automático mostra cada mudança na hora.

**Alternativa — servindo a pasta `site/` já gerada:**

Se o site já foi gerado com `uv run mkdocs build` e você quer apenas visualizar o resultado final (sem um servidor de desenvolvimento), é possível servir a pasta `site/` com um servidor HTTP simples, como o módulo embutido do Python:

```bash
python -m http.server --directory site
```

Esse comando inicia um servidor básico (por padrão em `http://localhost:8000`) apontando diretamente para os arquivos estáticos já construídos.

Em ambos os casos, evite abrir o arquivo `site/index.html` diretamente no navegador através do protocolo `file://` (por exemplo, clicando duas vezes no arquivo). O tema Material depende de requisições feitas por um servidor HTTP para carregar corretamente alguns recursos, em especial o índice de busca; ao abrir via `file://`, essas requisições costumam falhar silenciosamente e a busca do site simplesmente não funciona, mesmo que o restante da página pareça normal.
