import pypdfium2 as pdfium
from pathlib import Path
from PIL import Image
import img2pdf
import os

nombre_pdf = "fotobook.pdf"
nombre_pdf_comprimido = "comprimido.pdf"
nombre_pdf_sin_extension = Path(nombre_pdf).stem
escala = 2  # Escala para convertir PDF a imagen


"""
Extraer cada página del PDF como imagen
"""
pdf = pdfium.PdfDocument(nombre_pdf)
cantidad_paginas = len(pdf)
imagenes = []
for indice_pagina in range(cantidad_paginas):
    numero_pagina = indice_pagina+1
    nombre_imagen = f"{nombre_pdf_sin_extension}_{numero_pagina}.jpg"
    imagenes.append(nombre_imagen)
    print(f"Extrayendo página {numero_pagina} de {cantidad_paginas}")
    pagina = pdf.get_page(indice_pagina)
    imagen_para_pil = pagina.render(scale=escala).to_pil()
    imagen_para_pil.save(nombre_imagen)

imagenes_comprimidas = []
"""
Comprimir imágenes.
Entre menor calidad, menos peso del PDF resultante
"""
calidad = 20
for nombre_imagen in imagenes:
    print(f"Comprimiendo {nombre_imagen}...")
    nombre_imagen_sin_extension = Path(nombre_imagen).stem
    nombre_imagen_salida = nombre_imagen_sin_extension + \
        "_comprimida" + nombre_imagen[nombre_imagen.rfind("."):]
    imagen = Image.open(nombre_imagen)
    imagen.save(nombre_imagen_salida, optimize=True, quality=calidad)
    imagenes_comprimidas.append(nombre_imagen_salida)

"""
Escribir imágenes en un nuevo PDF
"""
print("Creando PDF comprimido...")
with open(nombre_pdf_comprimido, "wb") as documento:
    documento.write(img2pdf.convert(imagenes_comprimidas))

"""
Eliminar imágenes temporales
"""
for imagen in imagenes + imagenes_comprimidas:
    os.remove(imagen)
