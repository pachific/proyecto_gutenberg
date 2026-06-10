import re
import requests
from bs4 import BeautifulSoup

def get_links(n: int | list[int] = -1) -> tuple[ list[str], list[str] ]:
    """Obtiene los urls y los nombres de los libros del proyecto de Gutenberg
    deseados.

    Los libros se encuentran en formato txt bajo la sección descargados
    frecuentemente en:
        https://www.gutenberg.org/browse/scores/top.

    Los números `n` deben corresponder a los números en esta lista (empezando
    con uno).

    Parameters
    ----------
    n : int | list[int], optional
        Un entero o lista de enteros con los números de libros deseados.
        Escoge -1 (default) si se desean todos los libros.

    Returns
    -------
    links : list[str]
        Ligas a los archivos txt de los libros.
    titles : list[str]
        Títulos de los libros.
    """
    # Los libros top en el proyecto Gutenberg se encuentran aquí:
    url = "https://www.gutenberg.org/browse/scores/top"
    try:
        response = requests.get(url)

        # Parsear el contenido con BeautifulSoup
        parser = BeautifulSoup(response.text, 'html.parser')

        # Obten las ligas de los libros y sus nombres
        links = []
        titles = []

        # 1. Buscamos el encabezado exacto del Top 100
        encabezado = parser.find('h2', string=re.compile("Top 100 EBooks yesterday"))
        
        if not encabezado:
            return links, titles
            
        # La lista de libros es el primer <ol> después de ese encabezado
        lista_ol = encabezado.find_next_sibling('ol')
        enlaces = lista_ol.find_all('a')

        # 2. Lógica para manejar el parámetro 'n'
    
    indices = []
        if n == -1:
            indices = list(range(len(enlaces)))
        elif isinstance(n, int):
            indices = [n - 1] 
        else:
            indices = [i - 1 for i in n]

        # 3. Extracción de datos
        for i in indices:
            if 0 <= i < len(enlaces):
                etiqueta = enlaces[i]
                
                # --- Procesamiento del Título ---
                texto_crudo = etiqueta.text.strip()
                nombre_base = texto_crudo.rsplit(" (", 1)[0]
                nombre_limpio = "".join(c for c in nombre_base if c.isalnum() or c in " -_")
                titles.append(f"{nombre_limpio}.txt")
                
                # --- Procesamiento de la Liga ---
                href = etiqueta.get('href', '')
                id_match = re.findall(r'\d+', href)
                
                if id_match:
                    id_libro = id_match[0]
                    link_txt = f"https://www.gutenberg.org/cache/epub/{id_libro}/pg{id_libro}.txt"
                    links.append(link_txt)

        return links, titles

    except requests.exceptions.RequestException as e:
        print("wrong url for Gutenberg project")
        return [], []

def download_file(url, name, directory):
    """Guarda un archivo que se encuentra en un `url` bajo el nombre que demos
    en `name` en el directorio deseado.
    """
    response = requests.get(url, stream=True)
    name = directory + name
    with open(name, mode='wb') as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):  #10kb chunks
            file.write(chunk)
    print(f"Downloaded file: {name}")

def store_files(links, names, directory='./'):
    """Guarda cada liga de la lista de ligas `links` en la computadora
    utilizando el directorio deseado y cada uno de los nombres en names.
    """
    for url, name in zip(links, names):
        download_file(url, name, directory)

def main(n = -1, directory='./'):
    links, titles = get_links(n)
    store_files(links, titles, directory)
    print("Done")

if __name__ == '__main__':
    directory = 'Books/'
    n = range(1, 6)
    main(n, directory)
