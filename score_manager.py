"""
Adapter around `UserManager` to expose score-related operations
to the rest of the application.
"""


class ScoreManager:
    """
    Adapter that forwards score operations to a `UserManager` instance.

    Parameters
    - user_manager: an instance providing `update_best_score(username, score)`
      and `get_top_4()` methods (the project's `UserManager` fits this
      contract).

    Noa - Z125529
    """

    def __init__(self, user_manager):
        self.user_manager = user_manager

    def update_score(self, username, score):
        """
        Update the stored best score for `username` if `score` is higher.
        """
        self.user_manager.update_best_score(username, score)

    def get_top_4(self):
        """
        Return the top 4 users as provided by `UserManager.get_top_4()`.
        """
        return self.user_manager.get_top_4()

