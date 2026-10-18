const selectionCode=[
 'for (size_t i = 0; i + 1 < n; ++i) {',
 '  size_t menor = i;',
 '  for (size_t j = i + 1; j < n; ++j) {',
 '    if (v[j] < v[menor]) {',
 '      menor = j;',
 '    }',
 '  }',
 '  if (menor != i) {',
 '    int tmp = v[i];',
 '    v[i] = v[menor];',
 '    v[menor] = tmp;',
 '  }',
 '}'
];
function selectionTrace(input){
 const a=[...input],steps=[];let i=null,j=null,menor=null,tmp=null,done=0,comparisons=0,writes=0;
 const emit=(line,message,read=[],write=[])=>steps.push({a:[...a],i,j,menor,tmp,done,comparisons,writes,line,message,read,write});
 emit(-1,'Vetor inicial. Em cada rodada, buscamos o menor da parte restante.');
 for(i=0;i+1<a.length;i++){
  j=menor=tmp=null;emit(0,`Rodada ${i+1}: vamos definir a posição ${i}.`);
  menor=i;emit(1,`O candidato inicial é v[${menor}] = ${a[menor]}.`,[menor]);
  for(j=i+1;j<a.length;j++){
   emit(2,`j = ${j}: vamos comparar com o menor encontrado.`,[j,menor]);
   comparisons++;const smaller=a[j]<a[menor];
   emit(3,`${a[j]} < ${a[menor]}? ${smaller?'Sim: encontramos um novo menor.':'Não: mantemos o candidato.'}`,[j,menor]);
   if(smaller){menor=j;emit(4,`menor passa a ser o índice ${menor}, com valor ${a[menor]}.`,[menor])}
  }
  j=null;emit(7,menor!==i?`Menor no índice ${menor}. Vamos trocar com a posição ${i}.`:'O menor já está na posição correta. Nenhuma troca é necessária.',[i,menor]);
  if(menor!==i){
   tmp=a[i];emit(8,`Guardamos v[${i}] = ${tmp} em tmp.`,[i]);
   a[i]=a[menor];writes++;emit(9,`Copiamos o menor (${a[menor]}) para v[${i}].`,[menor],[i]);
   a[menor]=tmp;writes++;emit(10,`Gravamos tmp = ${tmp} em v[${menor}]. A troca fez duas escritas.`,[],[menor]);
  }
  done=i+1;emit(11,`Posição ${i} definida. A busca seguinte começa após ela.`);
 }
 i=j=menor=tmp=null;done=a.length;emit(-1,'Vetor ordenado. O último elemento também está na posição correta.');return steps;
}
const selectionSteps=selectionTrace([8,3,7,4,6,2,5,1]);
let selectionPosition=0,selectionTimer=null;
function stopSelection(){if(selectionTimer!==null)clearInterval(selectionTimer);selectionTimer=null;const button=document.querySelector('#selection-play');if(button)button.textContent='Reproduzir'}
function showSelection(){
 const panel=document.querySelector('[data-animation="selection"]');if(!panel)return;
 const s=selectionSteps[selectionPosition];
 panel.querySelectorAll('.code-line').forEach((line,k)=>line.classList.toggle('active',k===s.line));
 panel.querySelector('#selection-vars').textContent=`i = ${s.i??'—'}    j = ${s.j??'—'}    menor = ${s.menor??'—'}    tmp = ${s.tmp??'—'}`;
 const cells=panel.querySelector('.shell-cells');cells.replaceChildren();
 s.a.forEach((value,k)=>{const cell=document.createElement('div');cell.className='shell-cell';
  if(k<s.done)cell.classList.add('selection-sorted');
  if(k===s.menor)cell.classList.add('selection-min');
  if(s.read.includes(k))cell.classList.add('reading');if(s.write.includes(k))cell.classList.add('writing');
  const v=document.createElement('strong');v.textContent=value;const label=document.createElement('small');label.textContent=`[${k}]`;cell.append(v,label);cells.append(cell);
 });
 const indices=panel.querySelector('#selection-indices');indices.replaceChildren();
 s.a.forEach((_,k)=>{const chip=document.createElement('span');chip.textContent=k;chip.className=k===s.i?'insert-index':s.i!==null&&k>s.i?'previous-index':'';
  if(k===s.j)chip.classList.add('comparing-index');indices.append(chip)});
 const order=s.i===null?[]:Array.from({length:s.a.length-s.i-1},(_,k)=>s.i+k+1);
 panel.querySelector('#selection-order').textContent=order.length?order.join(' → '):'—';
 panel.querySelector('#selection-message').textContent=s.message;
 panel.querySelector('#selection-counts').textContent=`Comparações: ${s.comparisons} · Escritas no vetor: ${s.writes}`;
 panel.querySelector('#selection-progress').textContent=`Passo ${selectionPosition} / ${selectionSteps.length-1}`;
 panel.querySelector('#selection-prev').disabled=selectionPosition===0;panel.querySelector('#selection-next').disabled=selectionPosition===selectionSteps.length-1;
 if(selectionPosition===selectionSteps.length-1)stopSelection();
}
function mountSelection(){
 const panel=document.createElement('section');panel.id='shell-animation';panel.dataset.animation='selection';panel.setAttribute('aria-label','Execução animada do Selection Sort');
 panel.innerHTML=`<h1>Selection Sort: execução passo a passo</h1><p class="shell-sub">BUSCAR O MENOR · TROCAR · AVANÇAR A PARTE ORDENADA</p><div class="shell-layout"><div><div id="selection-vars"></div><div class="shell-cells"></div><p class="shell-key">Verde claro: posição definida · Dourado: menor · Azul: leitura · Verde: escrita</p><div class="shell-positions"><div id="selection-indices"></div><p class="position-key">Azul: posição i · Dourado: parte restante · Contorno: índice j</p><p class="position-order">Ordem da busca nesta rodada: <strong id="selection-order"></strong></p></div><div id="selection-message" aria-live="polite"></div><p id="selection-counts"></p></div><div class="shell-code"></div></div><div class="shell-controls"><button id="selection-reset">Reiniciar</button><button id="selection-prev">Passo anterior</button><button id="selection-play">Reproduzir</button><button id="selection-next">Próximo passo</button><label>Velocidade <select id="selection-speed"><option value="1200">Lenta</option><option value="700" selected>Normal</option><option value="250">Rápida</option></select></label><span id="selection-progress"></span></div><div class="shell-jumps">Ir para a rodada: <button data-round="0">1ª</button><button data-round="1">2ª</button><button data-round="2">3ª</button><button data-round="3">4ª</button></div>`;
 const jumps=panel.querySelector('.shell-jumps');jumps.textContent='Ir para a rodada: ';
 for(let round=0;round<selectionSteps[0].a.length-1;round++){const button=document.createElement('button');button.dataset.round=round;button.textContent=`${round+1}ª`;jumps.append(button)}
 const code=panel.querySelector('.shell-code');selectionCode.forEach((line,k)=>{const row=document.createElement('div');row.className='code-line';const number=document.createElement('span');number.textContent=String(k+1).padStart(2,'0');const source=document.createElement('code');source.textContent=line;row.append(number,source);code.append(row)});
 document.querySelector('#slide').append(panel);
 panel.querySelector('#selection-reset').onclick=()=>{stopSelection();selectionPosition=0;showSelection()};
 panel.querySelector('#selection-prev').onclick=()=>{stopSelection();selectionPosition=Math.max(0,selectionPosition-1);showSelection()};
 panel.querySelector('#selection-next').onclick=()=>{stopSelection();selectionPosition=Math.min(selectionSteps.length-1,selectionPosition+1);showSelection()};
 const play=()=>{if(selectionTimer){stopSelection();return}if(selectionPosition===selectionSteps.length-1)selectionPosition=0;panel.querySelector('#selection-play').textContent='Pausar';selectionTimer=setInterval(()=>{selectionPosition++;showSelection()},Number(panel.querySelector('#selection-speed').value))};
 panel.querySelector('#selection-play').onclick=play;panel.querySelector('#selection-speed').onchange=()=>{if(selectionTimer){stopSelection();play()}};
 panel.querySelectorAll('[data-round]').forEach(button=>button.onclick=()=>{stopSelection();selectionPosition=selectionSteps.findIndex(s=>s.line===0&&s.i===Number(button.dataset.round));showSelection()});showSelection();
}
