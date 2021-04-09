class Causal(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        if item >= 0: return super().__getitem__(item)
        else: return 0