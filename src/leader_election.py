#To do archit
class LeaderElection(process):
    def __init__(validators, window_size,exclude_size,reputation_leaders):
        self.validators = validators
        self.window_size=window_size
        self.excluded_size=excluded_size
        self.reputation_leaders=reputation_leaders

    def elect_reputation_leaders(qc):
        pass

    def update_leaders(qc):
        """
        Update the leader
        """
        pass

    def get_leader(round):
        return validators[(round/2) % len(validators)]