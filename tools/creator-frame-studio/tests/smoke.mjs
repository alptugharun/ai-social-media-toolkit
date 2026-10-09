import fs from 'node:fs';
import assert from 'node:assert/strict';

const html=fs.readFileSync(new URL('../index.html',import.meta.url),'utf8');
const css=fs.readFileSync(new URL('../styles.css',import.meta.url),'utf8');
const js=fs.readFileSync(new URL('../app.js',import.meta.url),'utf8');

assert.match(html,/Creator Frame Studio/);
assert.match(html,/styles\.css/);
assert.match(html,/app\.js/);
assert.ok(css.length>10000,'CSS unexpectedly small');
assert.ok(js.length>40000,'JavaScript unexpectedly small');

for(const id of ['ig45','ig34','ig11','igland','igstory','igreel','igavatar','ighighlight','pin23','ytvideo','ytshort','ytsmall']){
  assert.ok(js.includes(`id:'${id}'`),`missing preset: ${id}`);
}

for(const feature of ['exportPack','saveProject','openProjectFile','fitAllText','applyTextStyle','applyGuideProfile','readinessCard','window.FrameStudio']){
  assert.ok(js.includes(feature),`missing feature marker: ${feature}`);
}

assert.ok(!js.includes("const DEMO_ONE='data:image"),'embedded personal demo image remained');
assert.ok(!js.includes("const DEMO_TWO='data:image"),'embedded personal demo image remained');

console.log('Creator Frame Studio static smoke checks: PASS');

for(const id of ['styleHook','styleSub','styleCTA','guideBalanced','guideHook','guideCTA','readinessCard']) assert.ok(html.includes(`id="${id}"`),`missing premium control: ${id}`);
assert.ok(html.includes('v0.3 · BETA'),'version badge not updated');
assert.ok(js.includes('Beta 0.3'),'localized footer version not updated');
assert.ok(!js.includes('Beta 0.2'),'stale localized footer version remained');


const csp = html.match(/Content-Security-Policy" content="([^"]+)"/)?.[1] || '';
assert.ok(csp.includes("script-src 'self'"),'CSP must keep scripts self-only');
assert.ok(!csp.includes("script-src 'unsafe-inline'"),'CSP must not allow inline scripts');
assert.ok(!csp.includes("'unsafe-eval'"),'CSP must not allow eval');
assert.ok(csp.includes("style-src-attr 'unsafe-inline'"),'dynamic style attributes need explicit CSP allowance');
assert.ok(csp.includes("connect-src 'none'"),'editor must remain network-disconnected by CSP');
