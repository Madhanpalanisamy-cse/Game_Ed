import json
import os

class Student:
    def __init__(self, name="Scholar", level=1, xp=0):
        self.name = name
        self.level = level
        self.xp = xp
        self.xp_to_next_level = self.calculate_xp_needed()

    def calculate_xp_needed(self):
        # Linear progression: Level 1 -> 100, Level 2 -> 200, etc.
        return self.level * 100

    def add_xp(self, amount):
        self.xp += amount
        leveled_up = False
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = self.calculate_xp_needed()
            leveled_up = True
        return leveled_up

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next_level": self.xp_to_next_level
        }

class Task:
    def __init__(self, id, title, xp_reward=50, completed=False):
        self.id = id
        self.title = title
        self.xp_reward = xp_reward
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "xp_reward": self.xp_reward,
            "completed": self.completed
        }

class Question:
    def __init__(self, id, type, content, answer, xp_reward=100, solved=False):
        self.id = id
        self.type = type # "Aptitude" or "Programming"
        self.content = content
        self.answer = answer
        self.xp_reward = xp_reward
        self.solved = solved

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "content": self.content,
            "answer": self.answer,
            "xp_reward": self.xp_reward,
            "solved": self.solved
        }

class GameData:
    FILE_PATH = "data.json"

    def __init__(self):
        self.student = Student()
        self.tasks = []
        self.questions = []
        self.load()

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as f:
                data = json.load(f)
                self.student = Student(data["student"]["name"], data["student"]["level"], data["student"]["xp"])
                self.tasks = [Task(**t) for t in data["tasks"]]
                self.questions = [Question(**q) for q in data.get("questions", [])]
        
        # If no questions found, add default ones
        if not self.questions:
            self.questions = [
                Question(1, "Aptitude", "If a train travels at 60km/h, how far does it travel in 15 minutes? (Provide only the number in km)", "15"),
                Question(2, "Programming", "What is the output of 'print(2**3)' in Python?", "8"),
                Question(3, "Logical", "If all A are B and all B are C, are all A necessarily C? (Yes/No)", "Yes")
            ]
            self.save()

    def save(self):
        data = {
            "student": self.student.to_dict(),
            "tasks": [t.to_dict() for t in self.tasks],
            "questions": [q.to_dict() for q in self.questions]
        }
        with open(self.FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id and not task.completed:
                task.completed = True
                leveled_up = self.student.add_xp(task.xp_reward)
                self.save()
                return True, leveled_up
        return False, False

    def solve_question(self, question_id, user_answer):
        for q in self.questions:
            if q.id == question_id and not q.solved:
                if str(user_answer).strip().lower() == str(q.answer).strip().lower():
                    q.solved = True
                    leveled_up = self.student.add_xp(q.xp_reward)
                    self.save()
                    return True, leveled_up, "Correct! +" + str(q.xp_reward) + " XP"
                else:
                    return False, False, "Incorrect. Try again!"
        return False, False, "Already solved or not found."
