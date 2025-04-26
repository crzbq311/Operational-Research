import pandas as pd
from config import Config
from copy import deepcopy
from jmetal.core.problem import Problem, S
from jmetal.core.solution import CompositeSolution, FloatSolution, IntegerSolution, PermutationSolution
from fitness import Fitness
import random
from course import Course
random.seed(0)

class AlgoProblem(Problem):
    def number_of_variables(self) -> int:
        pass

    def number_of_objectives(self) -> int:
        pass

    def number_of_constraints(self) -> int:
        pass

    def name(self) -> str:
        pass

    def __init__(self):
        super().__init__()
        # course_id + type
        self.course_id_list = []
        self.course_list = []
        self.student_lectures_dict = {}
        self.course_dict = {}
        self.real_course_dict = {}
        self.classroom_id_list = []
        self.classroom_dict = {}
        self.number_of_objectives = 1
        self.number_of_constraints = 1
        self.number_of_variables = None

        self.other_lecture_dict = {}

        self.build()
        self.fitness = Fitness()
        self.obj_directions = [self.MINIMIZE]

    def get_name(self) -> str:
        pass

    def evaluate(self, solution: S):
        self.fitness.evaluate_fitness(solution)

    def create_solution(self) -> CompositeSolution:
        solution_list = []
        # Decide which semester to study
        # Starting Week
        # Scheduled Day
        # Course Order for each scheduled day
        sem_int_solution = IntegerSolution([0 for _ in range(len(self.course_id_list))],
                                           [1 for _ in self.course_id_list],
                                           self.number_of_objectives,
                                           self.number_of_constraints)
        sem_int_solution.variables = [int(random.uniform(0.0, 2.0)) for _ in self.course_id_list]

        start_week_solution = IntegerSolution([0 for _ in range(len(self.course_id_list))],
                                              [len(Config.sem_1_weeks) - 1 for _ in self.course_id_list],
                                              self.number_of_objectives,
                                              self.number_of_constraints)
        start_week_solution.variables = [int(random.uniform(0.0, len(Config.sem_1_weeks) * 1.0 - 1)) for _ in
                                         self.course_id_list]

        day_select_solution = IntegerSolution([1 for _ in range(len(self.course_id_list))],
                                              [5 for _ in self.course_id_list],
                                              self.number_of_objectives,
                                              self.number_of_constraints)
        day_select_solution.variables = [int(random.uniform(1.0, 6.0)) for _ in self.course_id_list]

        float_solution = FloatSolution([0.0] * len(self.course_id_list),
                                       [1.0] * len(self.course_id_list),
                                       self.number_of_objectives,
                                       self.number_of_constraints)
        float_solution.variables = [random.uniform(0.0, 1.0) for _ in range(len(self.course_id_list))]
        solution_list = [sem_int_solution, start_week_solution, day_select_solution, float_solution]
        return CompositeSolution(solution_list)

    def build(self):
        df = pd.read_excel(Config.data_file_path, sheet_name=None)
        course_set = set()
        for index, row in df["Timetable Data"].iterrows():
            key = row["Course Code"] + row["Activity Type"] + row["Delivery Semester"] + row["Allocated Location"] + "_" + row["Scheduled Days"] + row["Scheduled Start Time"]
            if key in course_set:
                continue
            course_set.add(key)
            course_obj = Course(row, index)
            self.course_list.append(course_obj)
            self.course_id_list.append(course_obj.id)
            self.course_dict[course_obj.id] = course_obj
            if course_obj.course_id not in self.real_course_dict:
                self.real_course_dict[course_obj.course_id] = []
            if course_obj.type == "lecture":
                self.real_course_dict[course_obj.course_id].append(course_obj)

        for index, row in df["Enrollment Data"].iterrows():
            if row["UNN"] not in self.student_lectures_dict:
                self.student_lectures_dict[row["UNN"]] = set()
            self.student_lectures_dict[row["UNN"]].add(row["Course Code"])

        for course_id, courses in self.real_course_dict.items():
            for index, course1 in enumerate(courses):
                for index2, course2 in enumerate(courses):
                    if course1.id == course2.id:
                        continue
                    if course1.type == "Lecture":
                        if course2.type == "Lecture":
                            course1.same_courses.append(course2)
                        else:
                            course1.neighbor_courses.append(course2)
                    else:
                        if course2.type == "Lecture":
                            course1.neighbor_courses.append(course2)
                        else:
                            course1.same_courses.append(course2)


