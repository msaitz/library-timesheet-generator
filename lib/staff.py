
class Staff:
    switcher = {
            'DLM': 9,
            'SUP': 4,
            'LA': 2,
            'RA': 0,
        }

    def __init__(self, name, job, start=0, finish=16):
        self.name = name
        self.job = job
        self.start = start
        self.finish = finish
        self.weight = Staff.switcher.get(job)
