import ast, base64, csv, html, io, json, re, zipfile
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

new('Shell Sort: execução passo a passo','GAPS POR METADES • 4, 2 E 1')
for y,label,values in [(360,'Entrada',[8,3,7,4,6,2,5,1]),(600,'Resultado',[1,2,3,4,5,6,7,8])]:
    text(105,y-60,label,35,True,TEAL)
    for k,value in enumerate(values):
        x=105+k*101;box((x,y,x+88,y+110),PALE)
        d.text((x+44,y+55),str(value),anchor='mm',font=font(42,True),fill=INK)
    textlog.append(label+': '+', '.join(map(str,values)))
code_source=(ROOT/'scripts/shell-animation.js').read_text(encoding='utf-8')
code_lines=ast.literal_eval('['+code_source.split('const shellCode = [',1)[1].split('\n];',1)[0]+']')
box((970,295,1810,790))
for k,line in enumerate(code_lines):
    d.text((990,320+k*39),line,font=ImageFont.truetype(str(FONT/'DejaVuSansMono.ttf'),23),fill=INK)
textlog.append('\n'.join(code_lines))
text(105,845,'Na web: reproduza, pause e avance com a linha do código destacada.',32)
note('O PDF contém este resumo estático. A execução animada está no HTML.')
save('Shell Sort: execução animada com código')
slides[-1]['animation']='shell'

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

def result_table(title,subtitle,headers,rows,footnote,part='Shell Sort'):
    new(title,subtitle)
    cols=[105,530,960,1390] if len(headers)==4 else [105,650,1220]
    for x,heading in zip(cols,headers):text(x+12,281,heading,32,True,TEAL)
    assert len(rows)==10
    for i,row in enumerate(rows):
        y=344+i*48
        if i%2==0:d.rectangle((105,y-4,1800,y+43),fill='white')
        for x,value in zip(cols,row):text(x+12,y,value,30)
    text(105,880,'Uma medição por combinação. Tempos e contagens não são médias.',29,False,MUTED)
    if footnote:text(105,938,footnote,29,False,MUTED)
    save(title);slides[-1]['part']=part
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
        ns=sorted(int(r['n']) for r in datasets['metades'] if r['tipo']==kind)
        table_rows=[]
        for n in ns:
            values=[integer(n)]
            for seq in ['metades','knuth','ciura']:
                row=next(r for r in datasets[seq] if r['tipo']==kind and int(r['n'])==n)
                values.append(row[metric] if metric=='segundos_ordenacao' else integer(row[metric]))
            table_rows.append(values)
        result_table('Tabela: '+label.lower()+' — '+kindname,
                     'SHELL SORT • '+ylabel.upper(),['n','Metades','Knuth','Ciura fixo'],table_rows,
                     'Movimentações incluem a gravação final do temporário.' if metric=='movimentacoes' else '')

new('Conclusão: a escolha dos gaps','NENHUMA SEQUÊNCIA VENCEU TODOS OS CENÁRIOS')
for y,title,body in [
    (290,'Knuth','Foi o mais rápido no teste decrescente com 10 milhões de elementos.'),
    (465,'Ciura fixo','Foi mais rápido nas entradas crescentes maiores, mas teve alto custo\nna decrescente. Sua lista termina em 1750.'),
    (690,'Tamanho e ordem da entrada','Os resultados mudaram conforme o tamanho do vetor e sua organização.')]:
    text(105,y,title,41,True,TEAL);text(105,y+65,body,33)
save('Conclusão: gaps e limites dos testes')

