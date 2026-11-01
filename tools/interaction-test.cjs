const {chromium}=require('playwright'),fs=require('fs'),assert=require('assert');
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-gpu']});const results=[],errors=[];
for(const [name,width,height,touch] of [['desktop',1280,720,false],['portrait',390,844,true],['landscape',844,390,true]]){
 const ctx=await browser.newContext({viewport:{width,height},hasTouch:touch,isMobile:touch}),page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/interaction-test',r=>r.fulfill({contentType:'text/html',body:fs.readFileSync('index.html','utf8').replace('labels();requestAnimationFrame(frame);','window.test={g,renderer,updateUI,advance};labels();')}));await page.goto('http://127.0.0.1:8080/interaction-test');
 const click=async selector=>{const el=page.locator(selector);await el.scrollIntoViewIfNeeded();if(touch)await el.tap();else await el.click();};await click('#start');
 const visible=async()=>page.evaluate(()=>['lesson','choices','helpPanel','pausePanel','recovery','ending'].filter(id=>!document.getElementById(id).hidden&&document.getElementById(id).getBoundingClientRect().height>0));
 const freeze=async()=>{assert(await page.evaluate(()=>{const snap=()=>JSON.stringify([test.g.progress,test.g.x,test.g.clock,test.g.time,test.g.health,test.g.energy,test.g.interference,test.g.gust,test.g.routes]);const a=snap();for(let i=0;i<1000;i++)test.g.tick(.1,1);return snap()===a;}));};
 for(let c=0;c<4;c++)for(const route of ['A','B','C']){
  await page.evaluate(c=>{const {g,updateUI,renderer}=test;g.reset();g.started=true;g.chapter=c-1;g.progress=[10,45,80,115][c]-.001;g.clock=10;for(let j=0;j<c;j++)g.routes[j]='B';g.tick(1/60);updateUI();renderer.draw(g);},c);
  assert.deepEqual(await visible(),['lesson']);await freeze();assert.equal(await page.evaluate(()=>Object.keys(test.g.routes).length),c);
  if(c===0&&route==='A')await page.screenshot({path:`evidence/flow-${name}-1-lesson.png`});
  await click('#help');assert.deepEqual(await visible(),['helpPanel']);await click('#helpPanel .modal-language');await click('#closeHelp');assert.deepEqual(await visible(),['lesson']);
  await click('#pause');assert.deepEqual(await visible(),['pausePanel']);await click('#resume');assert.deepEqual(await visible(),['lesson']);
  await click('#continueLesson');assert.deepEqual(await visible(),['choices']);await freeze();
  if(c===0&&route==='A')await page.screenshot({path:`evidence/flow-${name}-2-routes.png`});
  await click('#pause');await click('#pauseHelp');assert.deepEqual(await visible(),['helpPanel']);await click('#helpPanel .modal-language');await click('#closeHelp');assert.deepEqual(await visible(),['pausePanel']);await click('#resume');assert.deepEqual(await visible(),['choices']);
  const energy=await page.evaluate(()=>test.g.energy);
  await click(`#choices button:nth-child(${'ABC'.indexOf(route)+1})`);
  assert.equal(await page.evaluate(c=>test.g.routes[c],c),route);assert.equal(await page.evaluate(()=>test.g.energy),energy-(route==='C'?5:0));assert.deepEqual(await visible(),[]);
  assert((await page.locator('#route').textContent()).includes(route));const z=await page.evaluate(()=>test.g.progress);await page.evaluate(()=>test.advance(.1));assert((await page.evaluate(()=>test.g.progress))>z);
  if(c===0&&route==='A')await page.screenshot({path:`evidence/flow-${name}-3-flight.png`});
  results.push({name,chapter:c,route,passed:true});
 }
 // Queued collision knowledge cannot steal an unfinished route choice.
 await page.evaluate(()=>{const {g}=test;g.reset();g.started=true;g.chapter=0;g.progress=10;g.teach('wall',2,true);test.updateUI();});assert.deepEqual(await visible(),['choices']);await freeze();await click('#choices button:nth-child(3)');const e=await page.evaluate(()=>test.g.energy);await page.evaluate(()=>test.advance(.1));assert.deepEqual(await visible(),['lesson']);await freeze();assert.equal(await page.evaluate(()=>test.g.energy),e);await click('#continueLesson');
 // Checkpoint recovery returns to route selection without replaying the entrance card.
 await page.evaluate(()=>{test.g.health=0;test.g.checkRecovery();test.g.recoveryTime=2;test.updateUI();});assert.deepEqual(await visible(),['recovery']);await click('#retry');assert.deepEqual(await visible(),['choices']);await click('#choices button:nth-child(2)');assert.equal(await page.evaluate(()=>test.g.routes[0]),'B');
 await ctx.close();
}await browser.close();assert.deepEqual(errors,[]);fs.writeFileSync('evidence/interaction-results.json',JSON.stringify({cases:results,errors,extraChecks:['queued knowledge waits for route','checkpoint retry restores choice','100 simulated seconds frozen per reading/choice','help, pause and bilingual return paths'],physicalPhone:false},null,2));console.log('PASS',results.length,'route flows across three viewports');})();
