import json
import os
import maya.cmds as cmds #Import Maya Commands into Python Scripts

from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QCheckBox, QPushButton, QFileDialog, QMessageBox)

class OutlinerOrganiser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Outliner Organiser") #Window Settings
        self.setFixedSize(600, 300)

        layout = QVBoxLayout(self) # Window Element Spacing
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addWidget(QLabel("enter JSON rule path pretty please n thank u")) # Set Box For Json File
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Path to rules.json")
        layout.addWidget(self.path_input)

        browse = QPushButton("Browse JSON...") # Add Button To Browse For Json File
        browse.clicked.connect(self.browse_json)
        layout.addWidget(browse)

        self.selection = QCheckBox("Apply on selection only") # Add Check Boxes For Options (Set To False On Start)
        self.selection.setChecked(False)
        self.colors = QCheckBox("Apply colors")
        self.colors.setChecked(False)
        self.reorder = QCheckBox("Apply reorder")
        self.reorder.setChecked(False)

        for checkbox in (self.selection, self.colors, self.reorder):
            layout.addWidget(checkbox)

        button = QPushButton("Organise Outliner") # Add Button For Organiser
        button.clicked.connect(self.organise)
        layout.addWidget(button)

        self.setStyleSheet( # Window Setting Details/Colors
        """
            QWidget { background:#0D0B0B; color:#F04E29; font-family:"Segoe UI"; font-size:13px; }
            QLineEdit { background:#0D0B0B; border:2px solid #FF0000; border-radius:3px; padding:7px; color:#FF0000; }
            QPushButton { background:#5E0000; border:none; border-radius:2px; padding:5px; }
            QPushButton:hover { background:#990000; }
            QCheckBox { color:#990000;spacing:8px; }
        """)

    def browse_json(self): # Function To Search Json File Using The Browse Button
        path, _ = QFileDialog.getOpenFileName(
            self, "Select JSON Rules PLEASE n tahnk u", "", "JSON Files (*.json)" # "Name Of Window","Start Of Path","Filters .json Only"
        )
        if path:
            self.path_input.setText(path) # Puts The Path In The Search Bar

    def load_rules(self): # Function To Load Json File
        path = self.path_input.text().strip()                               #
        if not path or not os.path.isfile(path):                            # Check If Path Is OK
            raise ValueError("Please select a valid JSON rules file.")      #

        with open(path, encoding="utf-8") as file:                          # Open Json And Set As File Variable
            rules = json.load(file)                                         # Data Of File Stored Inside Rules Variable

        if not isinstance(rules, dict) or not rules:                        # Check If Data Is Dictionary Or Empty
            raise ValueError("JSON must contain prefix/color rules.")       #

        for prefix, rgb in rules.items():                                   # Check If Items Are OK
            if (not isinstance(prefix, str) or not prefix                   #
                    or not isinstance(rgb, list) or len(rgb) != 3           # Check If List Or Length Of 3
                    or any(not isinstance(v, (int, float))                  # Check If Numbers Are Between 0 And 1
                           or isinstance(v, bool) or not 0 <= v <= 1        #
                           for v in rgb)):                                  #
                raise ValueError(f"Invalid rule for prefix: {prefix}")      #

        return rules

    def get_targets(self, rules):                                               # Function To Select Element In Maya List
        if self.selection.isChecked():                                          # Is Checked? Yes
            nodes = cmds.ls(selection=True, long=True, objectsOnly=True) or []  #
            if not nodes:                                                       #
                raise ValueError("Select objects in Maya first.")               # Checked And No Object Selected
        else:                                                                   # Is Checked? No
            nodes = cmds.ls(type="transform", long=True) or []                  # 
        return list(dict.fromkeys(                                              # Return List Of Nodes
            node for node in nodes                                              # Matches with Json Data
            if cmds.nodeType(node) == "transform"                               #
            and any(node.rsplit("|", 1)[-1].startswith(p) for p in rules)       #
        ))

    def apply_colors(self, nodes, rules):                                               # Function To Apply Colors
        count = 0                                                                       #
        for node in nodes:                                                              # Nodes Returned By Function get_targets
            name = node.rsplit("|", 1)[-1]                                              # Get Node Short Name
            prefix = next((p for p in rules if name.startswith(p)), None)               # Find Matching Prefix Between Json And Maya
            if prefix is not None:                                                      # If Matching Found
                cmds.setAttr(node + ".useOutlinerColor", 1)                             #
                cmds.setAttr(node + ".outlinerColor", *rules[prefix], type="double3")   # 
                count += 1                                                              #
        return count                                                                    #

    def reorder_objects(self, nodes, rules):                                            #
        groups = {}                                                                     #
        for node in nodes:                                                              # Process All Objects
            parents = cmds.listRelatives(node, parent=True, fullPath=True) or []        # Check if Object Has Parent
            groups.setdefault(parents[0] if parents else None, []).append(node)         # Puts Same Parent Objects In Groups
        prefixes = {p: i for i, p in enumerate(rules)}                                  # Gives Each Prefixes A Priority For Sorting
                                                                                        #
        def key(node):                                                                  #
            name = node.rsplit("|", 1)[-1]                                              # Short Name For Objects
            prefix = next((p for p in prefixes if name.startswith(p)), "")              # 
            return prefixes.get(prefix, len(prefixes)), name.lower()                    # Sort Objects by Prefixes and Priority Number
        count = 0                                                                       #
                                                                                        #
        for siblings in groups.values():                                                #
            for node in reversed(sorted(siblings, key=key)):                            # Reverse Order For Better Sorting Final Order
                if cmds.objExists(node):                                                # Check If Object Is Still Valid
                    try:                                                                #
                        cmds.reorder(node, front=True)                                  # Sorts
                        count += 1                                                      #
                    except RuntimeError:                                                #
                        pass                                                            # Passes Object
        return count                                                                    #

    def organise(self):                                                                             # Main Function To Organise
        opened = False                                                                              #
        try:                                                                                        #
            rules = self.load_rules()                                                               # Load Json Data
            nodes = self.get_targets(rules)                                                         # Load Nodes (Selected)
            if not nodes:                                                                           # Check If Matching Objects Are Found
                QMessageBox.information(self, "Organiser", "No matching objects.")                  #
                return                                                                              #
                                                                                                    #
            cmds.undoInfo(openChunk=True, chunkName="OutlinerOrganiser")                            # Undo Operation
            opened = True                                                                           #
            colors = self.apply_colors(nodes, rules) if self.colors.isChecked() else 0              # Set Colors To Nodes If Checked
            reordered = self.reorder_objects(nodes, rules) if self.reorder.isChecked() else 0       # Reorder Nodes If Checked
            cmds.undoInfo(closeChunk=True)                                                          #
            opened = False                                                                          #
                                                                                                    #
            print(f"Matched: {len(nodes)}, colors: {colors}, reordered: {reordered}")               # Print In Maya Summary
                                                                                                    #
        except Exception as error:                                                                  # Criticals Errors While Chunk Is Open
            if opened:                                                                              #
                cmds.undoInfo(closeChunk=True)                                                      #
            QMessageBox.critical(self, "Outliner Organiser", str(error))                            #


def main():                                     # Main Function
    global widget                               # Setup UI
    try:                                        #
        widget.close()                          # Closes Past Windows
        widget.deleteLater()                    #
    except (NameError, RuntimeError):           #
        pass                                    #
    widget = OutlinerOrganiser()                # Build Window
    widget.show()                               # Show Window
                                                
main()                                          # Calls Main Function