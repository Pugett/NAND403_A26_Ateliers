import maya.cmds as cmds
import random

def generate_random_animation(parameters):

    cmds.undoInfo(openChunk=True, chunkName="Generate Random Animation")                            # OPENS CHUNK FOR CTRL+Z
    try:
        nodes = cmds.ls(selection=True, long=True, type="transform")                                # OBJET(S) SELECTION

        if not nodes:                                                                               # CHECK IF NO OBJET IS SELECTED
            raise ValueError("Select at least one object in Maya.")                                 #

        duration = parameters["duration"]                                                           # GET DURATION & STEP FROM UI
        step = parameters["step"]                                                                   #

        if duration <= 0 or step <= 0:                                                              # CHECK IF DURATION OR STEP IS EQUAL OR UNDER 0
            raise ValueError("Duration and step must be greater than zero.")                        #

        frames = list(range(0, duration + 1, step))                                                 # CREATE FRAME LIST
        if frames[-1] != duration:                                                                  # MAKE SURE THE LAST FRAME IS INCLUDED (100 IF DURATION = 100)
            frames.append(duration)                                                                 #

        animation_types = {                                                                         # DEFINE ANIMATION ATTRIBUTES IN DICTIONNARY (KEYS & VALUES)
            "translate": ["translateX", "translateY", "translateZ"],                                # (LIKE JSON)
            "rotate": ["rotateX", "rotateY", "rotateZ"],
            "scale": ["scaleX", "scaleY", "scaleZ"]
        }

        current_frame = cmds.currentTime(query=True)                                                # SAVE CURRENT MAYA FRAME

        for node in nodes:                                                                          # GENERATE ANIMATION FOR EACH OBJECT SELECTED
            for attributes in animation_types.values():                                             # CLEAR EXISTING KEYS ON OUR ATTRIBUTES
                cmds.cutKey(node, attribute=attributes, clear=True)                                 #

            start_values = {}                                                                       # STORES START VALUES OF ATTRIBUTES
            for frame in frames:                                                                    # GENERATE KEYFRAMES
                for animation, axes in animation_types.items():                                     # GET KEYS & VALUES
                    for i, attribute in enumerate(axes):                                            # GET INDEX AND ATTRIBUTES
                        axis = ["x", "y", "z"][i]                                                   # CONVERTS INDEX TO AXIS NAME

                        minimum = parameters[animation][axis]["min"]                                # GET MIN AND MAX VALUES FROM UI
                        maximum = parameters[animation][axis]["max"]                                #

                        if frame == frames[0]:                                                      # FIRST FRAME : GENERATE RANDOM VALUES
                            value = random.uniform(minimum, maximum)                                #
                            start_values[attribute] = value                                         #

                        elif frame == frames[-1]:                                                   # LAST FRAME : REUSE FIRST FRAME VALUES
                            value = start_values[attribute]                                         #

                        else:                                                                       # OTHER FRAMES : GENERATE RANDOM VALUES
                            value = random.uniform(minimum, maximum)                                #

                        cmds.setKeyframe(node, attribute=attribute, value=value, time=frame)        # CREATES ANIMATION IN MAYA

    finally:
        cmds.currentTime(current_frame)                                                             # RESTORE ORIGINAL MAYA FRAME
        print(f"Animation generated for {len(nodes)} object(s)!")
        print(f"Keyframes created at: {frames}")

        cmds.undoInfo(closeChunk=True)                                                              # CLOSES CHUNCK FOR CTRL+Z
