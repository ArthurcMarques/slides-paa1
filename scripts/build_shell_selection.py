import base64, csv, html, io, json, re, zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'build/shell'
OUT.mkdir(parents=True,exist_ok=True)
FONT=Path('C:/Users/arthur/AppData/Local/Programs/Python/Python314/Lib/site-packages/matplotlib/mpl-data/fonts/ttf')
BG='#F5F4EF'; INK='#172B36'; TEAL='#008780'; MUTED='#52616A'; LINE='#D1D9D8'; PALE='#E5F0EA'
def font(size,bold=False):return ImageFont.truetype(str(FONT/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)
slides=[]; im=None; d=None; textlog=[]
def text(x,y,s,size=42,bold=False,fill=INK):
    textlog.append(s)
    d.multiline_text((x,y),s,font=font(size,bold),fill=fill,spacing=13)
    for line in s.split('\n'):
        assert d.textlength(line,font=font(size,bold))<=(1890 if x>1800 else 1824)-x, (s,size)
def new(title,sub=''):
    global im,d,textlog
    im=Image.new('RGB',(1920,1080),BG); d=ImageDraw.Draw(im);textlog=[]
    text(96,76,title,64,True)
    if sub:
        d.rectangle((96,186,1807,191),fill=LINE);text(102,207,sub,27,True,TEAL)
def box(rect,fill='white',radius=12):d.rounded_rectangle(rect,radius=radius,fill=fill,outline=LINE,width=2)
def note(s):text(104,910,s,30,False,MUTED)
def save(title,links=None):
    n=len(slides)+1
    text(1832,1002,f'{n:02}',26,False,MUTED)
    p=OUT/f'shell-{n:02}.png';im.save(p)
    slides.append(dict(title=title,text='\n'.join(textlog),image='data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode(),links=links or [],part='Shell Sort'))

new('')
text(105,115,'PROJETO E ANÁLISE DE ALGORITMOS',30,True,TEAL)
d.rectangle((105,183,1810,188),fill=LINE)
text(105,265,'Shell Sort e',96,True)
text(105,385,'Selection Sort',96,True)
text(110,550,'Funcionamento, implementação e análise de desempenho',38,False,MUTED)
for j,value in enumerate([11,12,22,25,64]):
    x=110+j*215
    box((x,665,x+175,815),PALE if j<3 else 'white')
    d.text((x+87,740),str(value),anchor='mm',font=font(58,True),fill=TEAL if j<3 else INK)
textlog.append('Valores em ordem crescente: 11, 12, 22, 25, 64.')
text(110,946,'Projeto e Análise de Algoritmos | 2026',29,False,MUTED)
d.rectangle((1450,930,1795,1010),fill=TEAL)
d.text((1622,969),'Iniciar',anchor='mm',font=font(38,True),fill='white')
save('Shell Sort e Selection Sort',[
    dict(x=1450/19.2,y=930/10.8,w=345/19.2,h=80/10.8,target=2,label='Iniciar apresentação')])

new('História do Shell Sort','TRÊS NOMES PARA LEMBRAR')
for y,year,name,body in [
 (290,'1959','Donald L. Shell','Publicou o Shell Sort como uma melhoria\nda ordenação por inserção.'),
 (480,'1973','Donald E. Knuth','Apresentou a sequência de gaps\ngerada por 3h + 1.'),
 (670,'2001','Marcin Ciura','Publicou um estudo experimental de sequências\npara melhorar o desempenho médio.')]:
    text(106,y,year,52,True,TEAL);text(440,y,name,43,True);text(440,y+64,body,36)
note('Shell Sort aproxima os valores antes da última passagem.');save('História do Shell Sort')

new('Como funciona o Shell Sort','ORDENA PRIMEIRO OS VALORES MAIS DISTANTES')
for y,num,title,body in [
    (295,'1','Separar em grupos','O gap define a distância entre as posições de cada grupo.'),
    (475,'2','Ordenar cada grupo','Como na inserção: desloca os maiores e encaixa o valor.'),
    (655,'3','Diminuir o gap e repetir','Com gap 1, todos ficam no mesmo grupo e a ordenação termina.')]:
    text(106,y,num,58,True,TEAL)
    text(245,y,title,43,True)
    text(245,y+70,body,35)
note('Os primeiros gaps aproximam os valores das posições finais.')
save('Como funciona o Shell Sort')

new('Gaps e sua importância','O GAP É A DISTÂNCIA ENTRE AS POSIÇÕES')
text(104,277,'A escolha muda as passagens, os deslocamentos e o tempo.',38)
box((105,355,1800,530),PALE)
text(142,373,'Metades',40,True,TEAL)
text(142,429,'Começa em ⌊n/2⌋ e divide por dois, com divisão inteira, até 1.',33)
text(142,480,'Para n = 100: 50, 25, 12, 6, 3, 1.',33,True)
box((105,551,1800,726))
text(142,569,'Knuth',40,True,TEAL)
text(142,625,'1, 4, 13, 40, 121, 364, …',35,True)
text(142,676,'Próximo gap = 3h + 1.',33)
box((105,747,1800,922),PALE)
text(142,765,'Ciura fixo',40,True,TEAL)
text(142,821,'1, 4, 10, 23, 57, 132, 301, 701, 1750',35,True)
text(142,872,'Não usamos a versão estendida.',33)
text(104,954,'Usamos do maior para o menor, terminando em gap 1.',29,False,MUTED)
save('Gaps: Metades, Knuth e Ciura')

colors=['#D6EEE7','#E6EAF6','#F1E6D4','#EADFEA']
def array_row(y,label,values,gap):
    text(102,y+33,label,39,True,TEAL)
    textlog.append('Valores: '+', '.join(map(str,values)))
    for j,value in enumerate(values):
        x=410+j*158
        box((x,y,x+130,y+116),colors[j%gap] if gap>1 else PALE)
        d.text((x+65,y+57),str(value),anchor='mm',font=font(49,True),fill=INK)
        d.text((x+65,y+145),str(j),anchor='mm',font=font(25),fill=MUTED)

examples=[
    (4,[8,3,7,4,6,2,5,1],[6,2,5,1,8,3,7,4],
     'Grupos de posições: (0, 4), (1, 5), (2, 6) e (3, 7).',
     'No primeiro grupo, 8 e 6 viram 6 e 8. Os outros seguem a mesma ideia.'),
    (2,[6,2,5,1,8,3,7,4],[5,1,6,2,7,3,8,4],
     'Agora os grupos são as posições (0, 2, 4, 6) e (1, 3, 5, 7).',
     'Os grupos [6, 5, 8, 7] e [2, 1, 3, 4] ficam ordenados separadamente.'),
    (1,[5,1,6,2,7,3,8,4],[1,2,3,4,5,6,7,8],
     'Com gap 1, todas as posições formam um único grupo.',
     'A inserção encaixa cada valor entre os anteriores. O vetor fica ordenado.')]
for gap,before,after,explain,detail in examples:
    new(f'Exemplo: passagem com gap {gap}','OITO ELEMENTOS • GAPS POR METADES: 4, 2 E 1')
    array_row(315,'Antes',before,gap)
    array_row(560,'Depois',after,gap)
    text(104,795,explain,34)
    text(104,858,detail,32)
    note('Mesma cor = mesmo grupo. Os números abaixo indicam as posições.')
    save(f'Exemplo de funcionamento: gap {gap}')

new('Shell Sort é estável?','NÃO GARANTE A ORDEM ORIGINAL DOS VALORES IGUAIS')
text(105,279,'2A e 2B têm o mesmo valor. As letras identificam cada elemento.',35)
for y,label,values in [
    (365,'Entrada',['2A','2B','1','3']),
    (535,'Após gap 2',['1','2B','2A','3']),
    (705,'Após gap 1',['1','2B','2A','3'])]:
    text(105,y+32,label,37,True,TEAL)
    textlog.append('Valores: '+', '.join(values))
    for j,value in enumerate(values):
        x=565+j*285
        box((x,y,x+235,y+116),PALE if value in ['2A','2B'] else 'white')
        d.text((x+117,y+57),value,anchor='mm',font=font(48,True),fill=INK)
text(105,873,'O salto do gap 2 colocou 2A depois de 2B.',37,True)
text(105,940,'Mesmo com a inserção normal no final, essa ordem pode permanecer.',31,False,MUTED)
save('Estabilidade: Shell Sort não é estável')

new('Complexidades das implementações','MELHOR E PIOR CASO DE CADA VERSÃO')
xs=[110,820,1320]
for x,s in zip(xs,['Versão','Melhor caso','Pior caso']):text(x,296,s,36,True,TEAL)
for i,row in enumerate([['Metades','Θ(n log n)','Θ(n²)'],['Knuth','Θ(n log n)','Θ(n³ᐟ²)'],['Ciura fixo até 1750','Θ(n)','Θ(n²)']]):
    y=390+i*130;box((105,y-12,1800,y+90),'white' if i%2==0 else PALE)
    for x,s in zip(xs,row):text(x+15,y+15,s,40,x==110)
text(104,826,'Ciura: o melhor caso linear vale para a nossa lista fixa,',36)
text(104,882,'com no máximo nove passagens.',36)
save('Complexidades: melhor e pior caso')

new('Outras sequências','REFERÊNCIAS DO RELATÓRIO: NÃO IMPLEMENTADAS NEM TESTADAS')
for y,name,seq,bound in [(289,'Hibbard','2ᵏ − 1: 1, 3, 7, 15, 31, …','O(n³ᐟ²)'),(475,'Pratt','2ᵖ3ᑫ: 1, 2, 3, 4, 6, 8, 9, 12, …','O(n log² n)'),(661,'Sedgewick','Sequência específica: 1, 8, 23, 77, 281, …','O(n⁴ᐟ³)')]:
    text(105,y,name,42,True,TEAL);text(105,y+65,seq,35)
    text(1410,y+24,bound,42,True)
note('Limites de pior caso. A escolha dos gaps pode alterar a complexidade.');save('Outras sequências: limites de referência')

new('Shell: vantagens e desvantagens','POUCA MEMÓRIA EXTRA, MAS O DESEMPENHO DEPENDE DOS GAPS')
box((105,300,930,845),PALE)
box((970,300,1795,845))
text(145,340,'Vantagens',45,True,TEAL)
text(145,440,'Memória auxiliar constante.',35)
text(145,535,'Move valores distantes\nnas primeiras passagens.',35)
text(145,680,'Permite escolher diferentes\nsequências de gaps.',35)
text(1010,340,'Desvantagens',45,True,TEAL)
text(1010,440,'Não é estável.',35)
text(1010,535,'O desempenho depende\nda sequência de gaps.',35)
text(1010,680,'Algumas sequências têm\npior caso quadrático.',35)
note('A análise do pior caso é mais difícil que a do Selection Sort.')
save('Shell Sort: vantagens e desvantagens')

datasets={}
for seq in ['metades','knuth','ciura']:
    path=ROOT/'dados'/f'shell_{seq}_pt_BR.csv'
    with path.open(encoding='utf-8-sig',newline='') as f:datasets[seq]=list(csv.DictReader(f,delimiter=';'))
    assert len(datasets[seq])==30
    assert all(r['validacao']=='OK' for r in datasets[seq])
def integer(s):return f'{int(s):,}'.replace(',','.')
types={'aleatorio':'entrada aleatória','crescente':'entrada crescente','decrescente':'entrada decrescente'}
metrics=[('tempo','segundos_ordenacao','Tempo','Tempo (s)'),
         ('comparacoes','comparacoes','Comparações','Número de comparações'),
         ('movimentacoes','movimentacoes','Movimentações','Escritas no vetor')]
for slug,metric,label,ylabel in metrics:
    for kind,kindname in types.items():
        title=label+' — '+kindname
        new(title,'SHELL SORT • METADES, KNUTH E CIURA FIXO')
        # Mesmo recorte dos gráficos log/shell fornecidos, com o estilo dos slides.
        assert (ROOT/'graficos/referencia'/f'{slug}_{kind}_shell_log.png').is_file()
        with plt.rc_context({'font.family':'DejaVu Sans','font.size':19,
                             'text.color':INK,'axes.labelcolor':INK,
                             'xtick.color':MUTED,'ytick.color':MUTED}):
            fig,ax=plt.subplots(figsize=(17.1,6.25),dpi=100)
            fig.patch.set_facecolor(BG);ax.set_facecolor(BG)
            fig.subplots_adjust(left=.105,right=.98,bottom=.165,top=.94)
            for seq,version,color,marker in [('metades','Metades',TEAL,'o'),
                                             ('knuth','Knuth',INK,'s'),
                                             ('ciura','Ciura fixo','#B76A24','^')]:
                rows=sorted([r for r in datasets[seq] if r['tipo']==kind],key=lambda r:int(r['n']))
                assert len(rows)==10
                xs=[int(r['n']) for r in rows]
                ys=[float(r[metric].replace(',','.')) for r in rows]
                ax.plot(xs,ys,label=version,color=color,marker=marker,linewidth=3,markersize=8)
                textlog.append(version+': '+ '; '.join(f"n={r['n']}: {r[metric]}" for r in rows))
            ax.set_xscale('log');ax.set_yscale('log')
            ax.set_xlabel('Quantidade de elementos (n)',fontsize=21,labelpad=9)
            ax.set_ylabel(ylabel,fontsize=21,labelpad=12)
            ax.xaxis.set_major_locator(LogLocator(base=10,numticks=8))
            ax.yaxis.set_minor_formatter(NullFormatter())
            ax.grid(which='major',color=LINE,linewidth=1)
            ax.tick_params(axis='both',which='major',labelsize=18)
            for spine in ax.spines.values():spine.set_color(LINE)
            ax.legend(loc='upper left',fontsize=18,facecolor=BG,edgecolor=LINE,framealpha=.95)
            buffer=io.BytesIO();fig.savefig(buffer,format='png',facecolor=BG,dpi=100);plt.close(fig)
        buffer.seek(0);im.paste(Image.open(buffer).convert('RGB'),(96,278))
        text(105,925,'Escala logarítmica nos dois eixos. Uma medição por combinação, sem médias.',28,False,MUTED)
        if metric=='movimentacoes':text(105,972,'Escritas no vetor, incluindo a gravação final do temporário.',27,False,MUTED)
        elif kind=='decrescente':text(105,972,'Entrada decrescente não é, automaticamente, o pior caso matemático.',27,False,MUTED)
        save(title)

new('Conclusão: a escolha dos gaps','NENHUMA SEQUÊNCIA VENCEU TODOS OS CENÁRIOS')
for y,title,body in [
    (290,'Knuth','Foi o mais rápido no teste decrescente com 10 milhões de elementos.'),
    (465,'Ciura fixo','Foi mais rápido nas entradas crescentes maiores, mas teve alto custo\nna decrescente. Sua lista termina em 1750.'),
    (690,'Tamanho e ordem da entrada','Os resultados mudaram conforme o tamanho do vetor e sua organização.')]:
    text(105,y,title,41,True,TEAL);text(105,y+65,body,33)
text(105,900,'Uma medição por teste: repetir ajudaria a avaliar a variação dos tempos.',30,False,MUTED)
text(105,955,'Os resultados medidos não são uma garantia para qualquer entrada.',30,False,MUTED)
save('Conclusão: gaps e limites dos testes')

offset=len(slides)
raw=(ROOT/'historico/selection-sort/dist/data.js').read_text(encoding='utf-8')
original=json.loads(raw.removeprefix('const slides = ').removesuffix(';'))
assert len(original)==27
for i,s in enumerate(original,1):
    for l in s['links']:
        l['target']=1 if i==27 and l['label']=='Início' else l['target']+offset
    s['part']='Selection Sort'
    s['image']='data:image/png;base64,'+base64.b64encode((ROOT/f'historico/selection-sort/dist/slides/Slide{i}.PNG').read_bytes()).decode()
    slides.append(s)

comparison_start=len(slides)+1
new('Selection Sort × Shell Sort','COMPARAÇÃO COM SHELL POR METADES')
for x,title,body in [
    (105,'Selection Sort','Melhor caso: Θ(n²)\nPior caso: Θ(n²)\nBusca o menor a cada rodada.'),
    (970,'Shell por metades','Melhor caso: Θ(n log n)\nPior caso: Θ(n²)\nAproveita a organização dos gaps.')]:
    box((x,300,x+825,725),PALE if x==970 else 'white')
    text(x+38,340,title,43,True,TEAL)
    text(x+38,438,body,35)
text(105,788,'Ambos: memória auxiliar constante e sem garantia de estabilidade.',35)
text(105,861,'Mesmo pior caso não significa o mesmo tempo em todos os testes.',35,True)
note('Nesta comparação, usamos somente Selection e Shell por metades.')
save('Comparação: Selection e Shell por metades');slides[-1]['part']='Comparação'

with (ROOT/'dados/selection_tempos_relatorio.csv').open(encoding='utf-8-sig',newline='') as f:
    selection_times=list(csv.DictReader(f,delimiter=';'))
assert len(selection_times)==30
highlights={
    'aleatorio':('107.310,582 s','2,559 s'),
    'crescente':('105.912,840 s','0,487 s'),
    'decrescente':('105.923,688 s','0,570 s')}
for kind,kindname in types.items():
    new('Tempos — '+kindname,'SELECTION SORT × SHELL POR METADES')
    with plt.rc_context({'font.family':'DejaVu Sans','font.size':19,'text.color':INK,
                         'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED}):
        fig,ax=plt.subplots(figsize=(17.1,5.8),dpi=100)
        fig.patch.set_facecolor(BG);ax.set_facecolor(BG)
        fig.subplots_adjust(left=.105,right=.98,bottom=.18,top=.94)
        for data,label,color,marker in [(selection_times,'Selection Sort',INK,'s'),
                                        (datasets['metades'],'Shell por metades',TEAL,'o')]:
            rows=sorted([r for r in data if r['tipo']==kind],key=lambda r:int(r['n']))
            assert len(rows)==10
            ax.plot([int(r['n']) for r in rows],
                    [float(r['segundos_ordenacao'].replace(',','.')) for r in rows],
                    label=label,color=color,marker=marker,linewidth=3,markersize=8)
            textlog.append(label+': '+'; '.join(f"n={r['n']}: {r['segundos_ordenacao']} s" for r in rows))
        ax.set_xscale('log');ax.set_yscale('log')
        ax.set_xlabel('Quantidade de elementos (n)',fontsize=21,labelpad=9)
        ax.set_ylabel('Tempo (s)',fontsize=21,labelpad=12)
        ax.xaxis.set_major_locator(LogLocator(base=10,numticks=8))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.grid(which='major',color=LINE,linewidth=1)
        for spine in ax.spines.values():spine.set_color(LINE)
        ax.legend(loc='upper left',fontsize=18,facecolor=BG,edgecolor=LINE)
        buffer=io.BytesIO();fig.savefig(buffer,format='png',facecolor=BG,dpi=100);plt.close(fig)
    buffer.seek(0);im.paste(Image.open(buffer).convert('RGB'),(96,270))
    a,b=highlights[kind]
    text(105,870,'10 milhões de elementos:',32,True)
    text(105,921,f'Selection: {a}     Shell por metades: {b}',35,True,TEAL)
    text(105,979,'Escalas logarítmicas. Medições individuais do relatório, sem médias.',26,False,MUTED)
    save('Comparação de tempos — '+kindname);slides[-1]['part']='Comparação'

new('Menos escritas não garantem menor tempo','10 MILHÕES DE ELEMENTOS • ENTRADA ALEATÓRIA')
for x,title,comp,moves in [
    (105,'Selection Sort','49.999.995.000.000','19.999.976'),
    (970,'Shell por metades','1.113.901.611','1.118.919.386')]:
    box((x,290,x+825,730),PALE if x==970 else 'white')
    text(x+35,325,title,43,True,TEAL)
    text(x+35,425,'Comparações',32,False,MUTED)
    text(x+35,478,comp,40,True)
    text(x+35,573,'Escritas no vetor',32,False,MUTED)
    text(x+35,626,moves,40,True)
text(105,785,'Shell escreveu mais, mas fez muito menos comparações.',38,True)
text(105,854,'Na entrada crescente, Selection não fez trocas,',35)
text(105,908,'mas continuou fazendo todas as buscas.',35)
save('Comparação: escritas, comparações e tempo');slides[-1]['part']='Comparação'

new('Conclusão: Selection e Shell','O QUE OBSERVAMOS NOS TESTES')
for y,num,title,body in [
    (295,'1','Shell por metades foi mais rápido nos vetores grandes',
     'Com 10 milhões aleatórios: quase 30 horas contra cerca de 2,559 s.'),
    (475,'2','Selection não aproveitou a entrada já ordenada',
     'Sem trocas, mas com a mesma quantidade de comparações.'),
    (655,'3','O pior caso não descreve todas as entradas',
     'Ambos têm pior caso quadrático, mas os tempos medidos foram diferentes.')]:
    text(105,y,num,55,True,TEAL);text(220,y,title,37,True);text(220,y+70,body,32)
note('Precisamos olhar tempo, comparações e escritas em conjunto.')
save('Conclusão: comparação dos algoritmos');slides[-1]['part']='Conclusão'

comparison_count=len(slides)-(comparison_start-1)

new('Bibliografia do Shell Sort','REFERÊNCIAS')
sources=[
 ('Donald E. Knuth','The Art of Computer Programming, volume 3: Sorting and Searching.','https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/Shell.html'),
 ('Marcin Ciura (2001)','Estudo experimental de sequências de gaps.','https://doi.org/10.1007/3-540-44669-9_12'),
 ('Robert Sedgewick (1986 e 1996)','Limites e referências para outras sequências.','https://sedgewick.io/wp-content/themes/sedgewick/papers/1986Shellsort.pdf')]
links=[]
for i,(name,desc,url) in enumerate(sources):
    y=285+i*165;text(105,y,name,38,True,TEAL);text(105,y+58,desc,30)
    links.append(dict(x=5.4,y=y/10.8,w=88,h=11,target=url,label=name))
text(105,805,'Resultados: shell_metades, shell_knuth e shell_ciura (CSV).',31)
text(105,864,'Uma medição por combinação. Sem execução nova nem médias.',31)
text(105,923,'Comparação e conclusão: relatório do trabalho, seções 4 e 7.',29,False,MUTED)
links.append(dict(x=5.4,y=68.5,w=88,h=4,target='https://sedgewick.io/wp-content/themes/sedgewick/papers/1996Shellsort.pdf',label='Sedgewick — estudo de 1996'))
text(105,744,'Abrir também o estudo de 1996',26,False,TEAL)
save('Bibliografia do Shell Sort',links)
slides[-1]['part']='Bibliografia'

css=(ROOT/'historico/selection-sort/dist/style.css').read_text(encoding='utf-8')
css+='\n#chapter{max-width:22vw}nav{gap:8px}.hotspot{padding:0}#transcript a{color:#008780}#transcript{font-family:Arial,sans-serif}nav select{font-size:14px}@media(max-width:700px){#chapter{max-width:26vw}#select{max-width:30vw}nav{gap:4px}nav button{padding:8px}#count{font-size:10px}}'
script='''
const image=document.querySelector('#image'), links=document.querySelector('#links'), select=document.querySelector('#select'), chapter=document.querySelector('#chapter');
let current=1;
slides.forEach((s,i)=>select.add(new Option(`${i+1}. ${s.title}`,i+1)));
function go(n){
 current=Math.max(1,Math.min(slides.length,Number(n)||1));const s=slides[current-1];
 image.src=s.image;image.alt=s.title;links.replaceChildren();
 s.links.forEach(l=>{const b=document.createElement(typeof l.target==='number'?'button':'a');b.className='hotspot';b.style.cssText=`left:${l.x}%;top:${l.y}%;width:${l.w}%;height:${l.h}%`;b.setAttribute('aria-label',l.label);b.title=l.label;if(typeof l.target==='number')b.onclick=()=>go(l.target);else {b.href=l.target;b.target='_blank';b.rel='noopener noreferrer'}links.append(b)});
 select.value=current;chapter.value=s.part==='Bibliografia'?'bibliografia':['Comparação','Conclusão'].includes(s.part)?'comparacao':current<=SHELL_COUNT?'shell':'selection';document.querySelector('#count').textContent=`${current} / ${slides.length}`;
 document.querySelector('#prev').disabled=current===1;document.querySelector('#next').disabled=current===slides.length;
 document.querySelector('#text').textContent=s.text;document.title=`${s.title} — Shell e Selection Sort`;history.replaceState(null,'',`#slide-${current}`);
}
document.querySelector('#prev').onclick=()=>go(current-1);document.querySelector('#next').onclick=()=>go(current+1);select.onchange=()=>go(select.value);chapter.onchange=()=>go(chapter.value==='comparacao'?SHELL_COUNT+28:chapter.value==='bibliografia'?slides.length:chapter.value==='shell'?1:SHELL_COUNT+1);
async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch{}}
document.querySelector('#full').onclick=fullscreen;
document.addEventListener('keydown',e=>{if(['SELECT','BUTTON','INPUT','A','SUMMARY'].includes(document.activeElement.tagName))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();go(current+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();go(current-1)}if(e.key==='Home')go(1);if(e.key==='End')go(slides.length);if(e.key.toLowerCase()==='f')fullscreen()});
let startX;image.addEventListener('touchstart',e=>startX=e.changedTouches[0].clientX,{passive:true});image.addEventListener('touchend',e=>{const delta=e.changedTouches[0].clientX-startX;if(Math.abs(delta)>60)go(current+(delta<0?1:-1))},{passive:true});
window.addEventListener('hashchange',()=>go(location.hash.split('-')[1]));go(location.hash.split('-')[1]);
'''
doc='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shell e Selection Sort</title><meta name="description" content="Shell Sort: história, gaps e resultados experimentais. Apresentação completa de Selection Sort."><style>'''+css+'''</style></head><body><main><div id="slide" aria-label="Apresentação"><img id="image" alt="" draggable="false"><div id="links"></div></div></main><nav aria-label="Navegação"><button id="prev" aria-label="Slide anterior">←</button><label for="chapter" class="sr">Parte da apresentação</label><select id="chapter"><option value="shell">Shell Sort</option><option value="selection">Selection Sort</option></select><label for="select" class="sr">Escolher slide</label><select id="select"></select><span id="count" aria-live="polite"></span><button id="next" aria-label="Próximo slide">→</button><button id="full" aria-label="Tela cheia" title="Tela cheia (F)">⛶</button></nav><details id="transcript"><summary>Texto do slide</summary><pre id="text"></pre><p>Setas: navegar · F: tela cheia · Home: início · End: último slide.</p></details><script>const SHELL_COUNT='''+str(offset)+';const slides='+json.dumps(slides,ensure_ascii=False).replace('</','<\\/')+';\n'+script+'</script></body></html>'
doc=doc.replace('<option value="selection">Selection Sort</option>','<option value="selection">Selection Sort</option><option value="bibliografia">Bibliografia</option>')
doc=doc.replace('<option value="bibliografia">','<option value="comparacao">Comparação e conclusão</option><option value="bibliografia">')
dest=ROOT/'Shell_e_Selection_Sort.html';dest.write_text(doc,encoding='utf-8')
site_dir=ROOT/'site'
site_dir.mkdir(exist_ok=True)
(site_dir/'index.html').write_text(doc,encoding='utf-8')
(OUT/'app-check.js').write_text('const SHELL_COUNT='+str(offset)+';const slides=[];'+script,encoding='utf-8')
manifest=[dict(index=i+1,title=s['title'],part=s['part'],links=s['links']) for i,s in enumerate(slides)]
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(ROOT/'distribuicao/Shell_e_Selection_Sort_Web.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write(dest,dest.name)
    for path in (ROOT/'dados').glob('*.csv'):z.write(path,'dados/'+path.name)
with zipfile.ZipFile(ROOT/'distribuicao/site.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write(site_dir/'index.html','index.html')
assert len(slides)==offset+28+comparison_count
assert all(1<=l['target']<=len(slides) for s in slides for l in s['links'] if isinstance(l['target'],int))
# Check that all original slide bytes, titles and text remain unchanged.
for i,s in enumerate(slides[offset:offset+27]):
    assert s['text']==original[i]['text']
    assert base64.b64decode(s['image'].split(',')[1])==(ROOT/f'historico/selection-sort/dist/slides/Slide{i+1}.PNG').read_bytes()
print(f'{offset} Shell + 27 Selection + {comparison_count} de comparação/conclusão + bibliografia = {len(slides)} slides. Links validados.')
print(dest)
