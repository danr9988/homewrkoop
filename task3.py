# task3.py

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

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

    def __le__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() <= other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()


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

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() <= other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() == other._average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached \
                and course in student.courses_in_progress:
            student.grades.setdefault(course, []).append(grade)
        else:
            print("Ошибка")

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}"
        )


# Проверка
if __name__ == '__main__':
    some_student = Student('Ruoy', 'Eman', 'your_gender')
    some_student.courses_in_progress += ['Python', 'Git']
    some_student.finished_courses += ['Введение в программирование']
    some_student.grades = {'Python': [10, 10, 9], 'Git': [10]}

    some_lecturer = Lecturer('Some', 'Buddy')
    some_lecturer.courses_attached += ['Python']
    some_lecturer.grades = {'Python': [10, 9.8, 10]}

    some_reviewer = Reviewer('Some', 'Buddy')

    print(some_reviewer)
    print()
    print(some_lecturer)
    print()
    print(some_student)
    print()

    student2 = Student('Jane', 'Doe', 'female')
    student2.courses_in_progress = ['Python']
    student2.grades = {'Python': [8, 8, 8]}

    print(some_student > student2)  # True (9.8 > 8.0)
    print(some_student == student2)  # False

    lecturer2 = Lecturer('Leo', 'Smith')
    lecturer2.grades = {'Python': [9.0]}

    print(some_lecturer > lecturer2)  # True (9.9 > 9.0)