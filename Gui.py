from website import create_app

class Gui:
    def __init__(self):
        app = create_app()
        app.run(debug=True)
        
Gui()

