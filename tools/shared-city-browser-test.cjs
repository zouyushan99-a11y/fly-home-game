const fs=require('fs'),assert=require('assert'),{chromium}=require('playwright'),cp=require('child_process');
const out='evidence/city',after=fs.readFileSync('index.html','utf8'),before=cp.execFileSync('git',['show','0f6b627:index.html'],{encoding:'utf8'}),replays=JSON.parse(fs.readFileSync(out+'/replays.json'));
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});const report={errors:[],journeys:[],performance:[],checks:[],physicalPhone:false};
for(const [device,width,height] of [['desktop',1280,720],['portrait',390,844],['landscape',844,390]]){
 for(const [version,html] of [['before',before],['after',after]]){
 const context=await browser.newContext({viewport:{width,height},hasTouch:device!=='desktop',isMobile:device!=='desktop'}),page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));await page.route('**/city-test',r=>r.fulfill({contentType:'text/html',body:html.replace('labels();requestAnimationFrame(frame);','window.test={g,renderer,updateUI,restart,advance,entrancePassages,cameraZ};labels();')}));await page.goto('http://127.0.0.1:8080/city-test');await page.locator('#start').click();await page.evaluate(()=>test.renderer.draw(test.g));await page.waitForFunction(()=>test.renderer.groundImages&&Object.values(test.renderer.groundImages).every(i=>i.complete&&i.naturalWidth));await page.waitForFunction(()=>[...test.renderer.skies.values()].every(i=>i.complete&&i.naturalWidth));
 for(const route of ['A','B','C']){
 await page.evaluate(route=>{const {g,renderer:r}=test;g.reset();g.started=true;g.chapter=0;g.progress=30;g.routes[0]=route;g.clock=20;test.updateUI();r.draw(g)},route);await page.waitForFunction(()=>[...test.renderer.skies.values()].every(i=>i.complete&&i.naturalWidth));await page.waitForTimeout(100);await page.evaluate(()=>test.renderer.draw(test.g));await page.screenshot({path:`${out}/${device}-${route}-${version}.png`});
 const perf=await page.evaluate(async()=>{const times=[];for(let i=0;i<80;i++){await new Promise(requestAnimationFrame);const t=performance.now();test.renderer.draw(test.g);if(i>=20)times.push(performance.now()-t)}times.sort((a,b)=>a-b);return {meanMs:times.reduce((a,b)=>a+b)/times.length,p95Ms:times[Math.floor(times.length*.95)]}});report.performance.push({device,version,route,...perf});
 }
 if(version==='after'){
 const click=async id=>device==='desktop'?page.locator(id).click():page.locator(id).tap();
 for(const route of ['A','B','C']){
 await page.evaluate(()=>{test.restart();test.g.started=true;test.updateUI()});const replay=replays[route];let i=0,shots=0;const result={device,route,cards:0};
 while(i<replay.length){const chunk=replay.slice(i,i+120);const state=await page.evaluate(({chunk,i})=>{const {g,renderer:r}=test;let used=0;for(const input of chunk){if(g.lesson)break;g.tick(1/60,input);used++;if((i+used)%30===0)r.draw(g)}test.updateUI();r.draw(g);return {used,lesson:!!g.lesson,progress:g.progress,chapter:g.chapter,done:g.done,health:g.health}}, {chunk,i});i+=state.used;
 if(state.lesson){const frozen=await page.evaluate(()=>{const g=test.g,snap=()=>JSON.stringify([g.energy,g.health,g.progress,g.clock,g.interference,g.trackYaw]);const prev=snap();g.tick(.2,1);return prev===snap()});assert(frozen);await click('#continueLesson');result.cards++;}
 if(device==='desktop'&&state.chapter<2&&state.chapter>=0&&state.progress>18+shots*5&&shots<11){await page.screenshot({path:`${out}/flight-${route}-${String(shots).padStart(2,'0')}.png`});shots++;}
 if(state.done)break;
 }
 Object.assign(result,await page.evaluate(()=>({success:test.g.success,health:test.g.health,energy:test.g.energy,time:test.g.time,learned:[...test.g.learned],routes:test.g.routes})));assert(result.success&&result.health===100,JSON.stringify(result));assert(result.learned.length>=6);report.journeys.push(result);fs.writeFileSync(out+'/browser-progress.json',JSON.stringify(report,null,2));
 await click('#skipOutro');assert(await page.locator('#ending').isVisible());await click('#again');assert.equal(await page.evaluate(()=>test.g.trackYaw),0);
 }
 await page.evaluate(()=>{test.restart();test.g.started=true;test.g.chapter=0;test.g.progress=10;test.g.teach('glass');test.g.tick(1/60);test.updateUI()});if(await page.locator('#continueLesson').isVisible())await click('#continueLesson');
 await click('#pause');const frozen=await page.evaluate(()=>{const g=test.g,a=g.energy;test.advance(.2);return g.energy===a});assert(frozen);await click('#resume');await click('#help');await click('#helpPanel .modal-language');await click('#helpPanel .modal-language');await click('#closeHelp');
 // Actual input events exercise the existing controls, independently of replay steering.
 const prior=await page.evaluate(()=>test.g.x);
 if(device==='desktop'){await page.keyboard.down('ArrowLeft');await page.evaluate(()=>{for(let i=0;i<25;i++)test.advance(1/60)});await page.keyboard.up('ArrowLeft');}else{const bb=await page.locator('#left').boundingBox(),cdp=await context.newCDPSession(page);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:bb.x+bb.width/2,y:bb.y+bb.height/2}]});await page.evaluate(()=>{for(let i=0;i<25;i++)test.advance(1/60)});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await cdp.detach();}assert((await page.evaluate(()=>test.g.x))<prior);
 await page.evaluate(()=>{test.g.finish(false);test.updateUI()});await click('#skipOutro');assert(await page.locator('#ending').isVisible());await click('#again');report.checks.push(device+': keyboard/touch, pause, help, bilingual, card freeze, six topics, success/failure/restart');
 }
 await context.close();console.log(device,version,'PASS');
 }
}
assert.deepEqual(report.errors,[]);await browser.close();fs.writeFileSync(out+'/browser.json',JSON.stringify(report,null,2));})();
