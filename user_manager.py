import openpyxl
import os

class UserManager:
    def __init__(self, filename="info_snake.xlsx"):
        self.filename = filename
        self.users = {}
        self.load_users()

    def load_users(self):
        if not os.path.exists(self.filename):
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(["username", "password", "best_score"])
            wb.save(self.filename)

        wb = openpyxl.load_workbook(self.filename)
        sheet = wb.active

        for row in sheet.iter_rows(values_only=True):
            if row[0] != "username":
                self.users[row[0]] = {
                    "password": row[1],
                    "best_score": row[2]
                }

    def save_users(self):
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["username", "password", "best_score"])

        for username, data in self.users.items():
            sheet.append([username, data["password"], data["best_score"]])

        wb.save(self.filename)

    def authenticate(self, username, password):
        if username not in self.users:
            # créer un nouvel utilisateur
            self.users[username] = {"password": password, "best_score": 0}
            self.save_users()
            return True

        return self.users[username]["password"] == password

    def update_best_score(self, username, score):
        if score > self.users[username]["best_score"]:
            self.users[username]["best_score"] = score
            self.save_users()

    def get_top_4(self):
        # tri décroissant
        sorted_users = sorted(
            list(self.users.items()),
            key=lambda x: x[1]["best_score"],
            reverse=True
        )
        return sorted_users[:4]
