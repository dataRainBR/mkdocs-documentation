# Exemplos de código

Esta página ensina a documentar código Python e TypeScript no MkDocs. Em ambos os casos, o fluxo é: escrever a documentação no próprio código, configurar o handler correspondente e incluir uma diretiva `mkdocstrings` na página Markdown. O resultado aparece como documentação HTML gerada durante o build.

## Python com docstrings no formato Google

### 1. Escreva a função e a docstring em `teste.py`

O formato Google organiza a explicação em seções como `Args`, `Returns` e `Raises`. A descrição do argumento fica indentada sob `Args`; inclua o tipo na anotação Python e descreva o significado no texto:

```python
def calcular_media(valores: list[float]) -> float:
    """
    Calcula a média de uma lista de valores.

    Args:
        valores: Lista de valores numéricos.

    Returns:
        Média aritmética dos valores.

    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not valores:
        raise ValueError("A lista não pode estar vazia.")

    return sum(valores) / len(valores)
```

### 2. Configure o handler Python no `mkdocs.yml`

Em `plugins.mkdocstrings.handlers.python`, defina o caminho onde o módulo pode ser encontrado e informe que o parser deve interpretar docstrings Google:

````yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          paths: [.]
          options:
            show_source: true
            show_root_heading: true
            docstring_style: google
        typescript: {}
````

`paths: [.]` permite localizar `teste.py` na raiz do projeto. `docstring_style: google` faz o handler reconhecer as seções no formato Google; não altera a escrita do docstring.

### 3. Inclua o objeto na página Markdown

Escreva a diretiva no arquivo Markdown sem cercá-la por crases:

```markdown
::: teste.calcular_media
```

**Saída renderizada pelo MkDocs:** a diretiva abaixo é processada de verdade no build. O cabeçalho, a assinatura e as seções da documentação vêm de `teste.py`:

::: teste.calcular_media

## Bloco de código estático

