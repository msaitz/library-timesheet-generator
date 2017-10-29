from .symbol import Symbol

class Shift:

    min_staff = 7
    min_staff_site = 5
    time_slots = ['9', '10', '10.20', '10.40', '11', '12', '1', '2',
                    '3', '3.20', '3.40', '4', '5', '5.30', '6', '7']
    slot_value = [4, 1, 1, 1, 4, 4, 4, 4, 
                    1, 1, 1, 4, 2, 2, 4, 4]
    breaks = {'morning': [1, 2, 3], 'afternoon': [8, 9, 10], 
                'late': [12, 13],
                'lunch': [5, 6]}
    break_list = ['lunch', 'late', 'morning', 'afternoon']
    dalston_shifts = [Symbol.adu, Symbol.qp, Symbol.juv]
    

    @classmethod
    def print_time_slots(cls):
        print(end='  ')
        for idx in range(len(cls.time_slots)):
                print(idx + 1, end=' ')
        print()
