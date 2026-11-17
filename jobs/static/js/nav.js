(() => {
  const button = document.querySelector('.menu-toggle');
  const nav = document.getElementById(button?.getAttribute('aria-controls'));
  if (!button || !nav) return;

  const closeMenu = () => button.setAttribute('aria-expanded', 'false');

  button.addEventListener('click', () => {
    button.setAttribute('aria-expanded', String(button.getAttribute('aria-expanded') !== 'true'));
  });

  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      button.focus();
    }
  });

  window.matchMedia('(max-width: 980px)').addEventListener('change', closeMenu);
  document.documentElement.classList.add('nav-ready');
})();
