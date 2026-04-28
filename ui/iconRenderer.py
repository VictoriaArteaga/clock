# Iconos vectoriales dibujados con primitivas de Canvas (sin emojis ni imagenes).
# Cada metodo recibe el canvas y la posicion del centro del icono.

import math


class IconRenderer:
    """Conjunto de iconos para botones y acentos visuales del reloj."""

    @staticmethod
    def drawClock(canvas, centerX, centerY, size, color="#2c1810"):
        # Esfera con manecillas en posicion 10:10 (icono clasico de un reloj).
        radius = size / 2
        canvas.create_oval(centerX - radius, centerY - radius,
                           centerX + radius, centerY + radius,
                           outline=color, width=2)
        canvas.create_oval(centerX - 1, centerY - 1, centerX + 1, centerY + 1,
                           fill=color, outline=color)
        # Manecilla de horas hacia las 10.
        canvas.create_line(centerX, centerY,
                           centerX + (radius * 0.55) * math.cos(math.radians(-150)),
                           centerY + (radius * 0.55) * math.sin(math.radians(-150)),
                           fill=color, width=2)
        # Manecilla de minutos hacia las 2.
        canvas.create_line(centerX, centerY,
                           centerX + (radius * 0.75) * math.cos(math.radians(-60)),
                           centerY + (radius * 0.75) * math.sin(math.radians(-60)),
                           fill=color, width=2)
        # Marcas en 12, 3, 6 y 9.
        for angleDeg in (-90, 0, 90, 180):
            innerX = centerX + (radius * 0.85) * math.cos(math.radians(angleDeg))
            innerY = centerY + (radius * 0.85) * math.sin(math.radians(angleDeg))
            outerX = centerX + (radius * 0.95) * math.cos(math.radians(angleDeg))
            outerY = centerY + (radius * 0.95) * math.sin(math.radians(angleDeg))
            canvas.create_line(innerX, innerY, outerX, outerY, fill=color, width=2)

    @staticmethod
    def drawAlarm(canvas, centerX, centerY, size, color="#2c1810"):
        # Campana clasica: cuerpo, lados, base, badajo y patitas tipo despertador.
        radius = size / 2
        canvas.create_arc(centerX - radius * 0.85, centerY - radius * 0.9,
                          centerX + radius * 0.85, centerY + radius * 0.5,
                          start=0, extent=180,
                          outline=color, width=2, style="arc")
        canvas.create_line(centerX - radius * 0.85, centerY - radius * 0.2,
                           centerX - radius * 0.85, centerY + radius * 0.3,
                           fill=color, width=2)
        canvas.create_line(centerX + radius * 0.85, centerY - radius * 0.2,
                           centerX + radius * 0.85, centerY + radius * 0.3,
                           fill=color, width=2)
        canvas.create_line(centerX - radius, centerY + radius * 0.3,
                           centerX + radius, centerY + radius * 0.3,
                           fill=color, width=2)
        canvas.create_oval(centerX - radius * 0.15, centerY + radius * 0.35,
                           centerX + radius * 0.15, centerY + radius * 0.65,
                           fill=color, outline=color)
        canvas.create_line(centerX - radius * 0.7, centerY - radius * 0.85,
                           centerX - radius * 0.95, centerY - radius * 1.05,
                           fill=color, width=2)
        canvas.create_line(centerX + radius * 0.7, centerY - radius * 0.85,
                           centerX + radius * 0.95, centerY - radius * 1.05,
                           fill=color, width=2)

    @staticmethod
    def drawStopwatch(canvas, centerX, centerY, size, color="#2c1810"):
        # Reloj con corona superior (boton de cronometro).
        radius = size / 2
        canvas.create_rectangle(centerX - radius * 0.18, centerY - radius * 1.05,
                                centerX + radius * 0.18, centerY - radius * 0.85,
                                outline=color, width=2)
        canvas.create_oval(centerX - radius * 0.85, centerY - radius * 0.75,
                           centerX + radius * 0.85, centerY + radius * 0.95,
                           outline=color, width=2)
        canvas.create_line(centerX, centerY + radius * 0.1,
                           centerX + radius * 0.45, centerY - radius * 0.35,
                           fill=color, width=2)
        canvas.create_oval(centerX - 2, centerY + radius * 0.08,
                           centerX + 2, centerY + radius * 0.12,
                           fill=color, outline=color)

    @staticmethod
    def drawGlobe(canvas, centerX, centerY, size, color="#2c1810"):
        # Globo terraqueo: circulo, ecuador, meridiano y un paralelo.
        radius = size / 2
        canvas.create_oval(centerX - radius, centerY - radius,
                           centerX + radius, centerY + radius,
                           outline=color, width=2)
        canvas.create_line(centerX - radius, centerY, centerX + radius, centerY,
                           fill=color, width=2)
        canvas.create_oval(centerX - radius * 0.45, centerY - radius,
                           centerX + radius * 0.45, centerY + radius,
                           outline=color, width=2)
        canvas.create_line(centerX, centerY - radius, centerX, centerY + radius,
                           fill=color, width=2)
        canvas.create_arc(centerX - radius, centerY - radius * 0.95,
                          centerX + radius, centerY + radius * 0.95,
                          start=10, extent=160,
                          outline=color, width=1, style="arc")

    @staticmethod
    def drawTheme(canvas, centerX, centerY, size, color="#2c1810"):
        # Paleta de pintor con manchas de pintura.
        radius = size / 2
        canvas.create_oval(centerX - radius, centerY - radius * 0.9,
                           centerX + radius, centerY + radius * 0.9,
                           outline=color, width=2)
        canvas.create_oval(centerX + radius * 0.3, centerY - radius * 0.1,
                           centerX + radius * 0.7, centerY + radius * 0.3,
                           outline=color, width=2)
        for offsetX, offsetY in ((-0.45, -0.3), (-0.5, 0.2), (-0.1, -0.5), (0.1, 0.45)):
            canvas.create_oval(centerX + radius * offsetX - 2, centerY + radius * offsetY - 2,
                               centerX + radius * offsetX + 2, centerY + radius * offsetY + 2,
                               fill=color, outline=color)

    @staticmethod
    def drawPencil(canvas, centerX, centerY, size, color="#2c1810"):
        # Lapiz en diagonal con punta y borrador.
        radius = size / 2
        canvas.create_line(centerX - radius * 0.7, centerY + radius * 0.7,
                           centerX + radius * 0.5, centerY - radius * 0.5,
                           fill=color, width=3)
        canvas.create_polygon(centerX + radius * 0.5, centerY - radius * 0.5,
                              centerX + radius * 0.85, centerY - radius * 0.65,
                              centerX + radius * 0.65, centerY - radius * 0.85,
                              outline=color, width=2, fill="")
        canvas.create_line(centerX - radius * 0.7, centerY + radius * 0.7,
                           centerX - radius * 0.85, centerY + radius * 0.85,
                           fill=color, width=3)

    @staticmethod
    def drawPin(canvas, centerX, centerY, size, color="#2c1810"):
        # Marcador de ubicacion (gota con circulo central).
        radius = size / 2
        canvas.create_oval(centerX - radius * 0.7, centerY - radius,
                           centerX + radius * 0.7, centerY + radius * 0.4,
                           outline=color, width=2)
        canvas.create_polygon(centerX - radius * 0.4, centerY + radius * 0.2,
                              centerX + radius * 0.4, centerY + radius * 0.2,
                              centerX, centerY + radius,
                              outline=color, width=2, fill="")
        canvas.create_oval(centerX - radius * 0.25, centerY - radius * 0.55,
                           centerX + radius * 0.25, centerY - radius * 0.05,
                           outline=color, width=2)

    @staticmethod
    def drawCheck(canvas, centerX, centerY, size, color="#2c1810"):
        # Palomita de aceptar.
        radius = size / 2
        canvas.create_line(centerX - radius * 0.7, centerY + radius * 0.05,
                           centerX - radius * 0.15, centerY + radius * 0.6,
                           fill=color, width=3, capstyle="round")
        canvas.create_line(centerX - radius * 0.15, centerY + radius * 0.6,
                           centerX + radius * 0.7, centerY - radius * 0.5,
                           fill=color, width=3, capstyle="round")

    @staticmethod
    def drawCross(canvas, centerX, centerY, size, color="#2c1810"):
        # X de cancelar / eliminar.
        radius = size / 2
        canvas.create_line(centerX - radius * 0.6, centerY - radius * 0.6,
                           centerX + radius * 0.6, centerY + radius * 0.6,
                           fill=color, width=3, capstyle="round")
        canvas.create_line(centerX + radius * 0.6, centerY - radius * 0.6,
                           centerX - radius * 0.6, centerY + radius * 0.6,
                           fill=color, width=3, capstyle="round")

    @staticmethod
    def drawPlay(canvas, centerX, centerY, size, color="#2c1810"):
        radius = size / 2
        canvas.create_polygon(
            centerX - radius * 0.45, centerY - radius * 0.65,
            centerX - radius * 0.45, centerY + radius * 0.65,
            centerX + radius * 0.65, centerY,
            fill=color, outline=color,
        )

    @staticmethod
    def drawPause(canvas, centerX, centerY, size, color="#2c1810"):
        radius = size / 2
        canvas.create_rectangle(centerX - radius * 0.55, centerY - radius * 0.65,
                                centerX - radius * 0.15, centerY + radius * 0.65,
                                fill=color, outline=color)
        canvas.create_rectangle(centerX + radius * 0.15, centerY - radius * 0.65,
                                centerX + radius * 0.55, centerY + radius * 0.65,
                                fill=color, outline=color)

    @staticmethod
    def drawReset(canvas, centerX, centerY, size, color="#2c1810"):
        # Flecha circular para "Restablecer / Reiniciar".
        radius = size / 2
        canvas.create_arc(centerX - radius * 0.7, centerY - radius * 0.7,
                          centerX + radius * 0.7, centerY + radius * 0.7,
                          start=40, extent=280,
                          outline=color, width=3, style="arc")
        canvas.create_polygon(
            centerX + radius * 0.55, centerY - radius * 0.45,
            centerX + radius * 0.85, centerY - radius * 0.05,
            centerX + radius * 0.4, centerY - radius * 0.05,
            fill=color, outline=color,
        )

    @staticmethod
    def drawFlag(canvas, centerX, centerY, size, color="#2c1810"):
        # Banderin (vuelta del cronometro).
        radius = size / 2
        canvas.create_line(centerX - radius * 0.5, centerY - radius * 0.8,
                           centerX - radius * 0.5, centerY + radius * 0.8,
                           fill=color, width=2)
        canvas.create_polygon(
            centerX - radius * 0.5, centerY - radius * 0.8,
            centerX + radius * 0.6, centerY - radius * 0.45,
            centerX - radius * 0.5, centerY - radius * 0.1,
            fill=color, outline=color,
        )

    @staticmethod
    def drawPlus(canvas, centerX, centerY, size, color="#2c1810"):
        # Cruz para agregar elementos.
        radius = size / 2
        canvas.create_line(centerX, centerY - radius * 0.7, centerX, centerY + radius * 0.7,
                           fill=color, width=3, capstyle="round")
        canvas.create_line(centerX - radius * 0.7, centerY, centerX + radius * 0.7, centerY,
                           fill=color, width=3, capstyle="round")
