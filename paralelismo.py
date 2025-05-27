import threading

def crear_tablero():
    tablero = [[' ' for _ in range(8)] for _ in range(8)]
    for fila in range(3):
        for col in range(8):
            if (fila + col) % 2 == 1:
                tablero[fila][col] = 'n'
    for fila in range(5, 8):
        for col in range(8):
            if (fila + col) % 2 == 1:
                tablero[fila][col] = 'b'
    return tablero

def imprimir_tablero(tablero):
    print("    A B C D E F G H")
    print("   +++++++++++++++++")
    for idx, fila in enumerate(tablero):
        linea = f"{idx} |"
        for col in fila:
            linea += f" {col if col != ' ' else '.'}"
        linea += " |"
        print(linea)
    print("   +++++++++++++++++")

def coronar(tablero, x, y):
    if tablero[x][y] == 'b' and x == 0:
        tablero[x][y] = 'B'
    elif tablero[x][y] == 'n' and x == 7:
        tablero[x][y] = 'N'

def mover_ficha(tablero, origen, destino, jugador):
    ox, oy = origen
    dx, dy = destino
    pieza = tablero[ox][oy]

    if pieza.lower() != jugador:
        print("No es tu ficha.")
        return False

    if tablero[dx][dy] != ' ':
        print("Destino ocupado.")
        return False

    # Blancas suben (-1), negras bajan (+1)
    direccion = -1 if jugador == 'b' else 1

    # Movimiento simple
    if abs(dx - ox) == 1 and abs(dy - oy) == 1 and (dx - ox) == direccion:
        tablero[dx][dy] = pieza
        tablero[ox][oy] = ' '
        coronar(tablero, dx, dy)
        return True

    # Captura
    if abs(dx - ox) == 2 and abs(dy - oy) == 2:
        mx, my = (ox + dx) // 2, (oy + dy) // 2
        enemigo = 'n' if jugador == 'b' else 'b'
        if tablero[mx][my].lower() == enemigo:
            tablero[dx][dy] = pieza
            tablero[ox][oy] = ' '
            tablero[mx][my] = ' '
            coronar(tablero, dx, dy)
            return True

    print("Movimiento inválido.")
    return False

def parsear_movimiento(texto):
    m = texto.replace('-', '').replace(' ', '').upper()
    if len(m) != 4:
        raise ValueError("Formato inválido")
    letras = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
    if m[0] not in letras or m[2] not in letras:
        raise ValueError("Letra inválida")
    oy = letras[m[0]]
    ox = int(m[1])
    dy = letras[m[2]]
    dx = int(m[3])
    if not (0 <= ox < 8 and 0 <= dx < 8):
        raise ValueError("Fila fuera de rango")
    return (ox, oy), (dx, dy)

def calcular_movimientos(tablero, origen):
    ox, oy = origen
    pieza = tablero[ox][oy]
    if pieza == ' ':
        return []
    jugador = pieza.lower()
    dirs = []
    if pieza == 'b':
        dirs = [(-1, -1), (-1, 1)]
    elif pieza == 'n':
        dirs = [(1, -1), (1, 1)]
    else:  # coronas
        dirs = [(-1,-1), (-1,1), (1,-1), (1,1)]

    movimientos = []
    for dx, dy in dirs:
        nx, ny = ox + dx, oy + dy
        # simple
        if 0 <= nx < 8 and 0 <= ny < 8 and tablero[nx][ny] == ' ':
            movimientos.append((nx, ny))
        # captura
        cx, cy = ox + 2*dx, oy + 2*dy
        mx, my = ox + dx, oy + dy
        if (0 <= cx < 8 and 0 <= cy < 8 and
            tablero[cx][cy] == ' ' and
            tablero[mx][my].lower() in ('b','n') and
            tablero[mx][my].lower() != jugador):
            movimientos.append((cx, cy))
    return movimientos

def movimientos_jugador(tablero, jugador):
    todas = []
    for x in range(8):
        for y in range(8):
            if tablero[x][y].lower() == jugador:
                for dest in calcular_movimientos(tablero, (x, y)):
                    todas.append(((x, y), dest))
    return todas

def format_pos(pos):
    x, y = pos
    return f"{chr(y + 65)}{x}"

def juego():
    tablero = crear_tablero()
    turno = 'b'

    while True:
        print(f"\nTurno de {'blancas' if turno == 'b' else 'negras'}")

        # Variables compartidas y eventos de sincronización
        movimientos = []
        evt_movs = threading.Event()
        evt_imp = threading.Event()

        # Hilo para calcular movimientos
        def hilo_calcular():
            nonlocal movimientos
            movimientos = movimientos_jugador(tablero, turno)
            evt_movs.set()

        # Hilo para imprimir tablero
        def hilo_imprimir():
            imprimir_tablero(tablero)
            evt_imp.set()

        t1 = threading.Thread(target=hilo_calcular)
        t2 = threading.Thread(target=hilo_imprimir)
        t1.start()
        t2.start()

        # Espera a que ambos hilos terminen
        evt_movs.wait()
        evt_imp.wait()

        if not movimientos:
            print("¡No hay movimientos posibles! Fin del juego.")
            break

        print("Movimientos posibles:")
        print([f"{format_pos(o)}{format_pos(d)}" for o, d in movimientos])

        try:
            entrada = input("Movimiento (ej. A5B4, A5-B4 o A5 B4): ")
            origen, destino = parsear_movimiento(entrada)
            if mover_ficha(tablero, origen, destino, turno):
                turno = 'n' if turno == 'b' else 'b'
        except ValueError as ve:
            print(ve)
        except Exception:
            print("Error inesperado. Intenta de nuevo.")

if __name__ == "__main__":
    juego()