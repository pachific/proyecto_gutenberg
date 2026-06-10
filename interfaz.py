import os
from libros import crear_lista_libros_ingles
from recomendaciones import Recomendador


def iniciar_consola() -> None:
    """Maneja el flujo de interaccion con el usuario en la terminal."""
    carpeta_origen = "Books/"
    
    # Validacion inicial de seguridad
    if not os.path.exists(carpeta_origen) or not os.listdir(carpeta_origen):
        print(f"Error: La carpeta '{carpeta_origen}' no existe o esta vacia.")
        print("Asegurate de correr primero tu script de descarga de libros.")
        return

    print("================================================================")
    print("      SISTEMA DE RECOMENDACION LITERARIA (TF-IDF)       ")
    print("================================================================")
    print("Analizando biblioteca y calculando")
    
    # Cargamos e indexamos los objetos Libro
    lista_de_libros = crear_lista_libros_ingles(carpeta_origen)
    
    # Construimos y entrenamos el recomendador
    recomienda_bot = Recomendador(lista_de_libros)
    recomienda_bot.set_pesos()
    print("Procesamiento completado\n")

    # Bucle infinito del menu interactivo de la interfaz
    while True:
        print("\n==============================================")
        print("¿Que operacion deseas realizar el dia de hoy?")
        print(" [1] Obtener resumen de palabras representativas de un libro")
        print(" [2] Buscar recomendaciones basadas en una obra")
        print(" [3] Salir del sistema")
        print("==============================================")
        
        seleccion = input("Elige una opcion (1-3): ").strip()
        
        if seleccion == "1":
            recomienda_bot.mostrar_libros()
            try:
                indice_target = int(input("\nIntroduce el numero de indice del libro: "))
                if 0 <= indice_target < len(lista_de_libros):
                    cantidad_top = int(input("¿Cuantas palabras clave deseas en el resumen?: "))
                    resumen_palabras = recomienda_bot.resumen(indice_target, cantidad_top)
                    
                    print(f"\n*** PALABRAS MAS REPRESENTATIVAS DE: {lista_de_libros[indice_target].name} ***")
                    print(", ".join(resumen_palabras))
                else:
                    print("Error: El indice no corresponde a ningun libro disponible.")
            except ValueError:
                print("Error: Por favor introduce solo numeros enteros.")
                
        elif seleccion == "2":
            recomienda_bot.mostrar_libros()
            try:
                indice_target = int(input("\nIntroduce el indice del libro que te gusto: "))
                if 0 <= indice_target < len(lista_de_libros):
                    cantidad_libros = int(input("¿Cuantas recomendaciones sugeridas deseas obtener?: "))
                    sugeridos = recomienda_bot.libros_similares(indice_target, cantidad_libros)
                    
                    print(f"\n*** CLASICOS RECOMENDADOS BASADOS EN TU INTERES ***")
                    for ranking, nombre_libro in enumerate(sugeridos, start=1):
                        print(f" {ranking}. {nombre_libro}")
                else:
                    print("Error: El indice no corresponde a ningun libro disponible.")
            except ValueError:
                print("Error: Por favor introduce solo numeros enteros.")
                
        elif seleccion == "3":
            print("\n¡Muchas gracias por utilizar nuestro sistema! Que tengas excelentes lecturas.")
            break
        else:
            print("Opcion no valida. Por favor selecciona 1, 2 o 3.")


if __name__ == "__main__":
    iniciar_consola()