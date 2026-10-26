import json
import os
import maya.cmds as cmds

def get_targets():                                               # Function To Select Element In Maya List
    nodes = cmds.ls(selection=True, long=True, objectsOnly=True) or []  #
    if not nodes:                                                       #
        raise ValueError("Select objects in Maya first.")               # Checked And No Object Selected                  #
    return nodes

def main():
    cmds.playbackOptions(min=0, max=100)
    nodes = get_targets()
    value = 0;
    time =0;
    cmds.cutKey(nodes, clear=True) 
    for i in range(3):
        cmds.setKeyframe(nodes, attribute="tx", value=value+(i*25), time=time+(i*33))

main()
