const image=document.querySelector('#image'), links=document.querySelector('#links'), select=document.querySelector('#select');
let current=1;
slides.forEach((s,i)=>select.add(new Option(`${i+1}. ${s.title}`,i+1)));
function go(n){
 current=Math.max(1,Math.min(slides.length,Number(n)||1));
 const s=slides[current-1];
 image.src=`slides/Slide${current}.PNG`;image.alt=s.title;
 links.replaceChildren();
 s.links.forEach(l=>{const b=document.createElement('button');b.className='hotspot';b.style.cssText=`left:${l.x}%;top:${l.y}%;width:${l.w}%;height:${l.h}%`;b.setAttribute('aria-label',l.label);b.title=l.label;b.onclick=()=>go(l.target);links.append(b)});
 select.value=current;document.querySelector('#count').textContent=`${current} / ${slides.length}`;
 document.querySelector('#prev').disabled=current===1;document.querySelector('#next').disabled=current===slides.length;
 document.querySelector('#text').textContent=s.text;document.title=`${s.title} — Selection Sort`;
 history.replaceState(null,'',`#slide-${current}`);
 if(current<slides.length){const preload=new Image();preload.src=`slides/Slide${current+1}.PNG`}
}
document.querySelector('#prev').onclick=()=>go(current-1);document.querySelector('#next').onclick=()=>go(current+1);select.onchange=()=>go(select.value);
async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch{}}
document.querySelector('#full').onclick=fullscreen;
document.addEventListener('keydown',e=>{if(['SELECT','BUTTON','INPUT'].includes(document.activeElement.tagName))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();go(current+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();go(current-1)}if(e.key==='Home')go(1);if(e.key==='End')go(slides.length);if(e.key.toLowerCase()==='f')fullscreen()});
let startX;image.addEventListener('touchstart',e=>startX=e.changedTouches[0].clientX,{passive:true});image.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-startX;if(Math.abs(d)>60)go(current+(d<0?1:-1))},{passive:true});
window.addEventListener('hashchange',()=>go(location.hash.split('-')[1]));go(location.hash.split('-')[1]);
