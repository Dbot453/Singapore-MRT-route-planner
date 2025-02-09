from website import create_app

class Gui:
    """
    Class to run the program using GUI
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the Gui object.
        """
        app = create_app()
        app.run(debug=False)
        
if __name__ == "__main__":
    ui = Gui()