offset=len(slides)
raw=(ROOT/'historico/selection-sort/dist/data.js').read_text(encoding='utf-8')
original=json.loads(raw.removeprefix('const slides = ').removesuffix(';'))
assert len(original)==27
selection_numbers=[i for i in range(1,28) if not 9<=i<=14]
selection_count=len(selection_numbers)
selection_content={
1:('Selection Sort','SELECIONAR O MENOR • TROCAR • REPETIR', [('Ideia principal','Encontrar o menor valor da parte restante.'),('A cada rodada','Colocar esse valor na próxima posição livre.'),('Resultado','A parte ordenada cresce uma posição por vez.')]),
2:('História do Selection Sort','MÉTODOS DE SELEÇÃO NOS PRIMEIROS COMPUTADORES', [('Anos 1950','Já existiam estudos sobre ordenação por seleção.'),('1956 e 1958','Demuth, Friend e Bell estudaram métodos de ordenação.'),('O que lembrar','Não há um inventor comprovado da versão atual.')]),
3:('Selection: registros históricos','1956 • HOWARD B. DEMUTH', [('Estudo em Stanford','Seu doutorado tratou de formas de ordenar dados.'),('Relação com Selection','O trabalho descreve uma técnica relacionada à seleção.'),('Cuidado com a atribuição','Um registro antigo não prova quem inventou o algoritmo.')]),
4:('Selection: outros estudos','1956 E 1958', [('Edward H. Friend • 1956','Publicou um estudo sobre ordenação em computadores.'),('D. A. Bell • 1958','Também apresentou métodos de ordenação.'),('Métodos relacionados','As versões estudadas não eram todas iguais à atual.')]),
5:('Selection nos livros e nas aulas','UM ALGORITMO CLÁSSICO PARA APRENDER ORDENAÇÃO', [('Knuth • 1973','Publicou o volume sobre ordenação e busca.'),('Edição de 1998','O livro inclui ordenação por seleção.'),('MIT • 2000','Selection aparece em aulas de programação.')]),
6:('Selection: resumo da história','O QUE VALE LEMBRAR', [('Origem','Métodos de seleção já eram estudados nos anos 1950.'),('Difusão','O algoritmo passou a aparecer em livros e cursos.'),('Autoria','Não atribuímos um inventor único ao Selection Sort.')]),
7:('Como funciona o Selection Sort?','BUSCAR • GUARDAR A POSIÇÃO • TROCAR', [('1 • Procurar','Percorrer a parte ainda não ordenada e achar o menor.'),('2 • Trocar','Colocar o menor no início dessa parte.'),('3 • Repetir','Avançar uma posição e fazer uma nova busca.')]),
15:('Selection: a ideia central','UMA POSIÇÃO DEFINIDA POR RODADA', [('Busca','Guardar o índice do menor valor encontrado.'),('Troca','Trocar somente depois de terminar a busca.'),('Parte ordenada','As posições já definidas ficam prontas.')]),
16:('Selection no nosso trabalho','ARQUIVOS DE ENTRADA • ORDENAÇÃO • MEDIÇÃO', [('Entrada','O programa lê n inteiros de um arquivo.'),('Ordenação','A função selection_sort() reorganiza o vetor.'),('Registro','Salva tempo, comparações e movimentações.')]),
17:('Selection: código em C','A MESMA LÓGICA DA ANIMAÇÃO', [('i e j','i define a posição; j percorre os valores restantes.'),('menor','Guarda a posição do menor valor encontrado.'),('Troca efetiva','Se menor for diferente de i, são feitas duas escritas.')]),
18:('Selection: execução dos testes','DA LEITURA AO REGISTRO DOS RESULTADOS', [('Preparar','Localizar o arquivo, alocar o vetor e carregar os valores.'),('Executar','Medir o tempo da função de ordenação.'),('Finalizar','Registrar o resultado e liberar a memória.')]),
19:('Selection: entradas dos testes','10 TAMANHOS • 3 TIPOS DE ENTRADA', [('Organizações','Entrada aleatória, entrada crescente e entrada decrescente.'),('Tamanhos','De 10 a 10.000.000 de elementos.'),('Medições','Uma execução por combinação: não são médias.')]),
20:('Selection: o que contamos?','COMPARAÇÕES E ESCRITAS NO VETOR', [('Comparações','Cada comparação entre valores conta uma operação.'),('Movimentações','Uma troca efetiva conta duas escritas no vetor.'),('Exemplo com cinco valores','[64, 25, 12, 22, 11]: 10 comparações e 6 escritas.')]),
21:('Selection: complexidade','A BUSCA CONTINUA MESMO COM A ENTRADA ORDENADA', [('Melhor caso','Θ(n²): ainda percorre toda a parte restante.'),('Pior caso','Θ(n²): a quantidade de comparações é a mesma.'),('Memória auxiliar','Θ(1): usa poucas variáveis para ordenar o vetor.')]),
22:('Selection: crescimento do custo','AS COMPARAÇÕES CRESCEM RAPIDAMENTE', [('100 elementos','4.950 comparações.'),('1.000 elementos','499.500 comparações.'),('Ao multiplicar n por 10','O número de comparações aumenta cerca de 100 vezes.')]),
23:('Selection: estabilidade e memória','A VERSÃO COM TROCA DIRETA NÃO É ESTÁVEL', [('Valores iguais podem inverter a ordem','[2A, 2B, 1] → [1, 2B, 2A] após a primeira troca.'),('Memória auxiliar constante','A ordenação usa Θ(1) de espaço extra.'),('Poucas trocas','No máximo n − 1 trocas efetivas.')]),
25:('Selection: medição de desempenho','TEMPO SOMENTE DA ORDENAÇÃO', [('Cronômetro','clock_gettime() com relógio monotônico.'),('Trecho medido','Somente a chamada de selection_sort().'),('Resultados individuais','Cada combinação tem uma medição, sem calcular médias.')]),
26:('Selection: resultados dos testes','10 MILHÕES DE ELEMENTOS • ENTRADA ALEATÓRIA', [('Tempo','107.310,582 segundos: aproximadamente 29 h e 49 min.'),('Comparações','49.999.995.000.000 comparações entre valores.'),('Leitura do resultado','O custo quadrático pesa muito nas entradas grandes.')]),
27:('Conclusão: Selection Sort','SIMPLES, MAS CUSTOSO EM VETORES GRANDES', [('Comparações','A quantidade depende do tamanho, não da ordem inicial.'),('Movimentações','Dependem das trocas necessárias para aquela entrada.'),('Uso prático','É fácil de implementar, mas não escala bem.')])}
selection_targets={i:offset+selection_numbers.index(i)+1 for i in selection_numbers}
for i in range(9,15):selection_targets[i]=selection_targets[8]
for i,s in enumerate(original,1):
    if i not in selection_numbers:continue
    for l in s['links']:
        l['target']=1 if i==27 and l['label']=='Início' else selection_targets[l['target']]
    if i==8:
        new('Selection Sort: execução passo a passo','BUSCAR O MENOR • TROCAR • REPETIR')
        for y,label,values in [(355,'Entrada',[8,3,7,4,6,2,5,1]),(600,'Resultado',[1,2,3,4,5,6,7,8])]:
            text(105,y-55,label,34,True,TEAL)
            for k,value in enumerate(values):
                x=105+k*101;box((x,y,x+88,y+110),PALE)
                d.text((x+44,y+55),str(value),anchor='mm',font=font(42,True),fill=INK)
            textlog.append(label+': '+', '.join(map(str,values)))
        source=(ROOT/'scripts/selection-animation.js').read_text(encoding='utf-8')
        lines=ast.literal_eval('['+source.split('const selectionCode=[',1)[1].split('\n];',1)[0]+']')
        box((970,285,1810,815))
        for k,line in enumerate(lines):d.text((990,305+k*37),line,font=ImageFont.truetype(str(FONT/'DejaVuSansMono.ttf'),23),fill=INK)
        textlog.append('\n'.join(lines))
        note('Na web: vetor, código e índices animados. No PDF: resumo estático.')
        save('Selection Sort: execução animada com código')
        slides[-1]['part']='Selection Sort';slides[-1]['animation']='selection'
        continue
    if i==2:
        new('História do Selection Sort','MÉTODOS DE SELEÇÃO NOS PRIMEIROS COMPUTADORES')
        for y,year,name,body in [
            (290,'1956','Howard B. Demuth','Estudou métodos de ordenação\nem seu doutorado em Stanford.'),
            (480,'1956','Edward H. Friend','Publicou um estudo sobre\nordenação em computadores.'),
            (670,'1958','D. A. Bell','Também apresentou métodos\nrelacionados à ordenação.')]:
            text(106,y,year,52,True,TEAL);text(440,y,name,43,True);text(440,y+64,body,36)
        note('São registros históricos; não há um inventor único comprovado.')
        save('História do Selection Sort')
    elif i==7:
        new('Como funciona o Selection Sort','ENCONTRA O MENOR VALOR DA PARTE RESTANTE')
        for y,num,title,body in [
            (295,'1','Procurar o menor','Percorrer a parte ainda não ordenada e guardar o índice do menor.'),
            (475,'2','Colocar na posição','Trocar o menor com o início da parte ainda não ordenada.'),
            (655,'3','Avançar e repetir','A próxima busca começa uma posição à frente.')]:
            text(106,y,num,58,True,TEAL);text(245,y,title,43,True);text(245,y+70,body,35)
        note('A parte ordenada cresce uma posição a cada rodada.')
        save('Como funciona o Selection Sort')
    elif i==21:
        new('Complexidade do Selection Sort','MELHOR E PIOR CASO DA VERSÃO COM TROCA DIRETA')
        for x,label in zip([110,820,1320],['Algoritmo','Melhor caso','Pior caso']):text(x,296,label,36,True,TEAL)
        box((105,378,1800,480),'white')
        for x,label in zip([125,835,1335],['Selection Sort','Θ(n²)','Θ(n²)']):text(x,405,label,40,x==125)
        box((105,535,1800,725),PALE)
        text(142,565,'Mesmo com a entrada já ordenada',40,True,TEAL)
        text(142,635,'O algoritmo continua procurando o menor em toda a parte restante.',35)
        text(104,826,'A ordem inicial não muda a quantidade de comparações.',36)
        text(104,882,'Memória auxiliar da ordenação: Θ(1).',36)
        save('Selection Sort: complexidade')
    elif i==23:
        new('Selection Sort é estável?','NÃO GARANTE A ORDEM ORIGINAL DOS VALORES IGUAIS')
        text(105,279,'2A e 2B têm o mesmo valor. As letras identificam cada elemento.',35)
        for y,label,values in [(365,'Entrada',['2A','2B','1']),(535,'Após a troca',['1','2B','2A']),(705,'Resultado',['1','2B','2A'])]:
            text(105,y+32,label,37,True,TEAL)
            for j,value in enumerate(values):
                x=565+j*285;box((x,y,x+235,y+116),PALE if value in ['2A','2B'] else 'white')
                d.text((x+117,y+57),value,anchor='mm',font=font(48,True),fill=INK)
            textlog.append(label+': '+', '.join(values))
        text(105,873,'A troca colocou 2A depois de 2B.',37,True)
        text(105,940,'A versão com troca direta não preserva a ordem dos iguais.',31,False,MUTED)
        save('Estabilidade: Selection Sort não é estável')
    elif i==24:
        new('Selection: vantagens e desvantagens','POUCAS TROCAS, MAS MUITAS COMPARAÇÕES')
        for x,heading,items in [(105,'Vantagens',['Código curto e simples.','Memória auxiliar Θ(1).','No máximo n − 1 trocas.']),
                                (970,'Desvantagens',['Θ(n²) em todos os casos.','Não é estável.','Lento em vetores grandes.'])]:
            box((x,300,x+825,845),PALE if x==105 else 'white')
            text(x+40,340,heading,45,True,TEAL)
            for y,item in zip([440,550,680],items):text(x+40,y,item,35)
        note('Fazer poucas trocas não elimina o custo de procurar o menor.')
        save('Selection Sort: vantagens e desvantagens')
    else:
        title,subtitle,items=selection_content[i]
        new(title,subtitle)
        for y,(heading,body) in zip([300,495,690],items):
            text(105,y,heading,39,True,TEAL)
            text(105,y+70,body,33)
        save(title)
    slides[-1]['part']='Selection Sort'

