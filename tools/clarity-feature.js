const AREA_IMAGES={"glass": "assets/area-previews/glass.webp", "light": "assets/area-previews/light.webp", "green": "assets/area-previews/green.webp", "pond": "assets/area-previews/pond.webp", "wetland": "assets/area-previews/wetland.webp"};
const AREA_PREVIEWS=[
 {topic:'glass',title:['即將進入玻璃建築區','Entering the Glass Building District'],text:['部分建築倒映天空與樹木，讓鳥類難以辨認玻璃。','Some buildings reflect the sky and trees, making it difficult for birds to recognize the glass.'],hint:['仔細觀察建築表面。','Look carefully at the building surfaces.']},
 {topic:'light',title:['即將進入夜間城市','Entering the Night-time City'],text:['建築物的人工照明可能影響遷徙鳥類的夜間環境。','Artificial lights from buildings can affect the night-time environment for migratory birds.'],hint:['找出明亮的建築，以及減少照明的區域。','Look for brightly illuminated buildings and areas with reduced lighting.']},
 {topic:'green',title:['即將進入生態綠地','Entering the Ecological Green Space'],text:['合適的綠地能讓鳥類停歇和尋找食物。','Suitable green spaces can provide birds with places to rest and find food.'],hint:['留意樹木、植被、水域與合適的停歇處。','Look for trees, vegetation, water, and suitable resting places.']},
 {topic:'pond',title:['即將進入魚塘與村落','Entering the Fishpond and Village Area'],text:['魚塘與合適的鄉郊棲地能為水鳥提供覓食和停歇環境。','Fishponds and suitable rural habitats can provide important feeding and resting environments for waterbirds.'],hint:['找找魚塘、水面、村屋，以及水邊的鳥。','Look for fishponds, water surfaces, village houses, and birds near the water.']},
 {topic:'wetland',title:['即將抵達米埔內后海灣濕地','Approaching Mai Po Inner Deep Bay Wetlands'],text:['這片濕地為許多遷徙和留居水鳥提供重要棲地。','These wetlands provide important habitats for many migratory and resident waterbirds.'],hint:['觀察水域、泥灘、濕地植物與鳥類棲地。','Look for wetland water, mudflats, vegetation, and bird habitats.']}
];
const LEARNING_BANK=[
 ['glass-1','glass',['為甚麼反光玻璃可能危險？','Why can shiny glass be risky for birds?'],[['倒影看起來像天空或樹木','Reflections can look like sky or trees'],['玻璃總是很熱','Glass is always hot'],['鳥類只在室內飛行','Birds only fly indoors']],['倒影可能讓鳥類把玻璃誤認為可飛入的空間。','Reflections may make glass look like open space.']],
 ['glass-2','glass',['甚麼能幫助鳥類辨認玻璃？','What can help birds see glass?'],[['清楚、密集、重複的外部標記','Clear, closely spaced outside patterns'],['更多天空倒影','More sky reflections'],['清除所有標記','Removing every mark']],['合適的圖案能降低碰撞風險，但不保證完全安全。','Suitable patterns can lower risk, but cannot make all collisions impossible.']],
 ['light-1','light',['夜間可怎樣幫助部分遷徙鳥類？','What can help some birds at night?'],[['關閉不必要的燈光','Turn off lights that are not needed'],['讓每扇窗都更亮','Make every window brighter'],['把光束照向天空','Shine beams into the sky']],['減少不必要照明，能減少對部分鳥類的干擾。','Less unnecessary light can reduce disturbance for some birds.']],
 ['light-2','light',['人工照明對所有鳥類的影響都一樣嗎？','Do lights affect all birds in the same way?'],[['不一樣，影響因鳥類與情況而異','No. Effects vary between birds and situations'],['是，所有鳥都完全一樣','Yes. Every bird is exactly the same'],['燈光只影響魚類','Lights only affect fish']],['不同鳥類和環境條件，可能帶來不同影響。','Different birds and conditions can lead to different effects.']],
 ['green-1','green',['甚麼讓停歇處更合適？','What makes a good resting place?'],[['食物、水、遮蔽與較少干擾','Food, water, shelter and little disturbance'],['只有綠色油漆','Only green paint'],['繁忙的停車場','A busy car park']],['棲地品質取決於資源、植被、遮蔽和干擾程度。','Habitat quality depends on resources, plants, shelter and disturbance.']],
 ['green-2','green',['每一片綠地都適合鳥類嗎？','Is every green space good for birds?'],[['不一定，要看棲地條件','Not always. Habitat conditions matter'],['只要是綠色就一定適合','Yes, if it looks green'],['沒有綠地能幫助鳥類','No green space can help birds']],['合適的綠地能提供資源；外表綠色並不代表適合停歇。','Suitable green spaces offer resources. Green colour alone is not enough.']],
 ['pond-1','pond',['魚塘可以怎樣幫助水鳥？','How can fishponds help waterbirds?'],[['合適條件下提供覓食與停歇處','Offer feeding and resting places when conditions are suitable'],['每個魚塘都讓所有鳥類安全','Every pond keeps every bird safe'],['取代所有濕地','Replace all wetlands']],['合適的魚塘和鄉郊棲地可供水鳥覓食和停歇。','Suitable ponds and rural habitats can support feeding and resting.']],
 ['pond-2','pond',['觀察魚塘棲地時應留意甚麼？','What should we check in a pond habitat?'],[['食物、水況、岸邊植被與干擾','Food, water, bank plants and disturbance'],['只有魚塘的名字','Only the name of the pond'],['附近有多少廣告牌','How many adverts are nearby']],['並非所有魚塘都同樣合適，生態條件很重要。','Not every pond is equally suitable. Ecological conditions matter.']],
 ['wetland-1','wetland',['為甚麼要保護米埔濕地？','Why protect the Mai Po wetlands?'],[['它們支持遷徙和留居水鳥','They support migratory and resident waterbirds'],['它們只是一塊空地','They are just empty land'],['所有鳥類都住在高樓','All birds live in towers']],['水域、泥灘與植被共同構成重要的濕地棲地。','Water, mudflats and plants form important wetland habitats.']],
 ['wetland-2','wetland',['觀察濕地鳥類時怎樣做較好？','How can we watch wetland birds carefully?'],[['保持距離，減少干擾','Keep a distance and reduce disturbance'],['追逐牠們拍照','Chase them for photos'],['隨意走進棲息區','Walk anywhere in their resting areas']],['保持適當距離，有助減少對覓食和停歇鳥類的干擾。','Keeping a suitable distance reduces disturbance to feeding and resting birds.']]
];
function storageGet(key){try{return localStorage.getItem(key)}catch{return null}}
function storageSet(key,value){try{localStorage.setItem(key,value)}catch{}}
function pickLearningQuestions(previous=[],random=Math.random){
 const shuffle=a=>{a=[...a];for(let i=a.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a};
 const available=shuffle(LEARNING_BANK.filter(q=>!previous.includes(q[0]))),first=available[0],second=available.find(q=>q[1]!==first[1]);
 return [first,second].map(q=>({id:q[0],topic:q[1],question:q[2],answers:q[3],explain:q[4],order:shuffle([0,1,2])}));
}
function startPractice(){g.tutorial={left:false,right:false};g.heading=0;g.x=0;clearInput();clarityKey='';updateUI()}
function endPractice(){storageSet('urban-wings-tutorial','done');g.tutorial=null;g.heading=0;g.turnVelocity=0;g.x=0;clearInput();clarityKey='';updateUI()}
const clarityLayer=document.createElement('section');clarityLayer.id='clarityOverlay';clarityLayer.hidden=true;document.getElementById('game').append(clarityLayer);
const resourceLayer=document.createElement('aside');resourceLayer.id='resourceMeaning';resourceLayer.setAttribute('role','status');resourceLayer.hidden=true;document.getElementById('game').append(resourceLayer);
let clarityKey='';
function renderClarity(){
 const hint=g.resourceHint;resourceLayer.hidden=!hint||g.clock>hint.until||g.interaction!=='flight'||!!g.tutorial;
 if(hint)resourceLayer.textContent=hint.kind==='health'?tr('♥ 健康代表鳥的安全。碰撞會受傷；觀察通道，轉向避開建築。','♥ Health means safety. Collisions cause injury. Observe the gaps and steer clear.'):tr('⚡ 體力是飛行力量，每完成一段飛行消耗 5。只有指定合適停歇點能恢復。','⚡ Energy is flying strength. Each completed flight segment costs 5. Only designated suitable resting points restore it.');
 if(g.done&&g.summaryReady&&!g.learningDone&&!g.learning){let last=[];try{last=JSON.parse(storageGet('urban-wings-last-questions')||'[]')}catch{}g.learning={questions:pickLearningQuestions(last),index:0,correct:false,feedback:''};storageSet('urban-wings-last-questions',JSON.stringify(g.learning.questions.map(q=>q.id)));}
 const type=g.paused?'':g.tutorial?'tutorial':g.areaPreview!==null?'preview':g.done&&g.summaryReady&&!g.learningDone?'quiz':'';
 clarityLayer.hidden=!type;if(!type){clarityKey='';return;}
 clarityLayer.className=type==='tutorial'?'practice':'modal';
 const i=lang==='zh'?0:1,key=JSON.stringify([type,lang,g.areaPreview,g.tutorial,g.learning]);if(key===clarityKey)return;clarityKey=key;
 if(type==='tutorial'){
  const ready=g.tutorial.left&&g.tutorial.right;
  clarityLayer.innerHTML=`<div class="clarity-dialog practice-dialog" role="dialog" aria-labelledby="practiceTitle"><h2 id="practiceTitle">${tr('先練習一下','Try your wings')}</h2><p>${tr('你是一隻遷徙候鳥。在安全的海岸上，按住左右箭頭轉向；鬆開後保持方向。','You are a migratory bird. Practise over the safe coast: hold left or right to turn. Release to keep your heading.')}</p><p class="practice-progress">${g.tutorial.left?'✓':'←'} ${tr('向左轉','Turn left')}　${g.tutorial.right?'✓':'→'} ${tr('向右轉','Turn right')}</p><p>♥ ${tr('健康＝鳥的安全','Health = bird safety')}<br>⚡ ${tr('體力＝飛行力量','Energy = flying strength')}</p><p>${tr('觀察前方環境，飛入你選擇的通道。現在沒有危險障礙，也不消耗體力。','Observe the environment and fly into your chosen passage. This practice has no dangerous obstacles or Energy cost.')}</p><button id="finishPractice" class="primary" ${ready?'':'disabled'}>${tr('開始旅程','Begin the journey')}</button> <button id="skipPractice">${tr('略過練習','Skip practice')}</button></div>`;
  $('finishPractice').onclick=endPractice;$('skipPractice').onclick=endPractice;
 }else if(type==='preview'){
  const area=AREA_PREVIEWS[g.areaPreview];clearInput();
  clarityLayer.innerHTML=`<div class="clarity-dialog" role="dialog" aria-modal="true" aria-labelledby="areaPreviewTitle"><span class="eyebrow">${tr('前方環境','UP NEXT')}</span><h1 id="areaPreviewTitle">${area.title[i]}</h1><img class="area-image" src="${AREA_IMAGES[area.topic]}" alt="${area.title[i]}"><p>${area.text[i]}</p><p class="observation-hint">${tr('觀察提示：','Look for: ')}${area.hint[i]}</p><button id="continueArea" class="primary">${tr('繼續飛行','Continue flying')} →</button></div>`;
  $('continueArea').onclick=()=>{g.areaPreview=null;clearInput();clarityKey='';updateUI()};$('continueArea').focus({preventScroll:true});
 }else{
  const check=g.learning,q=check.questions[check.index],image=EDUCATION_CONTENT[q.topic].image;
  clarityLayer.innerHTML=`<div class="clarity-dialog learning-dialog" role="dialog" aria-modal="true" aria-labelledby="learningTitle"><span class="eyebrow">${tr('第','Question ')} ${check.index+1} ${tr('題，共 2 題','of 2')}</span><h1 id="learningTitle">${tr('學習小挑戰','Learning Check')}</h1><img class="learning-image" src="${image}" alt="${EDUCATION_CONTENT[q.topic].title[i]}"><h2>${q.question[i]}</h2><div class="learning-answers">${q.order.map((answer,n)=>`<button data-answer="${answer}" ${check.correct?'disabled':''}>${String.fromCharCode(65+n)}. ${q.answers[answer][i]}</button>`).join('')}</div><p class="learning-feedback" role="status">${check.feedback?tr(check.feedback==='right'?'答對了！':'再試一次。',check.feedback==='right'?'That’s right!':'Try again.')+' '+q.explain[i]:tr('沒有計時，也不會扣健康或體力。','No timer. Answers never cost Health or Energy.')}</p><button id="nextLearning" class="primary" ${check.correct?'':'disabled'}>${check.index===0?tr('下一題','Next question'):tr('查看原有旅程總結','Continue to your journey summary')}</button></div>`;
  for(const button of clarityLayer.querySelectorAll('[data-answer]'))button.onclick=()=>{check.correct=Number(button.dataset.answer)===0;check.feedback=check.correct?'right':'wrong';clarityKey='';updateUI()};
  $('nextLearning').onclick=()=>{if(!check.correct)return;if(check.index===0){check.index=1;check.correct=false;check.feedback='';}else g.learningDone=true;clarityKey='';updateUI();};
 }
 const languageButton=document.createElement('button');languageButton.className='clarity-language';languageButton.textContent=lang==='zh'?'English':'中文';languageButton.onclick=()=>{ $('language').click();clarityKey='';updateUI();};clarityLayer.querySelector('.clarity-dialog').append(languageButton);
}
