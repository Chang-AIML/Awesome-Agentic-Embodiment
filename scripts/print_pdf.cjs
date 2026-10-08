// Print an HTML file to an A4 PDF with headless Chromium (Playwright), page numbers in the footer.
// Usage: node scripts/print_pdf.cjs <in.html> <out.pdf>
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:7px;color:#898781;text-align:center;">' +
      '<span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' },
  });
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