comparison_start=len(slides)+1
new('Computador utilizado nos testes','DELL OPTIPLEX 3060')
specs=[
    ('Processador','Intel Core i5-8500T, 8ª geração'),
    ('Frequência base','2,10 GHz'),
    ('Núcleos e threads','6 núcleos e 6 threads'),
    ('Memória RAM','16 GB — 2 módulos de 8 GB'),
    ('Tecnologia da RAM','DDR4, 2400 MT/s'),
    ('Armazenamento','SSD NVMe ADATA SM2P41C3, 256 GB'),
    ('Sistema operacional','Ubuntu Server')]
for i,(label,value) in enumerate(specs):
    y=292+i*80
    if i%2==0:box((105,y-8,1800,y+64),'white')
    text(135,y+9,label,34,True,TEAL)
    text(650,y+9,value,34)
note('Configuração informada no relatório do trabalho.')
save('Computador utilizado nos testes');slides[-1]['part']='Comparação'

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
    table_rows=[]
    for row in sorted([r for r in selection_times if r['tipo']==kind],key=lambda r:int(r['n'])):
        shell_row=next(r for r in datasets['metades'] if r['tipo']==kind and r['n']==row['n'])
        table_rows.append([integer(row['n']),row['segundos_ordenacao'],shell_row['segundos_ordenacao']])
    result_table('Tabela de tempos — '+kindname,'SELECTION × SHELL POR METADES • TEMPO EM SEGUNDOS',
                 ['n','Selection Sort','Shell por metades'],table_rows,'','Comparação')

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

