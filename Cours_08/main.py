import os
import sys
import importlib
import maya.cmds as cmds

# Obtenue le folder dans lequel il y a notre fichier courant 
# __file__ = le fichier courant
absolute_file_path = os.path.abspath(__file__)
absolute_folder_path = os.path.dirname(absolute_file_path)
print(absolute_folder_path)
# On vient ajouter absolute_folder_path au path de python pour quil puisse trouver ui.py
sys.path.append(absolute_folder_path)

# APRES ON IMPORT LES CHOSES
import ui
from ui import RandomAnimationUI
importlib.reload(ui)

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