#   Este programa genera una copia sin exif del archivo de imagen original
#   Copyright (C) 2023 Cristian Tocci
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#   Contacto : toccicristian@hotmail.com / toccicristian@protonmail.ch


from PIL import Image
import PIL.ExifTags
import os
import sys
from tkinter import filedialog
import tkinter as tk

licencias = dict()
licencias['gplv3'] = """    delexif-gui.py  Copyright (C) 2023  Cristian Tocci
    This program comes with ABSOLUTELY NO WARRANTY; for details press 'w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; See COPYING.odt file for further details.
"""
licencias['gplv3logo'] = """
+----------------------------------------------------------------------------------------------------+
|oooooooo+~~~+~~~~~~+~~~~~+~~~~+~~~~~~+~~~~+~~~~~~+~~+~~~~+~~~~~+~~~~+~~~~~~++~~+~~+~~~~~~:  ::::::~+|
|oooooooo :::::::::::::::::::::::::::::::::::::::::::~::::::::::::::::::::::::::::::::. ~~~++ooooo+:.|
|ooooooo~::::::~:::::::::::::::::::::::::::::::::::::+::::::::::::::::::::::::~~.~:~:~+oooooooooooo:.|
|ooooooo :~:~~~~~~~~~~+~::: +~~~~~~~~~~~~~::++ :::::~+~:::::::::::::::::::~...~:::~ooooooooooooooo~.+|
|oooooo~~:~oo~~~~~~~~~oo~:~+oo ~~~~~~.ooo.~oo+~::::.+o ::::::::::::::::~  .~::::+oo+~:   +ooooooo::+o|
|oooooo::.+o+~::::::~+oo : oo~::::::::oo~:~oo~::::: oo~:::::::::::::: ~ ~::::.++~ ~:::::.+oooo+~ ~ooo|
|ooooo+~:~oo~:::::::::::::~oo::::::::+oo :+oo~:::::~oo+.::::::::::.:~ ~:::::: .:::::::~~oooo+:~ +oooo|
|ooooo::~+o+.:::::::::::: oo+~:::::: oo~~:oo~::::::~ooo~::::::::.~~.::::::::::::::::~~+oooooo+~::oooo|
|oooo+~::oo~:::~:~:~~::::~oo~       ~oo::+oo.::::::~ooo+~::::: ~~.:::::::::::::::: ~+oooooooooo~~oooo|
|oooo~::+oo :::~   +oo::.ooo~~~~~~~~~:.: oo+:::::::~oooo~:::~~+:::::::::::::::: ~+++~~~~oooooo+.~oooo|
|ooo+.: oo~:::::::.oo+.:~oo~::::::::::::~oo:::::::::oooo+~::++~::::::::::::::~   .::::::ooooo~.~ooooo|
|ooo~::~oo::::::::~oo~:~+o+~::::::::::: oo+~:::::::.+ooo~.~o+:::::::::::::::::::::::: +oooo+: +oooooo|
|ooo.: oo+.~~~~~~ +oo.::oo~::::::::::::~oo~~~~~~~:::+oo~ +oo ::::::::::::::::::::.:~ooooo+: ~oooooooo|
|oo~::.~~~~~~~~~~~~~ ::~+~.::::::::::::~+~~~~~~~~~:::o~ +ooo:::::::::::::::::: ~+oooooo~::~oooooooooo|
|o+ :~   ~::::::::::::.  ~::::: ..:::::::::::::::::::~ ~oooo~~::::::::::~. ~~+oooooo+~::+oooooooooooo|
|o~~:~~: ~ :~~. ~~.::~~~~. ::.~~~~::~:: :~~.~::~~ ::::.oooooo+~~::::~~~~ooooooooo+~::~+oooooooooooooo|
|o::~~~~:::~~~ ~~~.:: ::~.~:~.~~~: ~~~ :~~~: ~~~~~:::: oooooooooooooooooooooo++~::~+ooooooooooooooooo|
|+:::~::::::~~::::::::~~:::~::~:::::::::::~::::~:::::::~ooooooooooooooooo++~::~~+oooooooooooooooooooo|
|::::::::::::::::::::::::::::::::::::::::::::::::::::::: ~oooooooooo+~~~::~~+oooooooooooooooooooooooo|
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:~~~~~:    ::::::::~~~ooooooooooooooooooooooooooooo|
+----------------------------------------------------------------------------------------------------+
"""

