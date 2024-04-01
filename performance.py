import elo

class PlayerPerformance:
    def __init__(self, player, event_file):
        self.player = player
        self.event_file = event_file
        self.tasks, self.votes, self.reported, self.kills, self.timeAlive = 0
    
    def get_real_stats(self):
        self.tasks = self.get_tasks()
        self.votes = self.get_votes()
        self.reported = self.get_reported()
        self.kills = self.get_kills()
        self.timeAlive = self.get_timeAlive()
    def get_tasks(self):
        
    

