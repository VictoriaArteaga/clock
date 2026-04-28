# Vista de alarmas: formulario para crear nuevas alarmas, lista scrollable de
# alarmas guardadas y overlay con audio cuando una alarma dispara.

import os
import customtkinter as ctk

# Silenciamos el banner de pygame antes de importarlo.
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

from clock.ui.iconRenderer import IconRenderer


class AlarmView:
    """Panel de alarmas con formulario, lista y overlay de disparo con audio."""

    CENTER_X = 860
    ALARM_AUDIO_FILENAME = "jeremayjimenez-thailand-eas-alarm-2006-266492.mp3"

    def __init__(self, parent, alarmManager, clockContext, palette):
        self.parent = parent
        self.alarmManager = alarmManager
        # Necesitamos el contexto del reloj para "Aplazar" (hora actual del motor).
        self.clockContext = clockContext
        self.palette = palette
        self._loadPaletteAttrs()

        # Inicializa el audio (best-effort: si falla la GUI sigue funcionando).
        self._isAudioReady = False
        self._audioFilePath = os.path.join(
            os.path.dirname(__file__), "..", "assets", self.ALARM_AUDIO_FILENAME
        )
        try:
            pygame.mixer.init()
            self._isAudioReady = os.path.exists(self._audioFilePath)
            if not self._isAudioReady:
                print(f"Audio no encontrado: {self._audioFilePath}")
        except Exception as audioError:
            print(f"No se pudo iniciar el audio: {audioError}")

        # Variables del formulario "Nueva alarma".
        self._nameVar = ctk.StringVar(value="")
        self._hourVar = ctk.StringVar(value="00")
        self._minuteVar = ctk.StringVar(value="00")

        # Lista de (widget, kwargsDePlace) para mostrar/ocultar la vista.
        self._placedWidgets = []
        # Filas de alarma indexadas por id, para destruirlas al eliminar/recargar.
        self._alarmRowWidgets = {}
        # Alarma sonando actualmente (None si no hay overlay visible).
        self._triggeredAlarm = None

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
        self.GREEN = palette.GREEN
        self.INK = palette.INK

    def applyPalette(self, palette):
        wasVisible = self._isVisible
        triggeredAlarm = self._triggeredAlarm
        savedName = self._nameVar.get()
        savedHour = self._hourVar.get()
        savedMinute = self._minuteVar.get()

        self._destroyAllWidgets()
        self.palette = palette
        self._loadPaletteAttrs()

        self._nameVar = ctk.StringVar(value=savedName)
        self._hourVar = ctk.StringVar(value=savedHour)
        self._minuteVar = ctk.StringVar(value=savedMinute)
        self._triggeredAlarm = triggeredAlarm

        self._buildAllWidgets()

        if wasVisible:
            self.show()
        # Si una alarma estaba sonando, mostramos el overlay con la nueva paleta.
        if triggeredAlarm is not None:
            self._overlayNameLabel.configure(text=triggeredAlarm.name)
            self._overlayTimeLabel.configure(text=triggeredAlarm.getTimeString())
            self.overlayFrame.place(x=self.CENTER_X, y=350, anchor="center")
            self.overlayFrame.lift()

    # --- Construccion / destruccion -------------------------------------------
    def _buildAllWidgets(self):
        self._buildTitle()
        self._buildNewAlarmForm()
        self._buildAlarmListPanel()
        self._buildTriggerOverlay()
        # Si ya habia alarmas guardadas las repintamos en la lista.
        if self.alarmManager.alarms:
            self._rebuildAlarmList()

    def _destroyAllWidgets(self):
        for widget, _placeKwargs in self._placedWidgets:
            try:
                widget.destroy()
            except Exception:
                pass
        self._placedWidgets = []
        # Las filas estan dentro del scrollFrame que ya destruimos arriba.
        self._alarmRowWidgets = {}
        try:
            self.overlayFrame.destroy()
        except Exception:
            pass

    def _buildTitle(self):
        titleLabel = ctk.CTkLabel(
            self.parent, text="Alarmas",
            font=("Georgia", 26, "bold"),
            text_color=self.INK,
            fg_color=self.WOOD_LIGHT,
            corner_radius=10, padx=24, pady=6,
        )
        self._placedWidgets.append((titleLabel,
                                    dict(x=self.CENTER_X, y=15, anchor="n")))

    def _buildNewAlarmForm(self):
        self.formFrame = ctk.CTkFrame(
            self.parent,
            fg_color=self.WOOD_LIGHT,
            border_color=self.WOOD_DARK, border_width=3,
            corner_radius=10,
            width=1180, height=110,
        )
        self.formFrame.pack_propagate(False)

        ctk.CTkLabel(
            self.formFrame, text="Nueva alarma",
            font=("Georgia", 14, "bold"),
            text_color=self.INK, fg_color="transparent",
        ).place(x=18, y=8)

        # Campo "Nombre".
        ctk.CTkLabel(self.formFrame, text="Nombre:",
                     font=("Georgia", 12), text_color=self.INK,
                     fg_color="transparent").place(x=18, y=50)
        nameEntry = ctk.CTkEntry(
            self.formFrame, textvariable=self._nameVar,
            width=260, height=36, font=("Georgia", 13),
            fg_color=self.PARCHMENT, text_color=self.INK,
            border_color=self.WOOD_DARK, border_width=2,
            placeholder_text="Despertador",
        )
        nameEntry.place(x=92, y=46)

        # Campos "Hora" (HH y MM, sin segundos).
        ctk.CTkLabel(self.formFrame, text="Hora:",
                     font=("Georgia", 12), text_color=self.INK,
                     fg_color="transparent").place(x=380, y=50)
        timeEntryArgs = dict(
            width=64, height=36,
            font=("Consolas", 16, "bold"),
            justify="center",
            fg_color=self.PARCHMENT, text_color=self.INK,
            border_color=self.WOOD_DARK, border_width=2,
        )
        ctk.CTkEntry(self.formFrame, textvariable=self._hourVar,
                     **timeEntryArgs).place(x=438, y=46)
        ctk.CTkLabel(self.formFrame, text=":",
                     font=("Consolas", 18, "bold"),
                     text_color=self.INK, fg_color="transparent").place(x=506, y=48)
        ctk.CTkEntry(self.formFrame, textvariable=self._minuteVar,
                     **timeEntryArgs).place(x=518, y=46)

        addButton = self._buildIconButton(
            self.formFrame, "Agregar", IconRenderer.drawPlus, self._addNewAlarm,
            width=160, height=38,
        )
        addButton.place(x=620, y=46)

        # Mensaje de error inline.
        self._errorLabel = ctk.CTkLabel(
            self.formFrame, text="",
            font=("Georgia", 11, "italic"),
            text_color=self.RED, fg_color="transparent",
        )
        self._errorLabel.place(x=800, y=52)

        self._placedWidgets.append((self.formFrame,
                                    dict(x=self.CENTER_X, y=70, anchor="n")))

    def _buildAlarmListPanel(self):
        self.listFrame = ctk.CTkFrame(
            self.parent,
            fg_color=self.WOOD_LIGHT,
            border_color=self.WOOD_DARK, border_width=3,
            corner_radius=10,
            width=1180, height=510,
        )
        self.listFrame.pack_propagate(False)

        ctk.CTkLabel(
            self.listFrame, text="Alarmas guardadas",
            font=("Georgia", 14, "bold"),
            text_color=self.INK, fg_color="transparent",
        ).pack(pady=(8, 4))

        self.alarmScrollFrame = ctk.CTkScrollableFrame(
            self.listFrame,
            fg_color=self.WOOD_MED,
            scrollbar_button_color=self.GOLD,
            scrollbar_button_hover_color=self.GOLD_HOVER,
            width=1140, height=440,
        )
        self.alarmScrollFrame.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        # Mensaje cuando aun no hay alarmas.
        self._emptyListLabel = ctk.CTkLabel(
            self.alarmScrollFrame,
            text="Aun no hay alarmas. Crea una con el formulario de arriba.",
            font=("Georgia", 12, "italic"),
            text_color=self.PARCHMENT, fg_color="transparent",
        )
        self._emptyListLabel.pack(pady=20)

        self._placedWidgets.append((self.listFrame,
                                    dict(x=self.CENTER_X, y=200, anchor="n")))

    def _buildTriggerOverlay(self):
        # Modal centrado que aparece cuando una alarma dispara.
        self.overlayFrame = ctk.CTkFrame(
            self.parent,
            fg_color=self.RED,
            border_color=self.WOOD_DARKEST, border_width=4,
            corner_radius=12,
            width=560, height=280,
        )
        self.overlayFrame.pack_propagate(False)

        ctk.CTkLabel(
            self.overlayFrame, text="Alarma activada",
            font=("Georgia", 22, "bold"),
            text_color=self.PARCHMENT, fg_color="transparent",
        ).pack(pady=(18, 2))

        self._overlayNameLabel = ctk.CTkLabel(
            self.overlayFrame, text="",
            font=("Georgia", 16, "italic"),
            text_color=self.PARCHMENT, fg_color="transparent",
        )
        self._overlayNameLabel.pack(pady=2)

        self._overlayTimeLabel = ctk.CTkLabel(
            self.overlayFrame, text="",
            font=("Consolas", 28, "bold"),
            text_color=self.GOLD, fg_color="transparent",
        )
        self._overlayTimeLabel.pack(pady=4)

        # Fila inferior: Aplazar 5 min y Apagar.
        buttonsRow = ctk.CTkFrame(self.overlayFrame, fg_color="transparent")
        buttonsRow.pack(pady=(12, 16))

        snoozeButton = self._buildIconButton(
            buttonsRow, "Aplazar 5 min", IconRenderer.drawClock, self._snoozeRingingAlarm,
            width=200, height=44,
            fillColor=self.WOOD_LIGHT, hoverColor=self.GOLD,
        )
        snoozeButton.pack(side="left", padx=10)

        stopButton = self._buildIconButton(
            buttonsRow, "Apagar", IconRenderer.drawCross, self._stopRingingAlarm,
            width=180, height=44,
            fillColor=self.RED_DARK, hoverColor=self.WOOD_DARKEST,
            textColor=self.PARCHMENT,
        )
        stopButton.pack(side="left", padx=10)

    # --- Helper de boton ------------------------------------------------------
    def _buildIconButton(self, master, text, iconMethod, command,
                          width=160, height=38, fillColor=None, hoverColor=None,
                          textColor=None, iconSize=20):
        fillColor = fillColor or self.GOLD
        hoverColor = hoverColor or self.GOLD_HOVER
        textColor = textColor or self.WOOD_DARKEST

        button = ctk.CTkFrame(
            master, fg_color=fillColor,
            corner_radius=6, width=width, height=height,
            border_color=self.WOOD_DARK, border_width=2,
        )
        button.pack_propagate(False)

        iconCanvas = ctk.CTkCanvas(button, width=iconSize + 4, height=iconSize + 4,
                                    bg=fillColor, highlightthickness=0)
        iconCanvas.pack(side="left", padx=(10, 4), pady=6)
        iconMethod(iconCanvas, (iconSize + 4) / 2, (iconSize + 4) / 2,
                   iconSize, color=textColor)

        textLabel = ctk.CTkLabel(button, text=text,
                                  font=("Georgia", 13, "bold"),
                                  text_color=textColor, fg_color="transparent")
        textLabel.pack(side="left", padx=4)

        def onHoverEnter(_event):
            button.configure(fg_color=hoverColor)
            iconCanvas.configure(bg=hoverColor)

        def onHoverLeave(_event):
            button.configure(fg_color=fillColor)
            iconCanvas.configure(bg=fillColor)

        def onClick(_event):
            command()

        for widget in (button, iconCanvas, textLabel):
            widget.bind("<Enter>", onHoverEnter)
            widget.bind("<Leave>", onHoverLeave)
            widget.bind("<Button-1>", onClick)

        return button

    # --- Acciones del formulario ----------------------------------------------
    def _addNewAlarm(self):
        try:
            inputHour = int(self._hourVar.get())
            inputMinute = int(self._minuteVar.get())
        except ValueError:
            self._showFormError("Hora invalida")
            return
        if not (0 <= inputHour <= 23 and 0 <= inputMinute <= 59):
            self._showFormError("Valores fuera de rango")
            return

        # Las alarmas creadas por el usuario disparan al inicio del minuto.
        self.alarmManager.add(self._nameVar.get().strip(),
                              inputHour, inputMinute, second=0)
        # Limpiamos el formulario.
        self._nameVar.set("")
        self._hourVar.set("00")
        self._minuteVar.set("00")
        self._showFormError("")
        self._rebuildAlarmList()

    def _showFormError(self, message: str):
        self._errorLabel.configure(text=message)

    # --- Lista de alarmas -----------------------------------------------------
    def _rebuildAlarmList(self):
        # Destruimos las filas previas y reconstruimos desde el manager.
        for rowWidgets in self._alarmRowWidgets.values():
            for widget in rowWidgets:
                widget.destroy()
        self._alarmRowWidgets.clear()

        savedAlarms = self.alarmManager.alarms
        if not savedAlarms:
            self._emptyListLabel.pack(pady=20)
            return
        self._emptyListLabel.pack_forget()

        for alarm in savedAlarms:
            self._buildAlarmRow(alarm)

    def _buildAlarmRow(self, alarm):
        rowFrame = ctk.CTkFrame(
            self.alarmScrollFrame,
            fg_color=self.WOOD_LIGHT,
            border_color=self.WOOD_DARK, border_width=2,
            corner_radius=6, height=64,
        )
        rowFrame.pack(fill="x", padx=8, pady=4)
        rowFrame.pack_propagate(False)

        # Hora.
        ctk.CTkLabel(
            rowFrame, text=alarm.getTimeString(),
            font=("Consolas", 22, "bold"),
            text_color=self.INK, fg_color="transparent",
        ).pack(side="left", padx=(20, 12), pady=10)

        # Nombre de la alarma.
        ctk.CTkLabel(
            rowFrame, text=alarm.name,
            font=("Georgia", 14),
            text_color=self.WOOD_DARK, fg_color="transparent",
        ).pack(side="left", padx=12)

        # Switch ON/OFF.
        switchVar = ctk.BooleanVar(value=alarm.isActive)

        def onToggleSwitch():
            self.alarmManager.toggle(alarm.alarmId)
            switchVar.set(self._isAlarmActive(alarm.alarmId))

        ctk.CTkSwitch(
            rowFrame, text="", variable=switchVar, command=onToggleSwitch,
            fg_color=self.WOOD_DARK, progress_color=self.GREEN,
            button_color=self.PARCHMENT, button_hover_color=self.GOLD,
        ).pack(side="right", padx=12)

        deleteButton = self._buildIconButton(
            rowFrame, "Eliminar", IconRenderer.drawCross,
            lambda alarmId=alarm.alarmId: self._deleteAlarm(alarmId),
            width=130, height=36,
            fillColor=self.RED, hoverColor=self.RED_DARK,
            textColor=self.PARCHMENT,
        )
        deleteButton.pack(side="right", padx=12, pady=10)

        self._alarmRowWidgets[alarm.alarmId] = [rowFrame]

    def _isAlarmActive(self, alarmId: int) -> bool:
        for alarm in self.alarmManager.alarms:
            if alarm.alarmId == alarmId:
                return alarm.isActive
        return False

    def _deleteAlarm(self, alarmId: int):
        # Si la alarma que se elimina es la que esta sonando, paramos audio y overlay.
        if (self._triggeredAlarm is not None
                and self._triggeredAlarm.alarmId == alarmId):
            self._stopAlarmAudio()
            self.overlayFrame.place_forget()
            self._triggeredAlarm = None
        self.alarmManager.remove(alarmId)
        self._rebuildAlarmList()

    # --- Audio de la alarma ---------------------------------------------------
    def _playAlarmAudio(self):
        if not self._isAudioReady:
            return
        try:
            pygame.mixer.music.load(self._audioFilePath)
            # Bucle infinito: suena hasta que el usuario apague o aplazara.
            pygame.mixer.music.play(loops=-1)
        except Exception as audioError:
            print(f"Error reproduciendo audio: {audioError}")

    def _stopAlarmAudio(self):
        if not self._isAudioReady:
            return
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    # --- Overlay de disparo ---------------------------------------------------
    def _showTriggerOverlay(self, alarm):
        self._triggeredAlarm = alarm
        self._overlayNameLabel.configure(text=alarm.name)
        self._overlayTimeLabel.configure(text=alarm.getTimeString())
        self.overlayFrame.place(x=self.CENTER_X, y=350, anchor="center")
        self.overlayFrame.lift()
        self._playAlarmAudio()

    def _stopRingingAlarm(self):
        # "Apagar": detiene audio, cierra overlay; la alarma queda desactivada.
        self._stopAlarmAudio()
        self.overlayFrame.place_forget()
        self._triggeredAlarm = None
        self._rebuildAlarmList()

    def _snoozeRingingAlarm(self):
        # "Aplazar 5 min": detiene audio, reprograma la alarma 5 minutos en el
        # futuro y la deja activa.
        if self._triggeredAlarm is None:
            return
        self._stopAlarmAudio()
        currentTime = self.clockContext.getHms()
        self.alarmManager.snooze(
            self._triggeredAlarm.alarmId, currentTime, minutesAhead=5
        )
        self.overlayFrame.place_forget()
        self._triggeredAlarm = None
        self._rebuildAlarmList()

    # --- Mostrar / ocultar / disparo -----------------------------------------
    def show(self):
        self._isVisible = True
        for widget, placeKwargs in self._placedWidgets:
            widget.place(**placeKwargs)
        if self._triggeredAlarm is not None:
            self.overlayFrame.lift()

    def hide(self):
        self._isVisible = False
        for widget, _placeKwargs in self._placedWidgets:
            widget.place_forget()
        # El overlay sigue visible al cambiar de vista; solo desaparece con Apagar / Aplazar.

    def checkTrigger(self, currentTime: tuple):
        """Llamado por la GUI cuando avanza el motor (1 vez por segundo)."""
        dueAlarm = self.alarmManager.checkDue(currentTime)
        if dueAlarm is not None:
            self._showTriggerOverlay(dueAlarm)
