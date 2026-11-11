# ---------------------------------------------------------------------------
# Estágio 1: builder — instala as dependências do projeto em um ambiente
# isolado, usando o gerenciador uv e os arquivos de lock já existentes
# (pyproject.toml / uv.lock), antes de copiar o código-fonte da aplicação.
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

# Copia o binário oficial do uv (já compilado) para dentro da imagem, em vez
# de instalá-lo via pip, mantendo o estágio de build mais rápido e leve.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Define o diretório de trabalho onde o projeto será montado dentro da imagem.
WORKDIR /app

# Copia primeiro apenas os arquivos de manifesto de dependências, para que o
# cache de camadas do Docker seja reaproveitado quando só o código mudar.
COPY pyproject.toml uv.lock ./

# Instala exatamente as dependências travadas em uv.lock (--frozen), sem os
# grupos de desenvolvimento (--no-dev), mantendo o ambiente final mínimo.
RUN uv sync --frozen --no-dev

# Copia o código-fonte real da aplicação (main.py) e do exemplo documentado
# via mkdocstrings (teste.py) para dentro da imagem builder.
COPY main.py teste.py ./

# ---------------------------------------------------------------------------
# Estágio 2: runtime — imagem final, menor, contendo apenas o ambiente
# virtual já resolvido pelo uv e o código necessário para executar a
# aplicação, sem as ferramentas de build usadas no estágio anterior.
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

# Define o mesmo diretório de trabalho usado no estágio builder.
WORKDIR /app

# Copia o ambiente virtual já criado pelo uv no estágio builder, evitando
# reinstalar dependências e reduzindo o tamanho e o tempo de build da
# imagem final.
COPY --from=builder /app/.venv /app/.venv

# Copia o código-fonte já validado no estágio builder.
COPY --from=builder /app/main.py /app/teste.py ./

# Adiciona o ambiente virtual ao PATH, para que o comando `python` resolva
# para o interpretador e os pacotes instalados pelo uv, sem precisar
# ativar manualmente o ambiente virtual.
ENV PATH="/app/.venv/bin:$PATH"

# Define o comando padrão executado quando o container é iniciado. Este
# projeto não possui um pacote `src/` de aplicação (a pasta `src/`
# existente é o pacote de exemplo TypeScript de outra parte da
# documentação, não a aplicação), então o entrypoint real é o script
# `main.py` na raiz do projeto.
CMD ["python", "main.py"]
