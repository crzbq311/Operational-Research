# Extract all courses from the overlapping lectures analysis
overlapping_courses = pd.concat([pd.DataFrame(group['Courses']) for group in overlap_details])
unique_overlapping_courses = overlapping_courses['Course Code'].unique()

# Now, let's check each student's enrollments against this list of overlapping courses
# First, filter the enrollment data to include only those enrollments that are in the overlapping courses list
filtered_enrollments = enrollment_data[enrollment_data['Course Code'].isin(unique_overlapping_courses)]

# Group by student to see their enrolled courses
students_enrolled_in_overlapping_courses = filtered_enrollments.groupby('UNN')['Course Code'].apply(list)

# We'll now check for each student if they are enrolled in courses that actually overlap based on the detailed groups previously established
students_with_conflicts = {}

for unn, courses in students_enrolled_in_overlapping_courses.iteritems():
    enrolled_in_groups = []
    for detail in overlap_details:
        group_courses = [course['Course Code'] for course in detail['Courses']]
        # If a student is enrolled in more than one course from a group, it's a conflict
        intersection = list(set(group_courses) & set(courses))
        if len(intersection) > 1:
            enrolled_in_groups.append({
                'Semester': detail['Semester'],
                'Day': detail['Day'],
                'Start Time': detail['Start Time'],
                'Courses': intersection
            })
    if enrolled_in_groups:
        students_with_conflicts[unn] = enrolled_in_groups

# Since the output can be extensive, let's show the count of students with conflicts and details for a few examples
len(students_with_conflicts), {k: students_with_conflicts[k] for k in list(students_with_conflicts)[:5]}