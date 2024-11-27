import json
from tkinter.filedialog import askopenfilename

# file types recommended
file_types = [("Replay Files", "*.ttrm")]


# load the file
def load_file():
    try:
        with open(askopenfilename(title="Pick a .ttrm: a Tetrio Replay File", filetypes=file_types)) as file:
            global data
            data = json.load(file)
    except:
        print("File not found! Relaunch program and try again.")
        print("SOMETHING IS GOING WRONG !!!!!!!!!!!!!!!!")


class Player:
    def __init__(self, username, win_count, apm, pps, vs):
        self.username = username
        self.win_count = win_count
        self.apm = apm
        self.pps = pps
        self.vs = vs
        self.app = self.apm / (60 * self.pps)

    def print_information(self):
        print(f"Username: {self.username}\n"
              f"Win Count: {self.win_count}\n"
              f"APM: {self.apm}\n"
              f"PPS: {self.pps}\n"
              f"VS: {self.vs}\n"
              f"APP: {self.app}\n")


class Round:
    def __init__(self, usernames, apms, ppss, vss, round_number, round_length, winner):
        self.usernames = usernames
        self.apms = apms
        self.ppss = ppss
        self.vss = vss
        self.apps = self.calculate_app()
        self.round_number = round_number
        self.round_length = round_length
        self.winner = winner

    def print_information(self):
        print(f"ROUND NUMBER: {self.round_number}\n"
              f"Username: {self.usernames}\n"
              f"APM: {self.apms}\n"
              f"PPS: {self.ppss}\n"
              f"VS: {self.vss}\n"
              f"APP: {self.apps}\n")

    # calculates app. app = apm / (60 * pps)
    def calculate_app(self):
        apps = []
        for i in range(len(self.apms)):
            apps.append(self.apms[i] / (60 * self.ppss[i]))
        return apps


# gets all the relevant information about a player
def get_player_data():
    players = []

    # gets the section where the player's information is stored
    leaderboard = data["replay"]["leaderboard"]

    # creates two player objects with all the information gathered from the leaderboard section, then returns the two players
    for i in range(len(leaderboard)):
        player = Player(
            leaderboard[i]["username"],
            leaderboard[i]["wins"],
            leaderboard[i]["stats"]["apm"],
            leaderboard[i]["stats"]["pps"],
            leaderboard[i]["stats"]["vsscore"]
        )
        players.append(player)
    #print(players[0].apm)
    #print(players[1].apm)
    return players


# gets all the information about all the rounds
def get_round_information():
    rounds = []

    # gets the information
    for i in range(len(data["replay"]["rounds"])):
        winner_data = data["replay"]["rounds"][i][0]["stats"]
        winner_name = data["replay"]["rounds"][i][0]["username"]
        loser_data = data["replay"]["rounds"][i][1]["stats"]
        loser_name = data["replay"]["rounds"][i][1]["username"]

        # calculates round length
        round_length = round(data["replay"]["rounds"][i][0]["replay"]["frames"] / 60)

        # sort the names alphabetically
        names = [winner_name, loser_name]
        names.sort()
        first = names[0]

        # actually sorts the names, because tetrio's way of storing
        # the json file is that the winner always comes first
        # within the saved round
        if winner_name == first:
            apms = [winner_data["apm"], loser_data["apm"]]
            ppss = [winner_data["pps"], loser_data["pps"]]
            vss = [winner_data["vsscore"], loser_data["vsscore"]]

            rounds.append(Round(names, apms, ppss, vss, i + 1, round_length, winner_name))

        else:
            apms = [loser_data["apm"], winner_data["apm"]]
            ppss = [loser_data["pps"], winner_data["pps"]]
            vss = [loser_data["vsscore"], winner_data["vsscore"]]

            rounds.append(Round(names, apms, ppss, vss, i + 1, round_length, winner_name))

    return rounds


# calculate the average stats (apm, pps, vs, app)
def average_stats(rounds):
    # take the rounds selected and get the ones you actually want to calculate for
    rounds_list = get_round_information()
    rounds_to_calculate = []
    for i in range(len(rounds)):
        rounds_to_calculate.append(rounds_list[i])

    # return none if no rounds are selected
    if len(rounds_to_calculate) == 0:
        return [[None, None, None, None], [None, None, None, None]]

    # actually calculate the values
    # add up all the values then divide by the length

    """
    
    important: i don't know why this average doesn't equal the same as tetrio gets.
    if you round to the 2nd decimal or dont or anything, i can't replicate the value.
    i have no idea why tetrio gets a different value, it's just gonna be something
    that i have to warn about. so yeah, if you're reading this, sorry about that. 
    if you have an idea on how to fix this, dm me on discord - zachakaquack
    
    """
    stats_list = []
    # do all below twice for each player
    for j in range(2):
        avg_apm = 0
        avg_pps = 0
        avg_vs = 0
        avg_app = 0
        for i in range(len(rounds_to_calculate)):
            # add all up
            avg_apm += rounds_to_calculate[i].apms[j]
            avg_pps += rounds_to_calculate[i].ppss[j]
            avg_vs += rounds_to_calculate[i].vss[j]
            avg_app += rounds_to_calculate[i].apps[j]

        # divide by length of the list, aka the amount of rounds
        stats_list.append([round(avg_apm / len(rounds_to_calculate), 2),
                           round(avg_pps / len(rounds_to_calculate), 2),
                           round(avg_vs / len(rounds_to_calculate), 2),
                           round(avg_app / len(rounds_to_calculate), 2)])
    return stats_list

load_file()
