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
class Event:
    def __init__(self, event, match):
        self.match = match
        self.eventType = event['Event']
        self.time = event['Time']
        self.name = None
        self.player = None
        self.target = None
        self.type = None
        self.taskType = None
        self.taskName = None
        self.gameCode = None
        self.WinReason = None
        self.deadPlayer = None
        self.process_event(event)
    def process_event(self, event):
        match self.eventType:
            case "StartGame":
                self.gameCode = event['GameCode']
            case "Task":
                self.name = event['Name']
                self.taskType = event['TaskType']
                self.taskName = event['TaskName']
            case "Death":
                self.name = event['Name']
            case "EndGame":
                self.WinReason = event['WinReason']
                self.gameCode = event['GameCode']
            case "MeetingStart":
                self.gameCode = event['GameCode']
                self.player = event['Player'] if 'Player' in event else None
            case "MeetingEnd":
                self.gameCode = event['GameCode']
            case "PlayerVote":
                self.player = event['Player']
                self.target = event['Target']
                self.type = event['Type']
            case "GameCancel":
                self.player = event['Player']
            case "BodyReport":
                self.player = event['Player']
                self.deadPlayer = event['DeadPlayer']
            case "ManualGameEnd":
                self.player = event['Player']
            case "Disconnect":
                self.name = event['Name']



        

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
        self.events = []
        self.deadPlayers = []
        self.get_players()
        self.get_result()
        self.get_events()
        self.get_first_dead()
        #self.get_real_stats()

    def get_result(self):
        if(self.reason == "null"):
            if(self.result == "HumansByVote" or self.result == "HumansByTask"):
                self.reason = self.result
                self.result = "Crewmates Win"
            else:
                self.reason = self.result
                self.result = "Impostors Win"
    def get_players(self):
        players = []
        crewmates = []
        impostors = []
        for player in self.players:
            if(player in self.impostors):
                players.append(Player(player, "impostor"))
            elif(player in self.crewmates):
                players.append(Player(player))
        self.players = players
    def get_events(self):
        eventsFolder = './events'
        for events_file in os.listdir(eventsFolder):
            #print(f"Opening {events_file}")
            if(events_file.endswith(".json")):
                events_filePath = os.path.join(eventsFolder, events_file)
                with open(events_filePath, 'r') as file:
                    events = json.load(file)
                    for event in events:
                        eventObj = Event(event, self)
                        self.events.append(eventObj)
    def get_first_dead(self):
        try:
            deadPlayers = []
            for event in self.events:
                if event.eventType == "MeetingStart" or event.eventType == "PlayerVote" or event.eventType == "BodyReport":
                    if(len(deadPlayers) < 1):
                        continue
                    else:
                        break
                if event.eventType == "Death":
                    deadPlayers.append(event.name)
            self.deadPlayers = deadPlayers
        except Exception as error:
            print(f"Error: {error}")

                        



    
    
    # def get_real_stats(self):
    #     for player in self.players:
    #         if(player.team == "crewmate"):
                
    #         else:


#def get_time_of_death(events):


class Player:
    def __init__(self, name, team="crewmate"):
        self.name = name
        self.team = team
        self.firstDead = False
        self.kills = 0
        self.reported = 0
        self.timeAlive = ""
        self.votes = {}
        self.ejects = 0




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
                #print(f"Players: {players}")
                impostors = list(data['impostors'].replace(" ", "").split(","))
                #print(f"Impostors: {impostors}")
                crewmates = list(set(players).difference(impostors))
                #print(f"Crewmates: {crewmates}")
                #print(crewmates)
                result = data['result']
                reason = data['reason'] if 'reason' in data else "null"
                event_file = data['eventsLogFile']

                match = Match(id, timeOfMatch, players, crewmates, impostors, result, reason, event_file)
                matches.append(match)
                

    #print(matches)
match_folder = './matches'
process_match_files(match_folder)
matches = sorted(matches, key=lambda x:x.timeOfMatch)

for match in matches:
    match_players = []
    match_crewmates = []
    match_impostors = []
    match_events = []

    if match.result == "Canceled":
        continue

    for player in match.players:
        if player.team == "crewmate":
            match_crewmates.append(player.name)
        elif player.team == "impostor":
            match_impostors.append(player.name)
        match_players.append(player.name)


    #print(f"MatchId: {match.id} | Players: {match_players} | Crewmates: {match_crewmates} | Impostors: {match_impostors} | Result: {match.result} | Reason: {match.reason} | FirstDeads:  {match.deadPlayers}")
    f = open('matches.txt', 'a')
    f.write(f"MatchId: {match.id}   |   Players: {match_players}    |   Crewmates: {match_crewmates}    |   Impostors: {match_impostors}    |   Result: {match.result}  |   Reason: {match.reason}  |   FirstDeads:  {match.deadPlayers} \n")
    f.close()









