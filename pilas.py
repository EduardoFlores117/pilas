from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, 
    QVBoxLayout, QWidget, QMessageBox, QInputDialog
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Configuración básica de la ventana
        self.setWindowTitle("Aplicación de Pilas - Ejercicios")
        self.setGeometry(100, 100, 500, 400)

        # Aplicar estilo CSS modernizado con tema oscuro y mejoras visuales
        self.setStyleSheet("""
            QWidget {
                background-color: #2c2f33;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                margin: 10px;
                border-radius: 10px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #2c2f33;
                color: #4CAF50;
                border: 2px solid #4CAF50;
                transition: background-color 0.3s ease, color 0.3s ease;
                box-shadow: 3px 3px 10px #4CAF50;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                padding: 5px;
                border: 1px solid #000000;
                border-radius: 5px;
                transition: border-color 0.3s ease;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)

        # Etiqueta del título
        self.title_label = QLabel("Seleccione un ejercicio", self)
        self.title_label.setFont(QFont("Arial", 24))
        self.title_label.setAlignment(Qt.AlignCenter)

        # Botones para cada ejercicio con iconos
        self.btn1 = QPushButton("1. Invertir palabra", self)
        self.btn1.setIcon(QIcon('icons/flip_icon.png'))
        self.btn1.setIconSize(QSize(24, 24))
        self.btn1.clicked.connect(self.invertir_palabra)

        self.btn2 = QPushButton("2. Palíndromo", self)
        self.btn2.setIcon(QIcon('icons/palindrome_icon.png'))
        self.btn2.setIconSize(QSize(24, 24))
        self.btn2.clicked.connect(self.palindromo)

        self.btn3 = QPushButton("3. Suma de números grandes", self)
        self.btn3.setIcon(QIcon('icons/sum_icon.png'))
        self.btn3.setIconSize(QSize(24, 24))
        self.btn3.clicked.connect(self.sumar_numeros_grandes)

        self.btn4 = QPushButton("4. Reemplazar valor en pila", self)
        self.btn4.setIcon(QIcon('icons/replace_icon.png'))
        self.btn4.setIconSize(QSize(24, 24))
        self.btn4.clicked.connect(self.reemplazar_valor_pila)

        # Agregar animación de hover a los botones
        self.create_button_animation(self.btn1)
        self.create_button_animation(self.btn2)
        self.create_button_animation(self.btn3)
        self.create_button_animation(self.btn4)

        # Layout para organizar los widgets
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addWidget(self.btn4)

        # Configuración del widget principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_button_animation(self, button):
        """Crea una animación de hover suave en los botones."""
        animation = QPropertyAnimation(button, b"maximumSize")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutCubic)
        button.animation = animation

    def get_input(self, prompt):
        """Muestra un diálogo para ingresar texto."""
        while True:
            text, ok = QInputDialog.getText(self, 'Entrada', prompt)
            if ok:
                if text.strip():
                    return text
                else:
                    QMessageBox.warning(self, "Advertencia", "Este campo no puede estar vacío.")
            else:
                return None

    def invertir_palabra(self):
        palabra = self.get_input("Ingrese una palabra para invertir:")
        if palabra:
            pila = list(palabra)
            invertida = []
            while pila:
                invertida.append(pila.pop())
            resultado = ''.join(invertida)
            QMessageBox.information(self, "Resultado", f"Palabra invertida: {resultado}")

    def palindromo(self):
        palabra = self.get_input("Ingrese una palabra para verificar si es palíndromo:")
        if palabra:
            pila = list(palabra)
            es_palindromo = True
            for i in range(len(palabra) // 2):
                if palabra[i] != pila.pop():
                    es_palindromo = False
                    break
            if es_palindromo:
                QMessageBox.information(self, "Resultado", f"La palabra '{palabra}' es un palíndromo.")
            else:
                QMessageBox.information(self, "Resultado", f"La palabra '{palabra}' no es un palíndromo.")

    def sumar_numeros_grandes(self):
        num1 = self.get_input("Ingrese el primer número grande:")
        num2 = self.get_input("Ingrese el segundo número grande:")
        if num1 and num2:
            try:
                pila1 = list(map(int, num1))
                pila2 = list(map(int, num2))
                resultado = []
                carry = 0
                while pila1 or pila2 or carry:
                    digito1 = pila1.pop() if pila1 else 0
                    digito2 = pila2.pop() if pila2 else 0
                    suma = digito1 + digito2 + carry
                    carry = suma // 10
                    resultado.append(suma % 10)
                resultado.reverse()
                QMessageBox.information(self, "Resultado", f"La suma de los números es: {''.join(map(str, resultado))}")
            except ValueError:
                QMessageBox.warning(self, "Advertencia", "Por favor ingrese números válidos.")

    def reemplazar_valor_pila(self):
        pila_input = self.get_input("Ingrese los valores de la pila separados por espacio (Ej: 4 5 6 7 8):")
        if not pila_input:
            return
        try:
            pila = list(map(int, pila_input.split()))
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese solo números enteros.")
            return

        valor_viejo = self.get_input("Ingrese el valor que desea reemplazar:")
        valor_nuevo = self.get_input("Ingrese el nuevo valor que reemplazará al viejo:")

        if valor_viejo is None or valor_nuevo is None:
            return
        try:
            valor_viejo = int(valor_viejo)
            valor_nuevo = int(valor_nuevo)
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese solo números enteros.")
            return

        for i in range(len(pila)):
            if pila[i] == valor_viejo:
                pila[i] = valor_nuevo
        QMessageBox.information(self, "Resultado", f"Pila después del reemplazo: {' '.join(map(str, pila))}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
