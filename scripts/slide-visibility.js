const visibilityStorageKey='paa1-hidden-slides-v1';
let hiddenSlides=new Set();
try{const saved=JSON.parse(localStorage.getItem(visibilityStorageKey)||'[]');if(Array.isArray(saved))hiddenSlides=new Set(saved.filter(x=>typeof x==='string'))}catch{}
function slideKey(slide){return `${slide.part}::${slide.title}`}
function isSlideHidden(slide){return hiddenSlides.has(slideKey(slide))}
function findVisibleSlide(deck,start,direction,hidden=hiddenSlides){
 for(let index=start;index>=1&&index<=deck.length;index+=direction){if(!hidden.has(slideKey(deck[index-1])))return index}
 return null;
}
function persistVisibility(){try{localStorage.setItem(visibilityStorageKey,JSON.stringify([...hiddenSlides]))}catch{}}
function ensureVisibleSlide(){if(slides.length&&slides.every(isSlideHidden)){hiddenSlides.delete(slideKey(slides[0]));persistVisibility()}}
function moveSlide(direction){const next=findVisibleSlide(slides,current+direction,direction);if(next!==null)go(next)}
function setSlideVisible(index,visible){
 const slide=slides[index-1];if(!slide)return;
 if(!visible&&slides.filter(s=>!isSlideHidden(s)).length<=1)return;
 if(visible)hiddenSlides.delete(slideKey(slide));else hiddenSlides.add(slideKey(slide));
 persistVisibility();fillOptions();go(current);renderSlideManager(index);
}
function renderSlideManager(focusIndex){
 const list=document.querySelector('#visibility-list');list.replaceChildren();
 const count=slides.filter(s=>!isSlideHidden(s)).length;
 document.querySelector('#visibility-summary').textContent=`${count} de ${slides.length} slides visíveis nesta parte. Marque para exibir; desmarque para pular.`;
 slides.forEach((slide,i)=>{const row=document.createElement('label');row.className='visibility-row';const checkbox=document.createElement('input');checkbox.type='checkbox';checkbox.checked=!isSlideHidden(slide);checkbox.dataset.slide=i+1;checkbox.disabled=count===1&&checkbox.checked;
 checkbox.onchange=()=>setSlideVisible(i+1,checkbox.checked);const label=document.createElement('span');label.textContent=`${i+1}. ${slide.title}`;row.append(checkbox,label);list.append(row)});
 if(focusIndex)list.querySelector(`[data-slide="${focusIndex}"]`)?.focus();
}
function openSlideManager(){stopShell();stopSelection();stopSubsequence();renderSlideManager();document.querySelector('#visibility-dialog').showModal()}
function setupSlideManager(){
 document.querySelector('#manage-slides').onclick=openSlideManager;
 document.querySelector('#visibility-close').onclick=()=>document.querySelector('#visibility-dialog').close();
 document.querySelector('#visibility-all').onclick=()=>{slides.forEach(s=>hiddenSlides.delete(slideKey(s)));persistVisibility();fillOptions();go(current);renderSlideManager()};
 document.querySelector('#visibility-hide-current').onclick=()=>setSlideVisible(current,false);
}
