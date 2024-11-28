import json
from tkinter.filedialog import askopenfilename

# file type required
file_types = [("Replay Files", "*.ttrm")]


# load the file
#def load_file(is_link=False, link=""):
def load_file():
    # if is_link:
    #
    #     response = requests.get(link)
    #     file_path = f"{link[link.find("#R:") + 3:]}.ttrm"
    #
    #     if response.status_code == 200:
    #         with open(file_path, 'wb') as file:
    #             file.write(response.content)
    #         #print('File downloaded successfully')
    #
    #         with open(askopenfilename(title=file_path, filetypes=file_types)) as file:
    #             global data
    #             data = json.load(file)
    #
    #     else:
    #         #print('Failed to download file')
    #
    # else:
    try:
        with open(askopenfilename(title="Pick a .ttrm: a Tetrio Replay File", filetypes=file_types)) as file:
            global data
            data = json.load(file)
    except:
        print("File not found! Relaunch program and try again.")


class Player:
    def __init__(self, username, win_count, apm, pps, vs, arr, das, dcd, sdf, safelock, cancel, may20g):
        # misc
        self.username = username
        self.win_count = win_count

        # stats
        self.apm = apm
        self.pps = pps
        self.vs = vs
        self.app = self.apm / (60 * self.pps)

        # handling
        self.arr = arr
        self.das = das
        self.dcd = dcd
        self.sdf = sdf
        self.safelock = safelock  # prevent accidental hard drops
        self.cancel = cancel  # cancel das when changing directions
        self.may20g = may20g  # prefer soft drop over movement

    def print_information(self):
        print(f"Username: {self.username}\n"
              f"Win Count: {self.win_count}\n"
              f"APM: {self.apm}\n"
              f"PPS: {self.pps}\n"
              f"VS: {self.vs}\n"
              f"arr: {self.arr}\n"
              f"das: {self.das}\n"
              f"dcd: {self.dcd}\n"
              f"sdf: {self.sdf}\n"
              f"safelock: {self.safelock}\n"
              f"cancel: {self.cancel}\n"
              f"may20g: {self.may20g}\n")


class Round:
    def __init__(self, usernames, apms, ppss, vss, round_number, round_length, winner, frame_length, pieces_placeds,
                 clearss, garbages):
        # names
        self.usernames = usernames

        # stats
        self.apms = apms
        self.ppss = ppss
        self.vss = vss
        self.apps = self.calculate_app()

        # round information
        self.round_number = round_number
        self.round_length = round_length
        self.winner = winner
        self.frame_length = frame_length

        # player informations
        self.pieces_placeds = pieces_placeds
        self.clearss = clearss
        self.garbages = garbages

    def print_information(self):
        print(f"ROUND NUMBER: {self.round_number}\n"
              f"Username: {self.usernames}\n"
              f"APM: {self.apms}\n"
              f"PPS: {self.ppss}\n"
              f"VS: {self.vss}\n"
              f"APP: {self.apps}\n"
              f"round_number: {self.round_number}\n"
              f"round_length: {self.round_length}\n"
              f"winner: {self.winner}\n"
              f"frame_length: {self.frame_length}\n"
              f"pieces_placeds: {self.pieces_placeds}\n"
              f"clearss: {self.clearss}\n"
              f"garbages: {self.garbages}\n")

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
    leaderboard = data["replay"]

    # creates two player objects with all the information gathered from the leaderboard section, then returns the two players
    for i in range(len(leaderboard)):

        # this i and s thing exists because either im stupid or the way the replay file is set up is weird. i just need to invert whatever it is and itll get it properly idk
        if i == 0:
            s = 1
        else:
            s = 0

        player = Player(
            leaderboard["leaderboard"][i]["username"],  # usernamez
            leaderboard["leaderboard"][i]["wins"],  # win count for the set
            leaderboard["leaderboard"][i]["stats"]["apm"],  # average apm
            leaderboard["leaderboard"][i]["stats"]["pps"],  # average pps
            leaderboard["leaderboard"][i]["stats"]["vsscore"],  # average vs

            leaderboard["rounds"][0][s]["replay"]["options"]["handling"]["arr"],  # find arr
            leaderboard["rounds"][0][s]["replay"]["options"]["handling"]["das"],  # find das
            leaderboard["rounds"][0][s]["replay"]["options"]["handling"]["dcd"],  # find dcd
            leaderboard["rounds"][0][s]["replay"]["options"]["handling"]["sdf"],  # find sdf
            leaderboard["rounds"][0][s]["replay"]["options"]["handling"]["safelock"],  # find safelock
            leaderboard["rounds"][0][s]["replay"]["options"]["handling"]["cancel"],  # find direction das cancel
            leaderboard["rounds"][0][s]["replay"]["options"]["handling"]["may20g"],  # find soft drop over movement
        )
        players.append(player)

    return players


