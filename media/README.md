# Apresentação do site

`apresentacao-bem-estar-pilates.mp4`: vídeo horizontal de 45 segundos, Full HD (1920 × 1080), 30 fps, H.264/AAC. Usa capturas reais da landing page publicada, títulos em português, transições suaves e trilha ambiente sintetizada originalmente para esta apresentação. Sem narração.

Percurso: abertura, identidade visual, essência, Pilates, apresentação de Débora, versão móvel, contato e encerramento. Fotografias de Pilates continuam sendo cenas ilustrativas; o retrato de Débora e a logo foram fornecidos pelo cliente.

O vídeo não altera o conteúdo nem o acesso privado do site. Os dados comerciais são os mesmos do briefing confirmado.

## Recriação

Capture as telas pelo navegador em `outputs/video-site/capturas`, preservando os nomes esperados em `scripts/criar-video-site.py`. As telas desktop usam viewport 1920 × 1080; a móvel, 390 × 844. Instale Pillow em seu ambiente Python e utilize um FFmpeg com libx264.

```sh
python scripts/criar-video-site.py --ffmpeg CAMINHO_FFMPEG --captures outputs/video-site/capturas
```

Arquivos intermediários, capturas e a ferramenta FFmpeg ficam no diretório ignorado `outputs/`.
