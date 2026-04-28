# Vista del reloj analogico principal.
# Lee siempre del motor (clockContext.getHms()) para que los cambios manuales
# persistan, y expone Pausar/Reanudar para ejercer el patron State.

import customtkinter as ctk
import math

from clock.ui.iconRenderer import IconRenderer


class ClockView:
    """Reloj analogico grande + editor de hora en linea + boton pausar."""

    # Coordenadas centradas en el area derecha (ventana 1500x800, panel izq=220).
    CENTER_X = 860

    # Tamano del reloj analogico.
    CANVAS_SIZE = 560
    CLOCK_RADIUS = 250

    def __init__(self, parent, clockContext, palette):
        self.parent = parent
        self.clockContext = clockContext
        self.palette = palette
        self._loadPaletteAttrs()

        # Estado del editor de hora (modo lectura vs edicion).
        self._isEditing = False
        # El boton "Restablecer" solo aparece tras un cambio manual o al pausar.
        self._wasTimeChanged = False
        # Visibilidad para que applyPalette pueda re-mostrar tras reconstruir.
        self._isVisible = False

        # Variables de texto enlazadas a los entries del editor.
        self._hourVar = ctk.StringVar(value="00")
        self._minuteVar = ctk.StringVar(value="00")
        self._secondVar = ctk.StringVar(value="00")

        # Lista de (widget, kwargsDePlace) para mostrar/ocultar la vista.
        self._placedWidgets = []

        self._buildAllWidgets()

    # --- Paleta ---------------------------------------------------------------
    def _loadPaletteAttrs(self):
        # Mapeamos la paleta a los nombres historicos para no tocar el resto del codigo.
        palette = self.palette
        self.WOOD_DARKEST = palette.DARKEST
        self.WOOD_DARK = palette.DARK
        self.WOOD_MED = palette.MED
        self.WOOD_LIGHT = palette.LIGHT
        self.PARCHMENT = palette.PARCHMENT
        self.GOLD = palette.PRIMARY
        self.GOLD_HOVER = palette.PRIMARY_HOVER
        self.INK = palette.INK
        self.RED = palette.RED
        self.RED_DARK = palette.RED_DARK

    def applyPalette(self, palette):
        # Destruimos los widgets, recargamos la paleta y reconstruimos
        # preservando el estado del editor.
        wasVisible = self._isVisible
        savedHour = self._hourVar.get()
        savedMinute = self._minuteVar.get()
        savedSecond = self._secondVar.get()
        wasEditing = self._isEditing
        timeWasChanged = self._wasTimeChanged
        lastRunningState = getattr(self, "_lastRunningState", None)

        self._destroyAllWidgets()
        self.palette = palette
        self._loadPaletteAttrs()

        # Las viejas StringVars quedaron asociadas a entries destruidos.
        self._hourVar = ctk.StringVar(value=savedHour)
        self._minuteVar = ctk.StringVar(value=savedMinute)
        self._secondVar = ctk.StringVar(value=savedSecond)
        self._isEditing = wasEditing
        self._wasTimeChanged = timeWasChanged
        self._lastRunningState = lastRunningState

        self._buildAllWidgets()
        if self._isEditing:
            for entry in (self.hourEntry, self.minuteEntry, self.secondEntry):
                entry.configure(state="normal")

        if wasVisible:
            self.show()

    # --- Construccion / destruccion -------------------------------------------
    def _buildAllWidgets(self):
        self._buildTitle()
        self._buildClockCanvas()
        self._buildTimeEditor()
        self._buildButtons()

    def _destroyAllWidgets(self):
        for widget, _placeKwargs in self._placedWidgets:
            try:
                widget.destroy()
            except Exception:
                pass
        self._placedWidgets = []
        for buttonAttrName in ("changeBtn", "resetBtn", "pauseBtn", "acceptBtn", "cancelBtn"):
            button = getattr(self, buttonAttrName, None)
            if button is not None:
                try:
                    button.destroy()
                except Exception:
                    pass

    def _buildTitle(self):
        self.titleLabel = ctk.CTkLabel(
            self.parent,
            text="Venus",
            font=("Georgia", 26, "bold"),
            text_color=self.WOOD_DARKEST,
            fg_color=self.WOOD_LIGHT,
            corner_radius=10,
            padx=24, pady=6,
        )
        self._placedWidgets.append((self.titleLabel,
                                    dict(x=self.CENTER_X, y=10, anchor="n")))

    def _buildClockCanvas(self):
        outerSize = self.CANVAS_SIZE + 20
        # Marco con borde de madera oscura alrededor del canvas.
        self.canvasFrame = ctk.CTkFrame(
            self.parent,
            fg_color=self.PARCHMENT,
            corner_radius=12,
            border_color=self.WOOD_DARK,
            border_width=4,
            width=outerSize, height=outerSize,
        )
        self.canvasFrame.pack_propagate(False)

        self.clockCanvas = ctk.CTkCanvas(
            self.canvasFrame,
            width=self.CANVAS_SIZE, height=self.CANVAS_SIZE,
            bg=self.PARCHMENT,
            highlightthickness=0,
        )
        self.clockCanvas.pack(padx=6, pady=6)

        self._placedWidgets.append((self.canvasFrame,
                                    dict(x=self.CENTER_X, y=60, anchor="n")))

    def _buildTimeEditor(self):
        # Placa con tres entries (HH, MM, SS) y dos ":" como separadores.
        self.timeFrame = ctk.CTkFrame(
            self.parent,
            fg_color=self.WOOD_LIGHT,
            corner_radius=10,
            border_color=self.WOOD_DARK,
            border_width=2,
        )

        entryArgs = dict(
            font=("Consolas", 28, "bold"),
            width=68, height=44,
            justify="center",
            fg_color=self.PARCHMENT,
            text_color=self.WOOD_DARKEST,
            border_color=self.WOOD_DARK,
            border_width=2,
            state="disabled",
        )
        self.hourEntry = ctk.CTkEntry(self.timeFrame,
                                      textvariable=self._hourVar, **entryArgs)
        self.minuteEntry = ctk.CTkEntry(self.timeFrame,
                                        textvariable=self._minuteVar, **entryArgs)
        self.secondEntry = ctk.CTkEntry(self.timeFrame,
                                        textvariable=self._secondVar, **entryArgs)

        colonArgs = dict(
            font=("Consolas", 28, "bold"),
            text_color=self.WOOD_DARKEST,
            fg_color="transparent",
        )
        firstColon = ctk.CTkLabel(self.timeFrame, text=":", **colonArgs)
        secondColon = ctk.CTkLabel(self.timeFrame, text=":", **colonArgs)

        self.hourEntry.grid(row=0, column=0, padx=(14, 4), pady=8)
        firstColon.grid(row=0, column=1)
        self.minuteEntry.grid(row=0, column=2, padx=4, pady=8)
        secondColon.grid(row=0, column=3)
        self.secondEntry.grid(row=0, column=4, padx=(4, 14), pady=8)

        self._placedWidgets.append((self.timeFrame,
                                    dict(x=self.CENTER_X, y=640, anchor="n")))

    def _buildButtons(self):
        self.changeBtn = self._buildIconButton(
            "Cambiar Hora", None, self._enterEditMode,
            width=160, height=44,
        )
        self.resetBtn = self._buildIconButton(
            "Restablecer", IconRenderer.drawReset, self._resetToSystem,
            width=160, height=44,
        )
        self.pauseBtn = self._buildIconButton(
            "Pausar", IconRenderer.drawPause, self._togglePause,
            width=160, height=44,
            fillColor=self.WOOD_LIGHT, hoverColor=self.GOLD,
        )
        self.acceptBtn = self._buildIconButton(
            "Aceptar", IconRenderer.drawCheck, self._acceptTime,
            width=160, height=44,
        )
        self.cancelBtn = self._buildIconButton(
            "Cancelar", IconRenderer.drawCross, self._cancelEdit,
            width=160, height=44,
        )

        # Posiciones cuando solo hay 2 botones (sin Restablecer).
        self._changePlaceSolo = dict(x=self.CENTER_X - 5, y=730, anchor="ne")
        self._pausePlaceSolo  = dict(x=self.CENTER_X + 5, y=730, anchor="nw")
        # Posiciones cuando hay 3 botones (con Restablecer).
        self._changePlaceTrio = dict(x=self.CENTER_X - 90, y=730, anchor="ne")
        self._resetPlaceTrio  = dict(x=self.CENTER_X,       y=730, anchor="n")
        self._pausePlaceTrio  = dict(x=self.CENTER_X + 90, y=730, anchor="nw")
        # Posiciones del modo edicion.
        self._acceptPlace = dict(x=self.CENTER_X - 5, y=730, anchor="ne")
        self._cancelPlace = dict(x=self.CENTER_X + 5, y=730, anchor="nw")

    def _buildIconButton(self, text, iconMethod, command,
                         fillColor=None, hoverColor=None, textColor=None,
                         width=180, height=44):
        """Crea un boton compuesto (frame + icono opcional + label) con hover."""
        fillColor = fillColor or self.GOLD
        hoverColor = hoverColor or self.GOLD_HOVER
        textColor = textColor or self.WOOD_DARKEST

        button = ctk.CTkFrame(
            self.parent,
            fg_color=fillColor,
            corner_radius=6,
            width=width, height=height,
            border_color=self.WOOD_DARK,
            border_width=2,
        )
        button.pack_propagate(False)

        iconCanvas = None
        if iconMethod is not None:
            iconCanvas = ctk.CTkCanvas(button, width=24, height=24,
                                       bg=fillColor, highlightthickness=0)
            iconCanvas.pack(side="left", padx=(12, 4), pady=10)
            iconMethod(iconCanvas, 12, 12, 20, color=textColor)

        textLabel = ctk.CTkLabel(
            button, text=text,
            font=("Georgia", 14, "bold"),
            text_color=textColor, fg_color="transparent",
        )
        if iconCanvas is None:
            textLabel.pack(expand=True)
        else:
            textLabel.pack(side="left", padx=4)

        # Guardamos los colores activos para reconfigurar al cambiar de tema o estado.
        button._styleMeta = {
            "label": textLabel, "icon": iconCanvas,
            "fill": fillColor, "hover": hoverColor, "text": textColor,
        }

        def onHoverEnter(_event):
            button.configure(fg_color=button._styleMeta["hover"])
            if iconCanvas is not None:
                iconCanvas.configure(bg=button._styleMeta["hover"])

        def onHoverLeave(_event):
            button.configure(fg_color=button._styleMeta["fill"])
            if iconCanvas is not None:
                iconCanvas.configure(bg=button._styleMeta["fill"])

        def onClick(_event):
            command()

        widgetsToBind = [button, textLabel] + ([iconCanvas] if iconCanvas else [])
        for widget in widgetsToBind:
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
        meta["label"].configure(text=text, text_color=textColor)
        if meta["icon"] is not None:
            meta["icon"].configure(bg=fillColor)
            meta["icon"].delete("all")
            iconMethod(meta["icon"], 12, 12, 20, color=textColor)

    # --- Mostrar / ocultar ----------------------------------------------------
    def show(self):
        self._isVisible = True
        for widget, placeKwargs in self._placedWidgets:
            widget.place(**placeKwargs)
        self._placeButtonsForMode()

    def hide(self):
        self._isVisible = False
        for widget, _placeKwargs in self._placedWidgets:
            widget.place_forget()
        self.changeBtn.place_forget()
        self.resetBtn.place_forget()
        self.pauseBtn.place_forget()
        self.acceptBtn.place_forget()
        self.cancelBtn.place_forget()

    def _placeButtonsForMode(self):
        # Coloca los botones segun el modo lectura/edicion y si Restablecer aplica.
        if self._isEditing:
            self.changeBtn.place_forget()
            self.resetBtn.place_forget()
            self.pauseBtn.place_forget()
            self.acceptBtn.place(**self._acceptPlace)
            self.cancelBtn.place(**self._cancelPlace)
            return

        self.acceptBtn.place_forget()
        self.cancelBtn.place_forget()
        # Restablecer aparece tras cambiar la hora manualmente o al pausar.
        showResetButton = self._wasTimeChanged or not self.clockContext.isRunning()
        if showResetButton:
            self.changeBtn.place(**self._changePlaceTrio)
            self.resetBtn.place(**self._resetPlaceTrio)
            self.pauseBtn.place(**self._pausePlaceTrio)
        else:
            self.changeBtn.place(**self._changePlaceSolo)
            self.resetBtn.place_forget()
            self.pauseBtn.place(**self._pausePlaceSolo)

    # --- Modo edicion ---------------------------------------------------------
    def _enterEditMode(self):
        self._isEditing = True
        for entry in (self.hourEntry, self.minuteEntry, self.secondEntry):
            entry.configure(state="normal")
        self.hourEntry.focus_set()
        self.hourEntry.select_range(0, "end")
        self._placeButtonsForMode()

    def _exitEditMode(self):
        self._isEditing = False
        for entry in (self.hourEntry, self.minuteEntry, self.secondEntry):
            entry.configure(state="disabled")
        self._placeButtonsForMode()

    def _acceptTime(self):
        try:
            inputHour = int(self._hourVar.get())
            inputMinute = int(self._minuteVar.get())
            inputSecond = int(self._secondVar.get())
        except ValueError:
            self._flashError()
            return
        if not (0 <= inputHour <= 23 and 0 <= inputMinute <= 59 and 0 <= inputSecond <= 59):
            self._flashError()
            return
        # El cambio persiste porque la vista lee del motor en cada refresh.
        self.clockContext.setTime(inputHour, inputMinute, inputSecond)
        self._wasTimeChanged = True
        self._exitEditMode()

    def _cancelEdit(self):
        # No tocamos el motor; el siguiente refresh repondra los entries.
        self._exitEditMode()

    def _flashError(self):
        for entry in (self.hourEntry, self.minuteEntry, self.secondEntry):
            entry.configure(border_color=self.RED)
        self.parent.after(600, self._restoreEntryBorders)

    def _restoreEntryBorders(self):
        for entry in (self.hourEntry, self.minuteEntry, self.secondEntry):
            entry.configure(border_color=self.WOOD_DARK)

    # --- Restablecer hora del sistema -----------------------------------------
    def _resetToSystem(self):
        if self._isEditing:
            self._exitEditMode()
        self.clockContext.syncToSystem()
        # Tras restablecer dejamos el reloj corriendo (intencion: ver hora real avanzando).
        if not self.clockContext.isRunning():
            self.clockContext.setRunningState()
        self._wasTimeChanged = False
        self._placeButtonsForMode()

    # --- Pausar / reanudar (patron State en accion) ---------------------------
    def _togglePause(self):
        self.clockContext.togglePause()
        self._refreshPauseButton()
        # Restablecer puede aparecer/desaparecer al cambiar el estado de pausa.
        self._placeButtonsForMode()

    def _refreshPauseButton(self):
        if self.clockContext.isRunning():
            self._updateButtonStyle(
                self.pauseBtn, "Pausar", IconRenderer.drawPause,
                self.WOOD_LIGHT, self.GOLD, self.WOOD_DARKEST,
            )
        else:
            self._updateButtonStyle(
                self.pauseBtn, "Reanudar", IconRenderer.drawPlay,
                self.GOLD, self.GOLD_HOVER, self.WOOD_DARKEST,
            )

    # --- Refresco por tick ----------------------------------------------------
    def refresh(self):
        # Lee siempre del motor (CycleTime + State).
        currentHour, currentMinute, currentSecond = self.clockContext.getHms()
        self._drawAnalogClock(currentHour, currentMinute, currentSecond)

        # Solo actualizamos los entries fuera del modo edicion.
        if not self._isEditing:
            self._hourVar.set(f"{currentHour:02d}")
            self._minuteVar.set(f"{currentMinute:02d}")
            self._secondVar.set(f"{currentSecond:02d}")

        self._refreshPauseButton()

        # Si el estado de pausa cambio desde otra parte del codigo, recolocamos los botones.
        isRunningNow = self.clockContext.isRunning()
        if isRunningNow != getattr(self, "_lastRunningState", None):
            self._lastRunningState = isRunningNow
            if not self._isEditing:
                self._placeButtonsForMode()

    def _drawAnalogClock(self, currentHour, currentMinute, currentSecond):
        canvas = self.clockCanvas
        canvas.delete("all")

        centerX = self.CANVAS_SIZE / 2
        centerY = self.CANVAS_SIZE / 2
        radius = self.CLOCK_RADIUS

        # Anillo exterior madera oscura.
        canvas.create_oval(centerX - radius - 14, centerY - radius - 14,
                           centerX + radius + 14, centerY + radius + 14,
                           fill=self.WOOD_DARKEST, outline="")
        # Anillo medio madera con borde dorado.
        canvas.create_oval(centerX - radius, centerY - radius,
                           centerX + radius, centerY + radius,
                           fill=self.WOOD_MED, outline=self.GOLD, width=3)
        # Esfera color pergamino.
        canvas.create_oval(centerX - radius + 26, centerY - radius + 26,
                           centerX + radius - 26, centerY + radius - 26,
                           fill="#e8d4a8", outline=self.WOOD_DARK, width=2)

        # Numeros romanos en cada hora (XII arriba).
        romanNumerals = ["XII", "I", "II", "III", "IV", "V",
                          "VI", "VII", "VIII", "IX", "X", "XI"]
        for hourPosition in range(12):
            angleRad = math.radians(hourPosition * 30 - 90)
            numeralX = centerX + (radius - 60) * math.cos(angleRad)
            numeralY = centerY + (radius - 60) * math.sin(angleRad)
            canvas.create_text(numeralX, numeralY, text=romanNumerals[hourPosition],
                               font=("Georgia", 20, "bold"),
                               fill=self.WOOD_DARKEST)

        # Marcas de minutos y segundos alrededor de la esfera.
        for tickIndex in range(60):
            angleRad = math.radians(tickIndex * 6 - 90)
            isHourMark = (tickIndex % 5 == 0)
            innerOffset = 40 if isHourMark else 33
            outerOffset = 26
            markStartX = centerX + (radius - innerOffset) * math.cos(angleRad)
            markStartY = centerY + (radius - innerOffset) * math.sin(angleRad)
            markEndX = centerX + (radius - outerOffset) * math.cos(angleRad)
            markEndY = centerY + (radius - outerOffset) * math.sin(angleRad)
            canvas.create_line(markStartX, markStartY, markEndX, markEndY,
                               fill=self.WOOD_DARKEST if isHourMark else self.WOOD_DARK,
                               width=4 if isHourMark else 1)

        # Angulos a partir de la hora del motor (formato 24h pasado a 12h para la aguja de horas).
        hourMod12 = currentHour % 12
        secondAngle = math.radians(currentSecond * 6 - 90)
        minuteAngle = math.radians((currentMinute + currentSecond / 60) * 6 - 90)
        hourAngle = math.radians((hourMod12 + currentMinute / 60) * 30 - 90)

        # Aguja de horas: gruesa, oscura.
        hourHandLength = radius - 130
        canvas.create_line(centerX, centerY,
                           centerX + hourHandLength * math.cos(hourAngle),
                           centerY + hourHandLength * math.sin(hourAngle),
                           fill=self.WOOD_DARKEST, width=9, capstyle="round")
        # Aguja de minutos: mediana, dorada.
        minuteHandLength = radius - 80
        canvas.create_line(centerX, centerY,
                           centerX + minuteHandLength * math.cos(minuteAngle),
                           centerY + minuteHandLength * math.sin(minuteAngle),
                           fill=self.GOLD, width=6, capstyle="round")
        # Segundero: largo, fino, rojo.
        secondHandLength = radius - 50
        canvas.create_line(centerX, centerY,
                           centerX + secondHandLength * math.cos(secondAngle),
                           centerY + secondHandLength * math.sin(secondAngle),
                           fill=self.RED, width=2, capstyle="round")
        # Pivote central decorativo.
        canvas.create_oval(centerX - 12, centerY - 12, centerX + 12, centerY + 12,
                           fill=self.WOOD_DARKEST, outline=self.GOLD, width=2)
        canvas.create_oval(centerX - 5, centerY - 5, centerX + 5, centerY + 5,
                           fill=self.GOLD, outline="")
