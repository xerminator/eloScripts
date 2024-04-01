import csv, math, json, os

matches = []

class AmongUsELO:
    def __init__(self, k_factor, impostor_multiplier):
        self.k_factor = k_factor
        self.impostor_multiplier = impostor_multiplier

    def calculate_crewmate_elo(self, wins, total_games, voting_accuracy, max_voting_accuracy, task_completion, max_task_completion, normalized_early_death_penalty):
        crewmate_score = (wins / total_games) + (voting_accuracy / max_voting_accuracy) + (task_completion / max_task_completion) - normalized_early_death_penalty
        return crewmate_score

    def calculate_impostor_elo(self, wins, total_games, kills, max_kills, kill_streak, max_kill_streak):
        impostor_score = (wins / total_games) + (kills / max_kills) + (kill_streak / max_kill_streak)
        return impostor_score

    def calculate_overall_elo(self, crewmate_score, impostor_score):
        overall_elo = self.k_factor * (crewmate_score + self.impostor_multiplier * impostor_score)
        return overall_elo
    def calculate_crew_performance_player(votingAccuracyP, tasksP, timeAliveP, reportedBodyP):
        votingAccuracy = votingAccuracyP,
        tasks = tasksP,
        timeAlive = timeAliveP,
        reportedBody = reportedBodyP

        return (0.2 * tasks) * (0.2 * timeAlive) * (0.2 * reportedBody) * (0.4 * votingAccuracy)
    def calculate_imp_performance_player(timeAliveP, killsP, ejectsP):
        return (0.6 * timeAliveP) * (0.2 * killsP) * (0.2 * ejectsP)
    

# class Player:
#     def __init__(self, name):
#         self.name = name

    # def __init__(self, name, crewmate_wins, crewmate_losses, impostor_wins, impostor_losses):
    #     self.name = name
    #     self.crewmate_wins = crewmate_wins
    #     self.crewmate_losses = crewmate_losses
    #     self.impostor_wins = impostor_wins
    #     self.impostor_losses = impostor_losses
    #     self.crewmate_elo = 0
    #     self.impostor_elo = 0
    #     self.overall_elo = 0
class Match:
    def __init__(self, id, timeOfMatch, players, crewmates, impostors, result, reason, event_file):
        self.id = id
        self.timeOfMatch = timeOfMatch
        self.players = players
        self.crewmates = crewmates
        self.impostors = impostors
        self.result = result
        self.reason = reason
        self.event_file = event_file



# with open('matches.json') as matches:
#     for match in matches:
#         data = json.loads(match)

#         id = data['MatchID']
#         timeOfMatch = data['gameStarted']
#         players = data['players']
#         impostors = data['impostors']
#         crewmates = list(set(players) - set(impostors))
#         result = data['result']
#         reason = data['reason']

#         for player in players:
#             crew_win = 0
#             imp_win = 0
#             crew_loss = 0
#             imp_loss = 0

#             player_obj = Player()
def process_match_files(folderPath):
    for match_file in os.listdir(folderPath):
        if(match_file.endswith("_match.json")):
            match_filePath = os.path.join(folderPath, match_file)
            print(f"Process match file: {match_filePath}")
            with open(match_filePath, 'r') as file:
                data = json.load(file)
                id = data['MatchID']
                timeOfMatch = data['gameStarted']
                players = list(data['players'].replace(" ", "").split(","))
                print(f"Players: {players}")
                impostors = list(data['impostors'].replace(" ", "").split(","))
                print(f"Impostors: {impostors}")
                crewmates = list(set(players).difference(impostors))
                print(f"Crewmates: {crewmates}")
                #print(crewmates)
                result = data['result']
                reason = data['reason'] if 'reason' in data else "null"
                event_file = data['eventsLogFile']

                match = Match(id, timeOfMatch, players, crewmates, impostors, result, reason, event_file)
                matches.append(match)
    #print(matches)
match_folder = './matches'
process_match_files(match_folder)
#for match in matches:
    #print(f"MatchId: {match.id} | Players: {match.players} | Crewmates: {match.crewmates} | Impostors: {match.impostors} | Result: {match.result} | Reason: {match.reason}" )










