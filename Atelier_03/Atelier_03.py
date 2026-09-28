import sys

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
 
class MessageBoard(QWidget):
    def __init__(self): # Contructeur
        super().__init__() # Constructeur du parent (QWidget)
        self.setWindowTitle("Message board")
        self.create_ui()

    def create_ui(self):
        print("create UI")
        layout = QVBoxLayout(self)
        label = QLabel("Message Board")
        layout.addWidget(label)

        # QTextEdit

        # Qpushbutton

    def on_click(self):
        print("on click")

        # QmessgaeBox
 
def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()