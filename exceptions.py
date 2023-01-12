import logging


class startOver(Exception):
    # This exception is raised when the user wants to start over
    logging.info("startOver exception raised")
    pass


class playerFold(Exception):
    # This exception is raised when the player folds
    logging.info("playerFold exception raised")
    pass


class comFold(Exception):
    # This exception is raised when the computer folds
    logging.info("comFold exception raised")
    pass


class endTurn(Exception):
    # This exception is raised when the player wants to end their turn
    logging.info("endTurn exception raised")
    pass