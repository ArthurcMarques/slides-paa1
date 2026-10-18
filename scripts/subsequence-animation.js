const subsequenceCode=[
 'for (size_t gap = n / 2; gap > 0; gap /= 2) {',
 '  for (size_t r = 0; r < gap; ++r) {',
 '    for (size_t i = r + gap; i < n; i += gap) {',
 '      int tmp = v[i];',
 '      size_t j = i;',
 '      while (j >= gap && v[j-gap] > tmp) {',
 '        v[j] = v[j-gap];',
 '        j -= gap;',
 '      }',
 '      v[j] = tmp;',
 '    }',
 '  }',
 '}'
];
function subsequenceTrace(input){
 const a=[...input],steps=[];let gap=null,r=null,i=null,j=null,tmp=null;
 const emit=(line,message,read=[],write=[])=>steps.push({a:[...a],gap,r,i,j,tmp,line,message,read,write});
 emit(-1,'O mesmo vetor é mostrado inteiro e separado em grupos de posições.');
 for(gap=Math.floor(a.length/2);gap>0;gap=Math.floor(gap/2)){
  r=i=j=tmp=null;emit(0,`Gap ${gap}: separamos ${gap} subsequência${gap>1?'s':''}.`);
  for(r=0;r<gap;r++){
   i=j=tmp=null;emit(1,`Ordenamos o grupo que começa no índice ${r}, por inserção.`);
   for(i=r+gap;i<a.length;i+=gap){
    j=tmp=null;emit(2,`Próximo elemento do grupo: índice ${i}.`,[i]);
    tmp=a[i];emit(3,`Guardamos ${tmp} em tmp.`,[i]);
    j=i;emit(4,`j começa no índice ${j}.`,[j]);
    while(true){
     const move=j>=gap&&a[j-gap]>tmp;
     emit(5,j<gap?'Chegamos ao início da subsequência.':`${a[j-gap]} > ${tmp}? ${move?'Sim: deslocamos dentro do grupo.':'Não: podemos inserir tmp.'}`,j>=gap?[j-gap]:[]);
     if(!move)break;
     a[j]=a[j-gap];emit(6,`Deslocamos ${a[j-gap]} do índice ${j-gap} para ${j}.`,[j-gap],[j]);
     j-=gap;emit(7,`Voltamos ao índice ${j} do mesmo grupo.`,[j]);
    }
    a[j]=tmp;emit(9,`Inserimos ${tmp} no índice ${j}; o vetor e o grupo se atualizam juntos.`,[],[j]);
   }
   i=j=tmp=null;emit(10,`Grupo ${r} ordenado. Seus valores continuam nas posições originais do grupo.`);
  }
  r=null;emit(11,`Passagem com gap ${gap} concluída. Todos os grupos estão ordenados.`);
 }
 r=i=j=tmp=null;emit(-1,'Com gap 1 há um único grupo: o vetor inteiro ficou ordenado.');return steps;
}
const subsequenceSteps=subsequenceTrace([8,3,7,4,6,2,5,1]);
let subsequencePosition=0,subsequenceTimer=null;
function stopSubsequence(){if(subsequenceTimer!==null)clearInterval(subsequenceTimer);subsequenceTimer=null;const b=document.querySelector('#sub-play');if(b)b.textContent='Reproduzir'}
function showSubsequence(){
 const p=document.querySelector('[data-animation="subsequences"]');if(!p)return;
 const s=subsequenceSteps[subsequencePosition];
 p.querySelectorAll('.code-line').forEach((el,k)=>el.classList.toggle('active',k===s.line));
 p.querySelector('#sub-vars').textContent=`gap = ${s.gap??'—'} · grupo = ${s.r??'—'} · i = ${s.i??'—'} · j = ${s.j??'—'} · tmp = ${s.tmp??'—'}`;
 const gap=s.gap>0?s.gap:subsequencePosition===0?4:1;
 function cell(k){const el=document.createElement('div');el.className='sub-cell';el.style.borderBottomColor=['#008780','#6b75a4','#b76a24','#926881'][k%gap];
  if(s.read.includes(k))el.classList.add('reading');if(s.write.includes(k))el.classList.add('writing');
  const val=document.createElement('strong');val.textContent=s.a[k];const ix=document.createElement('small');ix.textContent=`[${k}]`;el.append(val,ix);return el}
 const array=p.querySelector('#sub-array');array.replaceChildren();s.a.forEach((_,k)=>array.append(cell(k)));
 const groups=p.querySelector('#sub-groups');groups.replaceChildren();
 for(let r=0;r<Math.min(gap,s.a.length);r++){
  const row=document.createElement('div');row.className='sub-group'+(r===s.r?' active-group':'');
  const label=document.createElement('span');label.textContent=`Grupo ${r}`;row.append(label);
  for(let k=r;k<s.a.length;k+=gap)row.append(cell(k));groups.append(row);
 }
 p.querySelector('#sub-message').textContent=s.message;
 p.querySelector('#sub-progress').textContent=`Passo ${subsequencePosition} / ${subsequenceSteps.length-1}`;
 p.querySelector('#sub-prev').disabled=subsequencePosition===0;p.querySelector('#sub-next').disabled=subsequencePosition===subsequenceSteps.length-1;
 if(subsequencePosition===subsequenceSteps.length-1)stopSubsequence();
}
function mountSubsequence(){
 const p=document.createElement('section');p.id='shell-animation';p.dataset.animation='subsequences';p.setAttribute('aria-label','Shell por subsequências');
 p.innerHTML=`<h1>Shell Sort: por subsequências</h1><p class="shell-sub">CADA GRUPO É ORDENADO POR INSERÇÃO · GAPS 4, 2 E 1</p><div class="shell-layout"><div><div id="sub-vars"></div><p class="sub-label">Vetor completo</p><div id="sub-array"></div><p class="sub-label">Subsequências: valor e índice no vetor</p><div id="sub-groups"></div><p class="sub-key">Mesma borda = mesmo grupo · Azul: leitura · Verde: escrita</p><div id="sub-message" aria-live="polite"></div></div><div class="shell-code"></div></div><div class="shell-controls"><button id="sub-reset">Reiniciar</button><button id="sub-prev">Passo anterior</button><button id="sub-play">Reproduzir</button><button id="sub-next">Próximo passo</button><label>Velocidade <select id="sub-speed"><option value="1200">Lenta</option><option value="700" selected>Normal</option><option value="250">Rápida</option></select></label><span id="sub-progress"></span></div><div class="shell-jumps">Ir para a passagem: <button data-sub-gap="4">Gap 4</button><button data-sub-gap="2">Gap 2</button><button data-sub-gap="1">Gap 1</button></div>`;
 subsequenceCode.forEach((line,k)=>{const el=document.createElement('div');el.className='code-line';const num=document.createElement('span');num.textContent=String(k+1).padStart(2,'0');const code=document.createElement('code');code.textContent=line;el.append(num,code);p.querySelector('.shell-code').append(el)});
 document.querySelector('#slide').append(p);
 p.querySelector('#sub-reset').onclick=()=>{stopSubsequence();subsequencePosition=0;showSubsequence()};
 p.querySelector('#sub-prev').onclick=()=>{stopSubsequence();subsequencePosition=Math.max(0,subsequencePosition-1);showSubsequence()};
 p.querySelector('#sub-next').onclick=()=>{stopSubsequence();subsequencePosition=Math.min(subsequenceSteps.length-1,subsequencePosition+1);showSubsequence()};
 const play=()=>{if(subsequenceTimer){stopSubsequence();return}if(subsequencePosition===subsequenceSteps.length-1)subsequencePosition=0;p.querySelector('#sub-play').textContent='Pausar';subsequenceTimer=setInterval(()=>{subsequencePosition++;showSubsequence()},Number(p.querySelector('#sub-speed').value))};
 p.querySelector('#sub-play').onclick=play;p.querySelector('#sub-speed').onchange=()=>{if(subsequenceTimer){stopSubsequence();play()}};
 p.querySelectorAll('[data-sub-gap]').forEach(b=>b.onclick=()=>{stopSubsequence();subsequencePosition=subsequenceSteps.findIndex(s=>s.line===0&&s.gap===Number(b.dataset.subGap));showSubsequence()});showSubsequence();
}