licencias['textow'] = """ 
    15. Disclaimer of Warranty.
    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY 
    APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT 
    HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT 
    WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT 
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
    PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE 
    OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU 
    ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
    
    16. Limitation of Liability.
    IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING 
    WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR 
    CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR 
    DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL 
    DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM 
    (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED 
    INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF 
    THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER 
    OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

    17. Interpretation of Sections 15 and 16.
    If the disclaimer of warranty and limitation of liability provided above 
    cannot be given local legal effect according to their terms, 
    reviewing courts shall apply local law that most closely approximates 
    an absolute waiver of all civil liability in connection with the Program, 
    unless a warranty or assumption of liability accompanies a copy of 
    the Program in return for a fee.
    """



jpg_salida_defaultdir='~'
jpg_salida_default='out.jpg'


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


def es_imagen(path):
    try:
        tmp = Image.open(path)
        tmp.close()
        return True
    except PIL.UnidentifiedImageError:
        return False


def quita_exif(entry_origen, entry_destino, logbox):
    errores=''
    if not os.path.isfile( os.path.normpath(os.path.expanduser( entry_origen.get()  ))  ):
        errores+="No se especificó un archivo original válido.\n"

    if not os.path.isdir( os.path.normpath(os.path.expanduser( os.path.split(entry_destino.get())[0]  ))  ):
        errores+="No se especificó un directorio de destino existente.\n"

    if len (os.path.split(entry_destino.get())[1])==0:
        errores+="No se especificó un nombre de archivo de destino para el resultado\n"

    if len(errores)>0:
        loguea(logbox,errores)
        return None

    original = Image.open(entry_origen.get())
    loguea(logbox,f"Datos exif originales:{cuenta_campos_exif(original)}\n")
    original.getexif().clear()

    destino=entry_destino.get()
    if not destino.lower().endswith('.jpg'):
        destino=destino+'.jpg'

    original.save(os.path.normpath(os.path.expanduser(destino)))
    copia = Image.open(os.path.normpath(os.path.expanduser(destino)))
    loguea(logbox,f"Datos exif en copia:{cuenta_campos_exif(copia)}\n")
    return None


def loguea(logbox, linea=str()):
    logbox.configure(state='normal')
    logbox.insert(tk.END, linea)
    logbox.see(tk.END)
    logbox.configure(state='disabled')


def file_browser():
    tipos = (('archivos de imagen', '*.png *.jpg *.jpeg *.JPG *.JPEG .PNG'),
             ('Todos los archivos', '*.*'))
    archivo_url = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                            title='Seleccionar Imagen...',
                                            filetypes=tipos)
    return archivo_url


def directory_browser(titulo="Seleccione directorio destino...", defaultdir=str()):
    directorio = filedialog.askdirectory(title=titulo)
    if not directorio:
        directorio = defaultdir
    return os.path.expanduser(os.path.normpath(directorio))


def examinar_imagen(entry_imagen):
    archivo_url = entry_imagen.get()
    archivo_url = file_browser()
    entry_imagen.delete(0,tk.END)
    entry_imagen.insert(0, archivo_url)


def examinar_dir(entry_url):
    head_url = os.path.expanduser(os.path.normpath(jpg_salida_defaultdir))
    tail_url = os.path.expanduser(os.path.normpath(jpg_salida_default))
    if len(entry_url.get()) != 0:
        head_url = os.path.split(os.path.normpath(os.path.expanduser(entry_url.get())))[0]
        tail_url = os.path.split(os.path.normpath(os.path.expanduser(entry_url.get())))[1]
    directorio_seleccionado = directory_browser('Seleccione directorio para ' + tail_url, head_url)
    entry_url.delete(0, tk.END)
    if not directorio_seleccionado:
        directorio_seleccionado = head_url
    entry_url.insert(tk.END, os.path.join(directorio_seleccionado, tail_url))
    return


