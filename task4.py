# task4.py

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            return "Ошибка"
        if (course not in self.courses_in_progress
                or course not in lecturer.courses_attached):
            return "Ошибка"
        if not isinstance(grade, int) or not (1 <= grade <= 10):
            return "Ошибка"
        lecturer.grades.setdefault(course, []).append(grade)
        return None

    def _average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self):
        avg = self._average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) or 'Нет'
        finished_courses = ', '.join(self.finished_courses) or 'Нет'
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {avg}\n"
            f"Курсы в процессе изучения: {courses_in_progress}\n"
            f"Завершенные курсы: {finished_courses}"
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self):
        avg = self._average_grade()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {avg}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached \
                and course in student.courses_in_progress:
            student.grades.setdefault(course, []).append(grade)
        else:
            print("Ошибка")

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# === ГЛОБАЛЬНЫЕ ФУНКЦИИ ===

def avg_grade_students(students, course):
    """
    Средняя оценка за ДЗ по курсу среди студентов.
    :param students: list[Student]
    :param course: str
    :return: float (округлено до 1 знака)
    """
    grades = []
    for student in students:
        if isinstance(student, Student) and course in student.grades:
            grades.extend(student.grades[course])
    return round(sum(grades) / len(grades), 1) if grades else 0.0


def avg_grade_lecturers(lecturers, course):
    """
    Средняя оценка за лекции по курсу среди лекторов.
    :param lecturers: list[Lecturer]
    :param course: str
    :return: float (округлено до 1 знака)
    """
    grades = []
    for lecturer in lecturers:
        if isinstance(lecturer, Lecturer) and course in lecturer.grades:
            grades.extend(lecturer.grades[course])
    return round(sum(grades) / len(grades), 1) if grades else 0.0


# === ПОЛЕВЫЕ ИСПЫТАНИЯ ===
if __name__ == '__main__':
    # --- Создаём 2 студентов ---
    student1 = Student('Алиса', 'Селезнёва', 'жен')
    student1.courses_in_progress = ['Python', 'Git']
    student1.finished_courses = ['Введение в программирование']

    student2 = Student('Борис', 'Громов', 'муж')
    student2.courses_in_progress = ['Python', 'Java']
    student2.finished_courses = ['Алгоритмы']

    # --- Создаём 2 лектора ---
    lecturer1 = Lecturer('Иван', 'Петров')
    lecturer1.courses_attached = ['Python', 'Git']

    lecturer2 = Lecturer('Мария', 'Ковалёва')
    lecturer2.courses_attached = ['Python', 'Java']

    # --- Создаём 2 проверяющих ---
    reviewer1 = Reviewer('Ольга', 'Дубровская')
    reviewer1.courses_attached = ['Python']

    reviewer2 = Reviewer('Сергей', 'Морозов')
    reviewer2.courses_attached = ['Git', 'Java']

    # --- Выставление оценок студентам (Reviewer → Student) ---
    reviewer1.rate_hw(student1, 'Python', 10)
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer2.rate_hw(student1, 'Git', 8)

    reviewer1.rate_hw(student2, 'Python', 7)
    reviewer2.rate_hw(student2, 'Java', 9)

    # --- Студенты оценивают лекторов (Student → Lecturer) ---
    student1.rate_lecture(lecturer1, 'Python', 10)
    student1.rate_lecture(lecturer1, 'Git', 9)
    student2.rate_lecture(lecturer1, 'Python', 8)

    student2.rate_lecture(lecturer2, 'Python', 9)
    student1.rate_lecture(lecturer2, 'Python', 10)  # Алиса учится на Python → может оценивать

    # --- Проверка __str__ ---
    print("=== Reviewer 1 ===")
    print(reviewer1)
    print("\n=== Lecturer 1 ===")
    print(lecturer1)
    print("\n=== Student 1 ===")
    print(student1)

    # --- Сравнения ---
    print("\n=== Сравнения ===")
    print(f"student1 > student2: {student1 > student2}")      # 9.3 > 8.0 → True
    print(f"lecturer1 < lecturer2: {lecturer1 < lecturer2}")  # 9.0 < 9.5 → True

    # --- Средние по курсам ---
    print("\n=== Средние по курсам ===")
    students_list = [student1, student2]
    lecturers_list = [lecturer1, lecturer2]

    print(f"Средняя оценка студентов по Python: {avg_grade_students(students_list, 'Python')}")
    print(f"Средняя оценка лекторов по Python: {avg_grade_lecturers(lecturers_list, 'Python')}")