new('Bibliografia do Shell Sort','REFERÊNCIAS • ALGORITMO E SEQUÊNCIAS DE GAPS')
sources=[
 ('KNUTH, Donald E.','The Art of Computer Programming, v. 3: Sorting and Searching.','https://www-cs-faculty.stanford.edu/~knuth/taocp.html'),
 ('CIURA, Marcin (2001)','Best Increments for the Average Case of Shellsort.','https://doi.org/10.1007/3-540-44669-9_12'),
 ('SEDGEWICK, Robert (1986 e 1996)','Sequências de gaps e limites de complexidade.','https://sedgewick.io/wp-content/themes/sedgewick/papers/1986Shellsort.pdf'),
 ('VITÁNYI, Paul (2018)','On the average-case complexity of Shellsort. DOI: 10.1002/rsa.20737.','https://doi.org/10.1002/rsa.20737'),
 ('JIANG, Tao; LI, Ming; VITÁNYI, Paul (1999)','A Lower Bound on the Average-Case Complexity of Shellsort.','https://arxiv.org/abs/cs/9906008'),
 ('POONEN, Bjorn (1993)','The Worst Case in Shellsort and Related Algorithms.','https://math.mit.edu/~poonen/papers/shell.pdf')]
links=[]
for i,(name,desc,url) in enumerate(sources):
    y=275+i*107
    text(105,y,name,32,True,TEAL);text(105,y+45,desc,28)
    links.append(dict(x=5.4,y=y/10.8,w=88,h=9,target=url,label=name))
text(105,930,'Sedgewick: estudo de 1996',25,False,TEAL)
links.append(dict(x=5.4,y=86,w=34,h=4,target='https://sedgewick.io/wp-content/themes/sedgewick/papers/1996Shellsort.pdf',label='Sedgewick (1996)'))
text(850,930,'Princeton: implementação de Shell',25,False,TEAL)
links.append(dict(x=44,y=86,w=45,h=4,target='https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/Shell.html',label='Princeton: Shell'))
save('Bibliografia do Shell Sort',links)
slides[-1]['part']='Bibliografia'

