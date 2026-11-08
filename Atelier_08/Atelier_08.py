# DOCUMENTATION COMMENT UTILISER L'OUTILS ET METTRE IMAGE
#   1) COPIER LE CODE PYTHON IMPORTER DANS UN TAB PYTHON DU SCRIPT EDITOR DE MAYA
#   2) CRÉER UN SHELF À L'AIDE DU PETIT ENGRENAGE DU SHELF EDITIOR EN HAUT À GAUCHE DE LA FENÊTRE MAYA
#   3) SELECTIONNER TOUT VOTRE CODE PYTHON ET AVEC LE BUTON DU MILIEU DE VOTRE SOURI, CLICKER ET AMENER JUSQU'À VOTRE SHELF VIDE
#   4) UNE ICONE DEVRAIT APPARAÎTRE
#   5) VOUS POUVEZ TESTER LE CODE EN CLIQUANT DIRECTEMENT SUR L'ICON, VOTRE CODE DEVRAIT S'EXECUTER
#   6) POUR CHANGER L'ICON DE CE NOUVEL OUTIL, FAITES UN CLICK DROIT SUR L'ICON ET SELECTIONNER "EDIT"
#   7) ALLER DANS L'ONGLET "SHELVES" EN HAUT À DROITE DE LA FENÈTRE
#   8) VOUS ALLER VOIR VERS LE BAS "ICON NAME", VOUS ALLLER CLICKER SUR LE DOSSIER À DROITE
#   9) ALLER CHERCHER L'IMAGE DE VOTRE CHOIX
#  
#
from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QCheckBox, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QStackedLayout
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtCore import QRectF
from PySide6.QtCore import QSizeF
import maya.cmds as cmds

class RandomAnimationUI(QWidget):
    def __init__(self):
            super().__init__()
            self.setWindowTitle("Outliner Organiser") #Window Settings
            self.setFixedSize(600, 300)
    
            self.scene = QGraphicsScene(self)
    
            self.video_item = QGraphicsVideoItem()
            self.scene.addItem(self.video_item)
            self.video_item.setSize(QSizeF(self.size()))
    
            self.video_view = QGraphicsView(self.scene, self)
            self.video_view.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )
            self.video_view.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )
            self.video_view.setFrameShape(QGraphicsView.Shape.NoFrame)
            self.video_view.setStyleSheet("background: transparent;")
            self.video_view.setBackgroundBrush(Qt.GlobalColor.transparent)
            self.video_view.setGeometry(self.rect()
            )
            self.video_view.lower()
    
            # Keep the video behind the normal UI
            panel = QWidget(self)
            panel.setAttribute(
                Qt.WidgetAttribute.WA_TranslucentBackground, True
            )
            panel.setAutoFillBackground(False)
            panel.setStyleSheet("background: transparent;")
            panel.setGeometry(self.rect())
            panel.raise_()
    
            layout = QVBoxLayout(panel)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
    
    
            # Local looping video background (change this path)
            self.audio = QAudioOutput()
            self.audio.setVolume(10)
    
            self.player = QMediaPlayer()
            self.player.setAudioOutput(self.audio)
            self.player.setVideoOutput(self.video_item)
    
            video_path = r"C:\Users\mpuget\_Session3\26_Python\CyberPunk2_Back.mp4"
            self.player.setSource(QUrl.fromLocalFile(video_path))
            self.player.setLoops(QMediaPlayer.Loops.Infinite)
            self.player.play()
    
            #layout.addWidget(QLabel("enter JSON rule path pretty please n thank u")) # Set Box For Json File
            #self.path_input = QLineEdit()
            #self.path_input.setPlaceholderText("Path to rules.json")
            #layout.addWidget(self.path_input)
    
            #self.selection = QCheckBox("Apply on selection only") # Add Check Boxes For Options (Set To False On Start)
            #self.selection.setChecked(False)
            #self.colors = QCheckBox("Apply colors")
            #self.colors.setChecked(False)
            #self.reorder = QCheckBox("Apply reorder")
            #self.reorder.setChecked(False)
    
            #for checkbox in (self.selection, self.colors, self.reorder):
            #    layout.addWidget(checkbox)
    
    
            self.setStyleSheet("""
        OutlinerOrganiser {
            background: transparent;
        }
    
        QWidget {
            background: transparent;
        }
    
        QLabel {
            background: transparent;
            color: #F04E29;
            font-family: "Segoe UI";
            font-size: 13px;
        }
    
        QLineEdit {
            background-color: #0D0B0B;
            border: 2px solid #FF0000;
            border-radius: 3px;
            padding: 7px;
            color: #FF0000;
            font-family: "Segoe UI";
            font-size: 13px;
        }
    
        QPushButton {
            background-color: #5E0000;
            color: #FFFFFF;
            border: 2px solid #F04E29;
            border-radius: 3px;
            padding: 6px;
            font-family: "Segoe UI";
            font-size: 13px;
        }
    
        QPushButton:hover {
            background-color: #990000;
            border: 2px solid #FFFFFF;
        }
    
        QCheckBox {
            background: transparent;
            color: #F04E29;
            spacing: 8px;
            font-family: "Segoe UI";
            font-size: 13px;
        }
    
        QCheckBox::indicator {
            width: 15px;
            height: 15px;
        }
    
        QCheckBox::indicator:unchecked {
            background-color: #0D0B0B;
            border: 1px solid #F04E29;
        }
    
        QCheckBox::indicator:checked {
            background-color: #FF0000;
            border: 1px solid #FFFFFF;
        }
    """)

import os
import sys
import importlib
import maya.cmds as cmds

# Obtenue le folder dans lequel il y a notre fichier courant 
# __file__ = le fichier courant
#absolute_file_path = os.path.abspath(__file__)
#absolute_folder_path = os.path.dirname(absolute_file_path)
#print(absolute_folder_path)
# On vient ajouter absolute_folder_path au path de python pour quil puisse trouver ui.py
#sys.path.append(absolute_folder_path)

# APRES ON IMPORT LES CHOSES

#absolute_path = os.path.abspath(os.path.curdir)
#print(absolute_path)

def main():                                     # Main Function
    global widget                               # Setup UI
    try:                                        #
        widget.close()                          # Closes Past Windows
        widget.deleteLater()                    #
    except (NameError, RuntimeError):           #
        pass                                    #
    widget = RandomAnimationUI()                      # Build Window
    widget.show()                               # Show Window
                                                
main()