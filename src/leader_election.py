class LeaderElection:
    """
    Leader election module
    """
    def __init__(self, n_validators):  #, window_size,exclude_size,reputation_leaders):
        self.n_validators = n_validators
        # self.window_size = window_size
        # self.excluded_size = exclude_size
        # self.reputation_leaders = reputation_leaders

    def elect_reputation_leaders(self, qc):
        pass

    def update_leaders(self, qc):
        """
        Update the leader
        """
        pass

    def get_leader(self, round):
        return round % self.n_validators
