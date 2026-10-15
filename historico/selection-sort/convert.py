import zipfile, xml.etree.ElementTree as E, posixpath, json
from pathlib import Path
z=zipfile.ZipFile(r'C:/Users/arthur/Downloads/Selection_Sort_Ate_Slide_27 (1).pptx')
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
rid='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
def rels(path):
    parent,name=posixpath.split(path)
    rp=parent+'/_rels/'+name+'.rels'
    return {r.get('Id'):posixpath.normpath(posixpath.join(parent,r.get('Target'))) for r in E.fromstring(z.read(rp))} if rp in z.namelist() else {}
p=E.fromstring(z.read('ppt/presentation.xml')); pr=rels('ppt/presentation.xml')
paths=[pr[s.get(rid)] for s in p.findall('p:sldIdLst/p:sldId',ns)]
size=p.find('p:sldSz',ns); w,h=int(size.get('cx')),int(size.get('cy'))
slides=[]
for path in paths:
    root=E.fromstring(z.read(path)); rr=rels(path); texts=[t.text or '' for t in root.findall('.//a:t',ns)]; links=[]
    for shape in root.findall('.//p:sp',ns):
        link=shape.find('.//a:hlinkClick',ns); xf=shape.find('p:spPr/a:xfrm',ns)
        if link is None or xf is None: continue
        target=rr.get(link.get(rid)); action=link.get('action',''); dest=None
        if target in paths: dest=paths.index(target)+1
        elif 'nextslide' in action: dest=min(len(paths),len(slides)+2)
        elif 'previousslide' in action: dest=max(1,len(slides))
        elif 'firstslide' in action: dest=1
        elif 'lastslide' in action: dest=len(paths)
        if dest is None: continue
        off=xf.find('a:off',ns); ext=xf.find('a:ext',ns)
        if off is None or ext is None: continue
        label=' '.join(t.text or '' for t in shape.findall('.//a:t',ns)) or 'Ir para slide '+str(dest)
        links.append(dict(x=int(off.get('x'))/w*100,y=int(off.get('y'))/h*100,w=int(ext.get('cx'))/w*100,h=int(ext.get('cy'))/h*100,target=dest,label=label))
    slides.append(dict(title=texts[0] if texts else 'Selection Sort',text='\n'.join(texts),links=links))
Path('dist/data.js').write_text('const slides = '+json.dumps(slides,ensure_ascii=False)+';',encoding='utf-8')
print(len(slides),'slides;',sum(len(s['links']) for s in slides),'links')
