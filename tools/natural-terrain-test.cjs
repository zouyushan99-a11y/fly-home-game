const fs=require('fs'),assert=require('assert'),{chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});const report=[];
for(const [device,width,height] of [['desktop',1280,720],['portrait',390,844],['landscape',844,390]]){
const page=await b.newPage({viewport:{width,height}});await page.route('**/terrain-test',r=>r.fulfill({contentType:'text/html',body:fs.readFileSync('index.html','utf8').replace('labels();requestAnimationFrame(frame);','window.test={g,renderer,roadWorld,palettes,updateUI};labels();')}));await page.goto('http://127.0.0.1:8080/terrain-test');await page.evaluate(()=>test.renderer.draw(test.g));await page.waitForFunction(()=>test.renderer.groundImages&&Object.values(test.renderer.groundImages).every(im=>im.complete&&im.naturalWidth));
const result=await page.evaluate(()=>{const r=test.renderer,g=test.g,m=r.terrainMap(),c=r.ctx,world=test.roadWorld();let calls=0,bad=0,maxUVError=0;
 const original=c.drawImage;const marker=world.junctions[2];for(const delta of [-.15,0,.15]){
  r.cz=marker[1]-100+delta;r.cx=marker[0]+delta;r.eye=34;r.nightMix=0;g.chapter=0;g.progress=r.cz/9+10;
  const screen=r.project([marker[0],0,marker[1]]);let markerRow=false;
  c.drawImage=function(image,...args){if(image===m.day||image===m.night){calls++;const [sx,sy,sw,sh,dx,y,dw,dh]=args;if(args.length!==8||!args.every(Number.isFinite)||sx<-.001||sy<-.001||sx+sw>image.width+.001||sy+sh>image.height+.001||sw<=0||sh<=0||y<r.horizon||dh>1.02)bad++;
   if(y<=screen[1]&&screen[1]<y+1){markerRow=true;const u=sx+(screen[0]-dx)/dw*sw,expected=(r.cx+(screen[0]-r.w/2)*r.eye/(y+.5-r.horizon)-m.minX)*m.scale;maxUVError=Math.max(maxUVError,Math.abs(u-expected));const expectedV=(marker[1]-m.minZ)*m.scale;if(expectedV<sy-.001||expectedV>sy+sh+.001)bad++;}
  }return original.call(this,image,...args)};
  c.setTransform(r.dpr,0,0,r.dpr,0,0);c.fillStyle='#112233';c.fillRect(0,0,r.w,r.h);r.streets(g,test.palettes[0]);if(!markerRow)bad++;
  const row=c.getImageData(0,Math.floor((r.horizon-5)*r.dpr),r.canvas.width,1).data;for(let i=0;i<row.length;i+=4)if(row[i]!==17||row[i+1]!==34||row[i+2]!==51)bad++;
 }
 c.drawImage=original;const edge=m.day.getContext('2d').getImageData(0,0,m.day.width,1).data;let maxEdgeAlpha=0;for(let i=3;i<edge.length;i+=4)maxEdgeAlpha=Math.max(maxEdgeAlpha,edge[i]);return {calls,bad,maxUVError,maxEdgeAlpha,mapSize:[m.day.width,m.day.height],accessPaths:m.accesses.length};});assert.equal(result.bad,0,JSON.stringify(result));assert(result.maxUVError<.000001);assert(result.maxEdgeAlpha<3);report.push({device,...result});console.log(device,result);
for(const [i,offset] of [-12,0,12].entries()){await page.evaluate(offset=>{const {g,renderer:r,updateUI}=test,j=test.roadWorld().junctions[2];g.started=true;g.chapter=0;g.routes={0:'B'};g.routeSelectedAt={0:0};g.clock=30;g.progress=(j[1]-100+offset)/9+10;g.x=Math.max(-1,Math.min(1,(j[0]-g.pathAt((g.progress-10)*9))/23));updateUI();r.draw(g);},offset);await page.screenshot({path:`evidence/natural/${device}-road-turn-${i}.png`});}
await page.close();}
await b.close();fs.writeFileSync('evidence/natural/terrain.json',JSON.stringify(report,null,2));})().catch(e=>{console.error(e);process.exit(1)});
