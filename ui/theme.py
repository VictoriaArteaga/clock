# Paletas de colores por tema. Cada paleta mapea un fondo a colores significativos
# de la imagen. La GUI mantiene una Palette activa y todas las vistas la consultan.

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    name: str
    image_file: str

    PRIMARY: str         # color principal de los botones.
    PRIMARY_HOVER: str

    LIGHT: str           # plaquetas claras (placas de madera).
    MED: str             # madera media (anillo del reloj, fondos secundarios).
    DARK: str            # bordes oscuros.
    DARKEST: str         # panel lateral / fondos profundos.
    PARCHMENT: str       # color pergamino del interior del reloj.
    INK: str             # texto principal sobre fondos claros.
    RED: str             # alertas y disparo de alarmas.
    RED_DARK: str
    GREEN: str = "#3a7d3a"  # verde para los switches activos.


# Londres: dorado y maderas (paleta original con los colores de Big Ben).
LONDRES = Palette(
    name="Londres",
    image_file="fondoLondres.jpg",
    PRIMARY="#d4af37",
    PRIMARY_HOVER="#c99f27",
    LIGHT="#c9a876",
    MED="#8b6f47",
    DARK="#5c4a2e",
    DARKEST="#2c1810",
    PARCHMENT="#f0e6d2",
    INK="#2c1810",
    RED="#c41e3a",
    RED_DARK="#8b1525",
)

# Praga: terracota y crema (tejados rojizos y piedra arenisca).
PRAGA = Palette(
    name="Praga",
    image_file="fondoPraga.jpg",
    PRIMARY="#c75b3a",
    PRIMARY_HOVER="#a8462a",
    LIGHT="#e8c89e",
    MED="#9c6f4a",
    DARK="#5e3a22",
    DARKEST="#2a1810",
    PARCHMENT="#f5e6d0",
    INK="#2a1810",
    RED="#c41e3a",
    RED_DARK="#8b1525",
)

# Kremlin: rojo profundo y crema calido (muros y cupulas doradas).
KREMLIN = Palette(
    name="Kremlin",
    image_file="fondoKremlin.jpg",
    PRIMARY="#b32024",
    PRIMARY_HOVER="#921b1f",
    LIGHT="#d9bc88",
    MED="#7a5a3e",
    DARK="#48301c",
    DARKEST="#1f140d",
    PARCHMENT="#f0e0c0",
    INK="#1f140d",
    RED="#a8232c",
    RED_DARK="#7a161e",
)

PALETTES = {
    "Londres": LONDRES,
    "Praga": PRAGA,
    "Kremlin": KREMLIN,
}
