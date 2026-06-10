import os
from pathlib import Path
from string import punctuation
import nltk

# Aseguramos la descarga de las stopwords de nltk de manera silenciosa
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords


class Libro:
    def __init__(self, name: str, filename: str) -> None:
        """Crear atributos públicos"""
        self._name = ""
        self._filename = ""
        
        # Ejecutamos las validaciones a través de los setters
        self.name = name
        self.filename = filename
        
        self.CARACTERES_ESPECIALES: str | None = None
        self.STOPWORDS: set[str] | None = None

    @property
    def name(self) -> str:
        """Regresa el nombre del libro."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Checar que el nombre sea un string"""
        if not isinstance(value, str):
            raise TypeError("El nombre del libro debe ser una cadena de texto (str).")
        self._name = value

    @property
    def filename(self) -> str:
        """Regresa la ruta o nombre del archivo."""
        return self._filename

    @filename.setter
    def filename(self, value: str) -> None:
        """Checar que el nombre sea un string y que el archivo existe"""
        if not isinstance(value, str):
            raise TypeError("El filename debe ser una cadena de texto (str).")
        if not os.path.exists(value):
            raise FileNotFoundError(f"El archivo especificado no existe en la ruta: {value}")
        self._filename = value

    def _limpiar_linea(self, linea: str) -> str:
        """Este método toma una línea de texto (str) y elimina los caracteres
        en `self.CARACTERES_ESPECIALES`.
        """
        if self.CARACTERES_ESPECIALES:
            for caracter in self.CARACTERES_ESPECIALES:
                linea = linea.replace(caracter, '')
        return linea

    def _limpiar_tokens(self, tokens: list[str]) -> list[str]:
        """Este método recibe una lista de palabras (`tokens`) y elimina
        aquellas que se encuentran en `self.STOPWORDS` modificando la lista
        original. (regresa lista de palabras sin stopwords)
        """
        if self.STOPWORDS:
            # Modificación in-place usando rebanado de lista completo [:]
            tokens[:] = [t for t in tokens if t not in self.STOPWORDS]
        return tokens

    def _preprocesar_linea(self, linea: str) -> list[str]:
        """Limpia una línea de texto regresando tokens limpios. La limpieza
        debe considerar eliminar espacios blancos al principio y final de la
        línea, convertir a minúsculas, eliminar caracteres especiales, crear
        tokens y eliminar stopwords en estos tokens.
        """
        # eliminar espacios blancos al principio y final de la línea
        linea_recortada = linea.strip()
        
        # convierte la linea a minúsculas
        linea_minusculas = linea_recortada.lower()
        
        # elimina los caracteres especiales
        linea_limpia = self._limpiar_linea(linea_minusculas)
        
        # obten tokens: transforma la linea en una lista de palabras
        tokens_crudos = linea_limpia.split()
        
        # limpia la lista de tokens quitando stopwords
        tokens_finales = self._limpiar_tokens(tokens_crudos)
        return tokens_finales

    def leer_libro(self) -> list[str]:
        """Lee cada línea del libro en `self.filename`, agregando aquellas que
        no esten vacías a una lista.
        """
        lineas_no_vacias = []
        with open(self.filename, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():
                    lineas_no_vacias.append(linea)
        return lineas_no_vacias

    def preprocesar_libro(self) -> dict[str, int]:
        """Regresa un diccionario de palabras relevantes del libro como llaves
        (los tokens limpios) y sus respectivas frecuencias como valores.
        """
        frecuencias: dict[str, int] = {}
        lineas = self.leer_libro()
        
        for linea in lineas:
            tokens = self._preprocesar_linea(linea)
            for token in tokens:
                frecuencias[token] = frecuencias.get(token, 0) + 1
        return frecuencias

    def __str__(self) -> str:
        """Regresa la representación de este objeto en forma de un string."""
        return f"Libro: {self.name} (Archivo: {self.filename})"

    def __repr__(self) -> str:
        """Regresa la representación formal del objeto."""
        return f"Libro(name={self.name!r}, filename={self.filename!r})"


# Los libros del proyecto Gutenberg empiezan dando información sobre el
# copyright y los créditos. El contenido se encuentra después de una línea que
# inicia con `*** START` y antes de la linea `*** END`. Esto debe
# considerarse al momento de leer el libro. Por lo tanto, reescribimos el
# método copprespondiente.
class LibroGutenberg(Libro):
    def leer_libro(self) -> list[str]:
        """Lee cada línea del libro en `self.filename`, agregando aquellas que
        no esten vacías a una lista. Además, empieza a agregar solo despues de
        la línea que comienza con `*** START` y antes de la línea `*** END`.
        """
        lineas_filtradas = []
        dentro_del_texto = False
        
        with open(self.filename, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                # El prólogo legal termina al encontrar *** START
                if linea.startswith('*** START'):
                    dentro_del_texto = True
                    continue
                # El epílogo legal empieza al encontrar *** END
                if linea.startswith('*** END'):
                    break
                
                # Si estamos en la zona de la novela, guardamos las líneas que tengan contenido
                if dentro_del_texto:
                    if linea.strip():
                        lineas_filtradas.append(linea)
                        
        return lineas_filtradas


# Los libros en distintos idiomas tienen distintos `STOPWORDS`.
class LibroEnglish(LibroGutenberg):
    def __init__(self, name: str, filename: str) -> None:
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en ingles (utiliza nltk).
        self.STOPWORDS = set(stopwords.words('english'))


class LibroSpanish(LibroGutenberg):
    def __init__(self, name: str, filename: str) -> None:
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en español (utiliza nltk).
        self.STOPWORDS = set(stopwords.words('spanish'))


class LibroFrench(LibroGutenberg):
    def __init__(self, name: str, filename: str) -> None:
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en francés (utiliza nltk).
        self.STOPWORDS = set(stopwords.words('french'))


# La siguiente función asume que todos los libros se encuentran en el
# directorio `directory`, tienen extensión `txt` y todos son en inglés.
def crear_lista_libros_ingles(directory: str, caract_especiales=punctuation):
    """Crea una lista de instancias `LibroEnglish` a partir de libros
    localizados en `directory`.

    No ocupas modificar esta función, se encuentra ya implementada.
    """
    libros = []
    path = Path(directory)
    for file in path.glob('*.txt'):
        filename = str(file.relative_to(path.parent))
        libro = LibroEnglish(file.name, filename)
        libro.CARACTERES_ESPECIALES = caract_especiales
        libros.append(libro)
    return libros