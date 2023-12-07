import random
from prettytable import PrettyTable

class Teacher:
    def __init__(self, name, subjects, max_hours):
        self.name = name
        self.subjects = subjects
        self.max_hours = max_hours


class Group:
    def __init__(self, group_name, subjects_hours):
        self.group_name = group_name
        self.subjects_hours = subjects_hours


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

subjects = [
    "Math", "Physics",
    "Computer Science", "Programming",
]

teachers = [
    Teacher("John Doe", ["Math", "Physics"], 30),
    Teacher("Eva Brown", ["Computer Science", "Programming"], 30),
    Teacher("Daniel Davis", ["Math"], 18),
    Teacher("Michael White", ["Programming"], 21),
    Teacher("Liam Wilson", ["Computer Science"], 20),
    Teacher("James Robinson", ["Physics"], 19),
    Teacher("Emily Garcia", ["Math"], 25),
    Teacher("Harper Lee", ["Computer Science", "Programming"], 18),
]

groups = [
    Group("Group1", {"Math": 2, "Physics": 3, "Programming": 4, "Computer Science": 2}),
    Group("Group2", {"Computer Science": 3, "Math": 1, "Physics": 2}),
    Group("Group3", {"Computer Science": 2, "Programming": 1, "Math": 4, "Physics": 2}),
    Group("Group4", {"Computer Science": 1, "Programming": 1, "Physics": 3, "Math": 2}),
]


def generate_population(n_pop):
    population = []
    for _ in range(n_pop):
        schedule = []
        for group in groups:
            for day in days:
                for j in range(10):
                    cell = {}
                    cell["Day"] = day
                    cell["Lesson"] = str(j + 1)
                    cell["Group"] = group
                    cell["Subject"] = random.choice(subjects)
                    cell["Teacher"] = get_random_teacher(cell["Subject"])
                    schedule.append(cell)
        population.append(schedule)
    return population


def get_random_teacher(subject):
    eligible_teachers = [teacher for teacher in teachers if subject in teacher.subjects]
    if eligible_teachers:
        return random.choice(eligible_teachers)
    else:
        return None


def crossover(p1, p2, r_cross):
    c1 = p1.copy()
    c2 = p2.copy()
    if random.random() < r_cross:
        pt = random.randint(1, len(p1) - 2)
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]


def selection(pop, scores, k=3):
    selection_ix = random.randint(0, len(pop) - 1)
    for _ in range(k - 1):
        ix = random.randint(0, len(pop) - 1)
        if scores[ix] > scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


def mutation(schedule, r_mut):
    for i in range(len(schedule)):
        if random.random() < r_mut:
            schedule[i]["Subject"] = random.choice(subjects)
            schedule[i]["Teacher"] = get_random_teacher(schedule[i]["Subject"])


def genetic_algorithm(objective, n_iter, n_pop, r_cross, r_mut):
    pop = generate_population(n_pop)
    best = pop[0].copy()
    best_eval = objective(pop[0])
    for gen in range(n_iter):
        print("Gen:", gen)
        scores = [objective(c) for c in pop]
        for i in range(n_pop):
            if scores[i] > best_eval:
                best = pop[i].copy()
                best_eval = scores[i]
                print("Current best score:", best_eval)
        selected = [selection(pop, scores) for _ in range(n_pop)]
        children = []
        for i in range(0, n_pop, 2):
            p1, p2 = selected[i], selected[i + 1]
            c1, c2 = crossover(p1, p2, r_cross)
            mutation(c1, r_mut)
            mutation(c2, r_mut)
            children.extend([c1, c2])
        pop = children.copy()
    return [best, best_eval]


def accurate(x):
    def_groups = {
        "Group1": {"Math": 2, "Physics": 3, "Chemistry": 3, "English": 2, "Programming": 4, "Literature": 4,
                   "History": 1, "Computer Science": 2, "Geography": 4},
        "Group2": {"English": 3, "Literature": 3, "History": 3, "Biology": 2, "Computer Science": 3, "Math": 1,
                   "Physics": 2, "Chemistry": 3},
        "Group3": {"Computer Science": 2, "Programming": 1, "Math": 4, "Physics": 2, "Literature": 4, "Geography": 1,
                   "History": 4, "Biology": 2, "Chemistry": 4, "Music": 4},
        "Group4": {"Music": 4, "Art": 2, "History": 3, "Computer Science": 1, "Programming": 1, "Biology": 3,
                   "English": 3, "Physics": 3, "Math": 2},
    }
    def_teachers = {}
    for item in x:
        group = item["Group"]
        subject = item["Subject"]
        teacher = item["Teacher"]
        if group not in def_groups:
            def_groups[group] = {}
        def_groups[group][subject] = def_groups[group].get(subject, 0) + 1
        if teacher is not None:
            if teacher not in def_teachers:
                def_teachers[teacher] = {}
            def_teachers[teacher][subject] = def_teachers[teacher].get(subject, 0) + 1
    groups_data = dict(def_groups)
    teachers_data = dict(def_teachers)
    return (teachers_accurate(teachers_data) + groups_accurate(groups_data)) / 2


def teachers_accurate(teachers):
    score = 0
    for teacher, subjects_hours in teachers.items():
        total_hours = sum(subjects_hours.values())
        if total_hours <= teacher.max_hours:
            score += 1
    return score / len(teachers)


def groups_accurate(groups):
    total_score = 0
    for group, actual_schedule in groups.items():
        planned_schedule = groups[group].get("subjects_hours", {})
        total_actual = sum(actual_schedule.values())
        total_planned = sum(planned_schedule.values()) if planned_schedule else 0
        score = sum(
            min(actual_schedule.get(subject, 0), planned_schedule.get(subject, 0)) for subject in planned_schedule)
        total_score += score / max(total_actual, total_planned)
    return total_score / len(groups)

def main():
    POPULATION_SIZE = 100
    MUTATION_RATE = 0.1
    GENERATIONS = 100
    CROSSOVER = 4
    best, score = genetic_algorithm(accurate, GENERATIONS, POPULATION_SIZE, CROSSOVER, MUTATION_RATE)
    print('Done!\n')

    table = PrettyTable()
    table.field_names = ["(index)", "Day", "Lesson", "Group", "Subject", "Teacher"]

    for i, cell in enumerate(best):
        table.add_row([i, cell["Day"], cell["Lesson"], str(cell["Group"].group_name),
                       cell["Subject"], str(cell["Teacher"].name) if cell["Teacher"] is not None else None])

    print(table)


if __name__ == "__main__":
    main()
