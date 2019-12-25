class D2D_link:
    def __init__(self):
        self.link_list = dict()

    def set_link(self, tx, rx):
        self.link_list[len(self.link_list)] = [tx, rx]

    def find_link(self, ue_key):
        for key, value in self.link_list.items():
            if ue_key in value:
                return key
        return -1

    def get_link_list(self):
        return self.link_list
