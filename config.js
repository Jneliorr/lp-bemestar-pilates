export const siteConfig = Object.freeze({
  name: 'Bem Estar Fisio Pilates',
  phone: '5521998328486',
  phoneDisplay: '(21) 99832-8486',
  instagram: 'https://www.instagram.com/bemestarpilates_fisio/',
  instagramHandle: '@bemestarpilates_fisio',
  posts: [
    'https://www.instagram.com/p/C5TXIdfuGcs/?img_index=1',
    'https://www.instagram.com/p/C2P9ocUupBO/',
  ],
  address: 'Av. 22 de Maio, prédio Helix, torre 1, sala 206',
  city: 'Itaboraí · Rio de Janeiro',
  mapQuery: 'Prédio Helix, Avenida 22 de Maio, Itaboraí, RJ',
  messages: {
    general: 'Olá, Bem Estar! Gostaria de conhecer o studio e saber mais sobre as aulas de Pilates.',
    start: 'Olá, Bem Estar! Quero começar no Pilates. Podemos conversar sobre os atendimentos?',
    visit: 'Olá, Bem Estar! Gostaria de combinar uma visita ao studio.',
  },
});

export function whatsappUrl(message = 'general') {
  return `https://wa.me/${siteConfig.phone}?text=${encodeURIComponent(siteConfig.messages[message] || siteConfig.messages.general)}`;
}
