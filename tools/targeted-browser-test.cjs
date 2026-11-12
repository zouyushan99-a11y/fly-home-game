const fs=require('fs'),assert=require('assert'),{chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-gpu']}),rows=[];
for(const [name,width,height]of [['desktop',1280,720],['portrait',390,844],['landscape',844,390]]){
 const p=await b.newPage({viewport:{width,height},hasTouch:name!=='desktop'}),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.route('**/targeted-test',r=>r.fulfill({contentType:'text/html',body:fs.readFileSync('index.html','utf8').replace('labels();requestAnimationFrame(frame);','window.test={g,renderer,updateUI,cameraZ,pathX,advance,hitsBuilding};labels();')}));await p.goto('http://127.0.0.1:8080/targeted-test');await p.locator('#start').click();await p.locator('#skipPractice').click();
 const pose=async(chapter,progress)=>p.evaluate(({chapter,progress})=>{const{g,renderer:r}=test;g.reset();Object.assign(g,{started:true,chapter,progress,cameraDistance:13});g.previewSeen=new Set([0,1,2,3,4]);g.routes[chapter]='B';g.routeSelectedAt[chapter]=-10;r.followPoint=null;r.draw(g);test.updateUI();},{chapter,progress});
 await pose(2,84);await p.waitForFunction(()=>[...test.renderer.skies.values()].every(i=>i.complete&&i.naturalWidth));await p.evaluate(()=>test.renderer.draw(test.g));await p.screenshot({path:`evidence/targeted/${name}-disturbance-before.png`});
 const approach=await p.evaluate(()=>{const{g,renderer:r}=test;for(let i=0;i<100&&!g.lesson;i++){g.tick(1/30,0);r.draw(g);}test.updateUI();return {state:g.disturbance,lesson:g.lesson?.id,health:g.health,progress:g.progress};});
 // Green/corridor may be seen first; continue it before testing the disturbance card.
 for(let n=0;n<6&&approach.lesson!=='birds';n++){const q=await p.evaluate(()=>{const{g,renderer:r}=test;if(g.lesson)g.continueLesson();for(let i=0;i<90&&!g.lesson;i++){g.tick(1/30,0);r.draw(g);}test.updateUI();return {state:g.disturbance,lesson:g.lesson?.id,health:g.health,progress:g.progress};});Object.assign(approach,q);}
 await p.screenshot({path:`evidence/targeted/${name}-disturbance-card.png`});assert.equal(approach.lesson,'birds',JSON.stringify(approach));assert(approach.state.reaction>=1.4);
 const frozen=await p.evaluate(()=>{const{g,renderer:r}=test,before=JSON.stringify([g.clock,g.energy,g.disturbance]);g.tick(.25,1);r.draw(g);return before===JSON.stringify([g.clock,g.energy,g.disturbance]);});assert(frozen);
 await p.evaluate(()=>{test.g.continueLesson();test.renderer.draw(test.g);test.updateUI();});await p.screenshot({path:`evidence/targeted/${name}-disturbance-after.png`});
 await pose(3,122);await p.evaluate(()=>test.renderer.draw(test.g));await p.screenshot({path:`evidence/targeted/${name}-ponds.png`});
 await pose(4,154);await p.evaluate(()=>test.renderer.draw(test.g));await p.screenshot({path:`evidence/targeted/${name}-wetland.png`});
 const signs=await p.evaluate(()=>{const{g,renderer:r}=test;let count=0;const old=r.ctx.fillText;r.ctx.fillText=()=>count++;g.chapter=2;g.routes={};r.forks(g,'en',true);r.navigation(g);r.ctx.fillText=old;return count;});assert.equal(signs,0);
 // Turning away from the encounter must not unlock the topic.
 await pose(2,84);const hidden=await p.evaluate(()=>{const{g,renderer:r}=test;g.heading=Math.PI;for(let i=0;i<50;i++){g.clock+=.1;r.draw(g);}return {reaction:g.disturbance?.reaction,seen:g.observedTopics.has('birds')};});assert.equal(hidden.reaction,0);assert(!hidden.seen);
 assert.deepEqual(errors,[]);rows.push({name,approach,frozen,signs,hidden,errors});await p.close();console.log('PASS',name);
}await b.close();fs.writeFileSync('evidence/targeted/browser.json',JSON.stringify(rows,null,2));})().catch(e=>{console.error(e);process.exit(1)});