def show_w(ventana_principal, textow):
    ventana_w = tk.Toplevel(ventana_principal)
    ventana_w.title('This program comes with ABSOLUTELY NO WARRANTY')
    ventana_w.geometry('800x600')
    tk.Label(ventana_w, text=textow).pack()
    ventana_w.focus_set()
    ventana_w.bind('<Escape>', lambda event: ventana_w.destroy())


def ayuda(ventana_principal):
    texto_ayuda = """
        F1 : Esta ayuda.
        w : Más acerca de la licencia
        Esc : Cierra la aplicación / Cierra esta ventana
        """
    ventana_ayuda = tk.Toplevel(ventana_principal)
    ventana_ayuda.title(' Atajos y ayuda')
    tk.Label(ventana_ayuda, text=texto_ayuda, justify='left').pack(side=tk.LEFT, padx=(0, 30), pady=(10, 10))
    ventana_ayuda.focus_set()
    ventana_ayuda.bind('<Escape>', lambda event: ventana_ayuda.destroy())


def muestra_ventana():
    v = tk.Tk()
    v.geometry("600x400")
    v.title("DELEXIF-GUI")

    #       DEFINICIONES
    l_ayuda=tk.Label(v, text="F1 - ayuda")
    f_origen=tk.Frame(v)
    l_origen=tk.Label(f_origen, text="Original:")
    f_ruta_origen=tk.Frame(f_origen)
    e_origen=tk.Entry(f_ruta_origen,width=53)
    b_origen=tk.Button(f_ruta_origen, text="Examinar...", command=lambda: examinar_imagen(e_origen))

    f_destino=tk.Frame(v)
    l_destino=tk.Label(f_destino, text="Copia a crear:")
    f_ruta_destino=tk.Frame(f_destino)
    e_destino=tk.Entry(f_ruta_destino,width=53)
    e_destino.delete(0, tk.END)
    e_destino.insert(tk.END, os.path.join(
                                        os.path.normpath(os.path.expanduser(jpg_salida_defaultdir)),
                                        os.path.normpath(os.path.expanduser(jpg_salida_default)) ))
    b_destino=tk.Button(f_ruta_destino, text="Examinar...",command=lambda: examinar_dir(e_destino))

    f_abajo=tk.Frame(v)
    logbox=tk.Text(f_abajo, height=4, width=50, font=("System",8), state="disabled")
    sb_logbox=tk.Scrollbar(f_abajo)
    b_delexif=tk.Button(text="DEL-EXIF!", command=lambda: quita_exif(e_origen,e_destino, logbox))

    #       PACKS
    l_ayuda.pack   (side=tk.TOP, pady=(5,5), padx=(10,10), anchor=tk.W)
    f_origen.pack  (side=tk.TOP, fill = tk.BOTH, expand = tk.YES, pady=(10, 10), padx=(10,10))
    l_origen.pack  (side=tk.TOP)
    f_ruta_origen.pack (side=tk.TOP)
    e_origen.pack(side=tk.LEFT)
    b_origen.pack(side=tk.LEFT, padx=(15,15))

    f_destino.pack (side=tk.TOP, fill = tk.BOTH, expand = tk.YES, pady=(10, 10), padx=(10,10))
    l_destino.pack (side=tk.TOP)
    f_ruta_destino.pack (side=tk.TOP)
    e_destino.pack (side=tk.LEFT)
    b_destino.pack (side=tk.LEFT, padx=(15,15))

    #               LOGBOX CON SCROLLBAR
    f_abajo.pack   (side=tk.TOP, fill = tk.BOTH, expand = tk.YES, pady=(10, 20), padx=(20,20))
    logbox.pack    (side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    sb_logbox.pack (side=tk.RIGHT, fill=tk.BOTH)
    logbox.config  (yscrollcommand=sb_logbox.set)
    sb_logbox.config (command=logbox.yview)

    b_delexif.pack(side=tk.RIGHT, pady=(10,20), padx=(10,20))


    #####################################################################################
    #               BINDEOS:
    #####################################################################################
    v.bind('<F1>', lambda event: ayuda(v))
    v.bind('<w>', lambda event: show_w(v, licencias['textow']))
    v.bind('<Escape>', lambda event: v.destroy())

    loguea(logbox,f"{licencias['gplv3']}")
    v.mainloop()
    return None

muestra_ventana()

