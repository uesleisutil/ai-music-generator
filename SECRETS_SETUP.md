# 🔐 GitHub Secrets - Guia Completo

Guia passo a passo para configurar os secrets necessários para o GitHub Actions.

---

## 📋 Secrets Necessários

Você precisa configurar **3 secrets**:

| Secret | O que é | Exemplo |
|--------|---------|---------|
| `AWS_ACCESS_KEY_ID` | Chave de acesso da AWS | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | Chave secreta da AWS | `wJalrXUtnFEMI/K7MDENG/bPxRfiCY...` |
| `S3_BUCKET_NAME` | Nome único do bucket S3 | `seu-nome-ai-music-2026` |

---

## 🔑 Passo 1: Criar Usuário IAM na AWS

### 1.1 Acessar o Console IAM

1. Faça login no [AWS Console](https://console.aws.amazon.com/)
2. No topo, busque por **IAM** e clique
3. Ou acesse direto: https://console.aws.amazon.com/iam/

### 1.2 Criar Novo Usuário

1. No menu lateral, clique em **Users** (Usuários)
2. Clique no botão **Create user** (Criar usuário)
3. Preencha:
   - **User name**: `github-actions-ai-music`
   - Marque: ✅ **Provide user access to the AWS Management Console** (opcional)
   - Clique **Next**

### 1.3 Adicionar Permissões

**Opção A: Usar Políticas Gerenciadas (Mais Fácil)**

Selecione **Attach policies directly** e marque:
- ✅ `AmazonEC2ContainerRegistryFullAccess`
- ✅ `AmazonS3FullAccess`
- ✅ `AWSBatchFullAccess`
- ✅ `IAMFullAccess`
- ✅ `CloudWatchLogsFullAccess`
- ✅ `AmazonEC2FullAccess`

**Opção B: Criar Política Customizada (Mais Seguro)**

1. Clique em **Create policy**
2. Clique na aba **JSON**
3. Cole este código:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "batch:*",
        "ecr:*",
        "s3:*",
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:GetRole",
        "iam:PassRole",
        "iam:AttachRolePolicy",
        "iam:DetachRolePolicy",
        "iam:CreateInstanceProfile",
        "iam:DeleteInstanceProfile",
        "iam:AddRoleToInstanceProfile",
        "iam:RemoveRoleFromInstanceProfile",
        "ec2:*",
        "logs:*",
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

4. Clique **Next**
5. Nome da política: `GitHubActionsAIMusicPolicy`
6. Clique **Create policy**
7. Volte e selecione essa política

Clique **Next** e depois **Create user**

### 1.4 Criar Access Keys

1. Clique no usuário que você acabou de criar
2. Clique na aba **Security credentials**
3. Role até **Access keys** e clique **Create access key**
4. Selecione: **Application running outside AWS**
5. Clique **Next**
6. (Opcional) Adicione uma descrição: `GitHub Actions AI Music Generator`
7. Clique **Create access key**

### 1.5 ⚠️ IMPORTANTE: Salvar as Credenciais

Você verá uma tela com:

```
Access key ID: AKIAIOSFODNN7EXAMPLE
Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**⚠️ ATENÇÃO**: 
- Copie AMBAS as chaves AGORA
- Você NÃO poderá ver a secret key novamente
- Salve em um lugar seguro (ex: gerenciador de senhas)

Clique em **Download .csv file** para ter um backup.

---

## 🪣 Passo 2: Escolher Nome do Bucket S3

O bucket S3 precisa ter um nome **globalmente único** (ninguém no mundo pode ter o mesmo nome).

### Sugestões de Nomes:

```
seu-nome-ai-music-2026
seu-nome-musicgen-output
ai-music-seu-nome-feb2026
musicgen-seu-nome-123
```

**Regras**:
- Apenas letras minúsculas, números e hífens
- Entre 3 e 63 caracteres
- Não pode começar ou terminar com hífen
- Não pode ter pontos consecutivos

**Exemplo**: Se seu nome é João Silva:
```
joao-silva-ai-music-2026
```

⚠️ **Não crie o bucket agora** - o Terraform vai criar automaticamente!

---

## 🔐 Passo 3: Configurar Secrets no GitHub

### 3.1 Acessar Configurações do Repositório

1. Vá para seu repositório no GitHub:
   ```
   https://github.com/uesleisutil/ai-music-generator
   ```

2. Clique na aba **Settings** (Configurações)

3. No menu lateral esquerdo, clique em:
   ```
   Secrets and variables > Actions
   ```

### 3.2 Adicionar o Primeiro Secret

1. Clique no botão **New repository secret**

2. Preencha:
   - **Name**: `AWS_ACCESS_KEY_ID`
   - **Secret**: Cole sua Access Key ID (ex: `AKIAIOSFODNN7EXAMPLE`)

3. Clique **Add secret**

### 3.3 Adicionar o Segundo Secret

1. Clique novamente em **New repository secret**

2. Preencha:
   - **Name**: `AWS_SECRET_ACCESS_KEY`
   - **Secret**: Cole sua Secret Access Key (a chave longa)

3. Clique **Add secret**

### 3.4 Adicionar o Terceiro Secret

1. Clique novamente em **New repository secret**

2. Preencha:
   - **Name**: `S3_BUCKET_NAME`
   - **Secret**: Digite o nome único que você escolheu (ex: `joao-silva-ai-music-2026`)

3. Clique **Add secret**

### 3.5 Verificar

Você deve ver 3 secrets listados:

```
✅ AWS_ACCESS_KEY_ID
✅ AWS_SECRET_ACCESS_KEY
✅ S3_BUCKET_NAME
```

---

## ✅ Passo 4: Testar a Configuração

### 4.1 Trigger Manual do Workflow

1. Vá para a aba **Actions** no GitHub

2. Clique em **Deploy to AWS** no menu lateral

3. Clique no botão **Run workflow**

4. Selecione branch **main**

5. Clique **Run workflow**

### 4.2 Monitorar o Deploy

1. Clique no workflow que está rodando

2. Você verá 3 jobs:
   - **Terraform Plan** (~2 min)
   - **Terraform Apply** (~5 min)
   - **Build and Push** (~10 min)

3. Clique em cada job para ver os logs

### 4.3 Verificar Sucesso

Se tudo der certo, você verá:
- ✅ Todos os jobs com check verde
- ✅ Mensagem "Deployment Complete"
- ✅ Recursos criados na AWS

---

## 🐛 Troubleshooting

### Erro: "Access Denied"

**Causa**: IAM user não tem permissões suficientes

**Solução**:
1. Volte no IAM Console
2. Clique no usuário
3. Adicione as políticas faltantes

### Erro: "Invalid credentials"

**Causa**: Access keys incorretas

**Solução**:
1. Verifique se copiou as keys corretamente
2. Não deve ter espaços no início/fim
3. Se necessário, crie novas access keys

### Erro: "Bucket already exists"

**Causa**: Nome do bucket já está em uso

**Solução**:
1. Escolha outro nome mais único
2. Atualize o secret `S3_BUCKET_NAME`
3. Re-rode o workflow

### Erro: "Region not specified"

**Causa**: Região AWS não configurada

**Solução**:
- O workflow usa `us-east-1` por padrão
- Se quiser mudar, edite `.github/workflows/deploy-aws.yml`

---

## 📊 Resumo Visual

```
┌─────────────────────────────────────────────────────────────┐
│                    AWS Console (IAM)                        │
│                                                             │
│  1. Criar usuário: github-actions-ai-music                 │
│  2. Adicionar permissões (Batch, ECR, S3, IAM, EC2, Logs)  │
│  3. Criar Access Keys                                       │
│  4. Copiar: Access Key ID + Secret Access Key              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              GitHub Repository Settings                      │
│                                                             │
│  Settings > Secrets and variables > Actions                 │
│                                                             │
│  Secret 1: AWS_ACCESS_KEY_ID                               │
│  Secret 2: AWS_SECRET_ACCESS_KEY                           │
│  Secret 3: S3_BUCKET_NAME (escolher nome único)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Actions                             │
│                                                             │
│  Actions > Deploy to AWS > Run workflow                     │
│                                                             │
│  ✅ Terraform Plan                                          │
│  ✅ Terraform Apply                                         │
│  ✅ Build & Push Docker                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    AWS Resources                            │
│                                                             │
│  ✅ S3 Bucket criado                                        │
│  ✅ ECR Repository criado                                   │
│  ✅ AWS Batch configurado                                   │
│  ✅ Docker image no ECR                                     │
│                                                             │
│  🎉 PRONTO PARA GERAR VÍDEOS!                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Checklist Final

Antes de rodar o workflow, verifique:

- [ ] Usuário IAM criado na AWS
- [ ] Access Keys geradas e salvas
- [ ] Nome único do bucket S3 escolhido
- [ ] 3 secrets configurados no GitHub
- [ ] Secrets verificados (sem espaços extras)
- [ ] Pronto para rodar o workflow!

---

## 💡 Dicas de Segurança

1. **Nunca compartilhe suas Access Keys**
   - Não commite no código
   - Não poste em issues/PRs
   - Não compartilhe em chat

2. **Rotacione as keys regularmente**
   - A cada 90 dias
   - Ou se suspeitar de vazamento

3. **Use MFA no usuário IAM**
   - Adiciona camada extra de segurança
   - Mesmo para acesso programático

4. **Monitore o uso**
   - Verifique CloudTrail
   - Configure alertas de custo

---

## 📞 Precisa de Ajuda?

Se tiver problemas:

1. **Verifique os logs** no GitHub Actions
2. **Leia a mensagem de erro** completa
3. **Consulte o troubleshooting** acima
4. **Abra uma issue** no GitHub com:
   - Mensagem de erro (sem expor secrets!)
   - Passo onde travou
   - Screenshots (sem mostrar keys!)

---

## 🎉 Próximos Passos

Depois de configurar os secrets:

1. ✅ Rode o workflow "Deploy to AWS"
2. ✅ Aguarde ~15 minutos
3. ✅ Teste com "Test Deployment"
4. ✅ Gere seu primeiro vídeo!

---

**Boa sorte!** 🚀

Se tudo der certo, em 15 minutos você terá um pipeline completo de geração de música com IA rodando na AWS!
