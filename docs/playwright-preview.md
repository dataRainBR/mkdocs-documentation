---
pdf: false
---

# Preview com Playwright

## 1. Introdução

O arquivo `docs_preview.py`, na raiz do projeto, é um script auxiliar que automatiza todo o fluxo de "gerar e abrir" a documentação. Sem ele, conferir o resultado final do site exigiria pelo menos três passos manuais: rodar `uv run mkdocs build` (ou `mkdocs serve`), iniciar algum servidor HTTP apontando para a pasta `site/` (lembrando que abrir `site/index.html` direto via `file://` quebra a busca do tema Material, como já explicado na página [Exemplos do notebook](exemplos-notebook.md)) e, por fim, abrir o navegador manualmente no endereço correto.

O `docs_preview.py` atualiza a página `docs/referencias.md` a partir das dependências declaradas, builda a documentação, inicia um servidor HTTP local servindo a pasta `site/` e abre a página inicial em uma janela real do navegador Chromium, já maximizada, esperando apenas que você aperte Enter no terminal quando quiser fechar tudo. É um script pensado para quem quer apenas *ver o resultado*, sem se preocupar com os comandos individuais de build e servidor.

## 2. Instalação do Playwright

Antes de rodar o script, é preciso instalar duas coisas em sequência: o pacote Python do Playwright e o navegador que ele controla. São etapas diferentes, e as duas são obrigatórias.

```bash
uv add playwright
```

Esse comando adiciona o pacote Python `playwright` às dependências do projeto, registrando-o no `pyproject.toml` e instalando-o no ambiente gerenciado pelo `uv` — da mesma forma que `uv add mkdocs` faz com o MkDocs. O pacote `playwright` instalado aqui é apenas a **biblioteca de automação**: o código Python que sabe como conversar com um navegador e controlá-lo (abrir páginas, clicar, esperar, fechar etc.).

```bash
uv run playwright install chromium
```

Esse segundo comando baixa e instala o **binário do navegador Chromium** que o Playwright vai controlar. Essa é uma etapa separada e obrigatória porque o pacote Python instalado no passo anterior não inclui o navegador em si — ele só contém a API que sabe *como* controlar um navegador, não o navegador executável. O Playwright suporta vários motores de navegador (Chromium, Firefox, WebKit), e cada um precisa ser baixado individualmente através do comando `playwright install <nome-do-navegador>`. Sem rodar esse segundo comando, o pacote Python estaria instalado, mas qualquer tentativa de abrir um navegador falharia, porque não haveria nenhum executável de Chromium disponível para ser lançado.

Na prática, você normalmente só precisa rodar os dois comandos acima uma vez por máquina. O próprio `docs_preview.py` também verifica e garante a instalação do Chromium automaticamente a cada execução (através da função `ensure_playwright_browser_installed`, descrita mais abaixo), então mesmo que você esqueça o segundo comando, o script tenta corrigir isso por conta própria na primeira vez que for executado.

## 3. O que é o Playwright e por que ele é usado aqui

O Playwright é uma biblioteca de automação de navegador, originalmente criada para testes end-to-end de aplicações web. Com ela, é possível escrever código que abre um navegador real (Chromium, Firefox ou WebKit), navega até uma URL, interage com elementos da página (clica em botões, preenche formulários, espera elementos aparecerem) e inspeciona o resultado — tudo de forma programática, sem precisar de um ser humano clicando manualmente.

No contexto do `docs_preview.py`, o Playwright não é usado para testar nada: ele é usado apenas pela sua capacidade de **abrir uma janela de navegador real e controlada por código**. Em vez de instruir o usuário a abrir o navegador manualmente e digitar um endereço, o script usa o Playwright para:

- lançar uma instância do Chromium já maximizada (`--start-maximized`);
- navegar automaticamente até o endereço do servidor local que acabou de ser iniciado;
- manter essa janela aberta até o usuário decidir encerrar (pressionando Enter no terminal), encerrando o navegador de forma limpa em seguida.

Ou seja, o Playwright é a peça que transforma o fluxo de "build + preview" em um único comando de terminal: ao rodar o script, a documentação é gerada e a janela do navegador já aparece na tela, sem nenhuma ação manual adicional.

## 4. Documentação das funções via mkdocstrings

