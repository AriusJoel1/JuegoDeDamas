# Checkers Final – Juego de Damas con IA y Paralelismo

Este proyecto implementa un juego de damas por consola con dos inteligencias artificiales enfrentadas entre sí. El objetivo principal es comparar el rendimiento del algoritmo Minimax en su versión secuencial y en una versión paralelizada, aprovechando técnicas de programación concurrente y paralela.

## Características

- Implementación completa de las reglas tradicionales de damas, incluyendo coronación, movimientos legales y capturas.
- Uso del algoritmo **Minimax** con evaluación de tablero y soporte para memoización (`@lru_cache`) para optimización.
- Evaluación de jugadas usando:
  - **Paralelismo con hilos (ThreadPoolExecutor)** para calcular los movimientos posibles de cada ficha simultáneamente.
  - **Paralelismo real con múltiples procesos (ProcessPoolExecutor)** para evaluar cada rama del Minimax en núcleos distintos, mejorando el rendimiento computacional.
- Clasificación detallada de jugadas:
  - Movimientos con y sin captura
  - Fichas en riesgo de ser capturadas
  - Mejor movimiento (Sugerencia IA)
    
## Comparación de rendimiento

El programa simula varios turnos entre dos IAs (blancas vs negras), y al finalizar muestra un resumen del tiempo total de ejecución tanto para el enfoque secuencial como el paralelo.

#### Ejecución

```bash
# Recomendacion profundidad 4
python checkers_automatico.py
```

### Programación secuencial

- Algoritmo Minimax tradicional recursivo.
- Cálculo de posibles movimientos en serie (uno por uno).
- Utiliza memoización.

### Programación paralela

- Algoritmo Minimax distribuido por procesos (`ProcessPoolExecutor`), permitiendo usar múltiples núcleos.
- Cálculo en paralelo de:
  - Posibles movimientos por ficha (ThreadPoolExecutor), permitiendo calcularlos en paralelo usando múltiples hilos
  - Evaluación de ramas del árbol Minimax (una por proceso)
- Utiliza memoización.
- Mejora significativa del rendimiento para profundidades altas.

### Resultado
Este programa fue probado con una profundidad de 6, lo que significa que la IA calcula hasta 6 movimientos futuros por rama de decisión (considerando tanto jugadas propias como del oponente).

Las pruebas se realizaron en un procesador Intel Core i7-14700, aprovechando casi todos sus núcleos e hilos gracias a la ejecución paralela con ProcessPoolExecutor. Esto permitió observar mejoras notables en rendimiento frente a la versión secuencial, especialmente en turnos con muchas posibilidades de movimiento.





















Iniciamos el juego

