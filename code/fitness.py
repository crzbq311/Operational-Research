import math
# from algo_problem import AlgoProblem
from jmetal.core.solution import Solution
from config import Config
import numpy as np
import itertools


class Fitness(object):
    def __init__(self):
        self.problem = None
        self.objs = []
        # key: sem, week, day, classroom, value: course_list
        self.day_dict = {}

    def reset(self):
        for index, task in self.problem.course_dict.items():
            task.reset()
        self.day_dict = {}

    def assign_courses(self, courses):
        courses = sorted(courses)
        start_time = Config.start_time
        for index, course in enumerate(courses):
            course.start_time = start_time
            course.end_time = start_time + course.unit_duration
            start_time = course.end_time
            if math.ceil(start_time) != math.floor(start_time):
                start_time += 0.5

    def evaluate_fitness(self, solution: Solution):
        # Decoding
        self.reset()
        solutions = solution.variables
        make_span = 0
        fuel_consumption = 0
        # Decide which semester to study
        # Starting Week
        # Scheduled Day
        # Course Order for each scheduled day
        # for course in self.problem.course_list:
        #     print(course.sort_index)
        self.problem.course_list = sorted(self.problem.course_list)
        for index, value in enumerate(solutions[0].variables):
            course_obj = self.problem.course_list[index]
            if value >= len(course_obj.semesters):
                value = 0
            course_obj.select_semester = course_obj.semesters[value]
            for same_course_obj in course_obj.same_courses:
                # if same_course_obj.select_semester is None:
                same_course_obj.select_semester = course_obj.select_semester
            for neighbor_course in course_obj.neighbor_courses:
                # if neighbor_course.select_semester is None:
                neighbor_course.select_semester = course_obj.select_semester
            start_week_index = solutions[1].variables[index]
            if value == 0:
                # Represent the first semester
                start_week = Config.sem_1_weeks[start_week_index]
            else:
                start_week = Config.sem_2_weeks[start_week_index]
            course_obj.start_week = start_week
            course_obj.select_day = solutions[2].variables[index]
            course_obj.value = solutions[3].variables[index]

        for course_obj in self.problem.course_list:
            if not course_obj.update_info():
                solution.objectives[0] = 10000000
                return
            for week in course_obj.select_weeks:
                if(course_obj.select_semester, week, course_obj.select_day, course_obj.classroom) not in self.day_dict:
                    self.day_dict[course_obj.select_semester, week, course_obj.select_day, course_obj.classroom] = []
                self.day_dict[course_obj.select_semester, week, course_obj.select_day, course_obj.classroom].append(course_obj)
                self.day_dict[course_obj.select_semester, week, course_obj.select_day, course_obj.classroom] = sorted(self.day_dict[course_obj.select_semester, week, course_obj.select_day, course_obj.classroom])
        # print("yes")
        penalty = 0
        find = True
        infeasible_courses = []
        infeasible_courses_dict = {}
        day_left = {}
        full_load_day = set()
        for key, courses in self.day_dict.items():
            start_time = Config.start_time
            end_time = Config.end_time
            week = key[1]
            if key not in day_left and key not in full_load_day:
                day_left[key] = end_time - start_time
            if week == Config.forbid_week:
                end_time = Config.forbid_start_time
            for index, course in enumerate(courses):
                if start_time + course.unit_duration > end_time:
                    infeasible_courses.append(course)
                    infeasible_courses_dict[course] = key
                    penalty += (start_time + course.unit_duration - end_time)
                    find = False
                    continue
                course.start_time = start_time
                course.end_time = start_time + course.unit_duration
                day_left[key] -= course.unit_duration
                if day_left[key] == 0:
                    day_left.pop(key)
                    full_load_day.add(key)
                start_time = course.end_time
                if math.ceil(start_time) != math.floor(start_time):
                    start_time += 0.5
        if not find:
            # print(penalty)
            feasible_courses = []
            for course in infeasible_courses:
                sem_weeks = Config.sem_1_weeks
                if course.select_semester != "sem1":
                    sem_weeks = Config.sem_2_weeks
                find1 = False
                for week in sem_weeks:
                    if week in course.forbid_weeks:
                        continue
                    for day in range(1, 6):
                        if (course.select_semester, week, day, course.classroom) in day_left and day_left[course.select_semester, week, day, course.classroom] - course.unit_duration >= 0:
                            if (course.select_semester, week, day, course.classroom) not in self.day_dict:
                                self.day_dict[course.select_semester, week, day, course.classroom] = []
                            self.day_dict[course.select_semester, week, day, course.classroom].append(course)
                            self.assign_courses(self.day_dict[course.select_semester, week, day, course.classroom])
                            day_left[course.select_semester, week, day, course.classroom] -= course.unit_duration
                            if day_left[course.select_semester, week, day, course.classroom] == 0:
                                day_left.pop((course.select_semester, week, day, course.classroom))
                            feasible_courses.append(course)
                            find1 = True
                            break
                    if find1:
                        break
                    else:
                        a = 1
                if not find1:
                    pass
            # print(len(infeasible_courses) - len(feasible_courses))
            if len(infeasible_courses) - len(feasible_courses) > 0:
                solution.objectives[0] = (len(infeasible_courses) - len(feasible_courses)) * 1000
        obj = 0.001
        for s, lecture_courses in self.problem.student_lectures_dict.items():
            temp_dict = {}
            for real_course_id in lecture_courses:
                if real_course_id not in self.problem.real_course_dict:
                    continue
                for course_obj in self.problem.real_course_dict[real_course_id]:
                    for week in course_obj.select_weeks:
                        if (course_obj.select_semester, week, course_obj.select_day) not in temp_dict:
                            temp_dict[course_obj.select_semester, week, course_obj.select_day] = []
                        temp_dict[course_obj.select_semester, week, course_obj.select_day].append(course_obj)
            for key, courses in temp_dict.items():
                if len(courses) < 2:
                    continue
                for course_pair in itertools.combinations(courses, 2):
                    left = course_pair[0]
                    right = course_pair[1]
                    if left.start_time > right.start_time and left.start_time < right.end_time:
                        obj += Config.penalty
                    if right.start_time > left.start_time and right.start_time < left.end_time:
                        obj += Config.penalty
        # print(obj)
        solution.objectives[0] = obj