# Sequência principal curta; todo o conteúdo restante continua no material de apoio.
new('Shell Sort: por subsequências','OUTRA FORMA DE PERCORRER OS GRUPOS DO MESMO GAP')
text(105,285,'Gap 4: cada linha é um grupo.',32,True,TEAL)
for r,values in enumerate([[8,6],[3,2],[7,5],[4,1]]):
    y=365+r*115;text(105,y+22,f'Grupo {r}',31,True,TEAL)
    for k,value in enumerate(values):
        x=320+k*240;box((x,y,x+195,y+90),['#D6EEE7','#E6EAF6','#F1E6D4','#EADFEA'][r])
        d.text((x+98,y+30),str(value),anchor='mm',font=font(35,True),fill=INK)
        d.text((x+98,y+68),f'índice {r+k*4}',anchor='mm',font=font(22),fill=MUTED)
source=(ROOT/'scripts/subsequence-animation.js').read_text(encoding='utf-8')
lines=ast.literal_eval('['+source.split('const subsequenceCode=[',1)[1].split('\n];',1)[0]+']')
box((970,285,1810,815))
for k,line in enumerate(lines):d.text((990,305+k*37),line,font=ImageFont.truetype(str(FONT/'DejaVuSansMono.ttf'),23),fill=INK)
textlog.append('\n'.join(lines))
text(105,865,'Ordenamos um grupo inteiro antes de passar para o próximo.',32)
note('Na web: inserção animada em cada grupo, com os índices do vetor original.')
save('Shell Sort: animação por subsequências');slides[-1]['animation']='subsequences'
new('Por que a análise do Shell é difícil?','EXISTEM PROVAS, MAS NEM TODOS OS CASOS ESTÃO RESOLVIDOS')
for y,num,title,body in [
    (275,'1','As passagens dependem umas das outras',
     'Cada gap reorganiza o vetor e muda o trabalho da passagem seguinte.'),
    (410,'2','A sequência de gaps faz diferença',
     'Já existem provas de melhor e pior caso para várias sequências.'),
    (545,'3','O caso médio ainda traz desafios',
     'Ainda faltam limites precisos para várias sequências usadas na prática.')]:
    text(105,y,num,48,True,TEAL);text(220,y,title,36,True);text(220,y+57,body,30)
box((105,690,1800,975),PALE)
text(140,712,'Poonen (1993): limite inferior do pior caso',35,True,TEAL)
formula_font=font(40)
formula_left='Ω(n ('
fraction_x=140+d.textlength(formula_left,font=formula_font)+10
fraction_width=d.textlength('log log n',font=formula_font)+16
d.text((140,781),formula_left,font=formula_font,fill=INK)
for formula_y,formula_label in [(755,'log n'),(806,'log log n')]:
    formula_width=d.textlength(formula_label,font=formula_font)
    d.text((fraction_x+(fraction_width-formula_width)/2,formula_y),formula_label,font=formula_font,fill=INK)
d.line((fraction_x,803,fraction_x+fraction_width,803),fill=INK,width=2)
d.text((fraction_x+fraction_width+10,781),')²)',font=formula_font,fill=INK)
textlog.append('Ω(n (log n / log log n)²)')
text(140,860,'Para qualquer sequência de gaps, existe uma entrada que exige pelo menos essa ordem de operações.',29)
text(140,902,'Logo, o Shell convencional não pode garantir pior caso O(n log n).',32,True)
save('Shell Sort: dificuldade da análise matemática')
new('Fontes: análise do Shell Sort','REFERÊNCIAS • CASO MÉDIO E PIOR CASO')
links=[]
references=[
    (285,'VITÁNYI, Paul (2018)',
     'On the average-case complexity of Shellsort.',
     'Random Structures & Algorithms, v. 52, n. 2, p. 354–363.',
     'DOI: 10.1002/rsa.20737','https://doi.org/10.1002/rsa.20737'),
    (505,'JIANG, Tao; LI, Ming; VITÁNYI, Paul',
     'A Lower Bound on the Average-Case Complexity of Shellsort.',
     'arXiv:cs/9906008 (1999); publicado no JACM em 2000.',
     'arxiv.org/abs/cs/9906008','https://arxiv.org/abs/cs/9906008'),
    (725,'POONEN, Bjorn (1993)',
     'The Worst Case in Shellsort and Related Algorithms.',
     'Journal of Algorithms, v. 15, n. 1, p. 101–124.',
     'math.mit.edu/~poonen/papers/shell.pdf','https://math.mit.edu/~poonen/papers/shell.pdf')]
for y,authors,title,venue,label,url in references:
    text(105,y,authors,35,True,TEAL);text(105,y+52,title,31)
    text(105,y+98,venue,27,False,MUTED);text(105,y+140,label,27,False,TEAL)
    links.append(dict(x=5.4,y=y/10.8,w=83,h=16,target=url,label=authors))
