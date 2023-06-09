class Session:
    """
    The Session class represents a user session.
    It's used to store the username of the currently logged-in user.
    """

    def __init__(self):
        """Initialize a new Session with no current user."""
        self._current_user = None

    def set_current_user(self, user):
        """
        Set the current user of the session.

        Parameters
        ----------
        user : str
            The username of the user to set as the current user.
        """
        self._current_user = user

    def get_current_user(self):
        """
        Get the username of the current user.

        Returns
        -------
        str
            The username of the current user.
        """
        return self._current_user
