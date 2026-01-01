class ScoreManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    def update_score(self, username, score):
        self.user_manager.update_best_score(username, score)

    def get_top_4(self):
        return self.user_manager.get_top_4()
