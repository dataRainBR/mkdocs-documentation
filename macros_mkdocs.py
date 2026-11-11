"""macros_mkdocs.py — módulo de macros do plugin `mkdocs-macros-plugin`.

Módulo dedicado de macros/variáveis Jinja2 para o Documentation_Site,
referenciado explicitamente via `module_name: macros_mkdocs` na configuração
do plugin `macros` em `mkdocs.yml`.

Por padrão, o `mkdocs-macros-plugin` procura um arquivo `main.py` na raiz do
projeto para usar como módulo de macros. Neste projeto, porém, `main.py` já
é a aplicação real (`def main(): ...`), e não um módulo de macros — por
isso a opção `module_name` é usada para apontar para este arquivo dedicado
em vez do padrão.
"""


def define_env(env):
    """Registra variáveis customizadas disponíveis nas páginas Markdown."""
    env.variables["projeto"] = "teste-mkdocks"
