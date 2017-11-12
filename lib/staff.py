
class Staff:
    def __init__(self, name, job, start=0, finish=16):
        self.name = name
        #self.initial = self.name[0]
        #self.initial = 'A'
        self.job = job
        self.start = start
        self.finish = finish
        self.switcher = {
            'DLM': 9,
            'SUP': 4,
            'LA': 2,
            'RA': 0,
        }
        self.weight = self.switcher.get(job)