text(1470,425,'PDF no CWI',26,False,TEAL)
links.append(dict(x=76,y=39,w=17,h=4,target='https://ir.cwi.nl/pub/27188/Vit-nyi-2017-Random_Structures_-_Algorithms.pdf',label='Vitányi: PDF no CWI'))
save('Fontes da análise matemática do Shell Sort',links);slides[-1]['part']='Bibliografia'
new('Bibliografia do Selection Sort','HISTÓRIA • FUNCIONAMENTO • ANÁLISE')
links=[]
for y,author,description,label,url in [
    (285,'BEADLE, Alan (2021)',
     'Historical Origins of Data Structures and Algorithms, p. 24.',
     'University of Rochester • material da disciplina CSC 162',
     'https://www.cs.rochester.edu/u/hbeadle/csc162/_static/lectures/ds_history.pdf'),
    (450,'ASTRACHAN, Owen (2003)',
     'Bubble Sort: An Archaeological Algorithmic Analysis.',
     'SIGCSE • contexto histórico dos métodos de ordenação',
     'https://scholars.duke.edu/publication/758385'),
    (615,'KNUTH, Donald E. (1998)',
     'The Art of Computer Programming, v. 3: Sorting and Searching.',
     '2ª edição • seção 5.2.3: Sorting by Selection',
     'https://www-cs-faculty.stanford.edu/~knuth/taocp.html'),
    (780,'SEDGEWICK, Robert; WAYNE, Kevin',
     'Algorithms, 4th edition: documentação da classe Selection.',
     'Princeton • implementação e análise do Selection Sort',
     'https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/Selection.html')]:
    text(105,y,author,35,True,TEAL)
    text(105,y+51,description,31)
    text(105,y+99,label,28,False,MUTED)
    links.append(dict(x=5.4,y=y/10.8,w=88,h=13,target=url,label=author))
save('Bibliografia do Selection Sort',links);slides[-1]['part']='Bibliografia'
full_slides=slides[:]
# A bibliografia de análise do Shell foi reunida no slide de fontes do algoritmo.
full_slides.pop(62)
main_numbers=[1,2,3,4,5,61,6,7,8,62,9,10,12,14,28,30,35,36,43,45,46,50,51,52,54,56,58,59,60,63]
assert len(full_slides)==63
support_numbers=[n for n in range(1,len(full_slides)+1) if n not in main_numbers]
destinations={n:('main',main_numbers.index(n)+1) if n in main_numbers else ('support',support_numbers.index(n)+1) for n in range(1,len(full_slides)+1)}
for item in full_slides:
    for link in item.get('links',[]):
        if isinstance(link['target'],int):link['view'],link['target']=destinations[link['target']]
slides=[full_slides[n-1] for n in main_numbers]
support_slides=[full_slides[n-1] for n in support_numbers]
for deck in [slides,support_slides]:
    for number,item in enumerate(deck,1):
        frame=Image.open(io.BytesIO(base64.b64decode(item['image'].split(',',1)[1]))).convert('RGB')
        stamp=ImageDraw.Draw(frame);stamp.rectangle((1820,985,1900,1060),fill=BG)
        stamp.text((1832,1002),f'{number:02}',font=font(26),fill=MUTED)
        buffer=io.BytesIO();frame.save(buffer,format='PNG')
        item['image']='data:image/png;base64,'+base64.b64encode(buffer.getvalue()).decode()

css=(ROOT/'historico/selection-sort/dist/style.css').read_text(encoding='utf-8')
css+=(ROOT/'scripts/shell-animation.css').read_text(encoding='utf-8')
css+=(ROOT/'scripts/selection-animation.css').read_text(encoding='utf-8')
css+=(ROOT/'scripts/subsequence-animation.css').read_text(encoding='utf-8')
css+=(ROOT/'scripts/slide-visibility.css').read_text(encoding='utf-8')
for face,bold in [('DejaVuSans.ttf',400),('DejaVuSans-Bold.ttf',700)]:
    css+="@font-face{font-family:'DejaVu Sans';font-weight:"+str(bold)+";src:url(data:font/ttf;base64,"+base64.b64encode((FONT/face).read_bytes()).decode()+") format('truetype');}"
