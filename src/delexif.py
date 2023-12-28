from PIL import Image
import PIL.ExifTags
import os
import sys


def cuenta_campos_exif(imagen):
    try:
        exif = {
            PIL.ExifTags.TAGS[k]: v
                for k, v in imagen._getexif().items()
                if k in PIL.ExifTags.TAGS
        }
        return len(exif)
    except AttributeError:
        return 0



ayuda = f"""
    {sys.argv[0]} crea una version de la imagen original pero sin datos exif.

    SINTAXIS:
    {sys.argv[0]} archivo_original.jpg archivo_destino.jpg

    {sys.argv[0]} -h/--help/--ayuda     imprime esta ayuda
"""

if len(sys.argv) == 2 and sys.argv[1] in ['-h','--help','--ayuda']:
    print(f'{ayuda}')
    sys.exit()

if len(sys.argv)<2 or not os.path.isfile(os.path.normpath(os.path.expanduser(sys.argv[1]))):
    print("falta un nombre de archivo valido")
    print(f'{ayuda}')
    sys.exit()

output='out.jpg'
if len(sys.argv)==3:
    output=sys.argv[2]


original = Image.open(sys.argv[1])
print(f"Datos exif en {sys.argv[1]} ... se encontraron {cuenta_campos_exif(original)}")

original.getexif().clear()
original.save(output)

copia = Image.open(output)
print(f"Datos exif de {output} ... se encontraron {cuenta_campos_exif(copia)}")

sys.exit()

