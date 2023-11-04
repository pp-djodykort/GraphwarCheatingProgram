# ============ Imports ============
import time

# ============ Functions ============
class Functions:
    # ======== Functions ========
    # -- Window points --
    @staticmethod
    def selectLeftTop(x, y, button, pressed):
        # ======== Imports ========
        # Packages
        # Internal
        from files.py.classes import ConfigData

        # ======== Start of Code ========
        if ConfigData.axis["left_top"] is None:
            ConfigData.axis["left_top"] = x, y
            print(f"Left top: {ConfigData.axis['left_top']}")

        # Stop the listener
        ConfigData.listener_leftTop.stop()

    @staticmethod
    def selectRightBottom(x, y, button, pressed):
        # ======== Imports ========
        # Packages
        # Internal
        from files.py.classes import ConfigData

        # ======== Start of Code ========
        if ConfigData.axis["right_bottom"] is None:
            ConfigData.axis["right_bottom"] = x, y
            print(f"Right bottom: {ConfigData.axis['right_bottom']}")

        # Stop the listener
        ConfigData.listener_rightBottom.stop()

    @staticmethod
    def getWindowPoints():
        # ======== Imports ========
        # Python
        import time

        # Internal
        from files.py.classes import ConfigData

        # Packages
        from tkinter import messagebox

        # ======== Start of Code ========
        # Display a notification to tell the user to click on the top left and bottom right corners of the game axes.
        messagebox.showinfo("Select Game Axes",
                            "Press OK and left click on the top left and then the bottom right corners of the game axes. Right click to cancel.")

        # Getting the left top
        ConfigData.listener_leftTop.start()
        while ConfigData.axis["left_top"] is None:
            time.sleep(1)

        # Getting the right bottom
        ConfigData.listener_rightBottom.start()
        while ConfigData.axis["right_bottom"] is None:
            time.sleep(1)

        # Printing both
        print(ConfigData.axis)

    # -- Graphwar points --
    @staticmethod
    def selectStartPoint(x, y, button, pressed):
        # ======== Imports ========
        # Packages
        # Internal
        from files.py.classes import ConfigData

        # ======== Start of Code ========
        if ConfigData.axis["start_point"] is None:
            ConfigData.axis["start_point"] = x, y
            print(f"Start point: {ConfigData.axis['start_point']}")

        # Stop the listener
        ConfigData.listener_startPoint.stop()

    @staticmethod
    def select_point_callback(x, y, button, pressed):
        # ======== Imports ========
        # Internal
        from files.py.classes import ConfigData
        # Packages
        from pynput import mouse

        # ======== Start of Code ========

        # If the left mouse button is pressed, store the selected point
        if button == mouse.Button.left and pressed:
            ConfigData.axis['selected_point'] = (x, y)

    @staticmethod
    def select_point():
        # ======== Imports ========
        # Packages
        from pynput import mouse

        # Internal
        from files.py.classes import ConfigData

        # ======== Start of Code ========

        # Create a listener for mouse clicks
        listener = mouse.Listener(
            on_click=lambda x, y, button, pressed: Functions.select_point_callback(x, y, button, pressed))
        listener.start()

        # Wait for the user to click the mouse
        while ConfigData.axis['selected_point'] is None:
            time.sleep(0.1)

        # Stop the listener
        listener.stop()

        # Return the selected point
        return ConfigData.axis['selected_point']

    # -- Formula --
    @staticmethod
    def calculate_formula_graphwar(point_list):
        sorted_points = sorted(point_list, key=lambda x: x[0])
        start = point_list[0]
        x1, y1 = start[0], 0
        result = ""

        def normalize(x):
            return str(x) if "-" in str(x) else "+" + str(x)

        for point in point_list[1:]:
            x2, y2 = point[0], point[1] - start[1]
            if x2 == x1:  # jump discontinuity, skip to get a jump
                raise Exception("bad thing happen")
            else:
                slope = (y2 - y1) / (x2 - x1)
                result += "+(1/(1+exp(-1000*(x{0})))-1/(1+exp(-1000*(x{1}))))*({2}*x{3})".format(normalize(round(-x1)),
                                                                                                 normalize(round(-x2)),
                                                                                                 str(round(-slope, 3)),
                                                                                                 normalize(round(
                                                                                                     -(y1 - slope * x1),
                                                                                                     3)))  # add a line segment with correct slope
            x1, y1 = x2, y2
        result = result[1:] + "+0.1*sin(60*x)"  # remove the leading plus sign
        return result

    # -- GraphWar --
    @staticmethod
    def gettingGraphwarPoints():
        # ======== Imports ========
        # Python
        import time

        # Internal
        from files.py.classes import ConfigData

        # Packages
        from tkinter import messagebox
        import keyboard

        # ======== Start of Code ========
        # Message box
        messagebox.showinfo("Game Start",
                            "Press OK and left click path points when your turn starts, starting with the player. Right click to complete point entry and copy result to clipboard. If no points selected, program exits.")

        # Get start point
        ConfigData.listener_startPoint.start()
        while ConfigData.axis["start_point"] is None:
            time.sleep(1)

        # Setting the points
        points = [(ConfigData.axis["start_point"][0] / ConfigData.scale_w - ConfigData.game_w / 2,
                   ConfigData.axis["start_point"][1] / ConfigData.scale_h - ConfigData.game_h / 2)]
        current_x = ConfigData.axis["start_point"][0]

        # Get the enemy path points
        while not keyboard.is_pressed("esc"):
            # ==== Declaring Variables ====
            # Points
            next_point = Functions.select_point()
            while next_point[0] is None:
                time.sleep(1)

            # ==== Start of Code ====
            # Normalize the point
            next_point = (
                next_point[0] - ConfigData.axis["left_top"][0], next_point[1] - ConfigData.axis["left_top"][1])

            if next_point[0] <= current_x:  # left or same as current one, which means jump down
                points.append((current_x / ConfigData.scale_w - ConfigData.game_w / 2,
                               next_point[1] / ConfigData.scale_h - ConfigData.game_h / 2))
            else:  # normal line segment
                points.append((next_point[0] / ConfigData.scale_w - ConfigData.game_w / 2,
                               next_point[1] / ConfigData.scale_h - ConfigData.game_h / 2))
                current_x = next_point[0]

            # Empty the selected point
            ConfigData.axis['selected_point'] = None
            # Update counter
            ConfigData.enemyCounter += 1
            print(f"Enemy point {ConfigData.enemyCounter}: {next_point}")

        return points

    # -- Start --
    @staticmethod
    def startGraphWarCheats():
        # ======== Imports ========
        # Internal
        from files.py.classes import ConfigData

        # Packages

        # ======== Declaring Variables ========
        # Window points
        Functions.getWindowPoints()

        # Scales
        ConfigData.scale_w, ConfigData.scale_h = (ConfigData.axis['right_bottom'][0] - ConfigData.axis['left_top'][
            0]) / ConfigData.game_w, (
                                                         ConfigData.axis['right_bottom'][1] -
                                                         ConfigData.axis['left_top'][0]) / ConfigData.game_h

        # Start & Enemy points
        points = Functions.gettingGraphwarPoints()
        print(points)

        # ======== Start of Code ========
        # Starting the program
        output = Functions.calculate_formula_graphwar(points)
        print(output)
