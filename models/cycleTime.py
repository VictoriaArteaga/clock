# Esta clase representa la lista circular doble.

from .unitTime import UnitTime

class CycleTime:

    def __init__(self):
        self.firstTime: 'UnitTime' = None # Cabeza de la lista.


    # 1. Insertar tiempo al inicio de la lista.
    def insertTimeAtBeginning(self, time) -> None:

        # Se instancia un nuevo nodo con el tiempo dado.
        newTime = UnitTime(time)

        # Se válida si la lista está vacía.
        if self.firstTime is None:
            self.firstTime = newTime
            newTime.setNextTime(newTime)
            newTime.setPrevTime(newTime)

        # Sino, se inserta el nuevo tiempo al inicio de la lista.
        else:
            lastTime = self.firstTime.getPrevTime() # Identifica el último nodo actual.
            newTime.setNextTime(self.firstTime) # El siguiente del nuevo nodo apunta a la antigua cabeza.
            self.firstTime.setPrevTime(newTime) # El anterior de la antigua cabeza apunta a la nueva cabeza.
            newTime.setPrevTime(lastTime) # El anterior del nuevo nodo apunta al último nodo.
            lastTime.setNextTime(newTime) # El siguiente del último nodo apunta a la nueva cabeza.
            self.firstTime = newTime # Se reasigna la cabeza al nuevo nodo.

    # 2. Insertar al final de la lista (queda como nuevo último; la cabeza no cambia).
    def insertTimeAtEnd(self, time) -> None:
        newTime = UnitTime(time)

        if self.firstTime is None:
            # Lista vacía: el nuevo nodo es a la vez cabeza y cola, en autociclo.
            self.firstTime = newTime
            newTime.setNextTime(newTime)
            newTime.setPrevTime(newTime)
        else:
            # Enlazamos el nuevo nodo entre la cola actual y la cabeza, sin mover la cabeza.
            lastTime = self.firstTime.getPrevTime()
            newTime.setNextTime(self.firstTime)
            self.firstTime.setPrevTime(newTime)
            newTime.setPrevTime(lastTime)
            lastTime.setNextTime(newTime)

    # 3. Eliminar un nodo específico manteniendo la circularidad doble.
    def removeTime(self, time) -> None:
        if self.firstTime is None:
            return

        # Único nodo en la lista: la lista queda vacía.
        if time.getNextTime() is time:
            if self.firstTime is time:
                self.firstTime = None
            return

        # Lista con varios nodos: se cortocircuitan los vecinos del nodo a eliminar.
        prevNode = time.getPrevTime()
        nextNode = time.getNextTime()
        prevNode.setNextTime(nextNode)
        nextNode.setPrevTime(prevNode)

        # Si eliminamos la cabeza, la cabeza pasa al siguiente.
        if self.firstTime is time:
            self.firstTime = nextNode

        # Desconectamos los punteros del nodo eliminado para evitar referencias colgantes.
        time.setNextTime(None)
        time.setPrevTime(None)

    # 4. Vaciar la lista (la circularidad se rompe al soltar la cabeza).
    def clear(self) -> None:
        self.firstTime = None

    # 5. Iterar los nodos en orden: cabeza, cabeza.next, ... hasta volver a la cabeza.
    def __iter__(self):
        if self.firstTime is None:
            return
        currentTime = self.firstTime
        while True:
            yield currentTime
            currentTime = currentTime.getNextTime()
            if currentTime is self.firstTime:
                break

    # 6. Cantidad de nodos en la lista (recorre el ciclo una vez).
    def __len__(self) -> int:
        if self.firstTime is None:
            return 0
        count = 0
        for _ in self:
            count += 1
        return count
