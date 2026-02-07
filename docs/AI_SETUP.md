# 🤖 Configuração de IA - Guia Completo

## Por que usar modelos de IA?

O gerador simples (sem IA) cria imagens básicas com formas geométricas. Para obter imagens de **qualidade profissional** como nos exemplos de canais lofi do YouTube, você **precisa** instalar os modelos de IA.

## 📦 Instalação Rápida

```bash
# Instalar todas as dependências de IA
pip install -r requirements-full.txt
```

⚠️ **Atenção**: Isso vai baixar ~10-15GB de modelos. Certifique-se de ter:
- Espaço em disco: 20GB+ livre
- RAM: 16GB recomendado
- GPU: NVIDIA com 6GB+ VRAM (recomendado, mas funciona em CPU)

## 🎨 Modelos Recomendados

### Para Melhor Qualidade (Padrão)

**Música**: `musicgen-medium`
- Tamanho: 1.5GB
- Qualidade: Boa
- Velocidade: Média
- GPU: Recomendada

**Imagem**: `sd-2-1` (Stable Diffusion 2.1)
- Tamanho: 5GB
- Qualidade: Excelente
- Velocidade: Média
- GPU: Recomendada

### Para Máxima Qualidade

```bash
python aimusic ai \
  --prompt "cozy lofi coffee shop" \
  --preset quality \
  --duration 180
```

Usa:
- `musicgen-large` (3.3GB)
- `sd-xl-base` (7GB)

### Para Testes Rápidos

```bash
python aimusic ai \
  --prompt "lofi beats" \
  --preset quick \
  --duration 30
```

Usa:
- `musicgen-small` (300MB)
- `wuerstchen` (3GB)

## 🚀 Uso com IA

### Comando Básico

```bash
# Usar modelos padrão (recomendado)
python aimusic ai --prompt "rainy night city lofi" --duration 60 --skip-upload
```

### Escolher Modelos Específicos

```bash
# Música: medium, Imagem: SD 2.1
python aimusic ai \
  --prompt "cozy coffee shop music" \
  --music-model musicgen-medium \
  --image-model sd-2-1 \
  --duration 120 \
  --skip-upload
```

### Usar Presets

```bash
# Preset balanced (melhor custo-benefício)
python aimusic ai --prompt "chill beats" --preset balanced --duration 180

# Preset quality (máxima qualidade)
python aimusic ai --prompt "jazz lofi" --preset quality --duration 180

# Preset quick (testes rápidos)
python aimusic ai --prompt "test" --preset quick --duration 30
```

## 📊 Comparação: Simples vs IA

### Modo Simples (sem IA)
```bash
python aimusic simple --prompt "lofi music" --duration 30
```
- ✅ Rápido (segundos)
- ✅ Não precisa GPU
- ✅ Não precisa download
- ❌ Qualidade básica
- ❌ Imagens abstratas/geométricas
- ❌ Música sintética simples

### Modo IA
```bash
python aimusic ai --prompt "lofi music" --duration 30
```
- ✅ Qualidade profissional
- ✅ Imagens realistas/artísticas
- ✅ Música complexa e natural
- ⚠️ Requer download de modelos
- ⚠️ Mais lento (minutos)
- ⚠️ GPU recomendada

## 🎯 Exemplos de Prompts para IA

### Café/Interior
```bash
python aimusic ai --prompt "cozy coffee shop with plants and warm lighting" --duration 120
```

### Cidade Noturna
```bash
python aimusic ai --prompt "rainy night city with neon lights" --duration 180
```

### Quarto/Estudo
```bash
python aimusic ai --prompt "bedroom with city view and desk setup" --duration 120
```

### Natureza
```bash
python aimusic ai --prompt "peaceful forest with sunlight through trees" --duration 180
```

## 🔧 Troubleshooting

### Erro: "No module named 'torch'"
```bash
pip install torch torchvision torchaudio
```

### Erro: "No module named 'audiocraft'"
```bash
pip install audiocraft
```

### Erro: "CUDA out of memory"
Use modelos menores:
```bash
python aimusic ai --preset quick --prompt "test" --duration 30
```

### Muito lento em CPU
Normal! IA em CPU é lento. Opções:
1. Use `--preset quick` para modelos menores
2. Reduza `--duration` para 30-60 segundos
3. Considere usar GPU (NVIDIA)

### Modelos não baixam
Verifique:
- Conexão com internet
- Espaço em disco (20GB+)
- Firewall/proxy

## 📈 Performance

### Com GPU (NVIDIA RTX 3060, 12GB VRAM)
- Música (30s): ~1-2 minutos
- Imagem: ~30-60 segundos
- Total: ~2-3 minutos

### Sem GPU (CPU Intel i7)
- Música (30s): ~5-10 minutos
- Imagem: ~3-5 minutos
- Total: ~10-15 minutos

## 💡 Dicas

1. **Primeira vez**: Use `--preset quick` para testar
2. **Produção**: Use `--preset balanced` ou modelos padrão
3. **Qualidade máxima**: Use `--preset quality`
4. **Testes**: Use `--duration 30` para economizar tempo
5. **GPU**: Instale CUDA Toolkit para acelerar

## 🔗 Links Úteis

- [Instalar CUDA](https://developer.nvidia.com/cuda-downloads)
- [PyTorch](https://pytorch.org/get-started/locally/)
- [Hugging Face](https://huggingface.co/)
- [MusicGen](https://github.com/facebookresearch/audiocraft)
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion)

## ✅ Checklist de Instalação

- [ ] Python 3.9+ instalado
- [ ] pip atualizado (`pip install --upgrade pip`)
- [ ] FFmpeg instalado (`brew install ffmpeg`)
- [ ] requirements-full.txt instalado
- [ ] 20GB+ espaço em disco livre
- [ ] GPU NVIDIA (opcional, mas recomendado)
- [ ] CUDA Toolkit instalado (se tiver GPU)

## 🎉 Resultado Esperado

Com os modelos de IA instalados, você terá:
- 🎵 Música de qualidade profissional
- 🎨 Imagens estilo anime/lofi realistas
- 🎬 Vídeos prontos para YouTube
- ⭐ Qualidade comparável a canais lofi populares

---

**Próximo passo**: Execute `python aimusic ai --prompt "cozy lofi music" --duration 60 --skip-upload`
