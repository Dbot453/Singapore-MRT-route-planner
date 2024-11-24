from website import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)

class Gui:
    def __init__(self):
        app = create_app()
        app.run(debug=True)
        