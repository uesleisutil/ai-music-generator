# 🚀 Guia de Deploy no GitHub

## Passo 1: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Nome do repositório: `ai-music-generator` (ou outro nome)
3. Descrição: "🎵 Generate AI music, create covers, and auto-upload to YouTube - 100% free & open-source"
4. Deixe como **Public**
5. **NÃO** marque "Initialize with README" (já temos um)
6. Clique em "Create repository"

## Passo 2: Conectar e Fazer Push

Copie e execute estes comandos no terminal (substitua SEU_USUARIO pelo seu username do GitHub):

```bash
# Adicionar remote
git remote add origin https://github.com/SEU_USUARIO/ai-music-generator.git

# Fazer push
git push -u origin main
```

## Passo 3: Configurar o Repositório

### Adicionar Topics (Tags)
No GitHub, vá em "About" (lado direito) e adicione:
- `ai`
- `music-generation`
- `stable-diffusion`
- `musicgen`
- `youtube`
- `python`
- `open-source`
- `machine-learning`

### Ativar Issues e Discussions
1. Vá em Settings → Features
2. Marque "Issues"
3. Marque "Discussions" (opcional, mas recomendado)

### Adicionar Descrição
No "About", adicione:
- Website: (deixe vazio ou adicione depois)
- Description: "🎵 Generate AI music, create covers, and auto-upload to YouTube - 100% free & open-source"

## Passo 4: Criar Release (Opcional)

1. Vá em "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Initial Release`
4. Description: Copie do CHANGELOG.md
5. Clique em "Publish release"

## Passo 5: Adicionar Badge de Status

O README já inclui badges. Eles aparecerão automaticamente após o primeiro push!

## Comandos Úteis

```bash
# Ver status
git status

# Adicionar mudanças
git add .

# Commit
git commit -m "Sua mensagem"

# Push
git push

# Ver remotes
git remote -v

# Ver branches
git branch -a
```

## Próximos Passos

1. ⭐ Peça para amigos darem star no projeto
2. 📝 Adicione exemplos de músicas geradas (se quiser)
3. 🎥 Crie um vídeo demo
4. 📢 Compartilhe nas redes sociais
5. 🤝 Aceite contribuições da comunidade

## Troubleshooting

### Erro de autenticação
Se pedir senha, use um Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Marque "repo"
4. Use o token como senha

### Repositório já existe
```bash
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/NOVO_NOME.git
git push -u origin main
```
