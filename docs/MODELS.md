# 🤖 Guia de Modelos de IA

## Visão Geral

Este projeto suporta múltiplos modelos de IA gratuitos e open-source para geração de música e imagens. Você pode escolher o modelo que melhor se adequa às suas necessidades e hardware.

## 🎵 Modelos de Música

### MusicGen (Meta/Facebook)

**MusicGen Small** (`musicgen-small`)
- ✅ Funciona em CPU
- 📦 300MB
- ⚡ Rápido
- 🎯 Qualidade básica
- 💡 Ideal para testes e protótipos

**MusicGen Medium** (`musicgen-medium`)
- ⚠️ Requer GPU
- 📦 1.5GB
- ⚡ Velocidade média
- 🎯 Boa qualidade
- 💡 Melhor equilíbrio qualidade/velocidade

**MusicGen Large** (`musicgen-large`)
- ⚠️ Requer GPU potente
- 📦 3.3GB
- ⚡ Lento
- 🎯 Excelente qualidade
- 💡 Melhor qualidade disponível

**MusicGen Melody** (`musicgen-melody`)
- ⚠️ Requer GPU
- 📦 1.5GB
- ⚡ Velocidade média
- 🎯 Boa qualidade
- 💡 Especializado em melodias, aceita áudio de referência

### AudioLDM

**AudioLDM** (`audioldm`)
- ✅ Funciona em CPU
- 📦 1.2GB
- ⚡ Rápido
- 🎯 Boa qualidade
- 💡 Ótimo para efeitos sonoros e música ambiente

**AudioLDM Large** (`audioldm-large`)
- ⚠️ Requer GPU
- 📦 2.5GB
- ⚡ Velocidade média
- 🎯 Excelente qualidade
- 💡 Versão melhorada do AudioLDM

### Riffusion

**Riffusion** (`riffusion`)
- ⚠️ Requer GPU
- 📦 2GB
- ⚡ Velocidade média
- 🎯 Boa qualidade
- 💡 Usa Stable Diffusion para gerar música, estilo único

## 🎨 Modelos de Imagem

### Stable Diffusion

**Stable Diffusion 1.5** (`sd-1-5`)
- ✅ Funciona em GPUs modestas
- 📦 4GB
- ⚡ Rápido
- 🎯 Boa qualidade
- 💡 Versão mais leve e rápida

**Stable Diffusion 2.1** (`sd-2-1`)
- ⚠️ Requer GPU
- 📦 5GB
- ⚡ Velocidade média
- 🎯 Excelente qualidade
- 💡 Modelo padrão recomendado

**Stable Diffusion XL** (`sd-xl-base`)
- ⚠️ Requer GPU potente
- 📦 7GB
- ⚡ Lento
- 🎯 Excepcional qualidade
- 💡 Melhor qualidade disponível

### Outros Modelos

**Kandinsky 2.2** (`kandinsky-2-2`)
- ⚠️ Requer GPU
- 📦 5GB
- ⚡ Velocidade média
- 🎯 Excelente qualidade
- 💡 Estilo artístico único, ótimo para capas

**Würstchen** (`wuerstchen`)
- ✅ Funciona em CPU
- 📦 3GB
- ⚡ Muito rápido
- 🎯 Boa qualidade
- 💡 Modelo compacto e eficiente

**DeepFloyd IF** (`deepfloyd-if`)
- ⚠️ Requer GPU potente
- 📦 8GB
- ⚡ Lento
- 🎯 Excepcional qualidade
- 💡 Qualidade fotorrealística

## ⚙️ Presets

### Quick (Rápido)
```bash
--preset quick
```
- Música: MusicGen Small
- Imagem: Würstchen
- ✅ Funciona em CPU
- ⚡ Muito rápido
- 💡 Ideal para testes

### Balanced (Balanceado)
```bash
--preset balanced
```
- Música: MusicGen Medium
- Imagem: Stable Diffusion 2.1
- ⚠️ Requer GPU
- ⚡ Velocidade média
- 💡 Melhor equilíbrio

