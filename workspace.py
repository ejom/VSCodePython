class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"My name is {self.name} and I am ({self.age}) years old"
    def greet(a):
        print(f"Hey, I'm {a.name}. What's your name?")
class Student(Person):
    def __init__(self, name, age, school):
        self.school = school
    def __str__(self):
        return f"My name is {self.name}, I am {self.age} years old and I go to {self.school}"
class StudentWorker(Student):
    def __init__(self, name, age, school, job):
        Person.__init__(self, name, age)
        self.job = job
    def __str__(self):
        return f"My name is {self.name}, I am {self.age} years old"
p1 = StudentWorker("John", 25, "MIT", "Software Engineer")
print(p1)