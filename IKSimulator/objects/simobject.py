class SimObject:
    """
    Template class to handle rendering and collisions
    """
    def __init__(self):
        pass

    """
    Called each mainloop pass. Overwritten to contain logic.
    """
    def tick(self):
        pass

    """
    Called each rendering pass. Overwritten to contain drawing information.
    """
    def draw(self, surface):
        pass