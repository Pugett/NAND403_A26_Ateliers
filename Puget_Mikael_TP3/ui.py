from PySide6.QtWidgets import QWidget, QSlider, QVBoxLayout, QPushButton, QLabel, QApplication, QSpinBox, QGridLayout, QHBoxLayout, QGroupBox
from maya import cmds
import maya.OpenMayaUI as omui                                                                  # IMPORT FOR "ALWAYS ON TOP"
from shiboken6 import wrapInstance                                                              #
from PySide6.QtCore import Qt, Signal
from Puget_Mikael_TP3 import animator

def maya_main_window():                                                                         # "ALWAYS ON TOP"
    pointer = omui.MQtUtil.mainWindow()                                                         #
    return wrapInstance(int(pointer), QWidget)                                                  #

class RandomAnimInterface(QWidget):
    generate_clicked = Signal()
    def __init__(self):
        super().__init__(maya_main_window())                                                    # "ALWAYS ON TOP" INSIDE __INIT__
        self.setWindowFlags(Qt.Window)                                                          #
        
        self.build_ui()                                                                         # CALLS BUILD UI FUNCTION

    def build_ui(self):
        self.setWindowTitle("Random Animation")
        self.setFixedSize(370, 610)

        main_layout = QVBoxLayout(self)                                                         # MAIN LAYOUT
        main_layout.setContentsMargins(12, 10, 12, 10)                                          #
        main_layout.setSpacing(10)                                                              #

        timing = QGroupBox("Animation Timing")                                                  # BOX #1 : ANIMATION TIMING
        timing_layout = QGridLayout(timing)                                                     #
                                                                                                
        self.duration = QSpinBox()                                                              # DURATION BOX
        self.duration.setRange(1, 10000)                                                        #
        self.duration.setValue(100)                                                             #
                                                                                                
        self.step = QSpinBox()                                                                  # STEP BOX
        self.step.setRange(1, 10000)                                                            #
        self.step.setValue(30)                                                                  #

        timing_layout.addWidget(QLabel("Durations (Frames):"), 0, 0)                            # LABEL DURATION
        timing_layout.addWidget(self.duration, 0, 1)                                            #
        timing_layout.addWidget(QLabel("Step (Frames):"), 0, 2)                                 # LABEL STEP
        timing_layout.addWidget(self.step, 0, 3)                                                #

        main_layout.addWidget(timing)                                                           # ADD BOX #1 TO MAIN LAYOUT

        self.translate = self.create_parameter_group(                                           # BOX #2 : TRANSLATE PARAMETERS
            "Translate Parameters",                                                             #
            ["x", "y", "z"],                                                                    #
            [-5, -5, -5],                                                                       #
            [5, 5, 5],                                                                          #
            -1000, 1000)                                                                        #

        main_layout.addWidget(self.translate["group"])                                          # ADD BOX #2 TO MAIN LAYOUT

        self.rotate = self.create_parameter_group(                                              # BOX #3 : ROTATE PARAMETERS
            "Rotate Parameters",                                                                #
            ["x", "y", "z"],                                                                    #
            [-180, -180, -180],                                                                 #
            [180, 180, 180],                                                                    #
            -360, 360)                                                                          #

        main_layout.addWidget(self.rotate["group"])                                             # ADD BOX #3 TO MAIN LAYOUT

        self.scale = self.create_parameter_group(                                               # BOX #4 : SCALE PARAMETERS
            "Scale Parameters",                                                                 #
            ["x", "y", "z"],                                                                    #
            [1, 1, 1],                                                                          #
            [2, 2, 2],                                                                          #
            0, 100)                                                                             #

        main_layout.addWidget(self.scale["group"])                                              # ADD BOX #4 TO MAIN LAYOUT

        self.generate_button = QPushButton("Generate")                                          # CREATE GENERATE BUTTON
        self.generate_button.clicked.connect(self.generate_animation)                           #

        main_layout.addWidget(self.generate_button)                                             # ADD BUTTON TO MAIN LAYOUT

        self.setStyleSheet                                                                      # STYLE
        ("""
            QWidget {background-color: #383838; color: #dddddd; font-size: 10px;}
            QGroupBox {border: 1px solid #414141; border-radius: 3px; margin-top: 10px; padding-top: 12px; font-weight: normal; color: #cccccc;}
            QGroupBox::title {subcontrol-origin: margin; left: 8px; padding: 0 3px;}
            QLabel {color: #cccccc;}
            QSpinBox {background-color: #505050; border: 1px solid #242424; border-radius: 2px; padding: 3px; min-width: 55px; color: white;}
            QSpinBox::up-button,
            QSpinBox::down-button {background-color: #666666; border: none; width: 15px;}
            QPushButton {background-color: #595959; border: 1px solid #666666; padding: 4px; color: white;}
            QPushButton:hover {background-color: #707070;}
            QPushButton:pressed {background-color: #454545;}
        """)

    def create_parameter_group(self, title, axes, min_values, max_values, min_range, max_range):# FUNCTION TO CREATE PARAMETER GROUPS (BOXES FOR UI)
        group = QGroupBox(title)
        layout = QGridLayout(group)

        min_inputs = {}
        max_inputs = {}

        for i, axis in enumerate(axes):                                                         # GET POSITION NUMBER (i) & CURRENT ELEMENT (AXIS)
            min_spin = QSpinBox()                                                               # MINIMUM INPUT
            min_spin.setRange(min_range, max_range)                                             #
            min_spin.setValue(min_values[i])                                                    #

            max_spin = QSpinBox()                                                               # MAXIMUM INPUT
            max_spin.setRange(min_range, max_range)                                             #
            max_spin.setValue(max_values[i])                                                    #

            min_inputs[axis] = min_spin                                                         # STORE INPUT IN BOXES (EX. LOOP #1 X, LOOP #2 Y)
            max_inputs[axis] = max_spin                                                         #

            layout.addWidget(QLabel(f"min {axis}:"), 0, i * 2)                                  # ADD MIN WIDGET TO GRID
            layout.addWidget(min_spin, 0, i * 2 + 1)                                            #

            layout.addWidget(QLabel(f"max {axis}:"), 1, i * 2)                                  # ADD MAX WIDGET TO GRID
            layout.addWidget(max_spin, 1, i * 2 + 1)                                            #

        return {"group": group, "min": min_inputs, "max": max_inputs}                           # RETURNS : GROUP, MIN, MAX

    def get_parameters(self):                                                                   # GET ALL VALUES FROM THE INTERFACE (UI)
        parameters = {"duration": self.duration.value(), "step": self.step.value(), "translate": {}, "rotate": {}, "scale": {}}     # DICTIONNARY CONTAINS ALL ANIMATION SETTTINGS

        for name, group in [                                                                    # LOOPS THOUGH 3 PARAMETERS GROUPS
            ("translate", self.translate),                                                      #
            ("rotate", self.rotate),                                                            #
            ("scale", self.scale)]:                                                             #

            for axis in ["x", "y", "z"]:                                                        # FOR EVERY ANIMATION TYPE GO THOUGH 3 AXES
                parameters[name][axis] = {                                                      # RETRIEVE VALUES
                    "min": group["min"][axis].value(),                                          #
                    "max": group["max"][axis].value()}                                          #      

        return parameters                                                                       # RETURNS ALL PARAMETERS

    def generate_animation(self):                                                               # FUNCTION TO CONNECT UI TO ANIMATOR
        parameters = self.get_parameters()                                                      # COLLECTS ALL PARAMETERS IN UI

        try:                                                                                    #
            animator.generate_random_animation(parameters)                                      # FUNCTION IN ANIMATOR
        except ValueError as error:                                                             #
            print(error)                                                                        #

def show_random_anim():                                                                         # FUNCTION TO SHOW UI
    global random_anim                                                                          #
    try:                                                                                        #
        random_anim.close()                                                                     #
    except Exception:                                                                           #   
        pass                                                                                    #
    random_anim_interface = RandomAnimInterface()                                               #
    random_anim_interface.show()                                                                # SHOW UI