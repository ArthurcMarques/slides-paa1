const shellCode = [
 'for (size_t gap = n / 2; gap > 0; gap /= 2) {',
 '  for (size_t i = gap; i < n; ++i) {',
 '    int tmp = v[i];',
 '    size_t j = i;',
 '    while (j >= gap && v[j - gap] > tmp) {',
 '      v[j] = v[j - gap];',
 '      j -= gap;',
 '    }',
 '    v[j] = tmp;',
 '  }',
 '}'
];
function shellTrace(input) {
 const a=[...input], steps=[]; let gap=null,i=null,j=null,tmp=null;
 const emit=(line,message,read=[],write=[])=>steps.push({a:[...a],gap,i,j,tmp,line,message,read,write});
 emit(-1,'Vetor inicial. Comece a execução ou avance um passo.');
 for(gap=Math.floor(a.length/2);gap>0;gap=Math.floor(gap/2)){
  i=j=tmp=null;emit(0,`Gap ${gap}: ordenamos por inserção as posições separadas por ${gap}.`);
  for(i=gap;i<a.length;i++){
   j=tmp=null;emit(1,`i = ${i}: vamos inserir o valor desta posição.`,[i]);
   tmp=a[i];emit(2,`Guardamos ${tmp} em tmp. O vetor ainda não muda.`,[i]);
   j=i;emit(3,`j começa em ${j}. Procuramos onde encaixar tmp = ${tmp}.`,[j]);
   while(true){
    const ok=j>=gap && a[j-gap]>tmp;
    const message=j<gap?'j é menor que gap: chegamos ao início do grupo.':`${a[j-gap]} > ${tmp}? ${ok?'Sim: vamos deslocar o maior.':'Não: encontramos a posição de inserção.'}`;
    emit(4,message,j>=gap?[j-gap]:[]);
    if(!ok)break;
    a[j]=a[j-gap];emit(5,`Copiamos v[${j-gap}] = ${a[j-gap]} para v[${j}]. tmp continua guardado.`,[j-gap],[j]);
    j-=gap;emit(6,`j recua ${gap} posições e passa a valer ${j}.`,[j]);
   }
   a[j]=tmp;emit(8,`Gravamos tmp = ${tmp} em v[${j}]. Esta inserção terminou.`,[],[j]);
  }
 }
 i=j=tmp=null;emit(0,'gap chegou a 0. Execução encerrada: vetor ordenado.');
 return steps;
}
let shellTimer=null, shellPosition=0;
const shellSteps=shellTrace([8,3,7,4,6,2,5,1]);
function shellPositions(i,gap,n){
 const positions=[];
 if(!Number.isInteger(i)||!Number.isInteger(gap)||gap<=0||i<0||i>=n)return positions;
 for(let p=i;p>=0;p-=gap)positions.push(p);
 return positions;
}
function stopShell(){if(shellTimer!==null)clearInterval(shellTimer);shellTimer=null;const b=document.querySelector('#shell-play');if(b)b.textContent='Reproduzir';}
function showShell(){
 const s=shellSteps[shellPosition],panel=document.querySelector('#shell-animation');if(!panel)return;
 panel.querySelectorAll('.code-line').forEach((el,k)=>el.classList.toggle('active',k===s.line));
 const cells=panel.querySelector('.shell-cells');cells.replaceChildren();
 s.a.forEach((value,k)=>{const cell=document.createElement('div');cell.className='shell-cell';
  cell.style.borderBottomColor=s.gap?['#008780','#6b75a4','#b76a24','#926881'][k%s.gap]:'#d1d9d8';
  if(s.read.includes(k))cell.classList.add('reading');if(s.write.includes(k))cell.classList.add('writing');
  const val=document.createElement('strong');val.textContent=value;const index=document.createElement('small');index.textContent=`[${k}]`;cell.append(val,index);cells.append(cell);
 });
 panel.querySelector('#shell-vars').textContent=`gap = ${s.gap??'—'}    i = ${s.i??'—'}    j = ${s.j??'—'}    tmp = ${s.tmp??'—'}`;
 const positions=shellPositions(s.i,s.gap,s.a.length);
 const indices=panel.querySelector('#shell-indices');indices.replaceChildren();
 s.a.forEach((_,k)=>{const chip=document.createElement('span');chip.textContent=k;
  chip.className=k===s.i?'insert-index':positions.includes(k)?'previous-index':'';
  if(s.line===4&&s.read.includes(k))chip.classList.add('comparing-index');
  indices.append(chip);
 });
 panel.querySelector('#shell-order').textContent=positions.length?positions.join(' → '):'Selecione uma inserção avançando a execução.';
 panel.querySelector('#shell-message').textContent=s.message;
 panel.querySelector('#shell-progress').textContent=`Passo ${shellPosition} / ${shellSteps.length-1}`;
 panel.querySelector('#shell-prev').disabled=shellPosition===0;
 panel.querySelector('#shell-next').disabled=shellPosition===shellSteps.length-1;
 if(shellPosition===shellSteps.length-1)stopShell();
}
function mountShell(){
 const panel=document.createElement('section');panel.id='shell-animation';panel.setAttribute('aria-label','Execução animada do Shell Sort');
 panel.innerHTML=`<h1>Shell Sort: execução passo a passo</h1><p class="shell-sub">GAPS POR METADES · OITO ELEMENTOS · INSERÇÃO COM SALTOS</p><div class="shell-layout"><div class="shell-visual"><div id="shell-vars"></div><div class="shell-cells"></div><p class="shell-key">Borda inferior: grupo do gap · Azul: leitura · Verde: escrita</p><div id="shell-message" aria-live="polite"></div><p class="shell-explain">Durante os deslocamentos, um valor pode aparecer duas vezes no vetor. O valor de inserção está guardado em <b>tmp</b>.</p></div><div class="shell-code" aria-label="Código em C"></div></div><div class="shell-controls"><button id="shell-reset">Reiniciar</button><button id="shell-prev">Passo anterior</button><button id="shell-play">Reproduzir</button><button id="shell-next">Próximo passo</button><label>Velocidade <select id="shell-speed"><option value="1200">Lenta</option><option value="700" selected>Normal</option><option value="250">Rápida</option></select></label><span id="shell-progress"></span></div><div class="shell-jumps">Ir para a passagem: <button data-gap="4">Gap 4</button><button data-gap="2">Gap 2</button><button data-gap="1">Gap 1</button></div>`;
 const code=panel.querySelector('.shell-code');shellCode.forEach((line,k)=>{const el=document.createElement('div');el.className='code-line';const number=document.createElement('span');number.textContent=String(k+1).padStart(2,'0');const source=document.createElement('code');source.textContent=line;el.append(number,source);code.append(el)});
 document.querySelector('#slide').append(panel);
 const positionPanel=document.createElement('div');positionPanel.className='shell-positions';
 positionPanel.innerHTML='<div id="shell-indices" aria-label="Índices do vetor"></div><p class="position-key"><b>Azul:</b> posição i · <b>Dourado:</b> anteriores do grupo · <b>Contorno:</b> comparação atual</p><p class="position-order">Ordem das posições consideradas: <strong id="shell-order"></strong></p><p class="position-hint">A busca pode parar antes de percorrer todas essas posições.</p>';
 panel.querySelector('.shell-key').after(positionPanel);
 panel.querySelector('#shell-reset').onclick=()=>{stopShell();shellPosition=0;showShell()};
 panel.querySelector('#shell-prev').onclick=()=>{stopShell();shellPosition=Math.max(0,shellPosition-1);showShell()};
 panel.querySelector('#shell-next').onclick=()=>{stopShell();shellPosition=Math.min(shellSteps.length-1,shellPosition+1);showShell()};
 const play=()=>{if(shellTimer){stopShell();return}if(shellPosition===shellSteps.length-1)shellPosition=0;panel.querySelector('#shell-play').textContent='Pausar';shellTimer=setInterval(()=>{shellPosition++;showShell()},Number(panel.querySelector('#shell-speed').value))};
 panel.querySelector('#shell-play').onclick=play;
 panel.querySelector('#shell-speed').onchange=()=>{if(shellTimer){stopShell();play()}};
 panel.querySelectorAll('[data-gap]').forEach(button=>button.onclick=()=>{stopShell();shellPosition=shellSteps.findIndex(s=>s.line===0&&s.gap===Number(button.dataset.gap));showShell()});
 showShell();
}
