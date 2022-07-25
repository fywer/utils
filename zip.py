from zipfile import ZipFile,ZipInfo
import os,sys,logging
from threading import Thread,Lock
import subprocess

slogan = '''
\t\t\t\t\t
\t ______     # ________     # ______    #
\t/_____/\    #/_______/\    #/_____/\   #
\t\:::__\/    #\__.::._\/    #\:::_ \ \  #
\t   /: /     #   \::\ \     # \:(_) \ \ #
\t  /::/___   #   _\::\ \__  #  \: ___\/ #
\t /_:/____/\ #  /__\::\__/\ #   \ \ \   #
\t \_______\/ #  \________\/ #    \_\/   #
\t            ##              ##          ##
\t\t\t   ╔══════════╗ 
\t\t\t   ║  by JN♥  ║ 
\t\t\t   ╚══════════╝
'''

sys.stdout.write(slogan)

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(levelname)7s %(asctime)s %(message)s',
    stream = sys.stderr
)
log = logging.getLogger('')

class Proceso(Thread):
    def __init__(self, objeto, nombre):
        Thread.__init__(self)
        self.__zip = objeto
        self.nombre = nombre

    def getNombre(self):
        return self.nombre
        
    def getZip(self):
        return self.__zip
        
    def run(self):
        nombre = self.getNombre()
        zip = self.getZip()
        try:
            log.info("Se ha iniciado el proceso del archivo: {0}".format(nombre)) 
            zip.extractall(os.getcwd())
            zip.close()
            
            log.info("Eliminando archivo {0} coprimido.".format(nombre))
            comandos = ("DEL", nombre)
            #ps = subprocess.Popen(comandos, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            ps = subprocess.run(comandos, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            error = ps.stderr.decode('ISO-8859-1')
            if len(error) > 1:
                log.warning("{0}\n".format(error))
                log.info("No se ha podido eliminar el archivo: {0}\n".format(nombre))
            else:
                #os.system("DEL {0}".format(nombre))
                log.info("Se ha eliminado el archivo {0}".format(nombre))
                log.info("Se ha finalizado el proceso del archivo: {0}\n".format(nombre))
        
        except Exception as e:
            log.warning("{0} {1}\n".format(nombre, e))
    
class Zipper:
    def __init__(self):
        self.directorio = os.getcwd()
    
    def getDirectorio(self):
        return self.directorio
        
    def descomprimir(self):
        directorio = self.getDirectorio()
        log.info("Escaneando directorio: {0}".format(directorio))
        try:
            items = os.scandir(directorio)
            for nombre in [arch.name for arch in items if arch.is_file()]:
                tipo = nombre.split('.')[1]
                if tipo not in ('zip','ZIP'):
                    log.warning("El tipo de archivo: {0} no ha sido reconocido.".format(tipo))
                    pass
                else:
                    zip = ZipFile(self.getDirectorio()+"\\"+nombre)
                    proceso = Proceso(zip, nombre)
                    proceso.start()
                    #proceso.join()
        except Exception as e:
            log.warning("{0} {1}\n".format(nombre, e))
            pass

zip = Zipper()
zip.descomprimir()
sys.stdout.write("\nEl sistema esta procesando...\n\n")