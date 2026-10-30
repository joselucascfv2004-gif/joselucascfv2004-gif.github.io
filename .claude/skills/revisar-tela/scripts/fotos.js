// Fotos de uma tela, rolando tela por tela, em uma ou mais larguras.
// Uso: node fotos.js <pasta-saida> <url ou arquivo.html> [--larguras 375,1280] [--telas 8]
//        [--clicar "Texto do botão"] [--esperar 3000] [--nome pagina]
// Saída: <pasta>/<nome>_<largura>_t01.jpg, _t02.jpg ... (uma imagem por tela)
// Tela por tela (e não a página inteira) porque avisos fixos ficam por cima e imagens "lazy" saem em branco.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const opc = { larguras: '375', telas: '8', clicar: '', esperar: '3000', nome: '' };
const pos = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--rede') opc.rede = true;
  else if (args[i].startsWith('--')) opc[args[i].slice(2)] = args[++i];
  else pos.push(args[i]);
}
const [saida, alvo] = pos;
if (!saida || !alvo) {
  console.log('Uso: node fotos.js <pasta-saida> <url ou arquivo.html> [--larguras 375,1280] [--telas 8] [--clicar "Texto"]');
  process.exit(1);
}
const url = /^https?:|^file:/.test(alvo) ? alvo : 'file://' + path.resolve(alvo);
const nome = opc.nome || path.basename(decodeURIComponent(url.split(/[?#]/)[0])).replace(/\.html?$/, '') || 'pagina';
fs.mkdirSync(saida, { recursive: true });

(async () => {
  // --rede: usa o proxy da máquina para sites de fora (Firebase, APIs); o servidor local fica de fora dele
  const rede = 'rede' in opc && process.env.HTTPS_PROXY
    ? { proxy: { server: process.env.HTTPS_PROXY, bypass: '127.0.0.1,localhost' } } : {};
  const navegador = await chromium.launch(rede);
  for (const largura of opc.larguras.split(',').map(Number)) {
    const altura = largura < 600 ? 812 : 800;
    const p = await navegador.newPage({ viewport: { width: largura, height: altura } });
    p.on('pageerror', e => console.log(`[${largura}px] erro na página: ${e.message.slice(0, 140)}`));
    await p.goto(url, { waitUntil: 'load', timeout: 30000 }).catch(e => console.log('aviso:', e.message.split('\n')[0]));
    await p.waitForTimeout(+opc.esperar);
    if (opc.clicar) {
      await p.getByText(opc.clicar, { exact: true }).first().click()
        .catch(() => p.getByText(opc.clicar).first().click())
        .catch(e => console.log('não achei para clicar:', opc.clicar, e.message.split('\n')[0]));
      await p.waitForTimeout(1200);
    }
    const total = await p.evaluate(() => document.documentElement.scrollHeight);
    const passo = altura - 52; // um pouco de sobreposição entre as telas
    let n = 0;
    for (let y = 0; n < +opc.telas; y += passo) {
      await p.evaluate(v => window.scrollTo(0, v), y);
      await p.waitForTimeout(600);
      n++;
      await p.screenshot({ path: path.join(saida, `${nome}_${largura}_t${String(n).padStart(2, '0')}.jpg`), quality: 80 });
      if (y + altura >= total) break;
    }
    console.log(`${nome} ${largura}px: ${n} tela(s), altura da página ${total}px`);
    await p.close();
  }
  await navegador.close();
})();
