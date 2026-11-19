import { siteConfig, whatsappUrl } from './config.js';

document.querySelectorAll('[data-whatsapp]').forEach(link => { link.href = whatsappUrl(link.dataset.whatsapp); });
document.querySelectorAll('[data-instagram]').forEach(link => { link.href = siteConfig.instagram; link.textContent = siteConfig.instagramHandle; });
document.querySelectorAll('[data-post]').forEach(link => { link.href = siteConfig.posts[Number(link.dataset.post)]; });
document.querySelectorAll('[data-phone]').forEach(link => { link.href = `tel:+${siteConfig.phone}`; link.textContent = siteConfig.phoneDisplay; });
document.querySelectorAll('[data-address]').forEach(el => { el.textContent = siteConfig.address; });
document.querySelectorAll('[data-city]').forEach(el => { el.textContent = siteConfig.city; });
document.querySelectorAll('[data-map]').forEach(link => { link.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(siteConfig.mapQuery)}`; });
document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

if (document.querySelector('link[rel="canonical"]')) {
  const schema = document.createElement('script');
  schema.type = 'application/ld+json';
  schema.textContent = JSON.stringify({
    '@context': 'https://schema.org', '@type': 'HealthAndBeautyBusiness',
    name: siteConfig.name, telephone: `+${siteConfig.phone}`,
    url: document.querySelector('link[rel="canonical"]').href,
    sameAs: [siteConfig.instagram],
    address: { '@type': 'PostalAddress', streetAddress: siteConfig.address,
      addressLocality: 'Itaboraí', addressRegion: 'RJ', addressCountry: 'BR' },
    founder: { '@type': 'Person', name: 'Débora dos Santos', jobTitle: 'Fisioterapeuta' },
  });
  document.head.append(schema);
}

const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
const mobileQuery = window.matchMedia('(max-width: 900px)');
function closeMenu(returnFocus = false) {
  menuButton?.setAttribute('aria-expanded', 'false');
  menuButton?.setAttribute('aria-label', 'Abrir menu');
  nav?.classList.remove('is-open');
  document.body.classList.remove('menu-open');
  if (returnFocus) menuButton?.focus();
}
menuButton?.addEventListener('click', () => {
  if (menuButton.getAttribute('aria-expanded') === 'true') { closeMenu(); return; }
  menuButton.setAttribute('aria-expanded', 'true');
  menuButton.setAttribute('aria-label', 'Fechar menu');
  nav.classList.add('is-open');
  document.body.classList.add('menu-open');
});
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu()));
document.addEventListener('keydown', event => {
  if (menuButton?.getAttribute('aria-expanded') !== 'true') return;
  if (event.key === 'Escape') closeMenu(true);
  if (event.key !== 'Tab') return;
  const lastLink = nav.querySelector('a:last-child');
  if (event.shiftKey && document.activeElement === menuButton) {
    event.preventDefault(); lastLink?.focus();
  } else if (!event.shiftKey && document.activeElement === lastLink) {
    event.preventDefault(); menuButton.focus();
  }
});
mobileQuery.addEventListener('change', () => closeMenu());

const floatingContact = document.querySelector('.floating-contact');
if ('IntersectionObserver' in window) {
  const contact = document.querySelector('#contato');
  if (contact && floatingContact) {
    const contactObserver = new IntersectionObserver(entries => {
      floatingContact.classList.toggle('is-hidden', entries[0].isIntersecting);
    }, { threshold: 0.15 });
    contactObserver.observe(contact);
  }
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.remove('is-pending');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('.section-heading, .essence-grid, .pilates-copy, .benefits-grid article, .audience-grid, .steps li, .professional-copy, .mind-grid, .instagram-post, .faq-grid, .contact-top').forEach(el => {
      if (el.getBoundingClientRect().top > window.innerHeight) {
        el.classList.add('reveal', 'is-pending');
        revealObserver.observe(el);
      }
    });
  }
}
