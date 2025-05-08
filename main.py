from data.database import Database
from views.login import LoginView

def startup():
    # Initialize the database
    Database.initialize()
    print("Database initialized successfully.")

    # Call the index function
    loginView = LoginView()
    loginView.run()

if __name__ == "__main__":
    startup()