css+='\n#chapter{max-width:22vw}nav{gap:8px}.hotspot{padding:0}#transcript a{color:#008780}#transcript{font-family:Arial,sans-serif}nav select{font-size:14px}@media(max-width:700px){#chapter{max-width:26vw}#select{max-width:30vw}nav{gap:4px}nav button{padding:8px}#count{font-size:10px}}'
css+='\n#support-toggle{font-size:12px;white-space:nowrap}#select{max-width:32vw}@media(max-width:700px){#chapter{display:none}#support-toggle{font-size:10px;padding:6px}#select{max-width:30vw}}'
css+=(ROOT/'scripts/mobile.css').read_text(encoding='utf-8')
script='''
const image=document.querySelector('#image'), links=document.querySelector('#links'), select=document.querySelector('#select'), chapter=document.querySelector('#chapter');
let current=1;
let activeView='main';
const mainSlides=slides.slice();
function fillOptions(){ensureVisibleSlide();select.replaceChildren();slides.forEach((s,i)=>{const option=new Option(`${i+1}. ${s.title}${isSlideHidden(s)?' (oculto)':''}`,i+1);option.disabled=isSlideHidden(s);select.add(option)})}
function switchView(view){activeView=view;slides.splice(0,slides.length,...(view==='support'?supportSlides:mainSlides));fillOptions();document.querySelector('#support-toggle').textContent=view==='support'?'Voltar à apresentação':'Material de apoio';}
fillOptions();
function go(n){
 stopShell();stopSelection();stopSubsequence();document.querySelector('#shell-animation')?.remove();
 const requested=Math.max(1,Math.min(slides.length,Number(n)||1));const direction=requested>=current?1:-1;
 current=findVisibleSlide(slides,requested,direction)??findVisibleSlide(slides,requested,-direction)??1;const s=slides[current-1];
 document.querySelector('#slide').classList.toggle('animated',Boolean(s.animation));
 document.querySelector('#zoom').disabled=Boolean(s.animation);
 document.querySelector('main').scrollLeft=0;
 image.src=s.image;image.alt=s.title;links.replaceChildren();
 if(s.animation==='shell'){shellPosition=0;mountShell()}
 if(s.animation==='selection'){selectionPosition=0;mountSelection()}
 if(s.animation==='subsequences'){subsequencePosition=0;mountSubsequence()}
 s.links.forEach(l=>{const b=document.createElement(typeof l.target==='number'?'button':'a');b.className='hotspot';b.style.cssText=`left:${l.x}%;top:${l.y}%;width:${l.w}%;height:${l.h}%`;b.setAttribute('aria-label',l.label);b.title=l.label;if(typeof l.target==='number')b.onclick=()=>{if(l.view&&l.view!==activeView)switchView(l.view);go(l.target)};else {b.href=l.target;b.target='_blank';b.rel='noopener noreferrer'}links.append(b)});
 select.value=current;chapter.value=s.part==='Bibliografia'?'bibliografia':['Comparação','Conclusão'].includes(s.part)?'comparacao':s.part==='Shell Sort'?'shell':'selection';document.querySelector('#count').textContent=`${current} / ${slides.length}`;
 document.querySelector('#prev').disabled=findVisibleSlide(slides,current-1,-1)===null;document.querySelector('#next').disabled=findVisibleSlide(slides,current+1,1)===null;
 document.querySelector('#text').textContent=s.text;document.title=`${s.title} — Shell e Selection Sort`;history.replaceState(null,'',activeView==='support'?`#apoio-${current}`:`#slide-${current}`);
}
document.querySelector('#prev').onclick=()=>moveSlide(-1);document.querySelector('#next').onclick=()=>moveSlide(1);select.onchange=()=>go(select.value);chapter.onchange=()=>{const parts={shell:['Shell Sort'],selection:['Selection Sort'],comparacao:['Comparação','Conclusão'],bibliografia:['Bibliografia']};const index=slides.findIndex(s=>!isSlideHidden(s)&&parts[chapter.value].includes(s.part));if(index>=0)go(index+1)};
document.querySelector('#support-toggle').onclick=()=>{switchView(activeView==='main'?'support':'main');go(1)};
async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch{}}
document.querySelector('#full').onclick=fullscreen;
document.querySelector('#zoom').onclick=()=>{const expanded=document.querySelector('main').classList.toggle('zoomed');document.querySelector('#zoom').textContent=expanded?'Ajustar':'Ampliar';document.querySelector('#zoom').setAttribute('aria-pressed',String(expanded))};
document.addEventListener('keydown',e=>{if(document.querySelector('#visibility-dialog').open)return;if(e.key.toLowerCase()==='m'&&!['INPUT','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();openSlideManager();return}if(['SELECT','BUTTON','INPUT','A','SUMMARY'].includes(document.activeElement.tagName))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();moveSlide(1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();moveSlide(-1)}if(e.key==='Home')go(findVisibleSlide(slides,1,1));if(e.key==='End')go(findVisibleSlide(slides,slides.length,-1));if(e.key.toLowerCase()==='f')fullscreen()});
let touchStart=null;const slideSurface=document.querySelector('#slide');
slideSurface.addEventListener('touchstart',e=>{touchStart=null;if(e.touches.length!==1||e.target.closest('button,a,select,input,#shell-animation')||document.querySelector('main').classList.contains('zoomed'))return;touchStart={x:e.touches[0].clientX,y:e.touches[0].clientY}},{passive:true});
slideSurface.addEventListener('touchend',e=>{if(!touchStart)return;const dx=e.changedTouches[0].clientX-touchStart.x,dy=e.changedTouches[0].clientY-touchStart.y;touchStart=null;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.5)moveSlide(dx<0?1:-1)},{passive:true});
slideSurface.addEventListener('touchcancel',()=>touchStart=null,{passive:true});
function loadHash(){const view=location.hash.startsWith('#apoio-')?'support':'main';if(view!==activeView)switchView(view);go(location.hash.split('-')[1])}
setupSlideManager();window.addEventListener('hashchange',loadHash);loadHash();
'''
doc='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shell e Selection Sort</title><meta name="description" content="Shell Sort: história, gaps e resultados experimentais. Apresentação completa de Selection Sort."><style>'''+css+'''</style></head><body><main><div id="slide" aria-label="Apresentação"><img id="image" alt="" draggable="false"><div id="links"></div></div></main><nav aria-label="Navegação"><button id="prev" aria-label="Slide anterior">←</button><label for="chapter" class="sr">Parte da apresentação</label><select id="chapter"><option value="shell">Shell Sort</option><option value="selection">Selection Sort</option></select><label for="select" class="sr">Escolher slide</label><select id="select"></select><span id="count" aria-live="polite"></span><button id="next" aria-label="Próximo slide">→</button><button id="full" aria-label="Tela cheia" title="Tela cheia (F)">⛶</button></nav><details id="transcript"><summary>Texto do slide</summary><pre id="text"></pre><p>Setas: navegar · F: tela cheia · Home: início · End: último slide.</p></details><script>const SHELL_COUNT='''+str(offset)+';const slides='+json.dumps(slides,ensure_ascii=False).replace('</','<\\/')+';\n'+script+'</script></body></html>'
doc=doc.replace('<nav aria-label="Navegação">','<nav aria-label="Navegação"><button id="support-toggle">Material de apoio</button>')
doc=doc.replace('<button id="full"','<button id="zoom" aria-pressed="false" title="Ampliar slide e arrastar para ler">Ampliar</button><button id="full"')
doc=doc.replace('<button id="support-toggle">','<button id="manage-slides" title="Gerenciar slides (M)">Slides</button><button id="support-toggle">')
doc=doc.replace('<script>const SHELL_COUNT=', '<dialog id="visibility-dialog" aria-labelledby="visibility-title"><h2 id="visibility-title">Exibir ou ocultar slides</h2><p id="visibility-summary"></p><div id="visibility-list"></div><div class="visibility-actions"><button id="visibility-hide-current">Ocultar slide atual</button><button id="visibility-all">Exibir todos</button><button id="visibility-close">Concluir</button></div></dialog><script>const SHELL_COUNT=')
animation_script='const supportSlides='+json.dumps(support_slides,ensure_ascii=False).replace('</','<\\/')+';\n'
animation_script+=(ROOT/'scripts/shell-animation.js').read_text(encoding='utf-8')
animation_script+='\n'+(ROOT/'scripts/selection-animation.js').read_text(encoding='utf-8')
animation_script+='\n'+(ROOT/'scripts/subsequence-animation.js').read_text(encoding='utf-8')
animation_script+='\n'+(ROOT/'scripts/slide-visibility.js').read_text(encoding='utf-8')
animation_script='const SELECTION_COUNT='+str(selection_count)+';\n'+animation_script
doc=doc.replace(';\n'+script,';\n'+animation_script+'\n'+script)
doc=doc.replace('<option value="selection">Selection Sort</option>','<option value="selection">Selection Sort</option><option value="bibliografia">Bibliografia</option>')
doc=doc.replace('<option value="bibliografia">','<option value="comparacao">Comparação e conclusão</option><option value="bibliografia">')
dest=ROOT/'Shell_e_Selection_Sort.html';dest.write_text(doc,encoding='utf-8')
site_dir=ROOT/'site'
site_dir.mkdir(exist_ok=True)
(site_dir/'index.html').write_text(doc,encoding='utf-8')
(OUT/'app-check.js').write_text('const SHELL_COUNT='+str(offset)+';const slides=[];'+animation_script+'\n'+script,encoding='utf-8')
manifest=[dict(index=i+1,title=s['title'],part=s['part'],links=s['links']) for i,s in enumerate(slides)]
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(ROOT/'distribuicao/Shell_e_Selection_Sort_Web.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write(dest,dest.name)
    for path in (ROOT/'dados').glob('*.csv'):z.write(path,'dados/'+path.name)
with zipfile.ZipFile(ROOT/'distribuicao/site.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write(site_dir/'index.html','index.html')
assert len(full_slides)==offset+selection_count+4+comparison_count
assert all(1<=l['target']<=(len(support_slides) if l['view']=='support' else len(slides)) for s in full_slides for l in s['links'] if isinstance(l['target'],int))
assert all(s['part']=='Selection Sort' for s in full_slides[offset:offset+selection_count])
print(f'{len(slides)} slides principais + {len(support_slides)} de apoio. Links validados.')
print(dest)
