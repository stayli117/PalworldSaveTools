"""IME-friendly popup helpers.

On Windows, windows created with the Qt.Popup flag never receive OS-level
window activation, so the input method editor (IME) cannot attach to them.
As a result, search boxes inside such popups cannot switch to Chinese (or any
IME-based) input.

Workaround: use a frameless Qt.Tool window instead (it can be activated, so
the IME works), and emulate Qt.Popup's "close when clicking outside / losing
activation" behavior with an event filter.
"""
from PySide6.QtCore import Qt, QEvent, QObject


class _AutoCloseFilter(QObject):
    """Hide the popup when it loses activation or when Esc is pressed."""

    def eventFilter(self, obj, ev):
        et = ev.type()
        if et == QEvent.WindowDeactivate:
            obj.hide()
        elif et == QEvent.KeyPress and ev.key() == Qt.Key_Escape:
            obj.hide()
            return True
        return False


def setup_ime_popup(popup):
    """Configure a frameless popup widget so that IME input works inside it.

    Use this instead of `setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)`
    whenever the popup contains a QLineEdit or other text input.
    """
    popup.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    # Parent the filter to the popup so it stays alive with it.
    popup.installEventFilter(_AutoCloseFilter(popup))


def show_ime_popup(popup):
    """Show and activate the popup so the IME attaches to its focused input."""
    popup.show()
    popup.raise_()
    popup.activateWindow()
