class ClassRoom(object):
    def __init__(self):
        self.id = None
        # key: [semester, week, day], value: courses
        self.course_dict = {}

