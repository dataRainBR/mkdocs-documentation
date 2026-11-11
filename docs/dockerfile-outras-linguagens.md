# Dockerfile e outras linguagens

## 1. Por que não existe um handler de mkdocstrings para estas linguagens

Nas páginas [Exemplos de código](exemplos-codigo.md) e [Preview com Playwright](playwright-preview.md), o plugin `mkdocstrings` gerou documentação automaticamente a partir do código-fonte real do projeto, usando diretivas como `::: teste.calcular_media`, `::: calcular-media` e `::: docs_preview`. Isso só é possível porque o `mkdocstrings` depende de um **handler** específico para cada linguagem — um componente capaz de ler o código-fonte, entender sua estrutura (módulos, funções, parâmetros, tipos) e extrair uma documentação estruturada a partir de comentários no formato de docstring:

- o handler `python` sabe interpretar docstrings no estilo Google (seções `Args`, `Returns`, `Raises`), como visto em `teste.calcular_media`;
- o handler `typescript` sabe interpretar comentários JSDoc (`@param`, `@returns`, `@throws`), delegando a leitura real do código para o TypeDoc, como visto em `calcular-media`.

Dockerfile, JavaScript puro (sem um toolchain de documentação configurado), YAML, Terraform, Shell e SQL **não possuem um handler oficial equivalente disponível neste projeto**. Não é que essas linguagens sejam "piores" ou que seus arquivos não possam ser documentados — é que não existe, aqui, um parser de docstring estruturado e configurado para extrair `Args`/`Returns`/`Raises` (ou equivalente) a partir de um `Dockerfile`, de um script Shell ou de uma consulta SQL, por exemplo.

Diante dessa limitação, há três caminhos possíveis para mostrar esse código na documentação:

1. **Copiar e colar o conteúdo manualmente** em um bloco de código estático — a abordagem mais simples, mas que corre o risco de ficar desatualizada em relação ao arquivo real, exatamente como já discutido para o bloco estático de `calcular_media` na página de Exemplos de código.
2. **Tentar usar o `mkdocstrings`** — não é uma opção aqui, já que não há handler configurado para nenhuma dessas linguagens neste projeto.
3. **Incorporar o conteúdo real do arquivo diretamente na página**, através da extensão `pymdownx.snippets` — a abordagem adotada nesta página, e explicada em detalhe a seguir.

## 2. Ferramentas complementares: Hadolint e Docker Buildx

Antes de entrar na técnica de incorporação, vale mencionar duas ferramentas comumente usadas junto de um `Dockerfile`, embora nenhuma das duas tenha sido instalada ou executada como parte desta documentação — elas são citadas aqui apenas como prática recomendada, para quem quiser ir além da leitura do código.

- **Hadolint**: um linter dedicado a arquivos `Dockerfile`. Ele analisa o arquivo em busca de problemas comuns de boas práticas, como ordenação ineficiente de camadas (o que invalida o cache de build sem necessidade), uso de `apt-get install` sem `--no-install-recommends`, falta de pinagem de versão em imagens base (`FROM python:3.12-slim` em vez de `FROM python` sem tag) e outras recomendações equivalentes às de um linter de código tradicional, só que voltadas especificamente para instruções Docker. Ele pode ser executado sem instalação local, via container, apontando o próprio `Dockerfile` para dentro dele pela entrada padrão:

  ```bash
  docker run --rm -i hadolint/hadolint < Dockerfile
  ```

- **Docker Buildx**: a extensão de build do Docker usada para efetivamente construir a imagem a partir do `Dockerfile`, com suporte a multi-estágio, cache avançado e múltiplas plataformas. Rodar um build é a forma mais direta de confirmar que o `Dockerfile` realmente funciona, não apenas que ele está bem escrito:

  ```bash
  docker buildx build .
  ```

Nenhum desses dois comandos foi executado neste ambiente — não há Docker instalado nesta máquina de documentação —, então o `Dockerfile` desta página foi revisado manualmente, mas não teve seu lint ou seu build validados automaticamente por essas ferramentas.

## 3. A técnica de incorporação: `pymdownx.snippets`

A extensão `pymdownx.snippets`, parte do pacote `pymdown-extensions`, adiciona uma sintaxe especial que pode ser usada **dentro** de um bloco de código Markdown: a linha `--8<-- "caminho/arquivo"`. Quando o MkDocs processa a página, ele substitui essa linha pelo conteúdo real do arquivo apontado, mantendo o restante do bloco de código (as crases de abertura/fechamento e a linguagem indicada para destaque de sintaxe) exatamente como foi escrito. Por exemplo:

````markdown
```dockerfile
--8<-- "Dockerfile"
```
````

O resultado, depois de processado pelo `mkdocs build`, é um bloco de código `dockerfile` contendo o conteúdo inteiro do arquivo `Dockerfile` da raiz do projeto, com o destaque de sintaxe apropriado para essa linguagem.

Isso só funciona sem configuração adicional por página porque a extensão `pymdownx.snippets` está configurada com a opção `base_path: .` na seção `markdown_extensions` do `mkdocs.yml`:

```yaml
markdown_extensions:
  - pymdownx.snippets:
      base_path: .
```

