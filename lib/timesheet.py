import random
from .symbol import Symbol
from .staff import Staff
from .shift import Shift

class TimeSheet:
    def __init__(self, cached_data):
        self.staff_num = cached_data['staff_number']
        self.col = len(Shift.time_slots)
        self.table = [[Symbol.blank] * self.col for _ in range(self.staff_num)]
        self.staff_list = self._import_staff_data(cached_data)
        self.staff_names = self._get_name_list()

        self.add_shifts(len(Shift.time_slots))
        
        for break_time in Shift.break_list:
            self.break_manager(break_time)
        
        shifts = Shift.dalston_shifts
        random.shuffle(shifts)

        for job in shifts:
            self.job_manager(job)


    def print_table(self):
        for idx in range(len(self.table)):
            print(self.staff_list[idx].initial, end=' ')
            for column in range(0, len(self.table[idx])):
                if column < 8:
                    print(self.table[idx][column], end=' ')
                else:
                    print(self.table[idx][column], end='  ')
            print()


    def add_shifts(self, shift_len):
        for idx, staff in enumerate(self.staff_list):
            if staff.start > 0:
                for shift in range(0, staff.start):
                    self.table[idx][shift] = Symbol.off_duty
            if staff.finish < shift_len:
                for shift in range(staff.finish, shift_len):
                    self.table[idx][shift] = Symbol.off_duty


    def _import_staff_data(self, data):
        staff_list = list()
        for i, key in enumerate(data['name']):
            staff_list.append(
                Staff(data['name'][i], data['job'][i],
                int(data['start'][i]), int(data['finish'][i])))
       
        #print('start... ', staff_list[0].start)
        #print('finish... ', staff_list[0].finish)
        return staff_list


    def break_manager(self, break_time):
        if break_time == 'morning' or break_time == 'afternoon':
            self._add_complex_break(break_time)
        elif break_time == 'lunch':
            self._add_simple_breaks(break_time)
            
            while True:
                if self._check_breaks('lunch') < 0:
                    break
                self._move_breaks(6)
        
        else:
            self._add_simple_breaks(break_time)
        
 
    def job_manager(self, job):
        weights = self._get_weight_list()
        for i, time_slot in enumerate(range(len(self.table[0]))):
            section = self._get_staff_section(0, weights=weights)
            
            if section:
                random_num = random.randint(0, len(section) - 1)
            else:
                continue
            

            # assign staff for first slot
            if i == 0:
                current_staff = section[random_num]
                self.table[current_staff][i] = job
            # use previous staff
            elif (self._decide_job_assignation(i, current_staff,
                    job) == 1  and 
                    self.table[current_staff][time_slot] == Symbol.blank):
                self.table[current_staff][time_slot] = job
            # select a random staff
            else:
                section = self._get_staff_section(time_slot, weights=weights)
                
                if section:
                    random_num = random.randint(0, len(section) - 1)
                    current_staff = section[random_num]
                    self.table[section[random_num]][time_slot] = job
                else:
                    continue
                
            weights[current_staff] += 1

    
    # returns 1 if previous last staff slot can be used, returns 0 if otherwise
    def _decide_job_assignation(self, time_slot, current_staff, job):
        sum_slot_value = 0 
        
        # avoid supervisors getting assigned extra timeslots
        if self.staff_list[current_staff].weight > 2:
            return 0

        # skip first time slot
        if time_slot == 0:
            return 0 
        
        i = time_slot - 1
        while self.table[current_staff][i] == job:
            sum_slot_value += Shift.slot_value[i]
            i -= 1

        sum_slot_value += Shift.slot_value[time_slot]
        
        if sum_slot_value < 7:
            return 1
        else:
            return 0
  
    
    # Adds triple time slot tea breaks to timetable
    def _add_complex_break(self, break_time):
        first = Shift.breaks[break_time][0]
        second = Shift.breaks[break_time][1]
        third = Shift.breaks[break_time][2]
        
        slots_early = [first, second]
        slots_late = [second, third]
        
        changer1 = 0
        changer = 1
        
        for i, staff in enumerate(self.staff_list):
            if break_time == 'morning' and self.staff_list[i].start > 4:
                continue
            if break_time == 'afternoon' and self.staff_list[i].start > 10:
                continue
            
            if self.staff_list[i].finish < 15:
                self.table[i][slots_early[changer1 % 2]] = Symbol.tea
                changer1 = changer1 + 1
            else:
                self.table[i][slots_late[changer % 2]] = Symbol.tea
                changer = changer + 1


    # Adds a simple tea break for each member of the staff
    def _add_simple_breaks(self, break_time):
        first = Shift.breaks[break_time][0]
        second = Shift.breaks[break_time][1]
        slots = [first, second]
        sym = Symbol.tea
        
        if break_time == 'lunch':
            sym = Symbol.lunch

            for i, staff in enumerate(self.staff_list):
                if self.staff_list[i].start > 4:
                    continue
                
                if self.staff_list[i].finish > 15:
                    self.table[i][slots[1]] = sym
                else:
                    self.table[i][slots[0]] = sym 
       
       # break time as late
        else:
            changer = 0
            for i, staff in enumerate(self.staff_list):
                if self.staff_list[i].start > 12:
                    continue

                if self.staff_list[i].finish > 15:
                    self.table[i][slots[changer % 2]] = sym
                    changer += 1


    # returns the number of staff doing x job for a time slot
    def _get_active_staff(self, time_slot, job):
        count = 0
        for staff_index in range(self.staff_num): 
            current_staff = self.table[staff_index][time_slot]
        
            if current_staff == job:
                count = count + 1
            
        return count


    # returns -1 if breaks are balanced, returns the breakslot
    def _check_breaks(self, break_time):
        first = Shift.breaks[break_time][0]
        second = Shift.breaks[break_time][1]
        
        first_num = self._get_active_staff(first, Symbol.blank)
        second_num = self._get_active_staff(second, Symbol.blank)
        
        if abs(first_num - second_num) > 2 and first_num > second_num:
            return second
        elif abs(first_num - second_num) > 2 and second_num > first_num:
            return first
        else:
            return -1


    # swaps break time (lunch) for a random member of the staff
    def _move_breaks(self, excess):
        if excess == 6:
            move_to = 5
        else:
            move_to = 6
        section = self._get_staff_section(excess, Symbol.lunch)
        
        if len(section) < 1:
            return -1

        random_num = random.randint(0, len(section) - 1)
        random_staff = section[random_num]
        self.table[random_staff][excess] = Symbol.blank
        self.table[random_staff][move_to] = Symbol.lunch
        
    
    # returns a list with the indexes of available staff members
    def _get_staff_section(self, time_slot, job=None, weights=None):
        # used for break management 
        if weights == None and job != None:
            section = [i for i, pos in enumerate(range(self.staff_num)) 
                    if self.table[i][time_slot] == job]
            return section
        
        # used for job adding functions
        else:
            minimum = self.get_min_number(weights)
            min_section = None
            failed_counter = 0
            
            while True:
                min_section = [i for i, staff in enumerate(range(self.staff_num))
                            if weights[i] == minimum and 
                            self.table[i][time_slot] == Symbol.blank]
                
                if min_section or failed_counter > 4:
                    break
                else:
                    failed_counter += 1 
                    minimum += 1
                    
            if not min_section:
                return None
            else:
                return min_section
    
    
    # returns the lowest number from the list
    def get_min_number(self, weights):
        minimum = weights[0]
        for number in weights:
            if number < minimum:
                minimum = number
        return minimum

    
    # returns the list of staff weight extracted from staff_list
    def _get_weight_list(self):
        weights = [obj.weight for obj in self.staff_list]
        return weights

    #TODO with the new variable some operations can be simplified
    def _get_name_list(self):
        names = [obj.name for obj in self.staff_list]
        return names

