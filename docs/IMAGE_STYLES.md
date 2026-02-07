# 🎨 Guia de Estilos de Imagem

## Estilos Disponíveis

O gerador de imagens detecta automaticamente o estilo baseado no seu prompt e aplica paletas de cores e elementos visuais apropriados.

## 🌃 Lofi / Chill

**Palavras-chave**: `lofi`, `chill`, `relax`, `cozy`, `calm`, `peaceful`

**Características**:
- Paleta: Roxo, rosa, azul neon
- Elementos: Cidade noturna, luzes neon, atmosfera urbana
- Estilo: Anime, aesthetic, soft lighting

**Exemplo de prompt**:
```bash
python aimusic simple --prompt "cozy lofi beats to study" --duration 60
```

**Resultado**: Cenário urbano noturno com tons roxos e rosas, luzes neon, atmosfera relaxante.

## ☕ Coffee Shop / Café

**Palavras-chave**: `coffee`, `cafe`, `shop`

**Características**:
- Paleta: Marrom, verde, amarelo quente
- Elementos: Interior aconchegante, plantas, janelas, luz natural
- Estilo: Tons de madeira, ambiente acolhedor

**Exemplo de prompt**:
```bash
python aimusic simple --prompt "cozy coffee shop morning music" --duration 60
```

**Resultado**: Interior de café com plantas, luz do sol entrando pelas janelas, tons quentes.

## 🌧️ Rainy / Chuva

**Palavras-chave**: `rain`, `rainy`, `storm`

**Características**:
- Paleta: Azul escuro, cinza, azul claro
- Elementos: Gotas de chuva, reflexos, atmosfera melancólica
- Estilo: Noite chuvosa, luzes refletindo

**Exemplo de prompt**:
```bash
python aimusic simple --prompt "rainy night city lofi beats" --duration 60
```

**Resultado**: Cidade à noite com chuva, reflexos nas poças, luzes azuladas.

## 🌆 Night City / Cidade Noturna

**Palavras-chave**: `night`, `city`, `urban`, `cyberpunk`

**Características**:
- Paleta: Azul escuro, roxo, rosa neon
- Elementos: Prédios, luzes da cidade, neon signs
- Estilo: Cyberpunk, futurista, atmosférico

**Exemplo de prompt**:
```bash
python aimusic simple --prompt "midnight city cyberpunk vibes" --duration 60
```

**Resultado**: Paisagem urbana noturna com neons, estilo cyberpunk.

## 🎷 Jazz

**Palavras-chave**: `jazz`, `saxophone`, `piano`

**Características**:
- Paleta: Dourado, marrom escuro, vermelho
- Elementos: Bar, instrumentos, iluminação quente
- Estilo: Vintage, elegante, atmosfera de jazz club

**Exemplo de prompt**:
```bash
python aimusic simple --prompt "smooth jazz evening" --duration 60
```

**Resultado**: Ambiente de jazz club com tons dourados e vermelhos.

## 🎨 Com IA (Modelos Avançados)

Quando usar modelos de IA reais, os prompts são automaticamente otimizados:

### Melhorias Automáticas

O sistema adiciona automaticamente:
- Qualificadores de estilo: "anime style", "lofi aesthetic", "studio ghibli style"
- Detalhes de iluminação: "soft lighting", "warm colors", "cinematic lighting"
- Qualidade: "4k", "highly detailed", "artstation"
- Elementos específicos baseados no contexto

### Exemplo com IA

```bash
# Prompt simples
python aimusic ai --prompt "cozy lofi coffee shop" --preset balanced --duration 60

# O sistema transforma em:
# "cozy lofi coffee shop, lofi aesthetic, anime style, soft lighting, warm colors,
#  cozy atmosphere, cozy coffee shop interior, plants, wooden furniture, warm lighting,
#  sunlight through windows, books on shelves, peaceful ambiance, anime background art,
#  studio ghibli style, detailed, 4k, highly detailed, professional digital art"
```

## 💡 Dicas para Melhores Resultados

### 1. Seja Específico
```bash
# Bom
"cozy lofi coffee shop with plants and sunlight"

# Melhor
"cozy lofi coffee shop morning with plants sunlight through windows"
```

### 2. Combine Estilos
```bash
"rainy night city lofi jazz cafe"
# Combina: chuva + noite + cidade + lofi + jazz + café
```

### 3. Use Palavras Descritivas
- **Atmosfera**: cozy, peaceful, calm, energetic, moody
- **Tempo**: morning, evening, night, midnight, sunset
- **Clima**: rainy, sunny, cloudy, foggy
- **Lugar**: city, urban, nature, indoor, outdoor

### 4. Experimente Variações
```bash
# Variação 1
"cozy lofi bedroom night city view"

# Variação 2
"peaceful lofi study room with plants"

# Variação 3
"chill lofi rooftop sunset city"
```

## 🎯 Prompts Recomendados

### Para Estudar
```bash
"cozy lofi study room with books and warm lighting"
"peaceful library lofi music atmosphere"
"calm coffee shop morning study vibes"
```

### Para Relaxar
```bash
"peaceful lofi bedroom night rain"
"cozy lofi living room fireplace"
"calm lofi nature forest sounds"
```

### Para Trabalhar
```bash
"productive lofi office workspace"
"focused lofi coffee shop work"
"energetic lofi city morning commute"
```

### Para Dormir
```bash
"peaceful lofi bedroom night stars"
"calm lofi rainy night window"
"relaxing lofi moonlight room"
```

## 🖼️ Comparação: Simples vs IA

### Modo Simples (Sem IA)
- ✅ Rápido (segundos)
- ✅ Funciona em CPU
- ✅ Estilo consistente
- ⚠️ Menos detalhes
- ⚠️ Elementos geométricos

### Modo IA (Com Modelos)
- ✅ Altamente detalhado
- ✅ Fotorrealístico/Artístico
- ✅ Elementos complexos
- ⚠️ Requer GPU (recomendado)
- ⚠️ Mais lento (minutos)

## 📊 Exemplos de Saída

### Lofi City Night
```
Paleta: Roxo (#1E1428), Rosa (#FF64C8), Azul (#5078F0)
Elementos: 15 prédios, 40 janelas iluminadas, 100 estrelas, 10 névoas
Texto: Centralizado, sombra pronunciada, cor vibrante
```

### Coffee Shop Morning
```
Paleta: Marrom (#3C2814), Verde (#64C864), Amarelo (#FFF0C8)
Elementos: Tons de madeira, luzes quentes, plantas
Texto: Terço inferior, fundo semi-transparente
```

## 🔧 Personalização Avançada

Para desenvolvedores que querem customizar:

### Adicionar Nova Paleta
Edite `src/generators/generate_image_simple.py`:

```python
elif "seu_estilo" in prompt.lower():
    colors = [(R1, G1, B1), (R2, G2, B2), (R3, G3, B3)]
    accent_color = (R, G, B)
    text_color = (R, G, B)
```

### Modificar Elementos
Ajuste quantidades em `generate_image_simple.py`:
- `range(15)` - Número de prédios/estruturas
- `range(40)` - Número de janelas/luzes
- `range(100)` - Número de estrelas/partículas

## 📚 Referências de Estilo

Inspirado em:
- Lofi Girl / ChilledCow
- Studio Ghibli backgrounds
- Makoto Shinkai cityscapes
- Anime aesthetic art
- Cyberpunk 2077 atmosphere

---

**Dica Final**: Experimente! A melhor forma de descobrir o que funciona é testar diferentes combinações de palavras-chave.
