# Instalação

## 1. Introdução: o que vamos instalar e por quê

Antes de configurar ou escrever qualquer página de documentação, precisamos preparar o ambiente instalando as ferramentas que tornam tudo isso possível. Neste projeto, usamos quatro pacotes Python que trabalham juntos:

- **`mkdocs`**: é o gerador de site estático. Ele lê arquivos Markdown (como este que você está lendo agora) e os transforma em um site HTML completo, com navegação, busca e layout prontos.
- **`mkdocs-material`**: é o tema visual "Material for MkDocs". Sem ele, o MkDocs ainda funciona, mas usa um tema padrão bem simples. O Material adiciona um visual moderno, modo claro/escuro, ícones, busca aprimorada e diversas opções de personalização.
- **`mkdocstrings`** (com o extra `python`): é o plugin que gera documentação **automaticamente** a partir dos *docstrings* do código-fonte. Em vez de copiar e colar manualmente a explicação de uma função no Markdown, o `mkdocstrings` lê o docstring diretamente do código Python e o renderiza como parte da página.

Com esses três pacotes, já é possível ter um site de documentação completo, com tema bonito e documentação de código gerada automaticamente a partir do Python. Neste projeto também instalamos um quarto pacote, explicado a seguir.

## 2. Pré-requisitos

Antes de instalar os pacotes, confirme que seu ambiente atende aos seguintes requisitos:

- **Python 3.12 ou superior** instalado na máquina. Você pode verificar a versão com:

```bash
python --version
```

- **`uv` instalado**. O `uv` é o gerenciador de pacotes e ambientes Python usado neste projeto (ele substitui o uso combinado de `pip` + `venv` por uma ferramenta única e mais rápida). Para verificar se já está instalado:

```bash
uv --version
```

  Se o comando não for reconhecido, siga as instruções de instalação do `uv` para o seu sistema operacional antes de continuar.

## 3. Comando de instalação do projeto

O projeto é gerenciado pelo `uv`, então a forma recomendada de instalar os pacotes é usando o comando `uv add`. Execute o comando abaixo na raiz do projeto:

```bash
uv add mkdocs mkdocs-material "mkdocstrings[python]" mkdocstrings-typescript
```

Vamos entender esse comando passo a passo:

- `uv add` diz ao `uv` para adicionar um ou mais pacotes como dependências do projeto, registrando-os no `pyproject.toml` e instalando-os no ambiente virtual gerenciado pelo `uv`.
- `mkdocs` e `mkdocs-material` são informados como nomes de pacote simples, sem nenhuma sintaxe especial.
- `"mkdocstrings[python]"` está entre aspas e usa a sintaxe de **extra** (`[python]`). Isso é necessário porque:
  - O pacote `mkdocstrings` é um núcleo genérico, que por si só não sabe documentar nenhuma linguagem específica. Ele precisa de um *handler* (manipulador) para cada linguagem que ele deve suportar.
  - O extra `[python]` instala automaticamente o handler Python do `mkdocstrings` (o pacote `mkdocstrings-python`) junto com o núcleo, habilitando a documentação de código Python a partir de docstrings.
  - As aspas são necessárias porque os colchetes (`[` e `]`) têm significado especial em muitos shells (por exemplo, são usados para expansão de glob). Colocar o pacote entre aspas garante que o shell trate `mkdocstrings[python]` como um texto literal e o passe exatamente assim para o `uv`, em vez de tentar interpretá-lo.
- `mkdocstrings-typescript` é instalado como um pacote separado, e não como um extra. Esse pacote adiciona um **handler para TypeScript** ao `mkdocstrings`, permitindo documentar código `.ts` da mesma forma que o handler Python documenta código `.py`. Ele é útil caso o projeto venha a incluir arquivos TypeScript no futuro: o mesmo mecanismo de diretivas do `mkdocstrings` poderá ser usado para gerar documentação a partir desse código, sem precisar de outra ferramenta.

### Instalar Node.js, npm e TypeDoc para documentação TypeScript

