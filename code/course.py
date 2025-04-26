from config import Config


class Course(object):
    def __init__(self, row, index):
        self.id = row["Course Code"] + row["Activity Type"] + row["Delivery Semester"] + row["Allocated Location"] + "_" + str(index)
        self.course_id = row["Course Code"]
        self.unit_duration = row["Duration"]
        self.classroom = row["Allocated Location"]
        self.weeks_num = row["Number of Teaching Week"]
        self.odd_even = row["Even/Odd Weeks"]
        if row["Delivery Semester"] == "sem2":
            self.semesters = ["sem2"]
        elif row["Delivery Semester"] == "sem1":
            self.semesters = ["sem1"]
        else:
            self.semesters = ["sem1", "sem2"]
        if row["Non-teaching Weeks"] > 0:
            self.forbid_weeks = [row["Non-teaching Weeks"]]
        else:
            self.forbid_weeks = []
        self.neighbor_courses = []
        # Classes that are also lectures
        self.same_courses = []
        self.type = row["Activity Type"]
        if self.type == "Lecture":
            self.prior = 1
        else:
            self.prior = 2
        self.sort_index = 1

        self.select_semester = None
        self.start_week = None
        self.end_week = None
        self.select_weeks = []
        self.select_day = None
        self.start_time = None
        self.end_time = None
        self.value = None

    def update_info(self):
        self.sort_index = 2
        min_start_week = 0
        max_start_week = 0
        sem_weeks = Config.sem_1_weeks
        if self.select_semester != "sem1":
            sem_weeks = Config.sem_2_weeks
        if self.type != "Lecture":
            for course_obj in self.neighbor_courses:
                self.start_week = min(course_obj.start_week, self.start_week)
                self.select_day = max(course_obj.select_day + 1, self.select_day)
                if self.select_day > 5:
                    return False
                min_start_week = max(min_start_week, self.start_week)
        else:
            self.select_day = min(4, self.select_day)
        if self.odd_even == "any":
            cur_week_num = 0
            for week in sem_weeks[::-1]:
                if week in self.forbid_weeks:
                    continue
                cur_week_num += 1
                if cur_week_num == self.weeks_num:
                    max_start_week = week
                    break
            # max_start_week = sem_weeks[len(sem_weeks) - self.weeks_num]
        elif self.odd_even == "odd":
            cur_week_num = 0
            for week in sem_weeks[::-1]:
                if week in self.forbid_weeks:
                    continue
                if week % 2 != 0:
                    cur_week_num += 1
                if cur_week_num == self.weeks_num:
                    max_start_week = week
                    break
        else:
            cur_week_num = 0
            for week in sem_weeks[::-1]:
                if week in self.forbid_weeks:
                    continue
                if week % 2 == 0:
                    cur_week_num += 1
                if cur_week_num == self.weeks_num:
                    max_start_week = week
                    break
        # if max_start_week < min_start_week:
        #     print("update info error")
        #     self.update_info()
        #     return False
        if self.start_week > max_start_week:
            self.start_week = max_start_week
        cur_week_num = 0
        if self.start_week not in sem_weeks:
            self.start_week += 1
        for week in sem_weeks[sem_weeks.index(self.start_week):]:
            if week in self.forbid_weeks:
                continue
            if self.odd_even == "any":
                self.select_weeks.append(week)
                cur_week_num += 1
            elif self.odd_even == "odd" and week % 2 != 0:
                self.select_weeks.append(week)
                cur_week_num += 1
            elif self.odd_even == "even" and week % 2 == 0:
                self.select_weeks.append(week)
                cur_week_num += 1
            if cur_week_num == self.weeks_num:
                break
        self.end_week = self.select_weeks[-1]
        return True

    def reset(self):
        self.select_semester = None
        self.start_week = None
        self.end_week = None
        self.select_day = None
        self.start_time = None
        self.end_time = None
        self.value = None
        self.sort_index = 1
        self.select_weeks = []

    def __lt__(self, other):
        if self.sort_index == 1:
            return self.prior <= other.prior
        else:
            return self.value <= other.value
