import os


class Config(object):
    """Non-teaching Weeks"""
    forbid_week = 3
    """Prohibited Class Start Time Period"""
    forbid_start_time = 12
    """Start Times of Classes Throughout the Day"""
    start_time = 9
    """End Times of Classes Throughout the Day"""
    end_time = 18
    """Set of Teaching Weeks in the First Semester"""
    sem_1_weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    """Set of Teaching Weeks in the Second Semester"""
    sem_2_weeks = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]
    """Penalty for Student Class Scheduling Conflicts"""
    penalty = 1
    """GA (Genetic Algorithm) Related Parameters"""
    population_size = 50
    offspring_population_size = 50
    mutation_probability = 0.2
    crossover_probability = 0.8
    max_evaluations = 200
    mento_caro_iter_num = 10
    """File Path"""
    root_folder_path = os.path.dirname(os.path.abspath(__file__))
    data_folder_path = os.path.join(root_folder_path, "data")
    """Workpiece File"""
    data_file_path = os.path.join(data_folder_path, "School of Mathematics.xlsx")
