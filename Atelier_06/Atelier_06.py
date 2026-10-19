import json
import os
import maya.cmds as cmds #Import Maya Commands into Python Scripts

from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QCheckBox, QPushButton, QFileDialog, QMessageBox)

class CreateFence(QWidget):
    def __init__(self):
        super().__init__()
        self.fence_count = 0
        self.setWindowTitle("Generate Fence To Save Village") #Window Settings
        self.setFixedSize(600, 300)

        layout = QVBoxLayout(self) # Window Element Spacing
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Build A Fence Using The Boxes Below!")) # Set Box For Json File

        layout.addWidget(QLabel("Set Length Of Fences")) # Set Box For Json File

        # BOX TO SET NUMBER OF FENCES / LENGTH
        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Length...")
        layout.addWidget(self.length_input)

        # BUTTON FOR NUMBER OF FENCES / LENGTH
        browse = QPushButton("Apply Settings...") # Add Button To Browse For Json File
        browse.clicked.connect(self.length_fence)
        layout.addWidget(browse)

        layout.addWidget(QLabel("Set Height Of Fence")) # Set Box For Json File

        # BOX TO SET HEIGHT OF FENCE
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Height...")
        layout.addWidget(self.height_input)

        # BUTTON FOR HEIGHT
        browse = QPushButton("Apply Settings...") # Add Button To Browse For Json File
        browse.clicked.connect(self.height_fence)
        layout.addWidget(browse)

        # BUTTON TO GENERATE FENCE IN MAYA
        button = QPushButton("Generate Fence!") # Add Button For Organiser
        button.clicked.connect(self.create_fence)
        layout.addWidget(button)

        self.setStyleSheet( # Window Setting Details/Colors
        """
            QWidget { background:#0D0B0B; color:#F04E29; font-family:"Segoe UI"; font-size:13px; }
            QLineEdit { background:#0D0B0B; border:2px solid #FF0000; border-radius:3px; padding:7px; color:#FF0000; }
            QPushButton { background:#5E0000; border:none; border-radius:2px; padding:5px; }
            QPushButton:hover { background:#990000; }
            QCheckBox { color:#990000;spacing:8px; }
        """)

    def length_fence(self): # Function To Set Length Of Fence
        length_value = int(self.length_input.text())
        print("LENGTH OF FENCE:", length_value)
        return length_value

    def height_fence(self): # Function To Set Height Of Fence
        height_value = int(self.height_input.text())
        print("HEIGHT OF FENCE:", height_value)                                                   
        return height_value

    def create_cubes(self, i):
        post_height_value = self.height_fence()
        post_length_value = 0.5
        post_thickness_value = 0.5
        post_distance_value = 0

        board_height_value = post_height_value/8
        board_length_value = 3
        board_thickness_value = 0.3
        board_distance_value = post_distance_value+1.5

        cmds.polyCube(name=f"Post_{i}", width=post_length_value, height=post_height_value, depth=post_thickness_value)
        cmds.move(post_distance_value, post_height_value/2, 0, f"Post_{i}")
        cmds.polyCube(name=f"Board_{i}", width=board_length_value, height=board_height_value, depth=board_thickness_value)
        cmds.move(board_distance_value, post_height_value*0.75, 0, f"Board_{i}")
        cmds.polyCube(name=f"Board2_{i}", width=board_length_value, height=board_height_value, depth=board_thickness_value)
        cmds.move(board_distance_value, post_height_value*0.45, 0, f"Board2_{i}")
        cmds.polyCube(name=f"Post2_{i}", width=post_length_value, height=post_height_value, depth=post_thickness_value)
        cmds.move(post_distance_value+3, post_height_value/2, 0, f"Post2_{i}")

        fence_group = cmds.group(f"Post_{i}", f"Board_{i}", f"Board2_{i}", f"Post2_{i}", name =f"FenceGroup_{i}")

    def create_fence(self):
        length_value = self.length_fence()
        fence_distance = 3
        self.fence_count += 1

        all_sections = []

        for i in range(length_value):
            fence_group = self.create_cubes(i)
            cmds.move(fence_distance*i, 0, 0, fence_group, relative=True)
            all_sections.append(fence_group)

        cmds.group(all_sections, f"Fence_{self.fence_count}")
        print("FENCE CREATED ! ! !")

def main():                                     # Main Function
    global widget                               # Setup UI
    try:                                        #
        widget.close()                          # Closes Past Windows
        widget.deleteLater()                    #
    except (NameError, RuntimeError):           #
        pass                                    #
    widget = CreateFence()                      # Build Window
    widget.show()                               # Show Window
                                                
main()                                          # Calls Main Function