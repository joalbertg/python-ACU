class EventPg:
    def __init__(self, pg):
        self.pg = pg

    def get_event(self):
        return self.pg.event.get()

    def event_keydown(self, type):
        if type == self.pg.KEYDOWN:
            return True
        return False

    def event_close(self, ev):
        # Detectamos si se presiona esc o hacen click sobre close.
        for event in ev:
            type = event.type
            if (self.event_keydown(type) and event.key == self.pg.K_ESCAPE) or type == self.pg.QUIT:
                return True
        return False
                # self.pg.quit()
                # exit() 