O `uv add` e o `uv sync` instalam dependências Python; eles não instalam o Node.js, o npm ou o TypeDoc. Quando uma página usa o handler TypeScript do `mkdocstrings`, o build precisa executar o comando `typedoc`. Por isso, além dos pacotes Python, instale o Node.js (que inclui o npm) e o TypeDoc.

1. Instale a versão LTS do [Node.js](https://nodejs.org/en/download/). O npm é instalado junto com ele.
2. Feche e abra novamente o terminal e confirme que os comandos estão disponíveis:

   ```powershell
   node --version
   npm --version
   ```

3. Se Node.js estiver instalado no local padrão do Windows, mas `node` ou `npm` não forem reconhecidos no PowerShell, adicione temporariamente os diretórios ao `PATH` da janela atual:

   ```powershell
   $env:Path = "C:\Program Files\nodejs;$env:APPDATA\npm;$env:Path"
   node --version
   npm --version
   ```

   Para manter a correção em novos terminais, abra **Editar as variáveis de ambiente do sistema** → **Variáveis de Ambiente** → `Path` (variáveis do usuário) e adicione `C:\Program Files\nodejs` e `%APPDATA%\npm`. Depois, abra um novo terminal. Se o Node.js estiver instalado em outro diretório, use o caminho real da instalação.

4. Instale o TypeDoc globalmente pelo npm e confirme que o comando está disponível:

   ```powershell
   npm install --global typedoc
   typedoc --version
   ```

Se `node` ou `npm` não forem reconhecidos, o terminal não está encontrando a instalação do Node.js no `PATH`. Se o build falhar com `FileNotFoundError: [WinError 2]`, confira também se o TypeDoc foi instalado globalmente e se `%APPDATA%\npm` está no `PATH`. Veja os passos detalhados na página [Exemplos de código](exemplos-codigo.md#pré-requisito-instalar-o-typedoc).

## 4. O que cada pacote faz

Para deixar bem claro o papel de cada dependência, segue um resumo individual:

### `mkdocs`

É o motor principal. Lê os arquivos Markdown da pasta `docs/`, aplica a configuração do `mkdocs.yml` (navegação, tema, plugins, extensões) e gera o site estático em HTML/CSS/JS. É ele que fornece os comandos `mkdocs build` (gerar o site) e `mkdocs serve` (visualizar localmente com recarregamento automático).

### `mkdocs-material`

É um tema para o MkDocs, instalado como um pacote independente e ativado na chave `theme.name: material` do `mkdocs.yml`. Fornece a aparência visual do site (cores, tipografia, modo claro/escuro), componentes de interface (como blocos de admonição e abas) e recursos de navegação (busca, índice lateral, botão de topo).

### `mkdocstrings[python]`

É o plugin que conecta o MkDocs ao código-fonte Python. Quando uma página Markdown contém uma diretiva como `::: teste.calcular_media`, o `mkdocstrings` (através do handler Python instalado pelo extra `[python]`) importa o módulo indicado, localiza a função ou classe, lê seu docstring e gera a seção de documentação diretamente no HTML final, formatando parâmetros, tipos de retorno e exceções.

### `mkdocstrings-typescript`

É o handler adicional que ensina o `mkdocstrings` a entender código TypeScript. Ele segue a mesma ideia do handler Python, mas analisa arquivos `.ts`/`.tsx` em vez de `.py`. Mesmo que o projeto ainda não tenha código TypeScript, instalar esse handler desde já deixa a configuração do `mkdocstrings` pronta (seção `plugins.mkdocstrings.handlers.typescript` no `mkdocs.yml`) para o caso de o projeto crescer e passar a incluir esse tipo de arquivo.

## 5. Alternativa: instalação com `pip`

Se você não estiver usando `uv` (por exemplo, em um ambiente que só tem `pip` disponível), é possível instalar os mesmos quatro pacotes com:

```bash
pip install mkdocs mkdocs-material "mkdocstrings[python]" mkdocstrings-typescript
```

O significado de cada parte do comando é o mesmo explicado na seção 3: o extra `[python]` instala o handler Python do `mkdocstrings`, e as aspas evitam que o shell interprete os colchetes como caracteres especiais. A única diferença é que o `pip` instala os pacotes no ambiente Python ativo no momento (por exemplo, um `venv` ativado manualmente), em vez de gerenciar o ambiente e o `pyproject.toml` automaticamente como o `uv` faz.

## 6. Verificando a instalação

Depois de instalar os pacotes, confirme que tudo funcionou corretamente verificando a versão do MkDocs:

```bash
uv run mkdocs --version
```

Se você instalou com `pip`, o comando equivalente é:

```bash
mkdocs --version
```

Em ambos os casos, o comando deve exibir o número da versão instalada do `mkdocs` (por exemplo, `mkdocs, version 1.6.1 from ...`), sem nenhuma mensagem de erro. Se o comando falhar com "comando não encontrado", revise se o ambiente virtual correto está ativo (ou use `uv run`, que já ativa o ambiente do projeto automaticamente) e repita a instalação da seção 3.

## 7. Diagnóstico de imagens e arquivos JavaScript que não carregam

Se o navegador ou o exportador de PDF registrar `ERR_FILE_NOT_FOUND`, confira se o arquivo existe dentro de `docs/`. Os caminhos configurados em `theme.logo`, `theme.favicon`, `extra_css` e `extra_javascript` são relativos ao diretório de documentação, não à raiz do repositório.

Por exemplo, estas configurações:

```yaml
theme:
  logo: assets/logo.png
  favicon: assets/favicon.svg

extra_javascript:
  - javascripts/mathjax.js
```

exigem que os arquivos estejam nestes locais:

```text
docs/
├── assets/
│   ├── logo.png
│   └── favicon.svg
└── javascripts/
    └── mathjax.js
```

No PowerShell, confirme os arquivos antes de gerar o site:

```powershell
Test-Path .\docs\assets\logo.png
Test-Path .\docs\assets\favicon.svg
Test-Path .\docs\javascripts\mathjax.js
```

Se `extra_javascript` aponta para um arquivo que não existe, crie-o no caminho esperado ou remova a referência do `mkdocs.yml` se ela não for necessária. O MkDocs copia arquivos existentes de `docs/` para `site/`; não cria esses arquivos por causa da configuração.

Confira também se a extensão corresponde ao formato real da imagem. Renomear um PNG para `.ico` não o converte em ícone ICO: use `.png` no arquivo e na configuração, ou converta-o para ICO de verdade. Isso evita que o servidor envie um tipo de conteúdo incompatível com os bytes da imagem.

Em imagens inseridas no Markdown, use o caminho relativo ao arquivo dentro de `docs/`. Por exemplo, em `docs/index.md`, para exibir `docs/assets/Imagem13.jpg`, escreva:

```markdown
![Logotipo](assets/Imagem13.jpg){: width="300" align="right" }
```

Não use `/docs/assets/Imagem13.jpg`: `docs/` é o diretório-fonte do MkDocs e não faz parte da URL publicada. Um `/` inicial aponta para a raiz do domínio. Confirme tanto o arquivo-fonte quanto o arquivo copiado para o site:

```powershell
Test-Path .\docs\assets\Imagem13.jpg
Test-Path .\site\assets\Imagem13.jpg
```

Depois de corrigir os caminhos, gere o site novamente e confirme que os recursos foram copiados:

```powershell
uv run mkdocs build --clean
Test-Path .\site\assets\logo.png
Test-Path .\site\javascripts\mathjax.js
```

Se os arquivos estiverem presentes mesmo assim, abra as ferramentas de desenvolvedor do navegador e confira a aba **Network**: ela mostra a URL requisitada e o status HTTP que falhou. Verifique também letras maiúsculas/minúsculas nos nomes; isso importa quando o site é publicado no Linux pelo GitHub Actions.
