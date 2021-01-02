class PumpDescription:
    Name = ""
    State = False
    OnIntervals = None
    Pin = 0

    def __init__(self, name, state, pin, onIntervals):
        self.Name = name
        self.State = state
        self.Pin = pin
        self.OnIntervals = onIntervals