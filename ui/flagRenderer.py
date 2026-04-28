# Banderas vectoriales para las tarjetas de la vista global. Cada bandera se
# dibuja dentro de un rectangulo (x, y, width, height) usando solo primitivas.

import math


class FlagRenderer:
    """Render simplificado de las banderas de los 15 paises del WorldView."""

    @classmethod
    def draw(cls, canvas, countryCode: str, x: float, y: float, width: float, height: float) -> None:
        # Despachamos al metodo `_draw{CODE}` correspondiente; si no existe,
        # mostramos una bandera placeholder gris.
        drawMethod = getattr(cls, f"_draw{countryCode}", None)
        if drawMethod is None:
            cls._drawPlaceholder(canvas, x, y, width, height)
            return
        drawMethod(canvas, x, y, width, height)
        # Borde fino comun para enmarcar todas las banderas.
        canvas.create_rectangle(x, y, x + width, y + height, outline="#2c1810", width=1)

    @staticmethod
    def _drawPlaceholder(canvas, x, y, width, height):
        canvas.create_rectangle(x, y, x + width, y + height,
                                fill="#cccccc", outline="#2c1810")

    @staticmethod
    def _drawUK(canvas, x, y, width, height):
        # Union Jack: aspas blancas + rojas y cruz central blanca + roja.
        canvas.create_rectangle(x, y, x + width, y + height, fill="#012169", outline="")
        canvas.create_line(x, y, x + width, y + height,
                           fill="#ffffff", width=int(height * 0.28))
        canvas.create_line(x, y + height, x + width, y,
                           fill="#ffffff", width=int(height * 0.28))
        canvas.create_line(x, y, x + width, y + height,
                           fill="#c8102e", width=int(height * 0.10))
        canvas.create_line(x, y + height, x + width, y,
                           fill="#c8102e", width=int(height * 0.10))
        canvas.create_rectangle(x, y + height * 0.35, x + width, y + height * 0.65,
                                fill="#ffffff", outline="")
        canvas.create_rectangle(x + width * 0.42, y, x + width * 0.58, y + height,
                                fill="#ffffff", outline="")
        canvas.create_rectangle(x, y + height * 0.42, x + width, y + height * 0.58,
                                fill="#c8102e", outline="")
        canvas.create_rectangle(x + width * 0.45, y, x + width * 0.55, y + height,
                                fill="#c8102e", outline="")

    @staticmethod
    def _drawFR(canvas, x, y, width, height):
        bandWidth = width / 3
        canvas.create_rectangle(x, y, x + bandWidth, y + height, fill="#0055a4", outline="")
        canvas.create_rectangle(x + bandWidth, y, x + 2 * bandWidth, y + height,
                                fill="#ffffff", outline="")
        canvas.create_rectangle(x + 2 * bandWidth, y, x + width, y + height,
                                fill="#ef4135", outline="")

    @staticmethod
    def _drawES(canvas, x, y, width, height):
        # Tres bandas: rojo, amarillo doble, rojo.
        canvas.create_rectangle(x, y, x + width, y + height * 0.25,
                                fill="#aa151b", outline="")
        canvas.create_rectangle(x, y + height * 0.25, x + width, y + height * 0.75,
                                fill="#f1bf00", outline="")
        canvas.create_rectangle(x, y + height * 0.75, x + width, y + height,
                                fill="#aa151b", outline="")
        # Escudo simplificado (rectangulo).
        shieldX = x + width * 0.32
        shieldY = y + height * 0.5
        canvas.create_rectangle(shieldX - width * 0.06, shieldY - height * 0.12,
                                shieldX + width * 0.06, shieldY + height * 0.12,
                                fill="#aa151b", outline="#2c1810")

    @staticmethod
    def _drawDE(canvas, x, y, width, height):
        canvas.create_rectangle(x, y, x + width, y + height / 3,
                                fill="#000000", outline="")
        canvas.create_rectangle(x, y + height / 3, x + width, y + 2 * height / 3,
                                fill="#dd0000", outline="")
        canvas.create_rectangle(x, y + 2 * height / 3, x + width, y + height,
                                fill="#ffce00", outline="")

    @staticmethod
    def _drawIT(canvas, x, y, width, height):
        bandWidth = width / 3
        canvas.create_rectangle(x, y, x + bandWidth, y + height, fill="#009246", outline="")
        canvas.create_rectangle(x + bandWidth, y, x + 2 * bandWidth, y + height,
                                fill="#ffffff", outline="")
        canvas.create_rectangle(x + 2 * bandWidth, y, x + width, y + height,
                                fill="#ce2b37", outline="")

    @staticmethod
    def _drawRU(canvas, x, y, width, height):
        canvas.create_rectangle(x, y, x + width, y + height / 3,
                                fill="#ffffff", outline="")
        canvas.create_rectangle(x, y + height / 3, x + width, y + 2 * height / 3,
                                fill="#0039a6", outline="")
        canvas.create_rectangle(x, y + 2 * height / 3, x + width, y + height,
                                fill="#d52b1e", outline="")

    @staticmethod
    def _drawCZ(canvas, x, y, width, height):
        # Mitad superior blanca, inferior roja, triangulo azul a la izquierda.
        canvas.create_rectangle(x, y, x + width, y + height / 2,
                                fill="#ffffff", outline="")
        canvas.create_rectangle(x, y + height / 2, x + width, y + height,
                                fill="#d7141a", outline="")
        canvas.create_polygon(x, y, x + width * 0.5, y + height * 0.5, x, y + height,
                              fill="#11457e", outline="")

    @staticmethod
    def _drawUS(canvas, x, y, width, height):
        # 13 barras alternadas + cuadro azul superior con estrellas simplificadas.
        stripeHeight = height / 13
        for stripeIndex in range(13):
            stripeColor = "#b22234" if stripeIndex % 2 == 0 else "#ffffff"
            canvas.create_rectangle(x, y + stripeIndex * stripeHeight,
                                    x + width, y + (stripeIndex + 1) * stripeHeight,
                                    fill=stripeColor, outline="")
        canvas.create_rectangle(x, y, x + width * 0.4, y + height * 7 / 13,
                                fill="#3c3b6e", outline="")
        starRows, starCols = 4, 5
        for rowIndex in range(starRows):
            for colIndex in range(starCols):
                starX = x + width * 0.4 * (colIndex + 1) / (starCols + 1)
                starY = y + (height * 7 / 13) * (rowIndex + 1) / (starRows + 1)
                canvas.create_oval(starX - 1, starY - 1, starX + 1, starY + 1,
                                   fill="#ffffff", outline="")

    @staticmethod
    def _drawMX(canvas, x, y, width, height):
        bandWidth = width / 3
        canvas.create_rectangle(x, y, x + bandWidth, y + height, fill="#006847", outline="")
        canvas.create_rectangle(x + bandWidth, y, x + 2 * bandWidth, y + height,
                                fill="#ffffff", outline="")
        canvas.create_rectangle(x + 2 * bandWidth, y, x + width, y + height,
                                fill="#ce1126", outline="")
        # Aguila central simplificada.
        eagleX = x + width / 2
        eagleY = y + height / 2
        canvas.create_oval(eagleX - width * 0.06, eagleY - height * 0.12,
                           eagleX + width * 0.06, eagleY + height * 0.12,
                           outline="#8b4513", width=1)

    @staticmethod
    def _drawBR(canvas, x, y, width, height):
        canvas.create_rectangle(x, y, x + width, y + height, fill="#009c3b", outline="")
        # Rombo amarillo y disco azul central.
        centerX = x + width / 2
        centerY = y + height / 2
        canvas.create_polygon(centerX, y + height * 0.12,
                              x + width * 0.92, centerY,
                              centerX, y + height * 0.88,
                              x + width * 0.08, centerY,
                              fill="#ffdf00", outline="")
        canvas.create_oval(centerX - width * 0.18, centerY - height * 0.27,
                           centerX + width * 0.18, centerY + height * 0.27,
                           fill="#002776", outline="")

    @staticmethod
    def _drawAR(canvas, x, y, width, height):
        canvas.create_rectangle(x, y, x + width, y + height / 3,
                                fill="#74acdf", outline="")
        canvas.create_rectangle(x, y + height / 3, x + width, y + 2 * height / 3,
                                fill="#ffffff", outline="")
        canvas.create_rectangle(x, y + 2 * height / 3, x + width, y + height,
                                fill="#74acdf", outline="")
        # Sol de mayo (circulo amarillo central).
        sunX = x + width / 2
        sunY = y + height / 2
        canvas.create_oval(sunX - height * 0.15, sunY - height * 0.15,
                           sunX + height * 0.15, sunY + height * 0.15,
                           fill="#f6b40e", outline="#85340a")

    @staticmethod
    def _drawJP(canvas, x, y, width, height):
        canvas.create_rectangle(x, y, x + width, y + height, fill="#ffffff", outline="")
        sunX = x + width / 2
        sunY = y + height / 2
        sunRadius = height * 0.3
        canvas.create_oval(sunX - sunRadius, sunY - sunRadius,
                           sunX + sunRadius, sunY + sunRadius,
                           fill="#bc002d", outline="")

    @staticmethod
    def _drawCN(canvas, x, y, width, height):
        canvas.create_rectangle(x, y, x + width, y + height, fill="#ee1c25", outline="")
        # Estrella grande.
        bigStarX = x + width * 0.2
        bigStarY = y + height * 0.3
        canvas.create_oval(bigStarX - width * 0.06, bigStarY - height * 0.12,
                           bigStarX + width * 0.06, bigStarY + height * 0.12,
                           fill="#ffff00", outline="")
        # Cuatro estrellas pequenas alrededor.
        for offsetX, offsetY in ((0.32, 0.12), (0.38, 0.25), (0.38, 0.42), (0.32, 0.55)):
            smallStarX = x + width * offsetX
            smallStarY = y + height * offsetY
            canvas.create_oval(smallStarX - 2, smallStarY - 2,
                               smallStarX + 2, smallStarY + 2,
                               fill="#ffff00", outline="")

    @staticmethod
    def _drawIN(canvas, x, y, width, height):
        canvas.create_rectangle(x, y, x + width, y + height / 3,
                                fill="#ff9933", outline="")
        canvas.create_rectangle(x, y + height / 3, x + width, y + 2 * height / 3,
                                fill="#ffffff", outline="")
        canvas.create_rectangle(x, y + 2 * height / 3, x + width, y + height,
                                fill="#138808", outline="")
        # Chakra de Ashoka (rueda azul central con radios).
        chakraX = x + width / 2
        chakraY = y + height / 2
        chakraRadius = height * 0.13
        canvas.create_oval(chakraX - chakraRadius, chakraY - chakraRadius,
                           chakraX + chakraRadius, chakraY + chakraRadius,
                           outline="#000080", width=1)
        for spokeAngleDeg in range(0, 360, 30):
            spokeAngleRad = math.radians(spokeAngleDeg)
            canvas.create_line(chakraX, chakraY,
                               chakraX + chakraRadius * math.cos(spokeAngleRad),
                               chakraY + chakraRadius * math.sin(spokeAngleRad),
                               fill="#000080", width=1)

    @staticmethod
    def _drawAU(canvas, x, y, width, height):
        canvas.create_rectangle(x, y, x + width, y + height, fill="#012169", outline="")
        # Mini Union Jack en el cuadrante superior izquierdo.
        FlagRenderer._drawUK(canvas, x, y, width * 0.5, height * 0.5)
        # Estrella grande de la federacion.
        federationStarX = x + width * 0.25
        federationStarY = y + height * 0.78
        canvas.create_oval(federationStarX - 3, federationStarY - 3,
                           federationStarX + 3, federationStarY + 3,
                           fill="#ffffff", outline="")
        # Cuatro estrellas de la Cruz del Sur.
        for offsetX, offsetY in ((0.68, 0.25), (0.85, 0.4), (0.78, 0.6), (0.7, 0.78)):
            crossStarX = x + width * offsetX
            crossStarY = y + height * offsetY
            canvas.create_oval(crossStarX - 2, crossStarY - 2,
                               crossStarX + 2, crossStarY + 2,
                               fill="#ffffff", outline="")
