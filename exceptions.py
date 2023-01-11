class startOver(Exception):
    # This exception is raised when the user wants to start over
    pass


class playerFold(Exception):
    # This exception is raised when the player folds
    pass


class comFold(Exception):
    # This exception is raised when the computer folds
    pass


class endTurn(Exception):
    # This exception is raised when the player wants to end their turn
    pass