import sys
import os

# Permitimos que `python clock/main.py` resuelva el paquete `clock.*`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clock.ui.ClockGui import ClockGui


def main():
    app = ClockGui()
    app.mainloop()


if __name__ == "__main__":
    main()
