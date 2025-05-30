import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app'))


def test_led_gui():
    try:
        from app.view.led_gui import LEDWindow
        from PyQt6.QtWidgets import QApplication
    except ImportError as e:
        print(f"ImportError: {e}")
        return
    
    app = QApplication(sys.argv)
    main_window = LEDWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_led_gui()