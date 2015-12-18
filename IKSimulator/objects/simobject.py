class SimObject:
    """
    Template class to handle rendering and collisions
    """
    def __init__(self):
        #self.surface = None
        raise NotImplementedError

    """
    Called each mainloop pass. Overwritten to contain logic.
    """
    def tick(self):
        raise NotImplementedError

    """
    Called each rendering pass. Overwritten to contain drawing information.
    Returns local surface (to be blitted onto global space)
    """
    def draw(self):
        #return self.surface
        raise NotImplementedError