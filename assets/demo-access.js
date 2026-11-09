/* Static UI demonstration only: these credentials and all site files are public. */
(() => {
  const root = new URL('../', document.currentScript.src);
  const loginURL = new URL('login.html', root);
  const isLogin = location.pathname === loginURL.pathname;
  const sessionKey = 'hmbot-demo-session-v1';
  const logKey = 'hmbot-demo-visits-v1';
  const clientKey = 'hmbot-demo-client-v1';
  const account = {username:'demo', password:'demo123'};
  let session = null, storageError = false;
  try { session = JSON.parse(sessionStorage.getItem(sessionKey)); } catch (_) { storageError = true; }
  const authenticated = session && session.username === account.username;
  if (!isLogin && !authenticated) {
    document.documentElement.classList.add('demo-locked');
    loginURL.searchParams.set('next', location.pathname + location.search + location.hash);
    location.replace(loginURL.href);
    return;
  }
  function destination() {
    let candidate;
    try { candidate = new URL(new URLSearchParams(location.search).get('next') || 'index.html', root); }
    catch (_) { return new URL('index.html',root).href; }
    // Keep the demo redirect within this site, including project Pages subpaths.
    return candidate.origin === root.origin && candidate.pathname.startsWith(root.pathname) &&
      candidate.pathname !== loginURL.pathname && candidate.pathname.endsWith('.html') ? candidate.href : new URL('index.html',root).href;
  }
  function readLogs() {
    const parsed = JSON.parse(localStorage.getItem(logKey) || '[]');
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(x=>x && typeof x.time==='string' && typeof x.page==='string' && typeof x.visitor==='string').slice(-200);
  }
  document.addEventListener('DOMContentLoaded', () => {
    if (isLogin) {
      const form = document.querySelector('#login-form');
      const error = document.querySelector('#login-error');
      if (storageError) error.textContent='浏览器存储不可用，请允许此网站使用浏览器存储。';
      form.addEventListener('submit', event => {
        event.preventDefault();
        if (form.elements.username.value.trim() !== account.username || form.elements.password.value !== account.password) {
          error.textContent='用户名或密码不正确。请使用下方演示账号。';
          return;
        }
        try {
          sessionStorage.setItem(sessionKey,JSON.stringify({username:account.username}));
          location.replace(destination());
        } catch (_) { error.textContent='无法保存演示登录状态，请允许浏览器存储后重试。'; }
      });
      return;
    }
    for (const button of document.querySelectorAll('[data-demo-logout]')) button.addEventListener('click', () => {
      try { sessionStorage.removeItem(sessionKey); } catch (_) {}
      location.replace(loginURL.href);
    });
    let logs=[], logError=false;
    try {
      let visitor=localStorage.getItem(clientKey);
      if (!visitor) {visitor='浏览器-'+crypto.randomUUID().slice(0,8);localStorage.setItem(clientKey,visitor);}
      logs=readLogs();
      // Deliberately exclude query strings and form values from this local demonstration.
      logs.push({time:new Date().toISOString(),page:location.pathname,title:document.title,visitor,username:session.username});
      logs=logs.slice(-200);
      localStorage.setItem(logKey,JSON.stringify(logs));
    } catch (_) {logError=true;}
    const body=document.querySelector('#visit-rows');
    if (!body) return;
    const status=document.querySelector('#visit-status');
    function show() {
      body.replaceChildren();
      for (const entry of [...logs].reverse()) {
        const row=document.createElement('tr');
        for (const value of [new Date(entry.time).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai',hour12:false}),entry.username||'demo',entry.visitor,'未采集（静态演示）',entry.page]) {
          const cell=document.createElement('td'); cell.textContent=value;row.append(cell);
        }
        body.append(row);
      }
      status.textContent=logError?'浏览器存储不可用，无法保存访问记录。':`${logs.length} 条本浏览器记录 · 最多保留 200 条 · 北京时间`;
    }
    document.querySelector('#clear-visits').addEventListener('click',()=>{
      try {localStorage.removeItem(logKey);logs=[];logError=false;}catch(_){logError=true;}
      show();
    });
    show();
  });
})();