### Quality (Qualidade)
```bash
--preset quality
```
- Música: MusicGen Large
- Imagem: Stable Diffusion XL
- ⚠️ Requer GPU potente
- ⚡ Lento
- 💡 Máxima qualidade

### Experimental
```bash
--preset experimental
```
- Música: Riffusion
- Imagem: Kandinsky 2.2
- ⚠️ Requer GPU
- ⚡ Velocidade média
- 💡 Estilos únicos e artísticos

## 📖 Como Usar

### Listar Modelos Disponíveis
```bash
python list_models.py
```

### Verificar Modelos Instalados
```bash
python check_models.py
```

### Usar Modelo Específico
```bash
python pipeline_ai.py \
  --prompt "cozy lofi music" \
  --music-model musicgen-medium \
  --image-model sd-2-1 \
  --duration 60 \
  --skip-upload
```

### Usar Preset
```bash
python pipeline_ai.py \
  --prompt "epic orchestral music" \
  --preset quality \
  --duration 120 \
  --skip-upload
```

### Gerar Apenas Música
```bash
python generate_music_ai.py \
  --prompt "jazz piano" \
  --model musicgen-small \
  --duration 60
```

### Gerar Apenas Imagem
```bash
python generate_image_ai.py \
  --prompt "jazz piano album cover" \
  --model sd-2-1
```

## 💾 Download de Modelos

Os modelos são baixados automaticamente na primeira vez que você os usa. Eles ficam salvos em:
```
~/.cache/huggingface/hub/
```

## 🔧 Requisitos de Hardware

### CPU Only (Sem GPU)
- Modelos recomendados:
  - `musicgen-small`
  - `audioldm`
  - `sd-1-5`
  - `wuerstchen`
- RAM: 8GB mínimo, 16GB recomendado
- Tempo: 5-10 minutos para 30s de música

### GPU Modesta (4-6GB VRAM)
- Modelos recomendados:
  - `musicgen-medium`
  - `audioldm`
  - `sd-2-1`
  - `kandinsky-2-2`
- RAM: 16GB recomendado
- Tempo: 1-3 minutos para 30s de música

### GPU Potente (8GB+ VRAM)
- Todos os modelos disponíveis
- RAM: 16GB+ recomendado
- Tempo: 30s-2min para 30s de música

## 🎯 Recomendações por Uso

### Testes Rápidos
```bash
--preset quick
```

### Produção Diária
```bash
--preset balanced
```

### Conteúdo Profissional
```bash
--preset quality
```

### Experimentação Artística
```bash
--preset experimental
```

## 📊 Comparação de Qualidade

| Modelo | Qualidade | Velocidade | GPU | Tamanho |
|--------|-----------|------------|-----|---------|
| musicgen-small | ⭐⭐ | ⚡⚡⚡ | ✗ | 300MB |
| musicgen-medium | ⭐⭐⭐ | ⚡⚡ | ✓ | 1.5GB |
| musicgen-large | ⭐⭐⭐⭐ | ⚡ | ✓ | 3.3GB |
| audioldm | ⭐⭐⭐ | ⚡⚡⚡ | ✗ | 1.2GB |
| sd-1-5 | ⭐⭐⭐ | ⚡⚡⚡ | ✗ | 4GB |
| sd-2-1 | ⭐⭐⭐⭐ | ⚡⚡ | ✓ | 5GB |
| sd-xl-base | ⭐⭐⭐⭐⭐ | ⚡ | ✓ | 7GB |

## 🆘 Troubleshooting

### Erro de memória
- Use modelos menores (`musicgen-small`, `sd-1-5`)
- Reduza a duração da música
- Feche outros programas

### Modelo não baixa
- Verifique conexão com internet
- Verifique espaço em disco
- Tente novamente

### GPU não detectada
- Instale CUDA Toolkit
- Verifique drivers NVIDIA
- Use modelos que funcionam em CPU

## 📚 Referências

- [MusicGen](https://github.com/facebookresearch/audiocraft)
- [AudioLDM](https://github.com/haoheliu/AudioLDM)
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion)
- [Hugging Face](https://huggingface.co/)
