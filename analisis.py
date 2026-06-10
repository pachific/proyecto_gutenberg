import re
import os

def tokenize(text: str) -> list[str]:
    """ Limpiando el texto"""
    #Convertir todo el texto a minúsculas
    text_lowercase = text.lower()
    
    #  Eliminar puntuación y caracteres especiales, dejando solo letras y espacios
    text_clean = re.sub(r'[^a-z\s]', '', text_lowercase)
    
    #Separar el texto por sus espacios en blanco
    tokens = text_clean.split()
    
    return tokens

def build_vocabulary(directory:str) -> list[str]:#[^a-z\s] elimina todo lo que no sea una letra o espacio.
    """lee todos los archivos, los tokeniza y crea el vocabulario"""
    vocabulario_global = set()
    archivos = os.listdir(directory)

    print("hacinedo vocabulario global")
    for archivo in archivos:
        if archivo.endswith('.txt'):
           ruta_completa = os.path.join(directory, archivo)

           with open(ruta_completa, 'r', encoding='utf-8') as f:
                 contenido = f.read()

           #llamamos a  la funcion tokenize
           tokens_libro = tokenize(contenido)
           vocabulario_global.update(tokens_libro)
           print(f" -> Procesado con éxito: {archivo}")
            
    return sorted(list(vocabulario_global))

# Bloque para probar que todo funcione junto
if __name__ == "__main__":
    carpeta_libros = "Books/"
    
    #Creamos el vocabulario usando los libros de la carpeta
    mi_vocabulario = build_vocabulary(carpeta_libros)
    
    print("\n Vocabulario Creado")
    print(f"Numero de palabras unicas totales en el proyecto: {len(mi_vocabulario)}")
    print("Primeras 15 palabras ordenadas alfabticamente:")
    print(mi_vocabulario[:15])
# Bloque de prueba
 
if __name__ == "__main__":
    carpeta = "Books/"
    
    # Listamos los archivos y hagarro el primero
    archivos = os.listdir(carpeta)
    if archivos:
        primer_libro = os.path.join(carpeta, archivos[0])
        
        print(f"Abriendo y tokenizando: {primer_libro}\n")
        
        # Leemos el archivo 
        with open(primer_libro, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        # Tokenizamos
        mis_tokens = tokenize(contenido)
        
        # Mostramos los resultados
        print(f"Número total de palabras (tokens) encontradas: {len(mis_tokens)}")
        print("Primeros 20 tokens del libro:")
        print(mis_tokens[:20])
    else:
        print("No se encontraron libros en la carpeta.")
