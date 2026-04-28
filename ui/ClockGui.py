# Ventana principal: panel lateral + 4 vistas intercambiables sobre el fondo del tema.


import os
import customtkinter as ctk
from PIL import Image

from clock.core.states.clockContext import ClockContext
from clock.models.alarm import AlarmManager
from clock.ui.iconRenderer import IconRenderer
from clock.ui.theme import PALETTES, LONDRES
from clock.ui.clockView import ClockView
from clock.ui.worldView import WorldView
from clock.ui.alarmView import AlarmView
from clock.ui.stopwatchView import StopwatchView


class ClockGui(ctk.CTk):

    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 800
    LEFT_PANEL_WIDTH = 220

    # Frecuencias del loop de actualizacion.
    GUI_TICK_MS = 50            # refresco visual.
    MOTOR_PERIOD_MS = 1000      # cada 1 s avanzamos el motor (CycleTime + State).

    def __init__(self):
        super().__init__()

        self.title("Venus")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.resizable(False, False)

        # Logica del taller.
        self.clockContext = ClockContext()  # arranca corriendo y sincronizado.
        self.alarmManager = AlarmManager()

        # Acumulador para disparar el motor cada MOTOR_PERIOD_MS.
        self._tickAccumulatorMs = 0

        self.assetsPath = os.path.join(os.path.dirname(__file__), "..", "assets")

        # Tema activo (paleta + imagen de fondo).
        self.palette = LONDRES
        self.currentThemeName = self.palette.name
        self._loadPaletteAttrs()
        self.configure(fg_color=self.WOOD_DARKEST)
        self._backgroundCtkImage = None

        # Fondo a tamano de ventana.
        self.backgroundLabel = ctk.CTkLabel(self, text="")
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)
        self._loadBackgroundImage(self.palette.image_file)

        self._buildLeftPanel()

        # Las cuatro vistas intercambiables.
        self.clockView = ClockView(self, self.clockContext, self.palette)
        self.worldView = WorldView(self, self.palette)
        self.alarmView = AlarmView(self, self.alarmManager, self.clockContext, self.palette)
        self.stopwatchView = StopwatchView(self, self.palette)

        self._views = {
            "clock": self.clockView,
            "world": self.worldView,
            "alarm": self.alarmView,
            "stopwatch": self.stopwatchView,
        }
        self._activeViewName = None
        self._showView("clock")

        self._tick()

    # --- Paleta ---------------------------------------------------------------
    def _loadPaletteAttrs(self):
        # Mapea la paleta activa a los nombres historicos para el resto del codigo.
        palette = self.palette
        self.WOOD_DARKEST = palette.DARKEST
        self.WOOD_DARK = palette.DARK
        self.WOOD_MED = palette.MED
        self.WOOD_LIGHT = palette.LIGHT
        self.PARCHMENT = palette.PARCHMENT
        self.GOLD = palette.PRIMARY
        self.GOLD_HOVER = palette.PRIMARY_HOVER

    # --- Panel izquierdo ------------------------------------------------------
    def _buildLeftPanel(self):
        self.leftPanel = ctk.CTkFrame(
            self, fg_color=self.WOOD_DARKEST,
            border_color=self.GOLD, border_width=2,
            width=self.LEFT_PANEL_WIDTH, height=self.WINDOW_HEIGHT,
        )
        self.leftPanel.pack_propagate(False)
        self.leftPanel.place(x=0, y=0)

        # Encabezado de la marca.
        ctk.CTkLabel(
            self.leftPanel, text="VENUS",
            font=("Georgia", 22, "bold"),
            text_color=self.GOLD,
            fg_color=self.WOOD_DARK,
            corner_radius=4,
        ).pack(pady=(15, 4), padx=12, fill="x")

        ctk.CTkLabel(
            self.leftPanel, text="Global Clock",
            font=("Georgia", 11, "italic"),
            text_color=self.WOOD_LIGHT,
        ).pack(pady=(0, 15))

        menuItems = [
            ("Reloj",      IconRenderer.drawClock,     lambda: self._showView("clock")),
            ("Alarma",     IconRenderer.drawAlarm,     lambda: self._showView("alarm")),
            ("Cronometro", IconRenderer.drawStopwatch, lambda: self._showView("stopwatch")),
            ("Global",     IconRenderer.drawGlobe,     lambda: self._showView("world")),
            ("Tema",       IconRenderer.drawTheme,     self._toggleThemeMenu),
        ]
        for itemText, iconMethod, command in menuItems:
            self._buildMenuButton(self.leftPanel, itemText, iconMethod, command)

        # Submenu de temas (oculto por defecto).
        self.themeMenu = ctk.CTkFrame(self.leftPanel, fg_color=self.WOOD_DARK)
        for themeName in PALETTES.keys():
            self._buildThemeButton(self.themeMenu, themeName)

    def _rebuildLeftPanel(self):
        # Recrea el panel izquierdo aplicando la paleta actual.
        wasThemeMenuOpen = self.themeMenu.winfo_viewable()
        try:
            self.leftPanel.destroy()
        except Exception:
            pass
        self._buildLeftPanel()
        if wasThemeMenuOpen:
            self.themeMenu.pack(pady=5, padx=10, fill="x")

    def _buildMenuButton(self, parent, text, iconMethod, command):
        button = ctk.CTkFrame(
            parent, fg_color=self.GOLD,
            corner_radius=5, height=55,
            border_color=self.WOOD_DARK, border_width=2,
        )
        button.pack(pady=8, padx=10, fill="x")
        button.pack_propagate(False)

        iconCanvas = ctk.CTkCanvas(
            button, width=30, height=30,
            bg=self.GOLD, highlightthickness=0,
        )
        iconCanvas.pack(side="left", padx=(12, 6), pady=10)
        iconMethod(iconCanvas, 15, 15, 24, color=self.WOOD_DARKEST)

        textLabel = ctk.CTkLabel(
            button, text=text,
            font=("Georgia", 13, "bold"),
            text_color=self.WOOD_DARKEST, fg_color="transparent",
        )
        textLabel.pack(side="left", padx=4)

        def onHoverEnter(_event):
            button.configure(fg_color=self.GOLD_HOVER)
            iconCanvas.configure(bg=self.GOLD_HOVER)

        def onHoverLeave(_event):
            button.configure(fg_color=self.GOLD)
            iconCanvas.configure(bg=self.GOLD)

        def onClick(_event):
            command()

        for widget in (button, iconCanvas, textLabel):
            widget.bind("<Enter>", onHoverEnter)
            widget.bind("<Leave>", onHoverLeave)
            widget.bind("<Button-1>", onClick)

    def _buildThemeButton(self, parent, themeName):
        button = ctk.CTkFrame(
            parent, fg_color=self.WOOD_MED,
            corner_radius=3, height=40,
        )
        button.pack(pady=4, padx=8, fill="x")
        button.pack_propagate(False)

        iconCanvas = ctk.CTkCanvas(
            button, width=22, height=22,
            bg=self.WOOD_MED, highlightthickness=0,
        )
        iconCanvas.pack(side="left", padx=(10, 4), pady=8)
        IconRenderer.drawPin(iconCanvas, 11, 11, 18, color=self.GOLD)

        textLabel = ctk.CTkLabel(
            button, text=themeName,
            font=("Georgia", 11),
            text_color=self.GOLD, fg_color="transparent",
        )
        textLabel.pack(side="left", padx=4)

        def onHoverEnter(_event):
            button.configure(fg_color=self.WOOD_LIGHT)
            iconCanvas.configure(bg=self.WOOD_LIGHT)

        def onHoverLeave(_event):
            button.configure(fg_color=self.WOOD_MED)
            iconCanvas.configure(bg=self.WOOD_MED)

        def onClick(_event):
            self._selectTheme(themeName)

        for widget in (button, iconCanvas, textLabel):
            widget.bind("<Enter>", onHoverEnter)
            widget.bind("<Leave>", onHoverLeave)
            widget.bind("<Button-1>", onClick)

    # --- Loop de actualizacion -----------------------------------------------
    def _tick(self):
        # Cada GUI_TICK_MS refrescamos pantalla; cada MOTOR_PERIOD_MS avanzamos motor.
        self._tickAccumulatorMs += self.GUI_TICK_MS
        if self._tickAccumulatorMs >= self.MOTOR_PERIOD_MS:
            self._tickAccumulatorMs -= self.MOTOR_PERIOD_MS
            # Patron State en accion: avanza si esta en RunningState, no avanza en Paused.
            self.clockContext.update()
            # Si el reloj principal corre, los relojes mundiales y las alarmas tambien.
            if self.clockContext.isRunning():
                self.worldView.advanceAllCountryClocks()
                self.alarmView.checkTrigger(self.clockContext.getHms())

        # Refresco visual de la vista activa.
        activeView = self._views.get(self._activeViewName)
        if activeView is not None and hasattr(activeView, "refresh"):
            activeView.refresh()

        self.after(self.GUI_TICK_MS, self._tick)

    def _showView(self, viewName: str):
        if self._activeViewName == viewName:
            return
        if self._activeViewName is not None:
            self._views[self._activeViewName].hide()
        self._views[viewName].show()
        self._activeViewName = viewName
        if self.themeMenu.winfo_viewable():
            self.themeMenu.pack_forget()

    # --- Temas / fondos ------------------------------------------------------
    def _toggleThemeMenu(self):
        if self.themeMenu.winfo_viewable():
            self.themeMenu.pack_forget()
        else:
            self.themeMenu.pack(pady=5, padx=10, fill="x")

    def _selectTheme(self, themeName: str):
        # Cambia paleta + fondo y reconstruye panel izquierdo y vistas.
        if themeName not in PALETTES:
            return
        self.palette = PALETTES[themeName]
        self.currentThemeName = themeName
        self._loadPaletteAttrs()
        self.configure(fg_color=self.WOOD_DARKEST)
        self._loadBackgroundImage(self.palette.image_file)
        self._rebuildLeftPanel()
        for view in self._views.values():
            view.applyPalette(self.palette)
        # La vista activa fue reconstruida y necesita re-mostrarse.
        activeView = self._views.get(self._activeViewName)
        if activeView is not None:
            activeView.show()
        if self.themeMenu.winfo_viewable():
            self.themeMenu.pack_forget()

    def _loadBackgroundImage(self, imageFilename: str):
        try:
            imagePath = os.path.join(self.assetsPath, imageFilename)
            if not os.path.exists(imagePath):
                print(f"Imagen no encontrada: {imagePath}")
                return
            image = Image.open(imagePath).resize(
                (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), Image.Resampling.LANCZOS
            )
            self._backgroundCtkImage = ctk.CTkImage(
                light_image=image, dark_image=image,
                size=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
            )
            self.backgroundLabel.configure(image=self._backgroundCtkImage, text="")
            self.backgroundLabel.lower()
        except Exception as imageError:
            print(f"Error al cargar imagen: {imageError}")
