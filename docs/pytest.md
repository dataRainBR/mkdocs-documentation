# pytest: escrever e executar testes

Um **teste** é um pequeno programa que verifica se outra parte do programa se comporta como esperado. Ele prepara uma entrada, executa uma função e compara o resultado com uma expectativa. Quando uma mudança quebra esse comportamento, o teste ajuda a detectar o problema antes de chegar ao usuário.

pytest é uma ferramenta que encontra e executa testes Python, apresenta erros com contexto e oferece recursos como fixtures e parametrização.

## 1. Instalar pytest e pytest-cov com uv

No terminal, a partir da pasta que contém `pyproject.toml`, instale o pytest e o plugin de cobertura como dependências de desenvolvimento:

```bash
uv add --dev pytest pytest-cov
```

O `pytest-cov` adiciona opções de cobertura ao pytest e usa a biblioteca Coverage.py para medir quais partes do código foram executadas.

## 2. Organizar o código e os testes

Uma estrutura comum para uma biblioteca Python é:

```text
meu-projeto/
├── pyproject.toml
├── src/
│   └── calculadora/
│       ├── __init__.py
│       └── operacoes.py
└── tests/
    └── test_operacoes.py
```

Crie a função que será testada em `src/calculadora/operacoes.py`:

```python
def somar(a: float, b: float) -> float:
    return a + b


def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("O divisor não pode ser zero.")
    return a / b
```

O pytest procura, por padrão, arquivos com nomes como `test_*.py` ou `*_test.py` e funções cujo nome começa com `test_`. Crie `tests/test_operacoes.py`:

```python
import pytest

from calculadora.operacoes import dividir, somar


def test_somar_dois_numeros():
    assert somar(2, 3) == 5


@pytest.mark.parametrize(
    ("a", "b", "esperado"),
    [
        (6, 2, 3),
        (9, 3, 3),
        (-8, 2, -4),
    ],
)
def test_dividir(a, b, esperado):
    assert dividir(a, b) == esperado


def test_dividir_por_zero_informa_erro():
    with pytest.raises(ValueError, match="zero"):
        dividir(10, 0)
```

Neste exemplo, `assert` compara o resultado com o esperado; `pytest.raises` verifica se a função lança a exceção esperada; e `@pytest.mark.parametrize` executa o mesmo teste com várias combinações de dados.

## 3. Executar e selecionar testes

Execute todos os testes na raiz do projeto:

```bash
uv run pytest
```

Opções comuns para controlar a execução:

```bash
uv run pytest -v                         # saída detalhada
uv run pytest -q                         # saída resumida
uv run pytest tests/test_operacoes.py    # seleciona um arquivo
uv run pytest tests/test_operacoes.py::test_somar_dois_numeros
uv run pytest -k dividir                 # seleciona testes pelo nome
uv run pytest -x                         # para na primeira falha
uv run pytest --collect-only             # mostra testes encontrados sem executá-los
```

Uma execução bem-sucedida mostra um resumo semelhante a este:

```text
============================= test session starts =============================
collected 5 items

tests/test_operacoes.py .....                                             [100%]

============================== 5 passed in 0.08s ==============================
```

Se um teste falhar, o pytest mostra a asserção que falhou e os valores observados, facilitando o diagnóstico.

## 4. Usar fixtures e arquivos temporários

Uma **fixture** prepara um valor ou recurso que um teste precisa. pytest fornece, por exemplo, `tmp_path`, uma pasta temporária exclusiva para cada teste:

```python
def test_gravar_arquivo_temporario(tmp_path):
    arquivo = tmp_path / "resultado.txt"
    arquivo.write_text("processado", encoding="utf-8")

    assert arquivo.read_text(encoding="utf-8") == "processado"
```

Também é possível criar fixtures próprias. pytest as encontra pelo nome do argumento da função de teste:

```python
import pytest


@pytest.fixture
def lista_vazia():
    return []


def test_lista_vazia_comeca_sem_itens(lista_vazia):
    assert lista_vazia == []
```

Fixtures ajudam a evitar a repetição de preparação de dados. Cada teste deve continuar claro e, sempre que possível, independente dos demais.

## 5. Configurar pytest no `pyproject.toml`