O `docs_preview.py` define sete funções públicas, incluindo `generate_references_markdown`, que gera a página de referências; as funções têm docstrings em pt-BR no estilo Google. Em vez de repetir essas docstrings manualmente nesta página — o que criaria o mesmo risco de desatualização discutido na página [Exemplos de código](exemplos-codigo.md) —, usamos uma única diretiva do `mkdocstrings` apontando para o **módulo inteiro**, em vez de uma diretiva por função:

```markdown
::: docs_preview
```

Como o `docs_preview.py` está localizado na raiz do projeto — exatamente o mesmo lugar onde está o `teste.py`, usado como exemplo na página de Exemplos de código —, a configuração `paths: [.]` já existente em `plugins.mkdocstrings.handlers.python` no `mkdocs.yml` também resolve o módulo `docs_preview` sem precisar de nenhuma configuração extra. Essa configuração diz ao handler Python do `mkdocstrings` para procurar módulos a partir da raiz do projeto, e tanto `teste.py` quanto `docs_preview.py` moram nesse mesmo diretório.

Ao apontar a diretiva para o módulo inteiro (`docs_preview`), em vez de uma função específica (como `docs_preview.main`), o `mkdocstrings` importa o módulo e renderiza automaticamente a documentação de **todas** as funções públicas definidas nele, uma após a outra, cada uma com sua assinatura e suas seções `Args`/`Returns`/`Raises` extraídas da docstring real. Abaixo, a diretiva é inserida de verdade na página, para que o `mkdocstrings` a processe:

::: docs_preview

### Função `generate_references_markdown`

Essa função mantém `docs/referencias.md` sincronizado com as dependências do projeto. Ela prioriza a lista `project.dependencies` do `pyproject.toml`, usa `tool.uv.sources` para apontar dependências Git à origem/revisão configurada e gera links do PyPI para os demais pacotes. Se o TOML não declarar dependências, usa `requirements.txt`; arquivos incluídos com `-r` também são lidos.

O arquivo gerado contém a tabela de dependências, o comando `uv sync` e uma diretiva do `mkdocstrings` para exibir a própria implementação da função. No preview local, ela roda antes do build. No GitHub Actions, o workflow a executa explicitamente antes de `mkdocs build`, para que a versão publicada inclua sempre a lista atual.

Para gerar apenas a página, sem iniciar o preview:

```bash
uv run docs_preview.py --generate-references
```

## 5. Como executar o script

Com o Playwright e o Chromium instalados, basta rodar:

```bash
uv run docs_preview.py
```

O script atualiza `docs/referencias.md` antes de iniciar o build. A execução isolada da função, sem abrir o navegador, está descrita na subseção anterior.

O `docs_preview.py` é um "script uv" autocontido: ele tem metadados no formato PEP 723 escritos em um comentário no topo do próprio arquivo, declarando que precisa do pacote `playwright>=1.47`. Graças a esses metadados, o `uv run` consegue criar automaticamente um ambiente Python efêmero contendo apenas essa dependência e executar o script dentro dele — sem precisar que você rode `uv add` ou `uv sync` manualmente antes. Isso é diferente de `teste.py`, por exemplo, que depende das dependências já declaradas no `pyproject.toml` do projeto.

Ao ser executado, o script segue o seguinte fluxo, na ordem:

1. **Geração de referências**: lê `pyproject.toml` ou, como alternativa, `requirements.txt` e atualiza `docs/referencias.md`.
2. **Build do MkDocs**: chama o executável `mkdocs` dentro do `.venv` do projeto diretamente (em vez de `uv run mkdocs build`), gerando o site estático atualizado em `site/`.
3. **Servidor HTTP local**: encontra uma porta TCP livre na máquina e inicia um servidor HTTP em segundo plano, servindo o conteúdo de `site/` em `http://127.0.0.1:<porta>/`.
4. **Abertura no Chromium**: garante que o Chromium do Playwright esteja instalado e, em seguida, abre a URL do servidor local em uma janela do Chromium maximizada, controlada pelo Playwright.
5. **Espera por Enter**: o terminal exibe a mensagem "Navegador aberto. Pressione Enter aqui para fechar..." e o script fica parado nesse ponto até você apertar Enter; só então o navegador é fechado e o servidor HTTP local é encerrado.
