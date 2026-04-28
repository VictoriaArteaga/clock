# Vista del cronometro: display digital grande, controles y lista de vueltas.

import customtkinter as ctk

from clock.core.stopwatch import Stopwatch
from clock.ui.iconRenderer import IconRenderer


class StopwatchView:
    """Cronometro con display, botones de control y registro de vueltas."""

    CENTER_X = 860

    def __init__(self, parent, palette):
        self.parent = parent
        self.palette = palette
        self._loadPaletteAttrs()

        # Motor del cronometro (independiente del tema).
        self.stopwatch = Stopwatch()

        self._placedWidgets = []
        self._lapRowWidgets = []
        self._isVisible = False

        self._buildAllWidgets()

    # --- Paleta ---------------------------------------------------------------
    def _loadPaletteAttrs(self):
        palette = self.palette
        self.WOOD_DARKEST = palette.DARKEST
        self.WOOD_DARK = palette.DARK
        self.WOOD_MED = palette.MED
        self.WOOD_LIGHT = palette.LIGHT
        self.PARCHMENT = palette.PARCHMENT
        self.GOLD = palette.PRIMARY
        self.GOLD_HOVER = palette.PRIMARY_HOVER
        self.RED = palette.RED
        self.RED_DARK = palette.RED_DARK
        self.INK = palette.INK

    def applyPalette(self, palette):
        wasVisible = self._isVisible
        self._destroyAllWidgets()
        self.palette = palette
        self._loadPaletteAttrs()
        self._buildAllWidgets()
        # Si el cronometro estaba corriendo, el boton arranca como "Iniciar"
        # tras la reconstruccion; lo corregimos para reflejar el estado real.
        if self.stopwatch.isRunning():
            self._updateButtonStyle(
                self.startPauseBtn, "Pausar", IconRenderer.drawPause,
                self.WOOD_LIGHT, self.GOLD_HOVER, self.WOOD_DARKEST,
            )
        if wasVisible:
            self.show()

    # --- Construccion / destruccion -------------------------------------------
    def _buildAllWidgets(self):
        self._buildTitle()
        self._buildTimeDisplay()
        self._buildControlButtons()
        self._buildLapsListPanel()
        # Repintamos las vueltas existentes con la paleta actual.
        for lapIndex, lapTotalMs in enumerate(self.stopwatch.laps, start=1):
            self._addLapRow(lapIndex, lapTotalMs)

    def _destroyAllWidgets(self):
        for widget, _placeKwargs in self._placedWidgets:
            try:
                widget.destroy()
            except Exception:
                pass
        self._placedWidgets = []
        # Las filas de vueltas las recreamos desde stopwatch.laps.
        self._lapRowWidgets = []

    def _buildTitle(self):
        titleLabel = ctk.CTkLabel(
            self.parent, text="Cronometro",
            font=("Georgia", 26, "bold"),
            text_color=self.INK,
            fg_color=self.WOOD_LIGHT,
            corner_radius=10, padx=24, pady=6,
        )
        self._placedWidgets.append((titleLabel,
                                    dict(x=self.CENTER_X, y=15, anchor="n")))

    def _buildTimeDisplay(self):
        # Placa con el tiempo grande HH:MM:SS.CC.
        self.displayFrame = ctk.CTkFrame(
            self.parent,
            fg_color=self.WOOD_LIGHT,
            border_color=self.WOOD_DARK, border_width=4,
            corner_radius=12, width=720, height=160,
        )
        self.displayFrame.pack_propagate(False)

        self.timeDisplayLabel = ctk.CTkLabel(
            self.displayFrame, text="00:00:00.00",
            font=("Consolas", 64, "bold"),
            text_color=self.INK, fg_color="transparent",
        )
        self.timeDisplayLabel.pack(expand=True)

        self._placedWidgets.append((self.displayFrame,
                                    dict(x=self.CENTER_X, y=80, anchor="n")))

    def _buildControlButtons(self):
        # Tres botones centrados: iniciar/pausar, vuelta, reiniciar.
        self.startPauseBtn = self._buildIconButton(
            "Iniciar", IconRenderer.drawPlay, self._toggleStopwatch,
            width=180, height=48, fillColor=self.GOLD,
        )
        self.lapBtn = self._buildIconButton(
            "Vuelta", IconRenderer.drawFlag, self._registerLap,
            width=180, height=48, fillColor=self.WOOD_LIGHT,
        )
        self.resetBtn = self._buildIconButton(
            "Reiniciar", IconRenderer.drawReset, self._resetStopwatch,
            width=180, height=48, fillColor=self.RED,
            textColor=self.PARCHMENT,
        )
        self._placedWidgets.append((self.startPauseBtn,
                                    dict(x=self.CENTER_X - 200, y=260, anchor="n")))
        self._placedWidgets.append((self.lapBtn,
                                    dict(x=self.CENTER_X, y=260, anchor="n")))
        self._placedWidgets.append((self.resetBtn,
                                    dict(x=self.CENTER_X + 200, y=260, anchor="n")))

    def _buildLapsListPanel(self):
        # Placa con la lista scrollable de vueltas.
        self.lapsFrame = ctk.CTkFrame(
            self.parent,
            fg_color=self.WOOD_LIGHT,
            border_color=self.WOOD_DARK, border_width=3,
            corner_radius=10, width=720, height=350,
        )
        self.lapsFrame.pack_propagate(False)

        ctk.CTkLabel(
            self.lapsFrame, text="Vueltas",
            font=("Georgia", 14, "bold"),
            text_color=self.INK, fg_color="transparent",
        ).pack(pady=(8, 4))

        self.lapScrollFrame = ctk.CTkScrollableFrame(
            self.lapsFrame,
            fg_color=self.WOOD_MED,
            scrollbar_button_color=self.GOLD,
            scrollbar_button_hover_color=self.GOLD_HOVER,
            width=680, height=290,
        )
        self.lapScrollFrame.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        self._emptyLapsLabel = ctk.CTkLabel(
            self.lapScrollFrame,
            text="Sin vueltas registradas. Presiona 'Vuelta' mientras corre el cronometro.",
            font=("Georgia", 12, "italic"),
            text_color=self.PARCHMENT, fg_color="transparent",
        )
        self._emptyLapsLabel.pack(pady=20)

        self._placedWidgets.append((self.lapsFrame,
                                    dict(x=self.CENTER_X, y=330, anchor="n")))

    # --- Helper de boton ------------------------------------------------------
    def _buildIconButton(self, text, iconMethod, command,
                          width=160, height=42, fillColor=None, hoverColor=None,
                          textColor=None, iconSize=22):
        fillColor = fillColor or self.GOLD
        hoverColor = hoverColor or self.GOLD_HOVER
        textColor = textColor or self.WOOD_DARKEST

        button = ctk.CTkFrame(
            self.parent, fg_color=fillColor,
            corner_radius=6, width=width, height=height,
            border_color=self.WOOD_DARK, border_width=2,
        )
        button.pack_propagate(False)

        iconCanvas = ctk.CTkCanvas(button, width=iconSize + 4, height=iconSize + 4,
                                    bg=fillColor, highlightthickness=0)
        iconCanvas.pack(side="left", padx=(14, 4), pady=8)
        iconMethod(iconCanvas, (iconSize + 4) / 2, (iconSize + 4) / 2,
                   iconSize, color=textColor)

        textLabel = ctk.CTkLabel(button, text=text,
                                  font=("Georgia", 13, "bold"),
                                  text_color=textColor, fg_color="transparent")
        textLabel.pack(side="left", padx=4)

        # Guardamos los colores para reconfigurar el boton dinamicamente.
        button._styleMeta = {
            "label": textLabel, "icon": iconCanvas,
            "fill": fillColor, "hover": hoverColor, "text": textColor,
        }

        def onHoverEnter(_event):
            button.configure(fg_color=button._styleMeta["hover"])
            iconCanvas.configure(bg=button._styleMeta["hover"])

        def onHoverLeave(_event):
            button.configure(fg_color=button._styleMeta["fill"])
            iconCanvas.configure(bg=button._styleMeta["fill"])

        def onClick(_event):
            command()

        for widget in (button, iconCanvas, textLabel):
            widget.bind("<Enter>", onHoverEnter)
            widget.bind("<Leave>", onHoverLeave)
            widget.bind("<Button-1>", onClick)

        return button

    def _updateButtonStyle(self, button, text, iconMethod, fillColor, hoverColor, textColor):
        """Cambia texto, icono y colores de un boton existente sin destruirlo."""
        meta = button._styleMeta
        meta["fill"] = fillColor
        meta["hover"] = hoverColor
        meta["text"] = textColor
        button.configure(fg_color=fillColor)
        meta["icon"].configure(bg=fillColor)
        meta["icon"].delete("all")
        iconMethod(meta["icon"], 13, 13, 22, color=textColor)
        meta["label"].configure(text=text, text_color=textColor)

    # --- Control del cronometro -----------------------------------------------
    def _toggleStopwatch(self):
        self.stopwatch.toggleRunning()
        if self.stopwatch.isRunning():
            self._updateButtonStyle(
                self.startPauseBtn, "Pausar", IconRenderer.drawPause,
                self.WOOD_LIGHT, self.GOLD_HOVER, self.WOOD_DARKEST,
            )
        else:
            self._updateButtonStyle(
                self.startPauseBtn, "Iniciar", IconRenderer.drawPlay,
                self.GOLD, self.GOLD_HOVER, self.WOOD_DARKEST,
            )

    def _registerLap(self):
        lapTotalMs = self.stopwatch.lap()
        if lapTotalMs < 0:
            return
        self._addLapRow(len(self.stopwatch.laps), lapTotalMs)

    def _resetStopwatch(self):
        self.stopwatch.reset()
        self.timeDisplayLabel.configure(text="00:00:00.00")
        self._updateButtonStyle(
            self.startPauseBtn, "Iniciar", IconRenderer.drawPlay,
            self.GOLD, self.GOLD_HOVER, self.WOOD_DARKEST,
        )
        for lapRow in self._lapRowWidgets:
            lapRow.destroy()
        self._lapRowWidgets.clear()
        self._emptyLapsLabel.pack(pady=20)

    def _addLapRow(self, lapIndex: int, lapTotalMs: int):
        if not self._lapRowWidgets:
            self._emptyLapsLabel.pack_forget()

        # Parcial = duracion de esta vuelta (diferencia con la vuelta anterior).
        if lapIndex >= 2:
            previousTotalMs = self.stopwatch.laps[lapIndex - 2]
        else:
            previousTotalMs = 0
        lapPartialMs = lapTotalMs - previousTotalMs

        rowFrame = ctk.CTkFrame(
            self.lapScrollFrame,
            fg_color=self.WOOD_LIGHT,
            border_color=self.WOOD_DARK, border_width=2,
            corner_radius=6, height=44,
        )
        rowFrame.pack(fill="x", padx=6, pady=3)
        rowFrame.pack_propagate(False)

        ctk.CTkLabel(
            rowFrame, text=f"#{lapIndex:02d}",
            font=("Georgia", 13, "bold"),
            text_color=self.WOOD_DARK, fg_color="transparent",
        ).pack(side="left", padx=(16, 12))

        ctk.CTkLabel(
            rowFrame, text=f"Parcial {Stopwatch.formatMs(lapPartialMs)}",
            font=("Consolas", 13),
            text_color=self.INK, fg_color="transparent",
        ).pack(side="left", padx=12)

        ctk.CTkLabel(
            rowFrame, text=f"Total {Stopwatch.formatMs(lapTotalMs)}",
            font=("Consolas", 13, "bold"),
            text_color=self.INK, fg_color="transparent",
        ).pack(side="right", padx=16)

        self._lapRowWidgets.append(rowFrame)

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
        # Solo actualizamos el display si el cronometro esta corriendo.
        if self.stopwatch.isRunning():
            self.timeDisplayLabel.configure(
                text=Stopwatch.formatMs(self.stopwatch.getElapsedMs())
            )
