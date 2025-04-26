from algo_problem import AlgoProblem
from config import Config
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover, CXCrossover, SPXCrossover, PMXCrossover, SBXCrossover
from jmetal.operator.mutation import CompositeMutation, IntegerPolynomialMutation, PermutationSwapMutation, BitFlipMutation, PolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from genetic_algorithm import GeneticAlgorithm
from jmetal.operator.selection import RouletteWheelSelection
import pandas as pd
import os
from jmetal.util.solution import get_non_dominated_solutions, read_solutions, print_function_values_to_file, \
    print_variables_to_file
import matplotlib.pyplot as plt


class Solver(object):
    def __init__(self):
        self.problem = AlgoProblem()
        self.problem.fitness.problem = self.problem
        # self.problem.build()

    @staticmethod
    def cal_transfer_time(task, p_id):
        return max(abs(task.bay - p_id), abs(task.column - task.end_column))

    @staticmethod
    def cal_transfer_time1(pos1, pos2):
        return max(abs(pos1[0] - pos2[1]), abs(pos1[1] - pos2[1]))

    def heuristic_solve(self):
        crossover_list = []
        mutation_list = []
        crossover_list.append(IntegerSBXCrossover(Config.crossover_probability, distribution_index=20))
        crossover_list.append(IntegerSBXCrossover(Config.crossover_probability, distribution_index=20))
        crossover_list.append(IntegerSBXCrossover(Config.crossover_probability, distribution_index=20))
        crossover_list.append(SBXCrossover(probability=Config.crossover_probability, distribution_index=20))

        mutation_list.append(IntegerPolynomialMutation(Config.mutation_probability))
        mutation_list.append(IntegerPolynomialMutation(Config.mutation_probability))
        mutation_list.append(IntegerPolynomialMutation(Config.mutation_probability))
        mutation_list.append(PolynomialMutation(probability=Config.mutation_probability, distribution_index=20))
        front = []
        algorithm = GeneticAlgorithm(
            problem=self.problem,
            population_size=Config.population_size,
            offspring_population_size=Config.offspring_population_size,
            mutation=CompositeMutation(mutation_list),
            crossover=CompositeCrossover(crossover_list),
            termination_criterion=StoppingByEvaluations(max_evaluations=Config.max_evaluations),
            selection=RouletteWheelSelection()
        )

        algorithm.run()
        front += [algorithm.get_result()]
        print("The Optimal Value：", algorithm.get_result().objectives[0])
        print_function_values_to_file(front, 'FUN.' + "'NSGAII")
        self.out_put_solution(front)

    def out_put_solution(self, front):
        writer = pd.ExcelWriter(os.path.join(Config.data_folder_path, "output.xlsx"))
        index = 0
        self.problem.fitness.evaluate_fitness(front[0])
        df = []
        df = []
        columns = ["course_id", "course_type", "classroom", "select_weeks", "select_day", "start_time", "end_time"]
        for course_obj in self.problem.course_list:
            df.append([course_obj.course_id, course_obj.type, course_obj.classroom, course_obj.select_weeks, course_obj.select_day, course_obj.start_time, course_obj.end_time])
        df = pd.DataFrame(df, columns=columns)
        df.to_excel(writer, index=False, sheet_name=str(index))
        writer._save()




