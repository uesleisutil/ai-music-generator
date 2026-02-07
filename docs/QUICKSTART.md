# 🚀 Quick Start Guide

## Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/uesleisutil/ai-music-generator.git
cd ai-music-generator

# Instale dependências básicas
pip install -r requirements.txt

# Instale FFmpeg (se ainda não tiver)
brew install ffmpeg  # macOS
```

## Teste Rápido (Sem IA)

Para testar o sistema rapidamente sem instalar modelos pesados de IA:

```bash
python pipeline_simple.py \
  --prompt "cozy lofi music" \
  --duration 30 \
  --title "My First Test" \
  --skip-upload
```

Isso vai gerar:
- ✅ Música de teste (síntese de áudio simples)
- ✅ Imagem de capa (gradiente com texto)
- ✅ Vídeo completo (música + imagem)

**Arquivos gerados em:** `output/`

## Modo Completo (Com IA)

Para usar os modelos de IA reais (requer GPU recomendada):

### 1. Instalar Modelos de IA

```bash
pip install -r requirements-full.txt
```

⚠️ **Atenção:** Isso vai baixar ~10GB de modelos. Pode demorar!

### 2. Gerar Música com IA

```bash
python pipeline.py \
  --prompt "cozy lofi home music with rain sounds" \
  --duration 180 \
  --title "Cozy Lofi Beats" \
  --skip-upload
```

## Upload para YouTube

### 1. Configurar YouTube API

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto
3. Ative a "YouTube Data API v3"
4. Crie credenciais OAuth 2.0
5. Baixe o arquivo JSON e renomeie para `client_secrets.json`
6. Coloque na raiz do projeto

### 2. Fazer Upload

```bash
# Sem --skip-upload
python pipeline_simple.py \
  --prompt "relaxing music" \
  --duration 60 \
  --title "Relaxing Music" \
  --privacy unlisted
```

Na primeira vez, um navegador abrirá para autorizar o acesso.

## Comandos Úteis

### Apenas Gerar Música
```bash
python generate_music_simple.py --prompt "jazz piano" --duration 60
```

### Apenas Gerar Imagem
```bash
python generate_image_simple.py --prompt "jazz piano album cover"
```

### Criar Vídeo de Arquivos Existentes
```bash
python create_video.py \
  --audio output/music.wav \
  --image output/cover.png \
  --output meu_video.mp4
```

## Opções de Privacidade

- `--privacy public` - Público (todos podem ver)
- `--privacy unlisted` - Não listado (só com link)
- `--privacy private` - Privado (só você)

## Troubleshooting

### Erro: FFmpeg não encontrado
```bash
# Instale FFmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Linux
```

### Erro: Memória insuficiente
Use o modo simples ou reduza a duração:
```bash
python pipeline_simple.py --prompt "test" --duration 10 --skip-upload
```

### Erro: client_secrets.json não encontrado
Você só precisa disso para upload no YouTube. Use `--skip-upload` para pular.

## Próximos Passos

1. ✅ Teste o modo simples
2. ✅ Verifique os arquivos em `output/`
3. ⚙️ Configure YouTube API (opcional)
4. 🚀 Instale modelos de IA completos (opcional)
5. 🎵 Crie suas músicas!

## Exemplos de Prompts

**Lofi/Chill:**
- "cozy lofi home music with rain sounds"
- "chill beats to study and relax"
- "peaceful lofi hip hop"

**Energético:**
- "upbeat electronic dance music"
- "energetic rock guitar solo"
- "fast-paced techno beats"

**Clássico:**
- "calm piano meditation music"
- "smooth jazz saxophone evening"
- "epic orchestral cinematic music"

## Ajuda

- 📖 Documentação completa: [README.md](README.md)
- 🔧 Guia de instalação: [SETUP.md](SETUP.md)
- 🐛 Reportar bugs: [Issues](https://github.com/uesleisutil/ai-music-generator/issues)

---

**Dica:** Comece sempre com `--duration 10` e `--skip-upload` para testes rápidos!