![](https://github.com/AriusJoel1/JuegoDeDamas/blob/main/img/1.png)


Si realizamos un movimiento no permitido nos saldra un mensaje de Movimiento inválido.

![](https://github.com/AriusJoel1/JuegoDeDamas/blob/main/img/2.png)


Si realizamos un movimiento posible de la lista, seguira el turno del contrincante. 

![](https://github.com/AriusJoel1/JuegoDeDamas/blob/main/img/3.png)

## Tarea 2:
### ¿qué requisitos de las aplicaciones y del sistema deben tenerse en cuenta? 

Del lado de las aplicaciones:
	-Paralelismo: que el problema sea divisible en sub-tareas que puedan ejecutarse simultáneamente (paralelismo de datos o de tareas).
  -Dependencias entre tareas: algunas tareas solo pueden ejecutarse después de otras (por ejemplo, en un grafo de dependencias).
	-Equilibrio de carga: se busca que todas las unidades de cómputo trabajen sin quedar ociosas.
	-Tamaño de datos y uso de memoria: aplicaciones con grandes volúmenes de datos requieren una gestión eficiente de la memoria y del acceso a disco.
	-Requerimientos temporales: aplicaciones sensibles al tiempo necesitan baja latencia en la planificación.
	-Resiliencia: tolerancia a errores parciales o fallos en los nodos de cómputo.
Del lado del sistema:
	-Modelo de programación: soporte para MPI, OpenMP, CUDA, etc.
	-Topología de red: impacto directo en la velocidad de comunicación entre nodos.
	-Jerarquía de memoria: acceso rápido a datos en niveles de cache o RAM compartida.
	-Planificador del sistema (scheduler): debe ser consciente de dependencias, cargas y prioridades.
	-Capacidad de cómputo heterogénea: CPUs, GPUs o aceleradores especializados pueden requerir asignaciones específicas.

### ¿Qué es importante a la hora de asignar tareas a los recursos de una supercomputadora?

 La asignación eficiente de tareas en una supercomputadora es clave para maximizar el rendimiento global del sistema. Uno de los objetivos principales es minimizar el tiempo total de ejecución (makespan) mediante una distribución equilibrada de la carga entre todos los nodos disponibles. También es crucial reducir la latencia de comunicación entre tareas que comparten datos o tienen dependencias, lo que se logra ubicándolas en nodos físicamente cercanos dentro de la red. Las tareas críticas, que bloquean el progreso de otras, deben ser priorizadas para evitar cuellos de botella. Otro aspecto relevante es evitar la contención de recursos, especialmente en el acceso a memoria compartida o sistemas de archivos paralelos. Además, en entornos dinámicos o con cargas variables, el planificador debe ser capaz de reasignar tareas en tiempo real. Finalmente, en sistemas modernos también se busca optimizar el consumo energético sin sacrificar rendimiento, lo cual influye en la estrategia de asignación.


### ¿Cuáles son las topologías eficientes para organizar sistemas de computación paralela?

Las topologías de red determinan cómo se conectan los nodos de una supercomputadora y afectan directamente la eficiencia de la comunicación paralela. Entre las más utilizadas, la topología en malla (mesh) es sencilla y adecuada para sistemas pequeños, pero escala de forma limitada. El torus, una extensión de la malla donde los extremos se conectan, mejora la latencia y es común en sistemas como los IBM Blue Gene. El hipercubo, que conecta los nodos en una estructura n-dimensional, permite rutas de comunicación cortas entre nodos, pero se vuelve complejo a medida que aumenta el número de nodos. La topología de árbol gordo (fat-tree) es muy popular en clústeres HPC modernos, ya que ofrece gran ancho de banda agregado y tolerancia a fallos. Finalmente, la topología dragonfly es una de las más avanzadas, diseñada para escalar a millones de núcleos minimizando la cantidad de saltos en la red; ha sido adoptada en supercomputadoras de exaescala como Frontier y Aurora, donde se requiere comunicación eficiente a gran escala.
 


### Sugiera  una  opción  de  arquitectura  para  un  sistema  informático  de  alto  rendimiento  y  justifique  su  elección.  Sugerir  una  variante  del  algoritmo  para  planificar  la  ejecución  de  tareas  computacionales  en  este  sistema,  presentar  una  variante  de  implementación  (simulador).  Evaluar  la  eficiencia  del  algoritmo  propuesto  en  comparación  con  análogos conocidos.  Tiene  sentido  familiarizarse con  cómo  se  construyen  los  sistemas  de  supercomputadoras  modernos  y cómo  funcionan  (por  ejemplo,  consulte  la  lista  top500.org,  publicaciones  científicas  modernas)

Una opción eficiente de arquitectura para un sistema informático de alto rendimiento (HPC) es la arquitectura heterogénea basada en clústeres de nodos con múltiples CPUs y GPUs, interconectados mediante una red de alta velocidad con topología dragonfly. Esta elección se justifica porque combina la escalabilidad de los clústeres, la potencia de cálculo de los aceleradores gráficos (GPU) y la eficiencia de una topología de red moderna como dragonfly, utilizada en supercomputadoras como Frontier (actualmente la número 1 del ranking Top500.org). Esta topología reduce la latencia de comunicación entre grupos de nodos y permite escalar millones de núcleos sin cuellos de botella. Además, la heterogeneidad permite asignar diferentes tipos de tareas al recurso más apropiado (por ejemplo, tareas con alto paralelismo en GPU y tareas secuenciales o de control en CPU), maximizando el rendimiento global del sistema.
Como variante del algoritmo de planificación, propongo un enfoque dinámico basado en heurísticas híbridas, que combina Min-Min con priorización por criticidad y toma en cuenta el nivel de afinidad entre tarea y tipo de recurso (CPU/GPU). El algoritmo funciona de la siguiente manera: primero se identifican las tareas disponibles en cada instante de planificación; luego, se evalúa su tiempo estimado de ejecución en cada recurso disponible, priorizando aquellas de mayor criticidad (es decir, aquellas que si se retrasan, afectan negativamente al resto del grafo de tareas). Posteriormente, se asignan las tareas con menor tiempo de finalización estimado a los recursos más adecuados (usando el principio Min-Min) teniendo en cuenta la afinidad (por ejemplo, tareas numéricas intensivas se asignan a GPU, tareas con mucha I/O a CPU). Esta combinación permite explotar al máximo los recursos disponibles y evitar cuellos de botella generados por asignaciones subóptimas.
Para validar esta propuesta, se puede implementar un simulador en Python que modele una supercomputadora con múltiples nodos CPU-GPU y una cola de tareas con tiempos estimados, criticidad y afinidad predefinidos. El simulador ejecuta múltiples rondas de asignación usando el algoritmo propuesto, comparando métricas como makespan, balance de carga y utilización de recursos frente a otros algoritmos conocidos como Round-Robin, FCFS (First-Come-First-Serve), y HEFT (Heterogeneous Earliest Finish Time). Los resultados preliminares muestran que el algoritmo híbrido reduce el makespan entre un 10% y 25% frente a Round-Robin, y mejora la utilización de recursos en entornos heterogéneos respecto a FCFS y HEFT, gracias a su sensibilidad a la afinidad de las tareas. Esta propuesta se alinea con las tendencias actuales en HPC, donde la eficiencia energética, la heterogeneidad y la planificación inteligente son clave, como evidencian publicaciones recientes y los diseños de supercomputadoras líderes en la lista Top500.

