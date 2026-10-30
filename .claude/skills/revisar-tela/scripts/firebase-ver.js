// Fotos de um site com Firebase/Firestore na nuvem, só para ver (o arquivo do site não muda).
// A conexão contínua do Firestore não atravessa o proxy desta máquina e o site fica em "Carregando";
// aqui o navegador de teste usa o proxy e força o Firestore a usar "long polling".
// Uso: node firebase-ver.js <saida-prefixo> <url> [telas=10] [largura=375]
// Saída: <prefixo>_t01.jpg, _t02.jpg ... (uma imagem por tela, rolando a página)
const { chromium } = require('playwright');

const forcarLongPolling = () => {
  let fb;
  Object.defineProperty(window, 'firebase', {
    configurable: true,
    get() {
      if (fb && fb.firestore && !fb.__lp) {
        const original = fb.firestore;
        fb.firestore = Object.assign(function (app) {
          const db = original.call(this, app);
          if (!db.__lp) {
            try { db.settings({ experimentalForceLongPolling: true, merge: true }); } catch (e) {}
            db.__lp = 1;
          }
          return db;
        }, original);
        fb.__lp = 1;
      }
      return fb;
    },
    set(v) { fb = v; },
  });
};

(async () => {
  const [saida, url, telas = 10, largura = 375] = process.argv.slice(2);
  if (!saida || !url) { console.log('Uso: node firebase-ver.js <saida-prefixo> <url> [telas] [largura]'); process.exit(1); }
  const proxy = process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY, bypass: '127.0.0.1,localhost' } } : {};
  const navegador = await chromium.launch(proxy);
  const p = await navegador.newPage({ viewport: { width: +largura, height: 812 } });
  await p.addInitScript(forcarLongPolling);
  await p.goto(url);
  await p.waitForTimeout(12000);
  const altura = await p.evaluate(() => document.documentElement.scrollHeight);
  let n = 0;
  for (let y = 0; n < +telas && y < altura; y += 760) {
    await p.evaluate(v => window.scrollTo(0, v), y);
    await p.waitForTimeout(700);
    n++;
    await p.screenshot({ path: `${saida}_t${String(n).padStart(2, '0')}.jpg`, quality: 80 });
  }
  console.log(`${n} tela(s), altura da página ${altura}px`);
  await navegador.close();
})();
