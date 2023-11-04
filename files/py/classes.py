# ============ Imports ============

# ============ Data Classes ============
class ConfigData:
    # ======== Imports ========
    # Internal
    from files.py.functions import Functions

    # Packages
    from pynput.mouse import Listener

    # ======== Declaring Variables ========
    # Ints
    enemyCounter = 0
    game_w, game_h = 50, 30  # total width and height of the game board in game coordinates
    scale_w, scale_h = None, None  # scale of the game board in pixels

    # Axis
    axis = {
        "left_top": None,
        "right_bottom": None,
        "start_point": None,
        "selected_point": None
    }

    # Listeners
    listener_leftTop = Listener(on_click=Functions.selectLeftTop)
    listener_rightBottom = Listener(on_click=Functions.selectRightBottom)
    listener_startPoint = Listener(on_click=Functions.selectStartPoint)

    # Points
    points = []