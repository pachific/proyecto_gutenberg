import math
from libros import Libro


class Recomendador:
    def __init__(self, libros: list[Libro]) -> None:
        """
        libros: lista con instancias de tipo `Libro`
        """
        self.libros: list[Libro] = libros
        self._pesos: list[dict[str, float]] | None = None  # Se calcularan con un setter

    def set_pesos(self) -> None:
        """Calcula los pesos del algorítmo TF-IDF requeridos para las
        recomendaciones y los guarda en `self._pesos`
        """
        # 1. Obtenemos las frecuencias de cada libro
        frecuencias_libros = [libro.preprocesar_libro() for libro in self.libros]
        
        # 2. Calculamos la longitud total de tokens válidos por libro para el TF
        totales_palabras = [sum(frec.values()) for frec in frecuencias_libros]
        
        # 3. Construimos el vocabulario global unificado
        vocabulario_global = set()
        for frec in frecuencias_libros:
            vocabulario_global.update(frec.keys())
            
        # 4. Calculamos Document Frequency (DF): En cuántos libros sale cada palabra
        df: dict[str, int] = {palabra: 0 for palabra in vocabulario_global}
        for frec in frecuencias_libros:
            for palabra in frec:
                df[palabra] += 1
                
        # 5. Calculamos el Inverse Document Frequency (IDF) global
        num_documentos = len(self.libros)
        idf: dict[str, float] = {}
        for palabra in vocabulario_global:
            # Fórmula matemática de IDF usando logaritmo natural
            idf[palabra] = math.log(num_documentos / df[palabra])
            
        # 6. Construimos la matriz final de pesos TF-IDF
        self._pesos = []
        for frec, total in zip(frecuencias_libros, totales_palabras):
            pesos_documento: dict[str, float] = {}
            for palabra in vocabulario_global:
                if palabra in frec and total > 0:
                    tf = frec[palabra] / total
                    pesos_documento[palabra] = tf * idf[palabra]
                else:
                    pesos_documento[palabra] = 0.0
            self._pesos.append(pesos_documento)

    def get_pesos(self) -> list[dict[str, float]] | None:
        """Regresa los pesos calculados"""
        return self._pesos

    def _producto_punto(self, idx_1: int, idx_2: int) -> float:
        """Producto punto entre los libros con índices idx_1 y idx_2."""
        if not self._pesos:
            return 0.0
            
        vector_1 = self._pesos[idx_1]
        vector_2 = self._pesos[idx_2]
        
        # Sumamos la multiplicación término a término del espacio vectorial
        resultado = sum(vector_1[palabra] * vector_2[palabra] for palabra in vector_1)
        return resultado

    def _similitud(self, idx_1: int, idx_2: int) -> float:
        """Similitud entre los libros con índices idx_1 y idx_2 de acuerdo al
        coseno del ángulo que forman sus vectores.
        """
        prod_punto = self._producto_punto(idx_1, idx_2)
        
        # La norma o magnitud de un vector es la raíz cuadrada de su producto punto consigo mismo
        norma_1 = math.sqrt(self._producto_punto(idx_1, idx_1))
        norma_2 = math.sqrt(self._producto_punto(idx_2, idx_2))
        
        if norma_1 == 0.0 or norma_2 == 0.0:
            return 0.0
            
        # Fórmula de la Similitud Coseno
        return prod_punto / (norma_1 * norma_2)

    def mostrar_libros(self) -> None:
        """Mostrarle al usuario el índice y nombre para cada libro de acuerdo a
        nuestra lista de libros `self.libros`.
        """
        print("\n--- Catálogo de Libros en el Sistema ---")
        for indice, libro in enumerate(self.libros):
            print(f" [{indice}] -> {libro.name}")

    def resumen(self, idx_libro: int, num_palabras: int) -> list[str]:
        """Regresa una lista con las palabras más representativas de un libro
        de acuerdo a los pesos.
        """
        if not self._pesos:
            return []
            
        pesos_libro = self._pesos[idx_libro]
        
        # Ordenamos las palabras del vocabulario basándonos en su peso de mayor a menor
        palabras_ordenadas = sorted(
            pesos_libro.keys(), 
            key=lambda palabra: pesos_libro[palabra], 
            reverse=True
        )
        return palabras_ordenadas[:num_palabras]

    def libros_similares(self, idx_libro: int, num_libros: int) -> list[str]:
        """Regresa una lista con los libros más parecidos a un libro dado."""
        listado_similitudes: list[tuple[int, float]] = []
        
        for i in range(len(self.libros)):
            if i != idx_libro:
                valor_coseno = self._similitud(idx_libro, i)
                listado_similitudes.append((i, valor_coseno))
                
        # Ordenamos la lista de mayor a menor basándonos en el valor del coseno
        listado_similitudes.sort(key=lambda item: item[1], reverse=True)
        
        # Extraemos los nombres de los libros ganadores
        libros_recomendados = [
            self.libros[item[0]].name for item in listado_similitudes[:num_libros]
        ]
        return libros_recomendados