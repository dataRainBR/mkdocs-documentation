# Git

Git é um sistema distribuído de controle de versão. Ele registra alterações em arquivos, permite criar linhas paralelas de trabalho (branches) e combinar essas alterações. GitHub é um serviço para hospedar repositórios Git e colaborar pela web; os comandos `git` funcionam localmente e não exigem o GitHub para criar commits.

## 1. Instalar e configurar a identidade

Instale o Git para seu sistema operacional e confirme que ele está disponível:

```powershell
git --version
```

Configure o nome e o e-mail que serão gravados nos commits. Use o endereço que deseja associar às contribuições; se quiser ocultar seu e-mail pessoal no GitHub, use o endereço `noreply` fornecido nas configurações da conta.

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@example.com"
git config --global init.defaultBranch main
```

Confira as configurações:

```bash
git config --global --list
```

Esses valores identificam autoria nos commits; não autenticam no GitHub. Para operações remotas, configure HTTPS com o GitHub CLI ou uma chave SSH. Veja também o [guia de GitHub CLI](github-cli.md).

## 2. Criar um repositório ou clonar um existente

Para iniciar um repositório Git em uma pasta local:

```bash
mkdir meu-projeto
cd meu-projeto
git init -b main
```

Para obter uma cópia local de um repositório que já existe no GitHub:

```bash
git clone https://github.com/ORGANIZACAO/REPOSITORIO.git
cd REPOSITORIO
```

Confira o estado e os endereços remotos configurados:

```bash
git status
git remote -v
```

### Conectar uma pasta local a um repositório remoto

Crie o repositório remoto primeiro no GitHub. Se a pasta local ainda não tiver commits, crie um arquivo inicial e registre-o:

```bash
echo "# Meu projeto" > README.md
git add README.md
git commit -m "docs: inicia o projeto"
```

Se a pasta já tem commits, não repita essa etapa. Configure `origin` e envie a branch principal:

```bash
git remote add origin https://github.com/ORGANIZACAO/REPOSITORIO.git
git remote -v
git push -u origin main
```

`origin` é apenas o nome convencional do remote. Se ele já existir, veja sua URL com `git remote -v` antes de alterá-la. Para configurar autenticação HTTPS pelo GitHub CLI:

```bash
gh auth login
gh auth setup-git
```

## 3. Ciclo básico: revisar, preparar e commitar

O Git só inclui no commit os arquivos que foram preparados com `git add`. Revise as alterações antes de registrá-las:

```bash
git status
git diff
git add docs/guia.md
git diff --staged
git commit -m "docs: adiciona guia do projeto"
```

Use `git add` com caminhos específicos para não incluir arquivos acidentais. Para adicionar todas as alterações rastreadas e não rastreadas, primeiro confira `git status` e então use:

```bash
git add -A
```

Um commit é salvo no histórico local. Para ver os commits recentes:

```bash
git log --oneline --graph --decorate -10
```

## 4. Branches, `pull`, `fetch` e `push`

Uma branch permite desenvolver uma alteração sem modificar diretamente a branch principal. Um fluxo comum é atualizar `main`, criar uma branch e trabalhar nela:

```bash
git switch main
git pull --ff-only
git switch -c docs/novo-capitulo
```

- `git fetch` baixa novos commits e atualiza as referências remotas, sem integrá-los à branch atual.
- `git pull` busca e integra as alterações da branch remota que está sendo acompanhada. `--ff-only` evita criar um merge commit automaticamente se houver divergência.
- `git push` envia commits locais para o remote.

Depois de commitar as alterações na branch, publique-a e configure o acompanhamento remoto:

```bash
git add docs/novo-capitulo.md
git commit -m "docs: adiciona novo capítulo"
git push -u origin docs/novo-capitulo
```

Após configurar a branch remota uma vez, os próximos envios podem usar:

```bash
git push
git pull
```

## 5. Integrar alterações com merge

O `merge` combina os commits de uma branch na branch atual. Depois que uma revisão de Pull Request estiver aprovada, atualize `main` e faça o merge da branch de trabalho:

```bash
git switch main
git pull --ff-only
git merge --no-ff docs/novo-capitulo
git push origin main
```

Em projetos colaborativos, geralmente o merge é feito no Pull Request pelo GitHub, em vez de enviar diretamente à branch principal. Isso permite revisão e verificações automáticas antes da integração.

### Resolver conflitos de merge

Se duas branches alterarem as mesmas linhas, o Git marca um conflito nos arquivos. Confira os caminhos afetados:

```bash
git status
```

Abra cada arquivo e escolha o conteúdo correto entre os marcadores `<<<<<<<`, `=======` e `>>>>>>>`. Depois de editar e revisar o resultado, marque o conflito como resolvido e conclua o merge:

```bash
git add caminho/do/arquivo
git diff --staged
git commit
```

Não apague os marcadores sem decidir qual conteúdo deve permanecer. Se ainda não começou a resolver e quiser cancelar um merge em andamento:

```bash
git merge --abort
```

## 6. Ignorar arquivos e desfazer alterações com segurança

O arquivo `.gitignore` lista arquivos locais ou gerados que não devem ser adicionados ao Git. Por exemplo:

```gitignore
.venv/
__pycache__/
site/
.env
```

Confira o que será incluído antes de commitar, especialmente arquivos de configuração local, logs e credenciais:

```bash
git status --short
git diff
```

Para desfazer uma alteração já commitada sem reescrever o histórico compartilhado, crie um commit inverso:

```bash
git revert HASH-DO-COMMIT
```

Evite `git push --force` em branches compartilhadas; ele pode remover commits publicados por outros colaboradores. Para aprender a criar Pull Requests e fazer merge pelo GitHub, consulte [GitHub CLI (`gh`)](github-cli.md).

## 7. Comandos principais

| Comando | Uso |
|---|---|
| `git status` | Mostra a branch atual e as alterações. |
| `git diff` | Exibe alterações ainda não preparadas. |
| `git add` | Prepara arquivos para o próximo commit. |
| `git commit` | Registra as alterações preparadas no histórico local. |
| `git log` | Consulta o histórico de commits. |
| `git switch` | Muda de branch ou cria uma branch. |
| `git fetch` | Atualiza referências remotas sem integrar commits. |
| `git pull` | Busca e integra alterações remotas. |
| `git push` | Publica commits locais no repositório remoto. |
| `git merge` | Integra o histórico de uma branch à branch atual. |
| `git remote -v` | Lista os remotes configurados. |

Para consultar as opções de qualquer comando:

```bash
git help <comando>
git help push
```

## 8. Referências oficiais

- [Git: primeiros passos](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [Manual do Git](https://git-scm.com/docs)
- [Conectar-se ao GitHub com SSH](https://docs.github.com/authentication/connecting-to-github-with-ssh)
- [GitHub CLI (`gh`)](github-cli.md)
