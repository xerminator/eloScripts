import csv, math
 
class Player:
    def __init__(self, name, elo=1000, crewwins=0, crewlosses=0, impwins=0, implosses=0):
        self.name = name
        self.elo = float(elo)
        self.crewwins = int(crewwins)
        self.crewlosses = int(crewlosses)
        self.impwins = int(impwins)
        self.implosses = int(implosses)
    
    def __repr__(self):
        return f'{self.name}: {round(self.elo)}'
    
    def updatecrew(self, prob, obs, firstdead=False):
        k = 10 if firstdead else 30
        self.elo += k*(obs - prob)
        self.crewwins += obs
        self.crewlosses += not obs
    
    def updateimp(self, prob, obs):
        self.elo += 30*(obs - prob)
        self.impwins += obs
        self.implosses += not obs
    
    def dict(self):
        return {
            'Name': self.name,
            'Elo': round(self.elo),
            'Crew Wins': self.crewwins,
            'Crew Losses': self.crewlosses,
            'Imp Wins': self.impwins,
            'Imp Losses': self.implosses
        }
 
class Crew:
    def __init__(self, players):
        assert len(players) == 8
        self.players = players
    
    def __repr__(self):
        return f'Crew: {" ".join(map(repr, self.players))}'
    
    def names(self):
        return set(p.name for p in self.players)
    
    def elo(self):
        return math.sqrt(sum(p.elo**2 for p in self.players) / len(self.players))
    
    def q(self):
        return 10 ** (self.elo()/350)
 
class Imps:
    def __init__(self, players):
        assert len(players) == 2
        self.players = players
    
    def __repr__(self):
        return f'Imps: {" ".join(map(repr, self.players))}'
    
    def names(self):
        return set(p.name for p in self.players)
    
    def elo(self):
        return math.sqrt(sum(p.elo**2 for p in self.players) / len(self.players))
    
    def q(self):
        return 10 ** (self.elo()/400)
 
class Game:
    def __init__(self, crew, imps):
        self.crew = crew
        self.imps = imps
        crewq = crew.q()
        impsq = imps.q()
        denom = crewq + impsq
        self.crewe = crewq / denom
        self.impse = impsq / denom
    
    def result(self, impwin, firstdead=set()):
        for c in self.crew.players:
            c.updatecrew(self.crewe, not impwin, c.name in firstdead)
        for i in self.imps.players:
            i.updateimp(self.impse, impwin)
    
    def save(self):
        return {p.name: p for p in \
            self.crew.players+self.imps.players}
 
 
totalgames = 0
players = dict()
 
with open('tournament.txt') as tournfile:
    for line in tournfile:
        try:
            winner, imps, crew, first = line.lower().strip().split(';')
        except ValueError:
            print(f'Error: {line}')
            quit()
        
        if winner not in {'c', 'i'}:
            print(f'Winner must be c or i: {line}')
            quit()
        
        impnames = set(imps.strip().split(' '))
        if len(impnames) != 2:
            print(f'Check the impostor names: {line}')
            quit()
        
        crewnames = set(crew.strip().split(' '))
        if len(crewnames) != 8:
            print(f'Check the crew names: {line}')
            quit()
        
        firstdead = set(first.strip().split(' '))
        if not (firstdead <= crewnames):
            print(f'First dead names must be subset of crew: {line}')
            quit()
        
        imps = Imps([players.get(i, Player(i)) for i in impnames])
        crew = Crew([players.get(c, Player(c)) for c in crewnames])
        
        game = Game(crew, imps)
        game.result(winner == 'i', firstdead)
        players |= game.save()
        totalgames += 1
 
 
with open('elos.csv', 'w', newline='') as elofile:
    scheme = ['Name', 'Elo', 'Crew Wins', 'Crew Losses', 'Imp Wins', 'Imp Losses']
    writer = csv.DictWriter(elofile, fieldnames=scheme)
 
    writer.writeheader()
    for p in sorted(players.values(), key=lambda p: -p.elo):
        writer.writerow(p.dict())
 
print(f'{totalgames} games')