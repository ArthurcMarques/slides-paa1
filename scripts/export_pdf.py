"""Exporta o HTML completo em PDF, com um slide por página e links clicáveis."""
import base64
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'build/pdf-export-deps'))
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

source = (ROOT / 'Shell_e_Selection_Sort.html').read_text(encoding='utf-8')
support = '--apoio' in sys.argv
data = source.split('const supportSlides=' if support else 'const slides=', 1)[1]
slides, _ = json.JSONDecoder().raw_decode(data)
output = ROOT / ('output/pdf/Shell_e_Selection_Sort_Apoio.pdf' if support else 'output/pdf/Shell_e_Selection_Sort.pdf')
output.parent.mkdir(parents=True, exist_ok=True)
width, height = 960, 540
pdf = canvas.Canvas(str(output), pagesize=(width, height), pageCompression=1)
pdf.setTitle('Shell Sort e Selection Sort')
pdf.setSubject('Apresentação completa: funcionamento, resultados, comparação e conclusão')
pdf.setAuthor('Arthur Cardoso Marques e Antônio Calixto da Silva')
for index, slide in enumerate(slides, 1):
    pdf.bookmarkPage(f'slide-{index}')
    pdf.addOutlineEntry(f"{index}. {slide['title']}", f'slide-{index}', level=0)
    image = ImageReader(io.BytesIO(base64.b64decode(slide['image'].split(',', 1)[1])))
    pdf.drawImage(image, 0, 0, width=width, height=height)
    for link in slide.get('links', []):
        x = link['x'] / 100 * width
        y = height - (link['y'] + link['h']) / 100 * height
        rect = (x, y, x + link['w'] / 100 * width, y + link['h'] / 100 * height)
        target = link['target']
        if isinstance(target, int):
            if link.get('view','main') != ('support' if support else 'main'):
                other = 'Shell_e_Selection_Sort.pdf' if support else 'Shell_e_Selection_Sort_Apoio.pdf'
                pdf.linkURL(f'{other}#page={target}', rect, relative=1, thickness=0)
            else:
                pdf.linkAbsolute(link['label'], f'slide-{target}', Rect=rect, thickness=0)
        else:
            pdf.linkURL(target, rect, relative=0, thickness=0)
    pdf.showPage()
pdf.save()

# Confere quantidade, proporção, links e renderiza páginas representativas.
import pymupdf
from PIL import Image
doc = pymupdf.open(output)
assert len(doc) == len(slides)
assert all(abs(page.rect.width / page.rect.height - 16 / 9) < .001 for page in doc)
assert sum(len(page.get_links()) for page in doc) == sum(len(s.get('links', [])) for s in slides)
qa = ROOT / 'build/pdf-review'
qa.mkdir(parents=True, exist_ok=True)
indices = [0, 10, 11, len(slides) - 3, len(slides) - 1]
sheet = Image.new('RGB', (960, 540 * len(indices)), 'white')
for row, index in enumerate(indices):
    pix = doc[index].get_pixmap(matrix=pymupdf.Matrix(1, 1), alpha=False)
    pix.save(str(qa / f'page-{index + 1}.png'))
    sheet.paste(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), (0, row * 540))
sheet.save(qa / 'review.png')
print(f'PDF: {len(doc)} páginas 16:9; links verificados.')
print(output)
