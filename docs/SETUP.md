# Guia de Configuração

## 1. Instalar Dependências

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar pacotes
pip install -r requirements.txt
```

## 2. Instalar FFmpeg

### macOS
```bash
brew install ffmpeg
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Windows
Baixe de: https://ffmpeg.org/download.html

## 3. Configurar YouTube API

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto
3. Ative a "YouTube Data API v3"
4. Crie credenciais OAuth 2.0
5. Baixe o arquivo JSON e renomeie para `client_secrets.json`
6. Coloque na raiz do projeto

## 4. Primeiro Uso

```bash
# Teste simples (30 segundos)
python pipeline.py --prompt "cozy lofi home music" --duration 30 --title "Cozy Lofi Music"
```

Na primeira vez, um navegador abrirá para você autorizar o acesso ao YouTube.

## Dicas

- **GPU**: Se tiver GPU NVIDIA, instale CUDA para acelerar a geração
- **Duração**: Comece com 30s para testar, depois aumente
- **Modelos**: 
  - `musicgen-small`: Mais rápido, menos qualidade
  - `musicgen-medium`: Balanceado
  - `musicgen-large`: Melhor qualidade, mais lento

## Troubleshooting

### Erro de memória
- Use `musicgen-small` no config.yaml
- Reduza a duração da música
- Feche outros programas

### FFmpeg não encontrado
- Verifique se está no PATH: `ffmpeg -version`
- Reinstale o FFmpeg

### Erro de autenticação YouTube
- Verifique se `client_secrets.json` está correto
- Delete `token.pickle` e tente novamente
