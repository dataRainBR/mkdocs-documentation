# Tutorial de MkDocs

Bem-vindo! Este tutorial vai te ensinar, passo a passo e em português, a criar e personalizar um site de documentação com o **MkDocs** — exatamente como foi feito neste projeto.

Ao longo das próximas páginas você vai aprender a:

- **Instalar os pacotes necessários** (`mkdocs`, `mkdocs-material`, `mkdocstrings[python]` e `mkdocstrings-typescript`) usando `uv`.
- **Configurar o arquivo `mkdocs.yml`**, entendendo para que servem as seções `nav`, `theme`, `plugins` e `markdown_extensions`.
- **Personalizar o visual do site**, ajustando fontes, paleta de cores, logo e favicon do tema Material.
- **Integrar com GitHub**, usando o GitHub CLI (`gh`) para autenticar, trabalhar com repositórios e pull requests e acompanhar o GitHub Actions.
- **Gerar documentação a partir de código-fonte** usando o plugin `mkdocstrings`, comparando um bloco de código estático com a documentação extraída automaticamente da docstring de uma função Python real do projeto.
- **Seguir um roteiro prático completo**, equivalente ao notebook `mkdocks.ipynb`, cobrindo desde a instalação dos pacotes até a visualização do site no navegador.

Não é necessário nenhum conhecimento prévio de MkDocs: cada página explica os conceitos do zero, com comandos reais que você pode copiar e executar no seu próprio terminal.

## O que é o MkDocs e por que usá-lo?

O [MkDocs](https://www.mkdocs.org/) é uma ferramenta que transforma arquivos Markdown simples (como este que você está lendo) em um site de documentação estático, pronto para ser publicado. Em vez de escrever HTML e CSS manualmente, você escreve apenas texto em Markdown dentro da pasta `docs/`, e o MkDocs se encarrega de gerar as páginas, o menu de navegação, a busca e o visual do site.

Algumas razões para usar o MkDocs:

- **Simplicidade**: basta escrever Markdown; não é preciso saber desenvolvimento web.
- **Tema profissional pronto para uso**: com o tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), o site já nasce com um visual moderno, responsivo e com modo claro/escuro.
- **Documentação de código automática**: plugins como o `mkdocstrings` leem as docstrings do seu código-fonte (Python, TypeScript, etc.) e geram a documentação de funções e classes automaticamente, sem duplicar esforço.
- **Configuração centralizada**: todo o comportamento do site — navegação, tema, plugins e extensões — é definido em um único arquivo, o `mkdocs.yml`.
- **Fluxo de trabalho simples**: com dois comandos (`mkdocs serve` para visualizar localmente com recarregamento automático, e `mkdocs build` para gerar o site final) você já tem um fluxo de documentação completo.

Agora que você já sabe o que é o MkDocs e por que ele é útil, siga as páginas abaixo na ordem sugerida para colocar tudo em prática:

1. [Instalação](instalacao.md)
2. [Configuração do mkdocs.yml](configuracao-yaml.md)
3. [Identidade visual](personalizacao.md)
4. [Exemplos de código](exemplos-codigo.md)
5. [Exemplos do notebook](exemplos-notebook.md)
6. [Integração com GitHub](integracao-github.md)
7. [GitHub CLI (`gh`)](github-cli.md)
