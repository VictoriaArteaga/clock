# Vista global: 15 tarjetas con bandera, nombre, mini reloj analogico y hora local.
# Cada pais tiene su propio Clock (CycleTime); todos avanzan juntos cuando la
# GUI llama a advanceAllCountryClocks().

import customtkinter as ctk
import math
from datetime import datetime
from zoneinfo import ZoneInfo

from clock.core.clock import Clock
from clock.models.country import COUNTRIES
from clock.ui.flagRenderer import FlagRenderer


class WorldView:
    """Grid 5x3 de relojes mundiales, cada uno con su propio motor CycleTime."""

    # Geometria del grid (centrado en el area derecha de la ventana).
    CENTER_X = 860
    GRID_TOP_Y = 90
    COLUMN_COUNT = 5
    ROW_COUNT = 3
    CARD_WIDTH = 230
    CARD_HEIGHT = 220
    CARD_GAP_X = 12
    CARD_GAP_Y = 12
    MINI_CLOCK_RADIUS = 42

    def __init__(self, parent, palette):
        self.parent = parent
        self.palette = palette
        self._loadPaletteAttrs()

        # Tarjetas con su frame, canvas, country y Clock dedicado.
        self._countryCards = []
        # Lista de (widget, kwargsDePlace) para mostrar/ocultar la vista.
        self._placedWidgets = []

        self._isVisible = False

        self._buildTitle()
        self._buildCountryCards()

    # --- Paleta ---------------------------------------------------------------
    def _loadPaletteAttrs(self):
        palette = self.palette
        self.WOOD_DARK = palette.DARK
        self.WOOD_MED = palette.MED
        self.WOOD_LIGHT = palette.LIGHT
        self.PARCHMENT = palette.PARCHMENT
        self.GOLD = palette.PRIMARY
        self.INK = palette.INK
        self.RED = palette.RED

    def applyPalette(self, palette):
        # Conservamos los Clocks de cada pais; solo redibujamos las tarjetas.
        wasVisible = self._isVisible
        clocksByCode = {card["country"].code: card["clock"]
                        for card in self._countryCards}

        for widget, _placeKwargs in self._placedWidgets:
            try:
                widget.destroy()
            except Exception:
                pass
        self._placedWidgets = []
        self._countryCards = []

        self.palette = palette
        self._loadPaletteAttrs()
        self._buildTitle()
        self._buildCountryCards()

        # Reasignamos los motores guardados a las nuevas tarjetas.
        for card in self._countryCards:
            preservedClock = clocksByCode.get(card["country"].code)
            if preservedClock is not None:
                card["clock"] = preservedClock

        if wasVisible:
            self.show()

    # --- Construccion ---------------------------------------------------------
    def _buildTitle(self):
        self.titleLabel = ctk.CTkLabel(
            self.parent,
            text="Relojes del Mundo",
            font=("Georgia", 26, "bold"),
            text_color=self.INK,
            fg_color=self.WOOD_LIGHT,
            corner_radius=10,
            padx=24, pady=6,
        )
        self._placedWidgets.append((self.titleLabel,
                                    dict(x=self.CENTER_X, y=15, anchor="n")))

    def _buildCountryCards(self):
        # Calculamos donde empieza la columna izquierda del grid.
        gridTotalWidth = (self.COLUMN_COUNT * self.CARD_WIDTH
                          + (self.COLUMN_COUNT - 1) * self.CARD_GAP_X)
        firstColumnX = self.CENTER_X - gridTotalWidth // 2

        for cardIndex, country in enumerate(COUNTRIES):
            rowIndex = cardIndex // self.COLUMN_COUNT
            columnIndex = cardIndex % self.COLUMN_COUNT
            cardX = firstColumnX + columnIndex * (self.CARD_WIDTH + self.CARD_GAP_X)
            cardY = self.GRID_TOP_Y + rowIndex * (self.CARD_HEIGHT + self.CARD_GAP_Y)

            cardFrame = ctk.CTkFrame(
                self.parent,
                width=self.CARD_WIDTH, height=self.CARD_HEIGHT,
                fg_color=self.WOOD_LIGHT,
                border_color=self.WOOD_DARK,
                border_width=3,
                corner_radius=8,
            )
            cardFrame.pack_propagate(False)

            cardCanvas = ctk.CTkCanvas(
                cardFrame,
                width=self.CARD_WIDTH - 16, height=self.CARD_HEIGHT - 16,
                bg=self.WOOD_LIGHT,
                highlightthickness=0,
            )
            cardCanvas.pack(pady=8, padx=8)

            # Motor propio del pais inicializado a su hora local.
            countryClock = Clock()
            try:
                localNow = datetime.now(ZoneInfo(country.timezone))
                countryClock.setTime(localNow.hour, localNow.minute, localNow.second)
            except Exception:
                # Si la zona horaria no resuelve, dejamos el motor en 00:00:00.
                pass

            # Pintamos los elementos estaticos una sola vez.
            self._drawStaticCardElements(cardCanvas, country)

            self._countryCards.append({
                "frame": cardFrame,
                "canvas": cardCanvas,
                "country": country,
                "clock": countryClock,
            })
            self._placedWidgets.append((cardFrame, dict(x=cardX, y=cardY)))

    def _drawStaticCardElements(self, canvas, country):
        # Bandera arriba a la izquierda.
        FlagRenderer.draw(canvas, country.code, 8, 8, 56, 36)
        # Nombre del pais a la derecha de la bandera.
        canvas.create_text(72, 14,
                           text=country.name,
                           font=("Georgia", 11, "bold"),
                           fill=self.INK, anchor="w", tags="static")
        # Capital debajo del nombre.
        canvas.create_text(72, 32,
                           text=country.capital,
                           font=("Georgia", 9, "italic"),
                           fill=self.WOOD_DARK, anchor="w", tags="static")
        # Esfera del mini reloj analogico.
        clockCenterX = (self.CARD_WIDTH - 16) / 2
        clockCenterY = 105
        clockRadius = self.MINI_CLOCK_RADIUS
        canvas.create_oval(clockCenterX - clockRadius, clockCenterY - clockRadius,
                           clockCenterX + clockRadius, clockCenterY + clockRadius,
                           fill=self.WOOD_MED, outline=self.WOOD_DARK,
                           width=2, tags="static")
        canvas.create_oval(clockCenterX - clockRadius + 4, clockCenterY - clockRadius + 4,
                           clockCenterX + clockRadius - 4, clockCenterY + clockRadius - 4,
                           fill=self.PARCHMENT, outline=self.WOOD_MED,
                           width=1, tags="static")
        # Marcas en 12, 3, 6 y 9.
        for angleDeg in (-90, 0, 90, 180):
            angleRad = math.radians(angleDeg)
            innerX = clockCenterX + (clockRadius - 8) * math.cos(angleRad)
            innerY = clockCenterY + (clockRadius - 8) * math.sin(angleRad)
            outerX = clockCenterX + (clockRadius - 14) * math.cos(angleRad)
            outerY = clockCenterY + (clockRadius - 14) * math.sin(angleRad)
            canvas.create_line(innerX, innerY, outerX, outerY,
                               fill=self.INK, width=2, tags="static")

    def _refreshCard(self, card):
        canvas = card["canvas"]
        countryClock = card["clock"]

        canvas.delete("dynamic")

        countryHour, countryMinute, countrySecond = countryClock.getHms()

        secondAngle = math.radians(countrySecond * 6 - 90)
        minuteAngle = math.radians((countryMinute + countrySecond / 60) * 6 - 90)
        hourAngle = math.radians(((countryHour % 12) + countryMinute / 60) * 30 - 90)

        clockCenterX = (self.CARD_WIDTH - 16) / 2
        clockCenterY = 105
        clockRadius = self.MINI_CLOCK_RADIUS

        hourHandX = clockCenterX + (clockRadius - 24) * math.cos(hourAngle)
        hourHandY = clockCenterY + (clockRadius - 24) * math.sin(hourAngle)
        canvas.create_line(clockCenterX, clockCenterY, hourHandX, hourHandY,
                           fill=self.INK, width=3, tags="dynamic")

        minuteHandX = clockCenterX + (clockRadius - 14) * math.cos(minuteAngle)
        minuteHandY = clockCenterY + (clockRadius - 14) * math.sin(minuteAngle)
        canvas.create_line(clockCenterX, clockCenterY, minuteHandX, minuteHandY,
                           fill=self.GOLD, width=2, tags="dynamic")

        secondHandX = clockCenterX + (clockRadius - 8) * math.cos(secondAngle)
        secondHandY = clockCenterY + (clockRadius - 8) * math.sin(secondAngle)
        canvas.create_line(clockCenterX, clockCenterY, secondHandX, secondHandY,
                           fill=self.RED, width=1, tags="dynamic")

        canvas.create_oval(clockCenterX - 3, clockCenterY - 3,
                           clockCenterX + 3, clockCenterY + 3,
                           fill=self.INK, outline=self.GOLD, tags="dynamic")

        canvas.create_text((self.CARD_WIDTH - 16) / 2, self.CARD_HEIGHT - 38,
                           text=f"{countryHour:02d}:{countryMinute:02d}:{countrySecond:02d}",
                           font=("Consolas", 16, "bold"),
                           fill=self.INK, tags="dynamic")

    # --- Avance de los motores -----------------------------------------------
    def advanceAllCountryClocks(self) -> None:
        """La GUI llama a esto cuando pasa 1 segundo del motor principal."""
        for card in self._countryCards:
            card["clock"].tick()

    # --- Mostrar / ocultar / refresco ----------------------------------------
    def show(self):
        self._isVisible = True
        for widget, placeKwargs in self._placedWidgets:
            widget.place(**placeKwargs)

    def hide(self):
        self._isVisible = False
        for widget, _placeKwargs in self._placedWidgets:
            widget.place_forget()

    def refresh(self):
        for card in self._countryCards:
            self._refreshCard(card)