# gets all the information about all the rounds
def get_round_information():
    rounds = []

    # gets the information
    for i in range(len(data["replay"]["rounds"])):
        player_one_alive = data["replay"]["rounds"][i][0]["alive"]

        if player_one_alive:
            winner_data = data["replay"]["rounds"][i][0]["stats"]
            winner_name = data["replay"]["rounds"][i][0]["username"]
            loser_data = data["replay"]["rounds"][i][1]["stats"]
            loser_name = data["replay"]["rounds"][i][1]["username"]
        else:
            winner_data = data["replay"]["rounds"][i][1]["stats"]
            winner_name = data["replay"]["rounds"][i][1]["username"]
            loser_data = data["replay"]["rounds"][i][0]["stats"]
            loser_name = data["replay"]["rounds"][i][0]["username"]

        # calculates round length
        round_length = round(data["replay"]["rounds"][i][0]["replay"]["frames"] / 60)
        frame_length = data["replay"]["rounds"][i][0]["replay"]["frames"]

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

            pieces_placeds = [data["replay"]["rounds"][i][0]["replay"]["results"]["stats"]["piecesplaced"],
                              data["replay"]["rounds"][i][1]["replay"]["results"]["stats"]["piecesplaced"]]

            clearss = [data["replay"]["rounds"][i][0]["replay"]["results"]["stats"]["clears"],
                       data["replay"]["rounds"][i][1]["replay"]["results"]["stats"]["clears"]]

            garbages = [data["replay"]["rounds"][i][0]["replay"]["results"]["stats"]["garbage"],
                        data["replay"]["rounds"][i][1]["replay"]["results"]["stats"]["garbage"]]


        else:
            apms = [loser_data["apm"], winner_data["apm"]]
            ppss = [loser_data["pps"], winner_data["pps"]]
            vss = [loser_data["vsscore"], winner_data["vsscore"]]

            pieces_placeds = [data["replay"]["rounds"][i][1]["replay"]["results"]["stats"]["piecesplaced"],
                              data["replay"]["rounds"][i][0]["replay"]["results"]["stats"]["piecesplaced"]]

            clearss = [data["replay"]["rounds"][i][1]["replay"]["results"]["stats"]["clears"],
                       data["replay"]["rounds"][i][0]["replay"]["results"]["stats"]["clears"]]

            garbages = [data["replay"]["rounds"][i][1]["replay"]["results"]["stats"]["garbage"],
                        data["replay"]["rounds"][i][0]["replay"]["results"]["stats"]["garbage"]]

        rounds.append(
            Round(names, apms, ppss, vss, i + 1, round_length, winner_name, frame_length, pieces_placeds, clearss,
                  garbages))

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
    stats_list = []

    # do all below twice for each player
    for j in range(2):

        apms = []
        ppss = []
        vss = []
        apps = []
        frame_counts = []

        for i in range(len(rounds_to_calculate)):
            round_frame_length = rounds_to_calculate[i].frame_length
            # add all up
            apms.append(round_frame_length * rounds_to_calculate[i].apms[j])
            ppss.append(round_frame_length * rounds_to_calculate[i].ppss[j])
            vss.append(round_frame_length * rounds_to_calculate[i].vss[j])
            apps.append(round_frame_length * rounds_to_calculate[i].apps[j])

            frame_counts.append(round_frame_length)

        # divide by frame count (weighted by time)
        stats_list.append(
            [round(sum(apms) / sum(frame_counts), 2),
             round(sum(ppss) / sum(frame_counts), 2),
             round(sum(vss) / sum(frame_counts), 2),
             round(sum(apps) / sum(frame_counts), 2)]
        )

    return stats_list


try:
    load_file()
    players = get_player_data()
    rounds = get_round_information()
except NameError:
    exit()
