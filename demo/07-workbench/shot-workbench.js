// Screenshot of the local workbench (demo tool, not part of the workshop package).
// usage: node shot-workbench.js URL OUT.png [OUT-PREVIEW.png]
// It opens the page, opens the folder 正文 and the first chapter in the file tree by clicking, scrolls the text
// back to its first line with the mouse wheel, and takes one 1280-pixel-wide screenshot. With a second file name
// it then clicks 预览 and takes another. The only thing covered is the absolute path of the workspace on this
// machine (Playwright's mask over #workspacePath); nothing on the page is rewritten.
const { chromium } = require('playwright');

(async () => {
  const [url, out, outPreview] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  const external = [];
  page.on('request', (r) => { if (!r.url().startsWith(url)) external.push(r.url()); });
  await page.goto(url);
  await page.waitForSelector('#fileTree .tree-label');
  await page.locator('#fileTree .tree-label', { hasText: /^正文$/ }).click();
  await page.locator('#fileTree .tree-label', { hasText: '第001章' }).click();
  await page.waitForSelector('#editorWorkspace:not([hidden])');
  await page.waitForTimeout(500);
  await page.locator('#editorInput').hover();
  await page.mouse.wheel(0, -5000);
  await page.waitForTimeout(500);
  const shot = { mask: [page.locator('#workspacePath')], maskColor: '#c9c9c9' };
  await page.screenshot({ path: out, ...shot });
  if (outPreview) {
    await page.getByRole('button', { name: '预览', exact: true }).click();
    await page.waitForSelector('#previewPane:not([hidden])');
    await page.waitForTimeout(500);
    await page.screenshot({ path: outPreview, ...shot });
  }
  console.log('requests to other hosts:', external.length);
  await browser.close();
})().catch((error) => { console.error(error); process.exit(1); });
