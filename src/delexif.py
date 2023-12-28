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


licencias = dict()
licencias['gplv3'] = """    delexif.py  Copyright (C) 2023  Cristian Tocci
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

    {sys.argv[0]} -g                    informacion de licencia
    {sys.argv[0]} -w                    mas detalles de licencia
    {sys.argv[0]} -l/--gplv3logo        Un lindo logo de la GPLV3 en ASCII
"""

if len(sys.argv) == 2 and sys.argv[1] in ['-h','--help','--ayuda']:
    print(f'{ayuda}')
    sys.exit()

if len(sys.argv) == 2 and sys.argv[1] == "-g":
    print(f"{licencias['gplv3']}")
    sys.exit()

if len(sys.argv) == 2 and sys.argv[1] == "-w":
    print(f"{licencias['textow']}")
    sys.exit()

if len(sys.argv) == 2 and sys.argv[1] in ["-l","--gplv3logo"]:
    print(f"{licencias['gplv3logo']}")
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

