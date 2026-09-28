#Atelier 02
#Lire un fichier JSON et faire un interface graphique avec PySide6 pour que le cowboy puisse voir les drinks offerts

"""
Liste a faire
1- Ouvrir un fichier JSON
    -> Path
    -> Fonction load

Create JSON FILE
Python Debugger
Pythong Debugger with arguments

    -> Faire une fenetre UI
    c:\WPy64-31180\python-3.11.8.amd64\python.exe -m venv .venv
    
"""
import sys
import json
from PySide6.QtWidgets import(
    QApplication,
    QMainWindow,
    QTableWidget
)

file_path = sys.argv[1]
print("JSON FILE >>>>>>>>> " + file_path + " <<<<<<<<<")

#Loader le Json File
try:
    file = open(file_path)
    data = json.load(file)
    print(type(data))
except:
    print(f"Erreur de chargement du fichier {file_path}")

#Parcourir les elemets du tableau
#possible aussi avec values i.values():
for i in data:
    for k in i.keys():
        print(f"     - {k}")

app = QApplication([])
window = QMainWindow();
window.show()
sys.exit(app.exec())