É possível configurar a descoberta de testes e o relatório básico no mesmo arquivo do uv:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
```

`testpaths` indica onde procurar testes quando você executa `uv run pytest` sem informar um caminho. `addopts = "-ra"` inclui no resumo informações sobre testes ignorados ou marcados como esperados para falhar.

## 6. O que significa cobertura de testes

**Cobertura** estima quanto do código foi executado enquanto os testes rodavam. A cobertura de linhas indica quais linhas executáveis foram percorridas; a cobertura de ramificações também verifica caminhos alternativos, como os lados verdadeiro e falso de um `if`.

Uma cobertura alta **não prova** que o programa está correto: um teste pode executar uma linha sem verificar se o resultado está certo. Use a cobertura para encontrar código sem testes e complemente a métrica com casos que verifiquem comportamentos importantes, entradas inválidas e limites.

## 7. Gerar relatório no terminal e HTML

Execute os testes medindo o pacote `calculadora` e gere um relatório com as linhas não cobertas e outro em HTML:

```bash
uv run pytest \
  --cov=calculadora \
  --cov-report=term-missing \
  --cov-report=html
```

No Windows PowerShell, se preferir evitar a continuação de linha com barra invertida, execute em uma linha:

```powershell
uv run pytest --cov=calculadora --cov-report=term-missing --cov-report=html
```

O pytest-cov imprime o resumo no terminal e cria `htmlcov/index.html`. Abra o relatório localmente pelo navegador ou sirva a pasta na raiz do projeto:

```bash
uv run python -m http.server 8000 --directory htmlcov
```

Depois acesse `http://localhost:8000` e interrompa o servidor com `Ctrl+C` quando terminar. O relatório HTML mostra os arquivos e destaca as linhas executadas e não executadas.

Outros relatórios úteis:

```bash
uv run pytest --cov=calculadora --cov-report=xml
uv run pytest --cov=calculadora --cov-branch --cov-report=term-missing
uv run pytest --cov=calculadora --cov-fail-under=80
```

- **`--cov-report=xml`** gera `coverage.xml`, formato frequentemente consumido por serviços de CI e cobertura.
- **`--cov-branch`** mede também as ramificações.
- **`--cov-fail-under=80`** faz a execução retornar erro se a cobertura ficar abaixo de 80%; o valor é um exemplo e deve ser definido pelo projeto.

Para obter os relatórios de terminal e HTML na mesma execução, informe os dois valores de `--cov-report`, como no primeiro exemplo.

## 8. Configurar cobertura e ignorar arquivos gerados

O `pyproject.toml` também pode conter opções de Coverage.py:

```toml
[tool.coverage.run]
branch = true
source = ["calculadora"]

[tool.coverage.report]
show_missing = true
fail_under = 80
```

`source` limita a medição ao pacote indicado; `branch` habilita a análise de ramificações; `show_missing` lista linhas não cobertas; e `fail_under` define um limite mínimo opcional.

Os arquivos de cobertura são resultados gerados. Não os versione no Git:

```gitignore
.coverage
.coverage.*
coverage.xml
htmlcov/
```

## 9. Executar testes e publicar o relatório no GitHub Actions

Para rodar testes e gerar relatórios em CI, adicione etapas como estas a um job que já tenha feito checkout do repositório e instalado uv:

```yaml
      - name: Instalar dependências
        run: uv sync --locked

      - name: Executar testes e cobertura
        run: >-
          uv run pytest
          --cov=calculadora
          --cov-report=term-missing
          --cov-report=xml
          --cov-report=html

      - name: Disponibilizar relatório HTML
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: cobertura-html
          path: htmlcov/
          if-no-files-found: ignore
```

Depois da execução, abra **GitHub → Actions → execução do workflow → Artifacts** para baixar a pasta HTML e abrir `index.html`. O relatório do terminal e o resultado dos testes também ficam nos logs do job. Para executar os mesmos comandos como tarefas locais e no CI, consulte [Taskipy](taskipy.md).

## Referências oficiais

- [Documentação do pytest](https://docs.pytest.org/en/stable/)
- [Como executar pytest](https://docs.pytest.org/en/stable/how-to/usage.html)
- [Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [Parametrização de testes](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [pytest-cov: relatórios de cobertura](https://pytest-cov.readthedocs.io/en/latest/reporting.html)
- [Taskipy: integrar testes em tarefas](taskipy.md)
