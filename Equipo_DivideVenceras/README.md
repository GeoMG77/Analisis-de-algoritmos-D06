Comparador de Algoritmos de Decodificación
Este proyecto compara el rendimiento de dos algoritmos para resolver el problema de decodificación de mensajes numéricos (ej. '123' -> 'ABC', 'AW', 'LC').

Los dos scripts son aplicaciones independientes con interfaz gráfica (GUI) que permiten probar cadenas numéricas y graficar en tiempo real el tiempo de ejecución contra la longitud de la entrada.

DIVIDE Y VENCERAS - sin PD.py: Implementa la solución recursiva pura (Divide y Vencerás), que tiene una complejidad exponencial y es muy lenta para entradas grandes.

DIVIDE Y VENCERAS PD.py: Implementa la solución optimizada con Programación Dinámica (Memoización), que tiene una complejidad lineal y es extremadamente rápida.

Requisitos
Este proyecto requiere Python 3 y la biblioteca matplotlib.

Puedes instalar la única dependencia necesaria usando pip:


pip install matplotlib
Ejecución
Debes ejecutar cada script de forma independiente desde tu terminal. Cada comando abrirá una ventana de aplicación separada.

Importante: Dado que los nombres de archivo contienen espacios, es fundamental que los encierres entre comillas al ejecutarlos en la terminal.

1. Versión con Programación Dinámica (Rápida)
Para ejecutar la versión optimizada (recomendada para entradas largas):


python "DIVIDE Y VENCERAS PD.py"
2. Versión con Divide y Vencerás (Lenta)
Para ejecutar la versión recursiva pura.

Advertencia: Esta versión se volverá extremadamente lenta (puede congelar la aplicación) con cadenas de entrada de más de 25-30 dígitos.


python "DIVIDE Y VENCERAS - sin PD.py"
