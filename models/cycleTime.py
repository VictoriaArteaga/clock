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
