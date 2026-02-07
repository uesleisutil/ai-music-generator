# 🎵 Como Usar o AI Music Generator

## ✅ Deploy Concluído!

Sua infraestrutura AWS está pronta e funcionando!

---

## 🎯 Opção 1: Via GitHub Actions (Mais Fácil)

### Passo 1: Ir para Actions
1. Acesse: https://github.com/uesleisutil/ai-music-generator/actions
2. Clique em **"Test Deployment"** (no menu lateral esquerdo)
3. Clique no botão **"Run workflow"** (canto superior direito)

### Passo 2: Configurar o Job
Preencha os campos:
- **prompt**: Descrição da música (ex: "cozy lofi coffee shop music")
- **duration**: Duração em segundos (ex: 30, 60, 90)
- **preset**: Qualidade
  - `quick` - Rápido (2-3 min)
  - `balanced` - Balanceado (3-5 min) ⭐ Recomendado
  - `quality` - Alta qualidade (5-8 min)
  - `experimental` - Estilos únicos (4-6 min)
- **resolution**: Resolução do vídeo
  - `hd` - 720p (1280x720) - Padrão, rápido
  - `fhd` - 1080p (1920x1080) - Full HD
  - `2k` - 1440p (2560x1440) - 2K QHD
  - `4k` - 2160p (3840x2160) - 4K UHD ⭐ Melhor qualidade
  - `youtube` - 1080p (1920x1080) - Otimizado YouTube

### Passo 3: Executar
1. Clique em **"Run workflow"** (botão verde)
2. Aguarde 3-5 minutos
3. Quando terminar, clique no workflow que acabou de rodar
4. Role até o final e baixe o **Artifact** (arquivo ZIP com música, imagem e vídeo)

### Exemplo:
```
prompt: cozy lofi coffee shop music with rain sounds
duration: 60
preset: balanced
resolution: 4k
```

---

## 🎯 Opção 2: Via Terminal (Linha de Comando)

### Passo 1: Instalar Dependências
```bash
pip install -r requirements-aws.txt
```

### Passo 2: Pegar o Nome do Bucket S3
```bash
cd terraform
terraform init
terraform output s3_bucket_name
cd ..
```

Você verá algo como: `ai-music-gen-200093399689-a1b2c3d4`

### Passo 3: Submeter um Job
```bash
python aws_submit_job.py \
  --prompt "cozy lofi coffee shop music" \
  --duration 60 \
  --preset balanced \
  --resolution 4k \
  --output-bucket ai-music-gen-200093399689-a1b2c3d4 \
  --wait
```

**Parâmetros**:
- `--prompt`: Descrição da música (obrigatório)
- `--duration`: Duração em segundos (padrão: 30)
- `--preset`: quick, balanced, quality, experimental (padrão: balanced)
- `--resolution`: hd, fhd, 2k, 4k, youtube (padrão: hd)
- `--output-bucket`: Nome do bucket S3 (obrigatório)
- `--wait`: Aguarda o job terminar (opcional)

### Passo 4: Baixar os Resultados
```bash
# Listar arquivos no bucket
aws s3 ls s3://ai-music-gen-200093399689-a1b2c3d4/output/

# Baixar um job específico
aws s3 sync s3://ai-music-gen-200093399689-a1b2c3d4/output/20260207_123456/ ./downloads/
```

---

## 🎯 Opção 3: Batch (Múltiplas Músicas)

### Editar o Script de Exemplo
```bash
nano examples/batch_generate.py
```

Altere a linha:
```python
OUTPUT_BUCKET = "ai-music-gen-200093399689-a1b2c3d4"  # Seu bucket aqui!
```

### Executar
```bash
python examples/batch_generate.py
```

Isso vai gerar 5 músicas diferentes automaticamente!

---

## 📊 Exemplos de Prompts

