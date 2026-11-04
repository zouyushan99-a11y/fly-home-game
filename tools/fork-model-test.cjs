const fs=require('fs'),vm=require('vm'),assert=require('assert');
function model(html){const c={};vm.createContext(c);vm.runInContext(html.split('<script>(()=>{')[1].split('const palettes=')[0]+';this.Journey=Journey;this.cameraZ=cameraZ;this.pathX=pathX;this.hitsBuilding=hitsBuilding;this.makeDistrict=makeDistrict;this.extraTrees=typeof EXTRA_TREES==="undefined"?[]:EXTRA_TREES;',c);return c;}
const report={routes:[],checks:[]};
for(const [version,html] of [['before',require('child_process').execFileSync('git',['show','66d1ba8:index.html'],{encoding:'utf8'})],['after',fs.readFileSync('index.html','utf8')]]){
 const m=model(html);for(const route of ['A','B','C']){const g=new m.Journey();g.started=true;let steps=0,distance=0,rests=[];
 while(!g.done&&steps++<30000){if(g.lesson){g.lesson=null;g.entryPending=false;}if(version==='before'&&g.waitingRoute)g.choose(route);
 const gate=g.buildings().filter(b=>b.gate!==undefined&&b.z+b.depth>m.cameraZ(g.progress)-3).sort((a,b)=>a.z-b.z)[0];
 const target=version==='after'&&g.waitingRoute?({A:-15/23,B:0,C:15/23}[route]):gate?gate.opening/23:0;
 const steer=Math.max(-1,Math.min(1,(target-g.x)*6-g.driftVelocity()/(version==='after'?.78:.62)));
 const z=m.cameraZ(g.progress),x=g.pathAt?g.pathAt(z):m.pathX(z),oldEnergy=g.energy;g.tick(1/60,steer);
 const zz=m.cameraZ(g.progress);distance+=Math.hypot(zz-z,(g.pathAt?g.pathAt(zz):m.pathX(zz))-x);
 if(g.energy>oldEnergy)rests.push({progress:g.progress,energy:g.energy});
 if(g.recovery==='health')throw Error(`${version} ${route} health recovery at ${g.progress}`);
 }
 const r={version,route,success:g.success,health:g.health,energy:g.energy,seconds:g.time,flightDistance:distance,ledger:g.energyLedger,emergency:g.emergencyUsed,routes:g.routes,rests};report.routes.push(r);assert(g.success&&!g.emergencyUsed,JSON.stringify(r));if(version==='after')assert(Object.values(g.routes).every(x=>x===route));
 }
}
const m=model(fs.readFileSync('index.html','utf8'));
report.addedTrees=[0,1,2,3,4].map(stage=>({stage,count:m.extraTrees.filter(t=>t.stage===stage).length}));assert(m.extraTrees.every(t=>t.height<33));
for(const state of ['lesson','paused']){const g=new m.Journey();g.started=true;g.chapter=0;g.progress=12;g.interference={duration:3,remaining:3,elapsed:0};if(state==='lesson')g.lesson={id:'city'};else g.paused=true;const snapshot=()=>JSON.stringify([g.progress,g.x,g.energy,g.health,g.clock,g.interference]);const a=snapshot();for(let i=0;i<100;i++)g.tick(.1,1);assert.equal(snapshot(),a);report.checks.push(state+' freezes simulation');}
for(const x of [-1,-.327,-7.5/23,0,7.5/23,.327,1]){const g=new m.Journey();g.started=true;g.chapter=0;g.progress=16.999;g.x=x;g.tick(.01);const expected=x<-7.5/23?'A':x>7.5/23?'C':'B';assert.equal(g.routes[0],expected);const ledger=g.energyLedger.detour;g.choose('C');assert.equal(g.routes[0],expected);assert.equal(g.energyLedger.detour,ledger);}
report.checks.push('boundary and missed-centre sectors are total, deterministic and single-shot');
for(const success of [true,false]){const g=new m.Journey();g.started=true;g.finish(success);const snap=()=>JSON.stringify([g.energy,g.health,g.progress,[...g.events]]),a=snap();for(let i=0;i<100;i++){g.tick(.05,1);g.collide('late');g.event('late',-10,-10)}assert.equal(a,snap());assert(g.summaryReady);g.reset();assert(!g.done&&!g.outro&&Object.keys(g.routes).length===0);}
report.checks.push('success/failure freeze, single summary and restart');
// Equal offset samples around the intended opening, not a scientific collision probability.
report.collisionSamples={};
for(const route of ['A','B']){const buildings=m.makeDistrict(0,route),gate=buildings.find(b=>b.gate===0);let hits=0;for(let offset=-12;offset<=12;offset+=.5){const x=m.pathX(gate.z)+gate.opening+offset;if(buildings.filter(b=>b.gate===0).some(b=>m.hitsBuilding(b,{x,z:gate.z-2},{x,z:gate.z+11})))hits++;}report.collisionSamples[route]=hits;}
assert(report.collisionSamples.A>report.collisionSamples.B&&report.collisionSamples.B>0);
// Change direction before the decision line; the final crossing, not the first lean, wins.
{const g=new m.Journey();g.started=true;g.chapter=0;g.progress=10;for(let i=0;i<50;i++)g.tick(1/60,-1);for(let i=0;i<100;i++)g.tick(1/60,1);while(g.waitingRoute)g.tick(1/60);assert.equal(g.routes[0],'C');const before=g.energy;g.rest(0);const once=g.energy;g.rest(0);assert.equal(g.energy,once);assert(once>=before);}
report.checks.push('late direction change selects final entry; rest cannot be farmed; A has more equal-offset collision samples than B, B is not risk-free');
fs.writeFileSync('evidence/forks/model.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