O trecho de Python mostrado acima é um **bloco de código estático**: um texto fixo, delimitado por crases (` ``` `) com a linguagem `python` indicada logo após as crases de abertura. Essa é a forma mais simples de exibir um exemplo de código em uma página MkDocs — você simplesmente copia e cola o conteúdo do arquivo-fonte (neste caso, `teste.py`) diretamente dentro do Markdown da página.

Não há nenhuma "mágica" por trás desse bloco: o MkDocs não lê `teste.py` para gerá-lo, não executa nada e não sabe que essa função realmente existe no projeto. O texto que aparece é exatamente o texto que foi digitado (ou colado) no arquivo `exemplos-codigo.md`. A única coisa que o MkDocs faz é aplicar o destaque de sintaxe (*syntax highlighting*) do Python ao conteúdo, graças às extensões `pymdownx.highlight` e `pymdownx.superfences` configuradas no `mkdocs.yml` — mas o texto em si é escrito manualmente por quem edita a página.

### Como a documentação é gerada

Agora, em vez de colar o código novamente, vamos deixar o plugin `mkdocstrings` gerar a documentação da mesma função automaticamente a partir do código-fonte. A sintaxe usada para isso é a seguinte:

```markdown
::: teste.calcular_media
```

Essa linha é chamada de **diretiva** do `mkdocstrings`. Ela não é um bloco de código: é uma instrução especial, reconhecida pelo plugin durante a geração do site, escrita diretamente no corpo da página Markdown (sem as crases de bloco de código). A diretiva inserida acima é processada pelo `mkdocstrings` e substituída pelo resultado gerado.

Passo a passo do que acontece quando o comando `mkdocs build` (ou `mkdocs serve`) processa essa diretiva:

1. **Leitura da página**: o MkDocs lê o arquivo `exemplos-codigo.md` e encontra a linha `::: teste.calcular_media`, que é reconhecida pelo plugin `mkdocstrings` (configurado na seção `plugins` do `mkdocs.yml`) como uma diretiva válida, e não como texto comum.
2. **Interpretação do identificador**: o `mkdocstrings` interpreta o texto após `:::` — `teste.calcular_media` — como um caminho no formato `módulo.função`. Isso indica ao handler Python do plugin que ele deve procurar um módulo chamado `teste` e, dentro dele, um objeto chamado `calcular_media`.
3. **Importação do módulo**: o handler Python importa o módulo `teste` (ou seja, executa `import teste` internamente), usando a lista `paths: [.]` configurada em `plugins.mkdocstrings.handlers.python` no `mkdocs.yml` para saber que deve procurar esse módulo a partir da raiz do projeto, onde o arquivo `teste.py` realmente está.
4. **Inspeção da função**: com o módulo importado, o `mkdocstrings` inspeciona o objeto `calcular_media` em tempo real — obtém sua assinatura (nome do parâmetro `valores`, anotação de tipo `list[float]`, tipo de retorno `float`) e lê a docstring completa da função, exatamente como ela está escrita em `teste.py` naquele momento.
5. **Geração do HTML**: a partir dessas informações (assinatura + docstring), o plugin gera automaticamente o HTML da documentação da função — incluindo um cabeçalho com o nome e a assinatura, e seções formatadas para `Args`, `Returns` e `Raises`, de acordo com o estilo de docstring configurado (`docstring_style: google`) — e insere esse HTML no lugar onde a diretiva estava escrita.

Em resumo: nada do conteúdo visível acima (assinatura, parâmetros, descrição, seções `Args`/`Returns`/`Raises`) foi digitado manualmente nesta página — tudo foi extraído e formatado automaticamente a partir do código real de `teste.py` no momento do build.

## Bloco estático vs. mkdocstrings — qual usar?

A diferença fundamental entre as duas formas mostradas nesta página está em **de onde vem o conteúdo** e **quando ele é atualizado**:

- **Bloco de código estático**: o conteúdo é um texto fixo, digitado ou colado manualmente dentro do arquivo `exemplos-codigo.md`. Ele representa uma "fotografia" do código no momento em que foi copiado. Se, no futuro, alguém alterar a função `calcular_media` em `teste.py` — por exemplo, mudando um parâmetro, a lógica interna ou a docstring — o bloco estático **não muda automaticamente**. Ele continuará mostrando a versão antiga do código até que alguém edite manualmente a página e cole o trecho atualizado. Ou seja, esse bloco pode ficar **desatualizado (dessincronizado)** em relação ao código real, e a responsabilidade de mantê-lo sincronizado é inteiramente de quem edita a documentação.
- **Diretiva do mkdocstrings** (`::: teste.calcular_media`): o conteúdo **não é armazenado** na página — apenas a referência `teste.calcular_media` é armazenada. Todo o restante (assinatura, parâmetros, docstring) é **gerado dinamicamente a cada execução de `mkdocs build` ou `mkdocs serve`**, lendo o código-fonte de `teste.py` naquele exato momento. Isso significa que, se a função `calcular_media` for alterada, a próxima vez que o site for reconstruído, a documentação exibida mudará automaticamente, sem que ninguém precise editar `exemplos-codigo.md`. Por isso essa forma **nunca fica desatualizada** em relação ao código real.

**Recomendação prática:**

- Use um **bloco de código estático** quando quiser mostrar um trecho de código ilustrativo, hipotético, simplificado ou que não corresponde a uma função real do projeto — por exemplo, um exemplo didático genérico que não precisa (e não deve) ser acoplado a um arquivo específico do código-fonte.
- Use a **diretiva do mkdocstrings** sempre que quiser documentar uma função, classe ou módulo que realmente existe no projeto. Isso evita duplicação de esforço (não é preciso copiar e colar código na documentação) e garante que a documentação do projeto esteja sempre fiel ao comportamento real do código, mesmo depois de várias alterações futuras em `teste.py`.

## Exemplo em TypeScript

As duas seções acima compararam um bloco de código estático com a documentação gerada automaticamente pelo `mkdocstrings`, usando a função Python `calcular_media`. A mesma comparação é repetida agora para um exemplo equivalente em TypeScript, a função `calcularMedia`, definida em `src/calcular-media/src/index.ts`. A diferença é que, para TypeScript, o `mkdocstrings` usa o handler `typescript`, que por sua vez depende do **TypeDoc** para extrair a documentação do código-fonte.

### Bloco de código estático

Assim como no exemplo em Python, o trecho abaixo é uma cópia fixa do conteúdo de `src/calcular-media/src/index.ts`, colada diretamente nesta página:

```typescript
/**
 * Calcula a média de uma lista de valores.
 *
 * @param valores - Lista de valores numéricos.
 * @returns Média aritmética dos valores.
 * @throws {Error} Se a lista estiver vazia.
 */
export function calcularMedia(valores: number[]): number {
  if (valores.length === 0) {
    throw new Error("A lista não pode estar vazia.");
  }

  return valores.reduce((soma, valor) => soma + valor, 0) / valores.length;
}
```

### Pré-requisito: instalar o TypeDoc

Diferente do handler Python do `mkdocstrings`, o handler `typescript` depende do **TypeDoc**, uma ferramenta Node.js que extrai a documentação dos arquivos TypeScript. Neste projeto, `src/calcular-media/typedoc.json` aponta diretamente para `src/index.ts`; não é necessário gerar um arquivo `.d.ts` antes do build.

Primeiro, instale a versão LTS do [Node.js](https://nodejs.org/en/download/). O instalador do Node.js também instala o **npm**, que será usado para instalar o TypeDoc. Depois da instalação, feche e abra novamente o terminal e confirme que os dois comandos estão disponíveis:

```bash
node --version
npm --version
```

Se o Node.js já estiver instalado, mas os comandos não forem reconhecidos no PowerShell, inclua os diretórios padrão nesta janela do terminal:

```powershell
$env:Path = "C:\Program Files\nodejs;$env:APPDATA\npm;$env:Path"
node --version
npm --version
```

Para manter a correção em novos terminais, adicione `C:\Program Files\nodejs` e `%APPDATA%\npm` à variável `Path` do usuário em **Variáveis de Ambiente** do Windows e abra um novo terminal. Se o Node.js estiver instalado em outro local, use o diretório real da instalação.

Em seguida, instale o TypeDoc globalmente:

```bash
npm install --global typedoc
```

O handler do `mkdocstrings` executa o comando `typedoc` diretamente. Confirme que ele está acessível no terminal antes de gerar a documentação:

```bash
typedoc --version
```

Se `typedoc` não for reconhecido, abra um novo terminal para atualizar o `PATH` ou confira se `%APPDATA%\npm` está incluído nele.

### Configure o handler e o pacote TypeScript

O handler TypeScript é habilitado em `mkdocs.yml` com `typescript: {}`. Para cada pacote documentado, o TypeDoc também precisa localizar o projeto e seus arquivos-fonte. Neste exemplo, o pacote está em `src/calcular-media/`:

````yaml
plugins:
  - mkdocstrings:
      handlers:
        typescript: {}
````

O `package.json` identifica o pacote pelo campo `name`. Esse mesmo nome será usado na diretiva:

````json
{
  "name": "calcular-media",
  "private": true
}
````

O arquivo `src/calcular-media/typedoc.json` indica ao TypeDoc o ponto de entrada `.ts` e o `tsconfig.json` do pacote:

````json
{
  "extends": ["../../typedoc.base.json"],
  "entryPointStrategy": "expand",
  "entryPoints": ["src/index.ts"],
  "tsconfig": "tsconfig.json"
}
````

Documente as funções no próprio TypeScript com comentários JSDoc (`/** ... */`) e tags como `@param`, `@returns` e `@throws`, como no exemplo de `calcularMedia` acima. O TypeDoc usa esse arquivo de configuração para extrair a documentação.

O identificador `calcular-media` não é um caminho de arquivo nem o nome de uma função TypeScript: é o valor de `name` em `package.json`. O handler padrão do projeto é o Python, por isso informe `handler: typescript` na diretiva.

Na página `.md`, escreva a diretiva sem cercá-la por crases:

```markdown
::: calcular-media
    handler: typescript
```

**Saída renderizada pelo MkDocs:** a diretiva abaixo é processada no build. O handler localiza o pacote `calcular-media`, executa o TypeDoc e apresenta a documentação extraída do `src/index.ts`:

::: calcular-media
    handler: typescript

### Bloco estático vs. mkdocstrings (TypeScript)

A mesma diferença explicada para o exemplo em Python se aplica aqui: o bloco de código estático acima é uma cópia fixa de `index.ts`, que pode ficar desatualizada se a função `calcularMedia` for alterada e ninguém lembrar de atualizar esta página manualmente. Já a diretiva `::: calcular-media` gera sua documentação dinamicamente a cada build, usando o TypeDoc configurado para ler `src/index.ts`.

Há, porém, uma diferença prática importante em relação ao exemplo Python: a diretiva `::: teste.calcular_media` funciona a partir do arquivo `.py`, enquanto a diretiva `::: calcular-media` precisa do Node.js e do TypeDoc disponíveis no ambiente de build. Não é necessário executar `tsc` separadamente: o TypeDoc lê o arquivo-fonte `.ts` configurado no pacote.

!!! warning "Toolchain do TypeDoc não disponível neste ambiente"
    Se Node.js, npm e TypeDoc não estiverem instalados — ou se o comando `typedoc` não estiver no `PATH` —, o handler `typescript` não consegue gerar a documentação e o build falha ao processar esta diretiva. No Windows, isso pode aparecer como `FileNotFoundError: [WinError 2]` ao tentar iniciar o processo `typedoc`.

    No GitHub Actions, o workflow instala Node.js e TypeDoc antes de executar `uv run mkdocs build --strict`. Em uma máquina local, siga os passos de instalação acima e depois rode `uv run mkdocs build --strict`.

### Diagnóstico: incompatibilidade do decoder do TypeDoc

Além de instalar o Node.js e o TypeDoc, o build precisa de versões compatíveis do handler TypeScript e do decoder que lê o JSON produzido pelo TypeDoc. Uma incompatibilidade entre `griffe-typedoc` 0.1.1 e a saída atual do TypeDoc fazia o build terminar com um erro semelhante a:

```text
Project.__init__() got an unexpected keyword argument 'schema_version'
```

Nesse caso, o TypeDoc já encontrou o ponto de entrada e produziu sua saída; a falha acontece depois, durante a desserialização do JSON pelo `griffe-typedoc`. Portanto, alterar o `tsconfig.json`, a diretiva desta página ou o ponto de entrada não corrige esse erro específico.

A correção foi implementada no [commit upstream d0afb317](https://github.com/mkdocstrings/griffe-typedoc/commit/d0afb31733b2954daed464b5015db6f0e832a21e), que adiciona suporte ao campo `schema_version` no modelo `Project`. Até que essa correção esteja disponível em uma versão publicada no PyPI, este projeto fixa `griffe-typedoc` nesse commit em `pyproject.toml` e `uv.lock`. Mantenha os dois arquivos sincronizados ao atualizar dependências:

```bash
uv lock --check
uv sync
uv run mkdocs build --strict
```

Após essa correção, o build e o deploy pelo GitHub Actions foram executados com sucesso. Para acompanhar uma execução futura, consulte **Actions → Build e publica a documentação** ou use os comandos `gh run list` e `gh run watch` descritos em [GitHub CLI](github-cli.md).