O `base_path: .` diz ao `pymdownx.snippets` que todo caminho usado em `--8<-- "..."` deve ser resolvido **a partir da raiz do projeto** — o mesmo diretório em que os comandos `mkdocs build`/`mkdocs serve` são executados. É por isso que `--8<-- "Dockerfile"` encontra o `Dockerfile` da raiz, e `--8<-- "examples/exemplo.js"` encontra o arquivo dentro da pasta `examples/`, sem que cada página precise declarar seu próprio caminho base.

Duas características importantes dessa técnica:

- **O conteúdo é sempre lido do arquivo real a cada build.** Diferente de copiar e colar manualmente o texto de um arquivo dentro da página Markdown, a linha `--8<-- "caminho/arquivo"` não armazena nenhum conteúdo — ela é apenas uma referência. Toda vez que `mkdocs build` (ou `mkdocs serve`) roda, o MkDocs lê o arquivo naquele exato momento e insere seu conteúdo atual no lugar da referência. Se o `Dockerfile` for alterado no futuro, a próxima vez que o site for reconstruído já mostrará a versão atualizada, sem que ninguém precise editar esta página.
- **É uma incorporação de texto bruto, não uma extração estruturada.** Essa é a diferença principal entre `pymdownx.snippets` e o `mkdocstrings`, usado nas páginas anteriores. O `mkdocstrings` interpreta o código-fonte (importa o módulo Python, ou processa o `.d.ts` via TypeDoc) e gera um HTML estruturado com cabeçalho, assinatura e seções separadas para `Args`/`Returns`/`Raises`, a partir de uma docstring. O `pymdownx.snippets`, por outro lado, não entende o conteúdo do arquivo: ele simplesmente copia todo o texto do arquivo, caractere a caractere, para dentro do bloco de código, sem extrair assinatura, parâmetros ou qualquer outra informação estruturada — é o mesmo texto que estaria lá se alguém tivesse colado manualmente, só que sempre sincronizado com o arquivo real.

## 4. Dockerfile

O `Dockerfile` deste projeto, na raiz, usa **dois estágios de build**:

- `builder`: instala as dependências do projeto com `uv sync --frozen --no-dev`, a partir de `pyproject.toml` e `uv.lock`, e copia o código-fonte da aplicação.
- `runtime`: copia apenas o ambiente virtual já resolvido e o código-fonte do estágio `builder`, sem as ferramentas usadas durante a instalação, resultando em uma imagem final mais leve. O comando padrão do container é `CMD ["python", "main.py"]`.

Abaixo, o conteúdo do `Dockerfile` é incorporado de verdade na página, através de `--8<-- "Dockerfile"`:

```dockerfile
--8<-- "Dockerfile"
```

## 5. Outras linguagens

Esta seção reúne os cinco arquivos de exemplo do diretório `examples/`, cada um representando uma linguagem sem handler de mkdocstrings configurado neste projeto. Cada subseção incorpora o conteúdo real do arquivo correspondente.

### JavaScript

O arquivo `examples/exemplo.js` define uma função `calcularMedia` em JavaScript puro — sem TypeScript, sem anotações de tipo e sem um toolchain de documentação como o TypeDoc, por isso não há como gerar sua documentação via `mkdocstrings` (diferente do exemplo equivalente em TypeScript, visto na página de Exemplos de código).

```javascript
--8<-- "examples/exemplo.js"
```

### YAML

O arquivo `examples/exemplo.yaml` é um pequeno arquivo de configuração, no mesmo formato usado pelo próprio `mkdocs.yml` deste projeto.

```yaml
--8<-- "examples/exemplo.yaml"
```

### Terraform

O arquivo `examples/exemplo.tf` declara um recurso Terraform simples. Embora a extensão do arquivo seja `.tf`, o destaque de sintaxe usado abaixo é `hcl` — a sigla de *HashiCorp Configuration Language*, a linguagem de configuração em que o Terraform é escrito (não existe uma linguagem de destaque chamada literalmente "terraform" nos realces de sintaxe usados pelo MkDocs).

```hcl
--8<-- "examples/exemplo.tf"
```

### Shell

O arquivo `examples/exemplo.sh` é um script Shell simples, que builda e publica uma imagem Docker — unindo conceitualmente esta página à seção sobre o `Dockerfile` acima.

```bash
--8<-- "examples/exemplo.sh"
```

### SQL

O arquivo `examples/exemplo.sql` contém uma criação de tabela e uma consulta simples, calculando a média de uma coluna numérica — o mesmo tipo de cálculo da função `calcular_media`/`calcularMedia`, só que expresso em SQL.

```sql
--8<-- "examples/exemplo.sql"
```

## 6. Resumo

| Linguagem  | Arquivo                 | Destaque de sintaxe |
|------------|--------------------------|----------------------|
| Dockerfile | `Dockerfile`             | `dockerfile`         |
| JavaScript | `examples/exemplo.js`    | `javascript`         |
| YAML       | `examples/exemplo.yaml`  | `yaml`               |
| Terraform  | `examples/exemplo.tf`    | `hcl`                |
| Shell      | `examples/exemplo.sh`    | `bash`               |
| SQL        | `examples/exemplo.sql`   | `sql`                |

Em todos os seis casos, o conteúdo exibido acima nesta página não foi copiado e colado: cada bloco de código contém uma linha `--8<-- "caminho/arquivo"`, resolvida pela extensão `pymdownx.snippets` a cada build a partir da raiz do projeto (`base_path: .`). Isso garante que, se qualquer um desses seis arquivos for alterado, esta página mostrará automaticamente a versão mais recente na próxima vez que `mkdocs build` ou `mkdocs serve` for executado.
