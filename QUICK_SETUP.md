# ⚡ Setup Rápido - 5 Minutos

Guia super simplificado para configurar e fazer deploy.

---

## 🎯 Você só precisa de 2 secrets!

Não precisa mais do `S3_BUCKET_NAME` - ele é gerado automaticamente! 🎉

---

## 📋 Passo 1: Pegar as Chaves AWS (5 min)

### 1.1 Acessar AWS Console

1. Faça login em: https://console.aws.amazon.com/
2. No topo, busque por **IAM** e clique

### 1.2 Criar Usuário

1. Menu lateral: **Users** > **Create user**
2. Nome: `github-actions`
3. Clique **Next**

### 1.3 Adicionar Permissões

Marque estas políticas:
- ✅ `AmazonEC2ContainerRegistryFullAccess`
- ✅ `AmazonS3FullAccess`
- ✅ `AWSBatchFullAccess`
- ✅ `IAMFullAccess`
- ✅ `CloudWatchLogsFullAccess`
- ✅ `AmazonEC2FullAccess`

Clique **Next** > **Create user**

### 1.4 Gerar Access Keys

1. Clique no usuário que você criou
2. Aba **Security credentials**
3. **Create access key**
4. Selecione: **Application running outside AWS**
5. **Next** > **Create access key**

### 1.5 ⚠️ COPIAR AS CHAVES AGORA!

Você verá:

```
Access key ID: AKIAIOSFODNN7EXAMPLE
Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**⚠️ IMPORTANTE**: 
- Copie AMBAS agora
- Você NÃO verá a secret key novamente
- Clique em **Download .csv** para backup

---

## 🔐 Passo 2: Configurar GitHub Secrets (2 min)

### 2.1 Ir para Settings

No seu repositório GitHub:
```
Settings > Secrets and variables > Actions
```

### 2.2 Adicionar Secret 1

1. **New repository secret**
2. Name: `AWS_ACCESS_KEY_ID`
3. Secret: Cole o **Access key ID** que você copiou
4. **Add secret**

### 2.3 Adicionar Secret 2

1. **New repository secret**
2. Name: `AWS_SECRET_ACCESS_KEY`
3. Secret: Cole o **Secret access key** que você copiou
4. **Add secret**

### ✅ Pronto! Só isso!

Você deve ver 2 secrets:
```
✅ AWS_ACCESS_KEY_ID
✅ AWS_SECRET_ACCESS_KEY
```

**Não precisa mais do S3_BUCKET_NAME!** Ele é gerado automaticamente como:
```
ai-music-gen-{sua-conta-aws}-{random}
```

---

## 🚀 Passo 3: Deploy Automático (1 clique)

### 3.1 Ir para Actions

No GitHub:
```
Actions > Deploy to AWS > Run workflow
```

### 3.2 Rodar

1. Branch: **main**
2. **Run workflow**

### 3.3 Aguardar

- ⏱️ Tempo: ~15 minutos
- 📊 Acompanhe o progresso na aba Actions

### 3.4 Ver o Bucket Criado

Quando terminar, veja o **Summary** do workflow:
- Mostra o nome do bucket S3 criado automaticamente
- Exemplo: `ai-music-gen-123456789012-a1b2c3d4`

---

## 🎵 Passo 4: Testar (1 clique)

### 4.1 Ir para Test Deployment

```
Actions > Test Deployment > Run workflow
```

### 4.2 Configurar

- Prompt: `cozy lofi coffee shop music`
- Duration: `30`
- Preset: `balanced`

### 4.3 Rodar

**Run workflow**

### 4.4 Baixar Resultado

Quando terminar:
1. Clique no workflow
2. Role até **Artifacts**
3. Baixe `test-results-...`
4. Descompacte e veja seu vídeo! 🎉

---

## 📊 Resumo Visual

```
┌─────────────────────────────────────────┐
│     1. AWS Console (IAM)                │
│                                         │
│  • Criar usuário: github-actions        │
│  • Adicionar 6 políticas                │
│  • Criar Access Keys                    │
│  • Copiar as 2 chaves                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│     2. GitHub Secrets                   │
│                                         │
│  • AWS_ACCESS_KEY_ID                    │
│  • AWS_SECRET_ACCESS_KEY                │
│                                         │
│  ✅ Só 2 secrets!                       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│     3. GitHub Actions                   │
│                                         │
│  • Deploy to AWS > Run workflow         │
│  • Aguardar ~15 min                     │
│  • Bucket criado automaticamente!       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│     4. Test Deployment                  │
│                                         │
│  • Test Deployment > Run workflow       │
│  • Aguardar ~5 min                      │
│  • Baixar vídeo dos Artifacts           │
│                                         │
│  🎉 PRONTO!                             │
└─────────────────────────────────────────┘
```

---

## 💰 Quanto Custa?

### GitHub Actions
- **GRÁTIS** (2.000 min/mês para repos públicos)

### AWS
- **Por vídeo**: ~$0.02 (R$ 0.11)
- **10 vídeos/dia**: ~$6/mês (R$ 34)
- **Primeiro mês**: Pode usar AWS Free Tier!

---

## 🐛 Problemas?

### "Access Denied"
- Verifique se adicionou todas as 6 políticas ao usuário IAM

### "Invalid credentials"
- Verifique se copiou as chaves corretamente (sem espaços)
- Tente criar novas access keys

### Workflow falhou
- Clique no workflow > Clique no job vermelho > Veja o erro
- Geralmente é problema de permissão

---

## 🎯 Checklist

Antes de rodar o workflow:

- [ ] Usuário IAM criado
- [ ] 6 políticas adicionadas
- [ ] Access Keys geradas
- [ ] 2 secrets configurados no GitHub
- [ ] Pronto para rodar!

---

## 📚 Quer Mais Detalhes?

- **Setup completo**: [SECRETS_SETUP.md](SECRETS_SETUP.md)
- **Guia de deployment**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Documentação AWS**: [docs/AWS_SETUP.md](docs/AWS_SETUP.md)

---

## 🎉 É Isso!

Só 2 secrets + 1 clique = Deploy automático na AWS!

**Tempo total**: ~5 minutos de configuração + 15 minutos de deploy

**Resultado**: Pipeline completo de geração de música com IA na nuvem! 🚀

---

## 💡 Dica Pro

Depois do primeiro deploy, você pode:

1. **Gerar vídeos via CLI**:
```bash
pip install -r requirements-aws.txt

# O bucket name está no Summary do workflow
python aws_submit_job.py \
  --prompt "seu prompt aqui" \
  --duration 60 \
  --preset balanced \
  --output-bucket ai-music-gen-123456789012-a1b2c3d4 \
  --wait
```

2. **Ou sempre via GitHub Actions**:
   - Actions > Test Deployment > Run workflow
   - Mais fácil e não precisa instalar nada!

---

**Boa sorte!** 🍀

Se tudo der certo, em 20 minutos você terá seu primeiro vídeo gerado com IA na AWS!
