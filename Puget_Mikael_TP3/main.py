import importlib                                                    # IMPORTS
import Puget_Mikael_TP3.ui as ui                                    #
import Puget_Mikael_TP3.animator as animator                        #

def main():
    importlib.reload(ui)
    importlib.reload(animator)
    ui.show_random_anim()                                           # FUNCTON FOR UI

main()