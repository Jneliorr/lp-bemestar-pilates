# Bem Estar Fisio Pilates

Landing page editorial em português, com HTML semântico, CSS e JavaScript sem dependências. Identidade: azul `#05A2E7`, rosa `#C65DA2`, Cormorant Garamond e Space Grotesk da referência Koisei fornecida.

## Executar

Requer Node.js 20 ou superior. Não precisa instalar pacotes.

```sh
npm run dev
npm run check
npm run build
```

Prévia em http://localhost:4173. Publicação estática em `dist/`.

## Dados e manutenção

- Cores e fontes: `styles.css`.
- Contatos, Instagram, localização e mensagens do WhatsApp: `config.js`.
- Conteúdo institucional estático: `index.html`.
- Briefing adaptado: `PROMPT-BEM-ESTAR.md`.

## Informações confirmadas pelo cliente

- Bem Estar Fisio Pilates / Studio de Pilates Bem Estar.
- Débora dos Santos, fisioterapeuta e proprietária; foto fornecida pelo cliente.
- Pilates com foco em qualidade de vida, condicionamento físico e objetivos individuais.
- Av. 22 de Maio, prédio Helix, torre 1, sala 206, Itaboraí/RJ. Sem número de rua ou CEP confirmado.
- Contato principal: +55 21 99832-8486.
- Instagram: https://www.instagram.com/bemestarpilates_fisio/.
- Frase: “Mente e corpo em completa sintonia”.

## Pendências e critérios editoriais

- O segundo contato foi recebido como `9773381-58`. Não foi corrigido por suposição e não está publicado.
- Idade, tempo de formação e vínculo municipal pertencem a uma postagem sem data confirmada. Foram omitidos para evitar informação desatualizada.
- O Instagram e os dois posts não puderam ser inspecionados. As cores são as fornecidas pelo cliente, não uma paleta extraída do perfil. Os posts aparecem apenas como links oficiais; suas imagens e assuntos não foram inventados.
- Logotipo fornecido pelo cliente e aplicado no cabeçalho, no rodapé, na página de privacidade e no ícone do navegador. O fundo foi removido com a ferramenta nativa ImageGen, gerando PNG com transparência. O tamanho do cabeçalho foi ajustado para acomodar a assinatura completa.
- Apenas o retrato da Débora é fotografia oficial fornecida. A imagem de Pilates é ilustrativa gerada por IA, identificada na página; não representa o studio, seus equipamentos ou pacientes reais.
- Não há horários, preços, CREFITO, avaliações, número de alunos, estrutura física ou especialidades adicionais confirmados. A atuação pediátrica mencionada não foi transformada em serviço oferecido no studio.
- O briefing menciona 15 seções, mas não inclui a lista original nem especificações técnicas restantes. Foi proposta uma arquitetura de 15 blocos, descrita no prompt adaptado.
- Textos de benefícios usam linguagem geral, sem promessa terapêutica ou prescrição. Referência editorial: [NHS — Pilates for beginners](https://www.nhs.uk/live-well/exercise/pilates-and-yoga/pilates-for-beginners/) e [NHS — Be active for your mental health](https://www.nhs.uk/every-mind-matters/mental-wellbeing-tips/be-active-for-your-mental-health/).

## Privacidade

Sem cookies de rastreamento, analytics, embeds de redes sociais ou coleta de dados em servidor. WhatsApp, Instagram e mapas são abertos apenas quando o visitante clica. As fontes são servidas localmente. A página de privacidade detalha esses fluxos.

## GitHub e hospedagem

Repositório: https://github.com/Jneliorr/lp-bemestar-pilates. Criado pelo cliente; o envio dos arquivos e dados comerciais ao repositório público foi expressamente autorizado. O projeto utiliza commits e pushes em marcos concluídos.

A hospedagem Sites permanece privada por padrão. A visibilidade do repositório não altera automaticamente a audiência da hospedagem.

## Verificação

`npm run check` confere sintaxe, arquivos locais, âncoras, IDs únicos, descrições e dimensões de imagens, links externos, mensagens reais do WhatsApp e ausência de informações institucionais pendentes. `npm run build` gera o pacote estático.

Na atualização da logo, o cabeçalho foi conferido no navegador em desktop e em viewport móvel de 390 × 844, com imagens carregadas, proporção preservada e sem transbordamento horizontal. A logo também está aplicada no rodapé e na página de privacidade. O PNG foi verificado com canal alpha transparente.

## Vídeo de apresentação

[Vídeo em MP4](media/apresentacao-bem-estar-pilates.mp4), com 45 segundos em Full HD, capturas reais do site em desktop e celular, títulos em português e trilha instrumental original sintetizada. Roteiro e reprodução em [media/README.md](media/README.md); montagem em `scripts/criar-video-site.py`.
