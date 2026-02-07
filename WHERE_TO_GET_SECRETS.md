# 🔑 Onde Pegar os Secrets - Guia Visual

Guia passo a passo com screenshots de onde pegar cada secret.

---

## 📊 Resumo: Só 2 Secrets Necessários!

| # | Secret | Onde Pegar | Tempo |
|---|--------|------------|-------|
| 1 | `AWS_ACCESS_KEY_ID` | AWS IAM Console | 3 min |
| 2 | `AWS_SECRET_ACCESS_KEY` | AWS IAM Console | 3 min |

**Total**: ~5 minutos

❌ ~~`S3_BUCKET_NAME`~~ - **NÃO PRECISA MAIS!** Gerado automaticamente! 🎉

---

## 🔑 Secret 1 e 2: AWS Access Keys

### Passo 1: Acessar AWS IAM Console

**URL**: https://console.aws.amazon.com/iam/

1. Faça login na AWS
2. No topo, busque por **IAM**
3. Clique em **IAM**

```
┌─────────────────────────────────────────────────────┐
│  AWS Console                                  🔍 IAM │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Services > Security, Identity, & Compliance > IAM  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Passo 2: Criar Usuário

1. Menu lateral esquerdo: **Users**
2. Botão laranja: **Create user**

```
┌─────────────────────────────────────────────────────┐
│  IAM > Users                                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Users (0)                    [Create user] ←       │
│                                                     │
│  No users found                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

3. Preencha:
   - **User name**: `github-actions`
   - ✅ Provide user access to AWS Management Console (opcional)

```
┌─────────────────────────────────────────────────────┐
│  Create user                                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  User name: [github-actions____________]           │
│                                                     │
│  ✅ Provide user access to AWS Management Console  │
│                                                     │
│                                    [Next] ←         │
└─────────────────────────────────────────────────────┘
```

### Passo 3: Adicionar Permissões

1. Selecione: **Attach policies directly**
2. Busque e marque estas 6 políticas:

```
┌─────────────────────────────────────────────────────┐
│  Set permissions                                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ⚪ Add user to group                              │
│  🔘 Attach policies directly ← Selecione           │
│  ⚪ Copy permissions                               │
│                                                     │
│  Search: [batch_______________] 🔍                 │
│                                                     │
│  ✅ AWSBatchFullAccess                             │
│  ✅ AmazonEC2ContainerRegistryFullAccess           │
│  ✅ AmazonS3FullAccess                             │
│  ✅ IAMFullAccess                                  │
│  ✅ CloudWatchLogsFullAccess                       │
│  ✅ AmazonEC2FullAccess                            │
│                                                     │
│                                    [Next] ←         │
└─────────────────────────────────────────────────────┘
```

**Lista completa para marcar**:
- ✅ `AWSBatchFullAccess`
- ✅ `AmazonEC2ContainerRegistryFullAccess`
- ✅ `AmazonS3FullAccess`
- ✅ `IAMFullAccess`
- ✅ `CloudWatchLogsFullAccess`
- ✅ `AmazonEC2FullAccess`

3. Clique **Next**
4. Clique **Create user**

### Passo 4: Criar Access Keys

1. Clique no usuário **github-actions** que você acabou de criar

```
┌─────────────────────────────────────────────────────┐
│  IAM > Users                                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Users (1)                                          │
│                                                     │
│  👤 github-actions ← Clique aqui                    │
│     Created: Just now                               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

2. Clique na aba **Security credentials**

```
┌─────────────────────────────────────────────────────┐
│  User: github-actions                               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Permissions] [Groups] [Tags] [Security credentials] ← │
│                                                     │
└─────────────────────────────────────────────────────┘
```

3. Role até **Access keys**
4. Clique **Create access key**

```
┌─────────────────────────────────────────────────────┐
│  Security credentials                               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Access keys                                        │
│  Access keys (0)              [Create access key] ← │
│                                                     │
│  No access keys                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

5. Selecione: **Application running outside AWS**

```
┌─────────────────────────────────────────────────────┐
│  Create access key                                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Use case:                                          │
│                                                     │
│  🔘 Application running outside AWS ← Selecione     │
│     Access AWS resources from applications          │
│     running outside of AWS                          │
│                                                     │
│  ⚪ Command Line Interface (CLI)                   │
│  ⚪ Local code                                     │
│  ⚪ Other                                          │
│                                                     │
│                                    [Next] ←         │
└─────────────────────────────────────────────────────┘
```

6. (Opcional) Adicione descrição: `GitHub Actions AI Music Generator`
7. Clique **Create access key**

### Passo 5: ⚠️ COPIAR AS CHAVES AGORA!

**ATENÇÃO**: Esta é a ÚNICA vez que você verá a Secret Access Key!

```
┌─────────────────────────────────────────────────────┐
│  Retrieve access keys                               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ✅ Access key created                             │
│                                                     │
│  Access key ID:                                     │
│  AKIAIOSFODNN7EXAMPLE                              │
│  [Show] [Copy] ← Copie este                        │
│                                                     │
│  Secret access key:                                 │
│  wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY          │
│  [Show] [Copy] ← Copie este também                 │
│                                                     │
│  [Download .csv file] ← Recomendado!               │
│                                                     │
│                                    [Done]           │
└─────────────────────────────────────────────────────┘
```

