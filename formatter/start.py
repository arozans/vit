from formatter import DateTime

class Start(DateTime):
    def get_active_state(self, start, task):
        return self.defaults.get_active_state(start, task)

    def colorize(self, start, task):
        return self.colorizer.active(self.get_active_state(start, task))
