const { chromium }=require('playwright');
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const hook=`window.__test={g,renderer,makeDistrict,hitsBuilding,worldPoint:typeof worldPoint!=='undefined'?worldPoint:null,buildingParts:typeof buildingParts!=='undefined'?buildingParts:null,Journey,cameraZ,pathX,advance,updateUI,getLang:()=>lang};window.__stop=true;`;
async function prepare(browser,version,width=1280,height=720,mobile=false){
 const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:mobile?2:1,isMobile:mobile,hasTouch:mobile});
 const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/test.html',route=>{
  let source=(version==='before'?require('child_process').execFileSync('git',['show','8ea2e9a0b96eea47e6742148ee1f9784549bebcc:index.html'],{cwd:root,encoding:'utf8'}):fs.readFileSync(path.join(root,'index.html'),'utf8'));
  source=source.replace('labels();requestAnimationFrame(frame);',hook+'labels();updateUI();renderer.draw(g,lang);');
  route.fulfill({contentType:'text/html',body:source});
 });
 await page.goto('http://127.0.0.1:8080/test.html');await page.locator('#start').click();await page.waitForTimeout(600);
 return {context,page,errors};
}
async function scene(page,stage,progress,x=0){
 await page.evaluate(({stage,progress,x})=>{const {g,renderer,updateUI}=__test;g.reset();Object.assign(g,{started:true,chapter:stage,progress,clock:progress,time:progress,x});for(let i=0;i<=3;i++){g.routes[i]='B';g.routeSelectedAt[i]=0;}updateUI();renderer.draw(g);},{stage,progress,x});
 await page.waitForTimeout(400);
 await page.evaluate(()=>__test.renderer.draw(__test.g));
}
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 const report={environment:{browser:await browser.version(),os:process.platform,physicalPhone:false,benchmark:'1280x720 DPR 1, fixed scene B day at progress 28; 20 RAF warmup + 120 RAF-paced draws, repeated 3 times, no simulation or screenshots inside timing'},performance:{},checks:[]};
 for(const version of ['before','after']){
  const {context,page,errors}=await prepare(browser,version);
  await scene(page,0,28);
  console.log('benchmark',version);const perf=await page.evaluate(async()=>{const {g,renderer}=__test;const runs=[];const frame=()=>new Promise(requestAnimationFrame);for(let r=0;r<3;r++){for(let i=0;i<20;i++){await frame();renderer.draw(g);}const times=[],intervals=[];let prev=await frame();for(let i=0;i<120;i++){const stamp=await frame();intervals.push(stamp-prev);prev=stamp;const t=performance.now();renderer.draw(g);times.push(performance.now()-t);}times.sort((a,b)=>a-b);intervals.sort((a,b)=>a-b);runs.push({meanMs:times.reduce((a,b)=>a+b,0)/times.length,p50Ms:times[60],p95Ms:times[114],rafFPS:1000/(intervals.reduce((a,b)=>a+b,0)/intervals.length),rafP95Ms:intervals[114]});}return {runs,textures:renderer.textures.size,foliage:renderer.foliage.size};});
  perf.moving=await page.evaluate(async()=>{const {g,renderer}=__test;const cpu=[],gaps=[];let prev;for(let i=0;i<90;i++){const stamp=await new Promise(requestAnimationFrame);g.progress=28+i/90;g.clock=g.progress;g.x=Math.sin(i/45)*.06;const t=performance.now();renderer.draw(g);if(i>=10){cpu.push(performance.now()-t);gaps.push(stamp-prev);}prev=stamp;}g.progress=28;g.clock=28;g.x=0;return {meanMs:cpu.reduce((a,b)=>a+b,0)/cpu.length,rafFPS:1000/(gaps.reduce((a,b)=>a+b,0)/gaps.length)};});
  report.performance[version]=perf;console.log(version,JSON.stringify(perf));
  await page.screenshot({path:path.join(root,`evidence/${version}-day.png`)});
  if(version==='after'){
   for(const [name,stage,progress,x] of [['day',0,28,0],['night',1,64,0],['corridor',2,101,0],['village',3,130,0],['wetland',4,153,0],['glass',0,24,-.35]]){
    await scene(page,stage,progress,x);await page.screenshot({path:path.join(root,`evidence/${name}.png`)});
   }
   // Continuous frames use deterministic camera travel, not an editor mockup.
   await scene(page,0,24,-.25);
   for(let i=0;i<8;i++){
    await page.evaluate(i=>{const {g,renderer}=__test;g.progress=24+i*.08;g.x=-.25+i*.022;g.clock=24+i*.08;renderer.draw(g);},i);
    await page.screenshot({path:path.join(root,`evidence/reflection-${String(i).padStart(2,'0')}.png`)});
   }
   const results=await page.evaluate(()=>{
    const {g,renderer,makeDistrict,hitsBuilding,worldPoint,buildingParts,Journey,updateUI}=__test,results=[];
    const check=(name,pass,detail)=>results.push({name,pass,detail});
    check('layout stable',JSON.stringify(makeDistrict(0,'B'))===JSON.stringify(makeDistrict(0,'B')));
    check('route density A > B > C',makeDistrict(0,'A').length>makeDistrict(0,'B').length&&makeDistrict(0,'B').length>makeDistrict(0,'C').length);
    check('six building types',new Set([0,1,2,3].flatMap(c=>makeDistrict(c,'B').filter(b=>!b.solidTree).map(b=>b.kind))).size===6);
    let tests=0,bad=0;
    for(const c of [0,1,2,3])for(const route of ['A','B','C'])for(const b of makeDistrict(c,route)){
     if(b.height<33)continue;
     for(const part of buildingParts(b)){
      if(part.y>35||part.y+part.h<33)continue;
      const pt=worldPoint(b,0,34,0);tests++;if(!hitsBuilding(b,{x:pt[0],z:pt[2]},{x:pt[0],z:pt[2]}))bad++;
     }
     const pt=worldPoint(b,b.width/2+4,34,0);tests++;if(hitsBuilding(b,{x:pt[0],z:pt[2]},{x:pt[0],z:pt[2]}))bad++;
    }
    check('rotated collision inside and outside',bad===0,{tests,bad});
    const b={x:0,z:0,width:10,depth:10,height:50,angle:.6,kind:'office'};
    check('swept collision catches tunnelling',hitsBuilding(b,{x:0,z:-50},{x:0,z:50}));
    const game=new Journey();game.started=true;game.tick(.1,0);game.paused=true;const before=JSON.stringify([game.progress,game.clock]);game.tick(.1,1);check('pause freezes simulation',before===JSON.stringify([game.progress,game.clock]));
    game.paused=false;game.chapter=0;check('route choice and C cost',game.choose('C')&&game.energy===95&&!game.choose('A'));
    game.grace=0;check('collision rules retained',game.collide('test',false)&&game.health===75);game.grace=0;check('severe collision retained',game.collide('test2',true)&&game.health===40);
    const journey=new Journey();journey.started=true;journey.x=.7;
    for(let i=0;i<18000&&!journey.done;i++){if(journey.chapter>=0&&journey.chapter<4&&!journey.routes[journey.chapter])journey.choose('C');journey.tick(1/60,-journey.driftVelocity()/.62);}
    check('full simulated journey C arrives',journey.done&&journey.success,{health:journey.health,energy:journey.energy,progress:journey.progress});
    g.paused=true;renderer.draw(g);const frozen=renderer.canvas.toDataURL();g.tick(.1,1);renderer.draw(g);check('pause freezes rendered animation',frozen===renderer.canvas.toDataURL());g.paused=false;
    check('four sky textures decoded',['day','night','dawn','dusk'].every(n=>renderer.skies.get(n)?.naturalWidth>0));
    check('texture cache bounded',renderer.textures.size<=96);
    renderer.reducedEffects=true;renderer.draw(g);const prev=renderer.reflectionClock;g.clock+=1;renderer.draw(g);check('reduced effects freeze reflection phase',renderer.reflectionClock===prev);
    return results;
   });report.checks.push(...results);
  }
  report.checks.push({name:`${version}: no browser exceptions`,pass:errors.length===0,detail:errors});
  await context.close();
 }
 // Touch, keyboard, language, pause and portrait rendering exercise actual UI events.
 const {context,page,errors}=await prepare(browser,'after',390,844,true);
 await scene(page,2,100);
 await page.screenshot({path:path.join(root,'evidence/mobile-corridor.png')});
 await page.locator('#language').click();report.checks.push({name:'bilingual toggle',pass:await page.evaluate(()=>__test.getLang()==='en')});
 const buttons=await page.locator('#controls button').evaluateAll(bs=>bs.map(b=>b.id));
 const box=await page.locator('#'+buttons[1]).boundingBox(),cdp=await context.newCDPSession(page);
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:box.x+box.width/2,y:box.y+box.height/2}]});
 await page.evaluate(()=>__test.advance(.1));let moved=await page.evaluate(()=>__test.g.x);
 await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
 report.checks.push({name:'touch hold steers',pass:moved>0});
 const oldx=await page.evaluate(()=>__test.g.x);await page.keyboard.down('ArrowLeft');await page.evaluate(()=>__test.advance(.1));await page.keyboard.up('ArrowLeft');
 report.checks.push({name:'keyboard steers',pass:await page.evaluate(x=>__test.g.x<x,oldx)});
 await page.locator('#pause').click();report.checks.push({name:'pause button',pass:await page.evaluate(()=>__test.g.paused)});
 report.checks.push({name:'mobile no browser exceptions',pass:errors.length===0,detail:errors});
 await context.close();await browser.close();
 fs.writeFileSync(path.join(root,'evidence/results.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
 if(report.checks.some(c=>!c.pass))process.exitCode=1;
})();
