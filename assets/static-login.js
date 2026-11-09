/* Static password prompt only. Source code and all hosted files remain public. */
(() => {
  const root = new URL('../', document.currentScript.src);
  const login = new URL('login.html', root);
  const isLogin = location.pathname === login.pathname;
  const key = 'hmbot-static-login-v2';
  let allowed = false;
  try { allowed = sessionStorage.getItem(key) === 'granted'; } catch (_) {}
  if (!isLogin && !allowed) {
    document.documentElement.classList.add('login-locked');
    login.searchParams.set('next',location.pathname + location.search + location.hash);
    location.replace(login.href);
    return;
  }
  function destination() {
    try {
      const url = new URL(new URLSearchParams(location.search).get('next') || 'index.html',root);
      if (url.origin === root.origin && url.pathname.startsWith(root.pathname) && url.pathname !== login.pathname && url.pathname.endsWith('.html')) return url.href;
    } catch (_) {}
    return new URL('index.html',root).href;
  }
  document.addEventListener('DOMContentLoaded', () => {
    if (isLogin) {
      const form = document.querySelector('#login-form');
      const error = document.querySelector('#login-error');
      form.addEventListener('submit',event => {
        event.preventDefault();
        if (form.elements.password.value !== 'migbot2026') {
          error.textContent = '密码不正确，请重试。';
          return;
        }
        try {
          sessionStorage.setItem(key,'granted');
          location.replace(destination());
        } catch (_) { error.textContent = '无法保存登录状态，请允许浏览器存储后重试。'; }
      });
    }
    for (const button of document.querySelectorAll('[data-logout]')) button.addEventListener('click', () => {
      try { sessionStorage.removeItem(key); } catch (_) {}
      location.replace(login.href);
    });
  });
})();