### Lofi / Chill
```
cozy lofi coffee shop music with rain sounds
peaceful lofi beats for studying
relaxing lofi hip hop with vinyl crackle
chill lofi music for late night coding
```

### Ambiente / Nature
```
peaceful forest ambience with birds chirping
ocean waves and seagulls sounds
thunderstorm with rain on window
campfire crackling in the woods
```

### Eletrônica
```
upbeat electronic music for studying
energetic synthwave music for gaming
ambient electronic soundscape
chill downtempo electronic beats
```

### Piano / Instrumental
```
relaxing piano music for meditation
emotional piano ballad
uplifting acoustic guitar melody
soft jazz piano for reading
```

---

## 💰 Custos

- **Por vídeo**: ~$0.02 (2 centavos de dólar)
- **10 vídeos/dia**: ~$6/mês
- **50 vídeos/dia**: ~$29/mês
- **100 vídeos/dia**: ~$58/mês

**Dica**: Use Spot Instances (já configurado) para economizar até 70%!

---

## 📁 Arquivos Gerados

Cada job gera 4 arquivos:

1. **music.wav** - Áudio gerado (WAV, alta qualidade)
2. **cover.png** - Imagem de capa (1280x720, estilo lofi/anime)
3. **video.mp4** - Vídeo final (música + imagem)
4. **metadata.json** - Informações do job

---

## 🔍 Monitorar Jobs

### Ver Jobs em Execução
```bash
aws batch list-jobs \
  --job-queue ai-music-generator-queue \
  --job-status RUNNING
```

### Ver Logs em Tempo Real
```bash
aws logs tail /aws/batch/ai-music-generator --follow
```

### Ver Jobs Concluídos
```bash
aws batch list-jobs \
  --job-queue ai-music-generator-queue \
  --job-status SUCCEEDED
```

---

## ⚙️ Modelos Disponíveis

### Música (7 modelos)
- **musicgen-small** - Rápido, CPU (300MB)
- **musicgen-medium** - Balanceado, GPU (1.5GB) ⭐
- **musicgen-large** - Melhor qualidade, GPU (3.3GB)
- **audioldm** - Text-to-audio (1.2GB)
- **riffusion** - Estilo único (2GB)

### Imagem (6 modelos)
- **sd-1-5** - Leve (4GB)
- **sd-2-1** - Excelente qualidade (5GB) ⭐
- **sd-xl-base** - Melhor qualidade (7GB)
- **kandinsky-2-2** - Estilo artístico (5GB)

### Presets
- **quick**: musicgen-small + wuerstchen (2-3 min)
- **balanced**: musicgen-medium + sd-2-1 (3-5 min) ⭐
- **quality**: musicgen-large + sd-xl-base (5-8 min)
- **experimental**: riffusion + kandinsky (4-6 min)

---

## 🚨 Troubleshooting

### Job falhou?
```bash
# Ver logs do job
aws logs tail /aws/batch/ai-music-generator --follow

# Ver detalhes do job
aws batch describe-jobs --jobs <JOB_ID>
```

### Bucket não encontrado?
```bash
# Listar buckets
aws s3 ls

# Verificar outputs do Terraform
cd terraform
terraform output
```

### Credenciais AWS?
```bash
# Testar credenciais
aws sts get-caller-identity

# Configurar se necessário
aws configure
```

---

## 🎉 Pronto!

Agora você pode gerar músicas com IA na AWS!

**Dicas**:
- Use `balanced` preset para melhor custo/benefício
- Duração de 30-60s é ideal para testes
- Prompts em inglês funcionam melhor
- Seja específico no prompt (ex: "cozy lofi" ao invés de só "music")

**Links Úteis**:
- GitHub Actions: https://github.com/uesleisutil/ai-music-generator/actions
- AWS Console: https://console.aws.amazon.com/batch/
- CloudWatch Logs: https://console.aws.amazon.com/cloudwatch/

---

**Divirta-se criando músicas! 🎵**