**O que fazer**:
1. ✅ Clique em **Copy** no Access key ID
2. ✅ Cole em um lugar seguro (ex: Notes, gerenciador de senhas)
3. ✅ Clique em **Copy** no Secret access key
4. ✅ Cole em um lugar seguro
5. ✅ Clique em **Download .csv file** (backup)
6. ✅ Clique **Done**

**Exemplo do que você copiou**:
```
Access key ID: AKIAIOSFODNN7EXAMPLE
Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

---

## 🔐 Configurar no GitHub

### Passo 1: Ir para Settings

No seu repositório GitHub:

```
https://github.com/SEU-USUARIO/ai-music-generator
```

1. Clique na aba **Settings**

```
┌─────────────────────────────────────────────────────┐
│  seu-usuario / ai-music-generator                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Code] [Issues] [Pull requests] [Settings] ←       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

2. Menu lateral esquerdo: **Secrets and variables** > **Actions**

```
┌─────────────────────────────────────────────────────┐
│  Settings                                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  General                                            │
│  Access                                             │
│  Secrets and variables ▼                            │
│    > Actions ← Clique aqui                          │
│    > Codespaces                                     │
│    > Dependabot                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Passo 2: Adicionar Secret 1

1. Clique **New repository secret**

```
┌─────────────────────────────────────────────────────┐
│  Actions secrets and variables                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Secrets    Variables                               │
│                                                     │
│  Repository secrets (0)   [New repository secret] ← │
│                                                     │
│  No secrets yet                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

2. Preencha:

```
┌─────────────────────────────────────────────────────┐
│  Actions secrets / New secret                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Name *                                             │
│  [AWS_ACCESS_KEY_ID_______________]                │
│                                                     │
│  Secret *                                           │
│  [AKIAIOSFODNN7EXAMPLE____________]                │
│  [________________________________]                │
│                                                     │
│                          [Add secret] ←             │
└─────────────────────────────────────────────────────┘
```

- **Name**: `AWS_ACCESS_KEY_ID`
- **Secret**: Cole o Access key ID que você copiou

3. Clique **Add secret**

### Passo 3: Adicionar Secret 2

1. Clique **New repository secret** novamente

2. Preencha:

```
┌─────────────────────────────────────────────────────┐
│  Actions secrets / New secret                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Name *                                             │
│  [AWS_SECRET_ACCESS_KEY___________]                │
│                                                     │
│  Secret *                                           │
│  [wJalrXUtnFEMI/K7MDENG/bPxRfiCY_]                │
│  [EXAMPLEKEY______________________]                │
│                                                     │
│                          [Add secret] ←             │
└─────────────────────────────────────────────────────┘
```

- **Name**: `AWS_SECRET_ACCESS_KEY`
- **Secret**: Cole o Secret access key que você copiou

3. Clique **Add secret**

### ✅ Verificar

Você deve ver 2 secrets:

```
┌─────────────────────────────────────────────────────┐
│  Actions secrets and variables                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Repository secrets (2)                             │
│                                                     │
│  ✅ AWS_ACCESS_KEY_ID                              │
│     Updated 1 minute ago                            │
│                                                     │
│  ✅ AWS_SECRET_ACCESS_KEY                          │
│     Updated now                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎉 Pronto!

Agora você tem os 2 secrets configurados!

### Próximo Passo: Deploy

```
Actions > Deploy to AWS > Run workflow
```

O bucket S3 será criado automaticamente como:
```
ai-music-gen-123456789012-a1b2c3d4
```

Você verá o nome no **Summary** do workflow quando terminar!

---

## 📝 Resumo do que você copiou

```
Secret 1: AWS_ACCESS_KEY_ID
Valor: AKIAIOSFODNN7EXAMPLE
Onde usar: GitHub Secrets

Secret 2: AWS_SECRET_ACCESS_KEY  
Valor: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Onde usar: GitHub Secrets
```

---

## 🔒 Segurança

**NUNCA compartilhe suas Access Keys!**

- ❌ Não commite no código
- ❌ Não poste em issues/PRs
- ❌ Não compartilhe em chat
- ✅ Use apenas GitHub Secrets
- ✅ Rotacione a cada 90 dias

---

## 💡 Dica

Se você perdeu as keys ou esqueceu de copiar:

1. Volte no IAM Console
2. Clique no usuário
3. Security credentials
4. **Delete** a access key antiga
5. **Create access key** novamente
6. Copie as novas keys
7. Atualize os GitHub Secrets

---

## 📚 Mais Ajuda

- **Setup rápido**: [QUICK_SETUP.md](QUICK_SETUP.md)
- **Setup completo**: [SECRETS_SETUP.md](SECRETS_SETUP.md)
- **Guia de deployment**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**Boa sorte!** 🚀

Qualquer dúvida, abra uma [issue](https://github.com/uesleisutil/ai-music-generator/issues)!
