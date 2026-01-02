import openpyxl
import os


# --- Exceptions personnalisées pour la gestion des erreurs  ---
class UserManagerError(Exception):
    pass  


class EmptyFieldError(UserManagerError):
    pass  # Levée quand username/password sont vides


class InvalidCredentialsError(UserManagerError):
    pass  # Levée quand les identifiants sont invalides


class FileAccessError(UserManagerError):
    pass  # Levée quand le fichier Excel ne peut être lu/écrit


class User:
    def __init__(self, username, password, best_score=0):
        self.username = username
        self.password = password
        self.best_score = best_score

    def __lt__(self, other):
        # Permet de trier les utilisateurs par score (utilisé pour le classement)
        return self.best_score < other.best_score

    def __eq__(self, other):
        # Compare deux utilisateurs par leur nom d'utilisateur
        if isinstance(other, User):
            return self.username == other.username
        return False

    def __add__(self, value):
        # Permet User + int -> retourne un nouvel User avec score augmenté (non destructif)
        if isinstance(value, int):
            return User(self.username, self.password, self.best_score + value)
        return NotImplemented

    def __iadd__(self, value):
        # Permet += pour augmenter le score en place
        if isinstance(value, int):
            self.best_score += value
            return self
        return NotImplemented

    def __repr__(self):
        return f"User(username={self.username!r}, best_score={self.best_score})"


class UserManager:
    def __init__(self, filename="info_snake.xlsx"):
        self.filename = filename
        self.users = {}
        self.load_users()

    def load_users(self):
        if not os.path.exists(self.filename):
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(["username", "password", "best_score"])  # entête du fichier
            wb.save(self.filename)

        try:
            wb = openpyxl.load_workbook(self.filename)
        except Exception as e:
            # Propagation via exception spécifique pour faciliter les tests 
            raise FileAccessError(f"\033[31mImpossible de lire le fichier users\033[0m: {e}")

        sheet = wb.active

        for row in sheet.iter_rows(values_only=True):
            if row[0] != "username":
                # Construction d'un objet User au lieu d'un dict (surcharge d'opérateurs disponible)
                best = row[2] if row[2] is not None else 0
                self.users[row[0]] = User(row[0], row[1], best)

    def save_users(self):
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["username", "password", "best_score"])  # entête

        for username, user in self.users.items():
            # user est une instance de User
            sheet.append([username, user.password, user.best_score])

        try:
            wb.save(self.filename)
        except Exception as e:
            raise FileAccessError(f"\033[31mImpossible d'écrire le fichier users\033[0m: {e}")

    def authenticate(self, username, password):
        # Validation minimale des champs
        if not username or not password:
            raise EmptyFieldError("\033[31mLe nom d'utilisateur et le mot de passe ne peuvent pas être vides\033[0m")

        if username not in self.users:
            # créer un nouvel utilisateur si inexistant
            self.users[username] = User(username, password, 0)
            self.save_users()
            return True

        # Comparaison du mot de passe existant
        user = self.users[username]
        if user.password == password:
            return True
        # Pour l'évaluation : lever une exception quand le mot de passe est incorrect
        raise InvalidCredentialsError("\033[31mPassword incorrect\033[0m")

    def update_best_score(self, username, score):
        if username not in self.users:
            raise InvalidCredentialsError("\033[31mUser unknown\033[0m")

        user = self.users[username]
        if score > user.best_score:
            user.best_score = score
            self.save_users()

    def get_top_4(self):
        # tri décroissant
        # On retourne une structure compatible avec l'existant: (username, {"best_score": ...})
        sorted_users = sorted(
            list(self.users.items()),
            key=lambda x: x[1].best_score,
            reverse=True
        )

        result = []
        for username, user in sorted_users[:4]:
            result.append((username, {"best_score": user.best_score}))
        return result

