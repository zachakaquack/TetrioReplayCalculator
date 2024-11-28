import math

import calculator

from tkinter import StringVar, BooleanVar

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkScrollableFrame


class Program(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        # centers the window to the screen
        width = 1280
        height = 720

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width / 2) - (width / 2)))
        y = int(((screen_height / 2) - (height / 2)))

        self.geometry(f"{width}x{height}+{x}+{y}")

        # hit escape to quit
        self.bind("<Escape>", lambda z: self.quit())

        # no resizing windows
        self.resizable(False, False)

        # title of window
        self.title("Zach's Replay Calculator")

        # variables
        self.enabled_rounds = []

        # extra
        self.font = CTkFont(family="Calibiri", size=12, weight="bold")

        # outlines of the window
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=2, uniform="a")
        self.columnconfigure(0, weight=4, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")

        self.main_frame = CTkFrame(self, fg_color="#2b2b2b")
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.main_frame.rowconfigure(0, weight=1, uniform="a")

        self.main_frame.columnconfigure(0, weight=1, uniform="a")

        self.create_all()

    def load_file(self):
        calculator.load_file()
        self.create_all()

    def average_stats_button(self):
        rounds = []
        for i in range(len(self.enabled_rounds)):
            if self.enabled_rounds[i].get():
                rounds.append(i)

        return calculator.average_stats(rounds)

    def enable_all_rounds(self):
        for i in range(len(self.enabled_rounds)):
            self.enabled_rounds[i].set(True)

    def disable_all_rounds(self):
        for i in range(len(self.enabled_rounds)):
            self.enabled_rounds[i].set(False)

    def create_checkbox(self, value, round_check_section):
        ctk.CTkCheckBox(round_check_section, text="", variable=self.enabled_rounds[value]).grid(row=value,
                                                                                                column=0, padx=20,
                                                                                                sticky="nsew")

    def create_all(self):

        rounds_values = calculator.get_round_information()

        Sidebar(self)
        TopBar(self)

        self.enabled_rounds = []

        rounds = CTkScrollableFrame(self.main_frame)
        rounds.grid(row=0, column=0, sticky="nsew")

        rounds.rowconfigure(0, weight=1, uniform="a")

        rounds.columnconfigure(0, weight=1, uniform="a")
        rounds.columnconfigure(3, weight=1, uniform="a")
        rounds.columnconfigure(6, weight=1, uniform="a")
        rounds.columnconfigure((1, 2, 4, 5), weight=3, uniform="a")

        round_count_section = CTkFrame(rounds)
        round_count_section.grid(row=0, column=0, sticky="nsew")

        left_rounds_section = CTkFrame(rounds)
        left_rounds_section.grid(row=0, column=1, columnspan=2, sticky="nsew")

        round_timer_section = CTkFrame(rounds)
        round_timer_section.grid(row=0, column=3, sticky="nsew")

        right_rounds_section = CTkFrame(rounds)
        right_rounds_section.grid(row=0, column=4, columnspan=2, sticky="nsew")

        round_check_section = CTkFrame(rounds)
        round_check_section.grid(row=0, column=6, sticky="nsew")

        rows = []

        # generate amount of rows needed
        for i in range(len(rounds_values)):
            rows.append(i)
            self.enabled_rounds.append(BooleanVar(value=True))

        left_rounds_section.rowconfigure(rows, weight=1, uniform="a")
        right_rounds_section.rowconfigure(rows, weight=1, uniform="a")
        round_count_section.rowconfigure(rows, weight=1, uniform="a")
        round_timer_section.rowconfigure(rows, weight=1, uniform="a")
        round_check_section.rowconfigure(rows, weight=1, uniform="a")

        left_rounds_section.columnconfigure(0, weight=1, uniform="a")
        right_rounds_section.columnconfigure(0, weight=1, uniform="a")
        round_count_section.columnconfigure(0, weight=1, uniform="a")
        round_timer_section.columnconfigure(0, weight=1, uniform="a")
        round_check_section.columnconfigure(0, weight=1, uniform="a")

        winner_blue_color = "#256cca"
        winner_red_color = "#cb2525"

        loser_blue_color = "#293c49"
        loser_red_color = "#4a2117"


        for i in range(len(rounds_values)):
            # WINNER IS FIRST PERSON IN ALPHABET, AKA PLAYER ONE (BLUE WIN, RED LOSE)
            #print(rounds_values[i].winner, rounds_values[i].usernames)
            #print(rounds_values[i].print_information())
            if rounds_values[i].winner == rounds_values[i].usernames[0]:
                blue_color = winner_blue_color
                red_color = loser_red_color
            else:
                blue_color = loser_blue_color
                red_color = winner_red_color

            RoundSection(left_rounds_section,
                         rounds_values[i].apms[0],
                         rounds_values[i].ppss[0],
                         rounds_values[i].vss[0],
                         rounds_values[i].apps[0], blue_color).grid(row=i, column=0, sticky="nsew")

            RoundSection(right_rounds_section,
                         rounds_values[i].apms[1],
                         rounds_values[i].ppss[1],
                         rounds_values[i].vss[1],
                         rounds_values[i].apps[1], red_color).grid(row=i, column=0, sticky="nsew")

            ctk.CTkLabel(round_count_section, text="Round " + str(rounds_values[i].round_number), font=self.font).grid(
                row=i, column=0, sticky="nsew")

            time = rounds_values[i].round_length
            if time % 60 == 0:
                possible_zero = "0"
            else:
                possible_zero = ""
            formatted_time = f"{math.floor(time / 60)}:{time % 60}" + possible_zero

            ctk.CTkLabel(round_timer_section, text=formatted_time, font=self.font).grid(row=i, column=0,
                                                                                        sticky="nsew")

            self.create_checkbox(i, round_check_section)


class TopBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#242424")

        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.columnconfigure((0, 2), weight=2, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")

        self.grid(row=0, column=0, sticky="nsew")

        averages = calculator.get_player_data()

        # sort alphabetically into correct order
        player_one = averages[0]
        player_two = averages[1]

        names = [player_one.username, player_two.username]
        names.sort()

        if player_one.username != names[0]:
            temp = player_one
            player_one = player_two
            player_two = temp


        font = CTkFont(family="Calibiri", weight="bold", size=48)
        smaller_font = CTkFont(family="Calibiri", weight="bold", size=24)

        CTkLabel(self, text=player_one.username, font=font, fg_color="#2b2b2b", corner_radius=10).grid(row=0, column=0,
                                                                                                       sticky="nsew",
                                                                                                       pady=20, padx=30)
        CTkLabel(self, text=player_two.username, font=font, fg_color="#2b2b2b", corner_radius=10).grid(row=0, column=2,
                                                                                                       sticky="nsew",
                                                                                                       pady=20, padx=30)

        RoundSection(self, player_one.apm, player_one.pps, player_one.vs, player_one.app, "#256cca").grid(row=1,
                                                                                                          column=0,
                                                                                                          sticky="nsew",
                                                                                                          padx=20,
                                                                                                          pady=10)
        RoundSection(self, player_two.apm, player_two.pps, player_two.vs, player_two.app, "#cb2525").grid(row=1,
                                                                                                          column=2,
                                                                                                          sticky="nsew",
                                                                                                          padx=20,
                                                                                                          pady=10)


        CTkLabel(self, text=str(player_one.win_count) + " - " + str(player_two.win_count), font=font,
                 fg_color="#2b2b2b", corner_radius=10
                 ).grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

        # load more information button

        ctk.CTkButton(self, text="More Info", corner_radius=10, font=smaller_font, fg_color="#2b2b2b",
                      hover_color="#242424", command=lambda: MoreInformation(master)).grid(row=1, column=1,
                                                                                           sticky="nsew", padx=10,
                                                                                           pady=10)


class MoreInformation(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.font = CTkFont(family="Calibiri", weight="bold", size=16)

        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

        self.grid(row=1, column=0, sticky="nsew")

        self.create_extra_information()
        self.create_player_handling()
        self.create_extra_rounds()

    def create_extra_information(self):

        extra_information = ctk.CTkFrame(self)

        extra_information.rowconfigure(0, weight=1, uniform="a")
        extra_information.rowconfigure(1, weight=7, uniform="a")
        extra_information.columnconfigure((0, 1, 2), weight=1, uniform="a")

        extra_information.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

        extra_information_content = ctk.CTkFrame(extra_information)

        extra_information_content.rowconfigure((0, 1, 2), weight=1, uniform="a")
        extra_information_content.columnconfigure((0, 1, 2), weight=1, uniform="a")

        extra_information_content.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=5, padx=5)

        ctk.CTkLabel(extra_information, text="Extra Information", font=self.font).grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(extra_information_content, text="Total Sent", font=self.font).grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(extra_information_content, text="Total Received", font=self.font).grid(row=1, column=1,
                                                                                            sticky="nsew")
        ctk.CTkLabel(extra_information_content, text="Biggest Spike", font=self.font).grid(row=2, column=1,
                                                                                           sticky="nsew")

        for k in range(2):

            total_sent = []
            total_received = []
            max_spikes = []

            for i in range(len(calculator.get_round_information())):
                total_sent.append(calculator.get_round_information()[i].garbages[k]["sent"])
                total_received.append(calculator.get_round_information()[i].garbages[k]["received"])
                max_spikes.append(calculator.get_round_information()[i].garbages[k]["maxspike"])

                max_spikes.sort(reverse=True)

                if k == 0:
                    col = 0
                else:
                    col = 2

                ctk.CTkLabel(extra_information_content, text=str(sum(total_sent)) + " Lines", font=self.font).grid(
                    row=0, column=col,
                    sticky="nsew")
                ctk.CTkLabel(extra_information_content, text=str(sum(total_received)) + " Lines", font=self.font).grid(
                    row=1, column=col,
                    sticky="nsew")
                ctk.CTkLabel(extra_information_content, text=str(max_spikes[0]) + " Lines", font=self.font).grid(row=2,
                                                                                                                 column=col,
                                                                                                                 sticky="nsew")

    def create_player_handling(self):

        player_handling = ctk.CTkFrame(self)
        player_handling_content = ctk.CTkFrame(player_handling)

        player_handling.rowconfigure(0, weight=1, uniform="a")
        player_handling.rowconfigure(1, weight=7, uniform="a")
        player_handling.columnconfigure((0, 1, 2), weight=1, uniform="a")

        player_handling_content.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="a")
        player_handling_content.columnconfigure((0, 1, 2), weight=1, uniform="a")

        player_handling.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)
        player_handling_content.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=5, padx=5)

        ctk.CTkLabel(player_handling, text="Player Handling Information", font=self.font).grid(row=0, column=1)

        subjects = ["ARR", "DAS", "DCD", "SDF", "Safelock?", "Cancel DAS?", "Softdrop > Movement?"]
        for i in range(len(subjects)):
            ctk.CTkLabel(player_handling_content, text=subjects[i], font=self.font).grid(row=i, column=1,
                                                                                         sticky="nsew", pady=3)

        player_information = calculator.get_player_data()

        player_one = player_information[0]
        player_two = player_information[1]

        names = [player_one.username, player_two.username]
        names.sort()

        if player_one.username == names[0]:
            temp = player_one
            player_one = player_two
            player_two = temp

        subjects_values = [[player_one.arr, player_two.arr],
                           [player_one.das, player_two.das],
                           [player_one.dcd, player_two.dcd],
                           [player_one.sdf, player_two.sdf],
                           [player_one.safelock, player_two.safelock],
                           [player_one.cancel, player_two.cancel],
                           [player_one.may20g, player_two.may20g]]

        subjects_values_notation = ["F", "F", "F", "x", "", "", ""]

        for i in range(len(subjects)):
            ctk.CTkLabel(player_handling_content, text=str(subjects_values[i][0]) + subjects_values_notation[i],
                         font=self.font).grid(row=i, column=0, sticky="nsew", pady=3)
            ctk.CTkLabel(player_handling_content, text=str(subjects_values[i][1]) + subjects_values_notation[i],
                         font=self.font).grid(row=i, column=2, sticky="nsew", pady=3)

    def create_extra_rounds(self):

        smaller_font = CTkFont(family="Calibiri", weight="bold", size=12)

        rounds_values = calculator.get_round_information()
        rows = []
        for i in range(len(rounds_values)):
            rows.append(i)

        new_info = ctk.CTkFrame(self)

        new_info.rowconfigure(rows, weight=1, uniform="a")
        new_info.columnconfigure((0, 1, 2), weight=1, uniform="a")

        new_info.grid(row=2, column=0, sticky="nsew", padx=10, pady=20)

        winner_blue_color = "#256cca"
        winner_red_color = "#cb2525"

        loser_blue_color = "#293c49"
        loser_red_color = "#4a2117"

        for round_ in range(len(rounds_values)):


            if rounds_values[round_].winner == rounds_values[round_].usernames[0]:
                blue_color = winner_blue_color
                red_color = loser_red_color
            else:
                blue_color = loser_blue_color
                red_color = winner_red_color

            for player in range(2):

                content_frame = ctk.CTkFrame(new_info)
                content_frame.rowconfigure((0, 1, 2, 3), weight=1)
                content_frame.columnconfigure(0, weight=1, uniform="a")

                if player == 0:
                    content_frame.grid(row=round_, column=0, sticky="nsew", pady=(5, 50))
                    color = blue_color
                else:
                    content_frame.grid(row=round_, column=2, sticky="nsew", pady=(5, 50))
                    color = red_color

                # ROUND TEXT
                ctk.CTkLabel(content_frame, text="Round " + str(rounds_values[round_].round_number),
                             font=smaller_font).grid(row=0, column=0, sticky="nsew")

                # PIECES PLACED

                pieces_frame = ctk.CTkFrame(content_frame, fg_color=color, corner_radius=0)

                pieces_frame.rowconfigure(0, weight=1, uniform="a")
                pieces_frame.columnconfigure(0, weight=1, uniform="a")

                pieces_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

                ctk.CTkLabel(pieces_frame, text="Pieces Placed: " + str(rounds_values[round_].pieces_placeds[player]),
                             corner_radius=0, font=self.font).grid(row=0, column=0, sticky="nsew", pady=5)

                # CLEARS
                lines = rounds_values[round_].clearss[player]
                clears_list = [["Singles: " + str(lines["singles"]),
                                "Doubles: " + str(lines["doubles"])],

                               ["Triples: " + str(lines["triples"]),
                                "Quads: " + str(lines["quads"])],

                               ["T-Spin Singles: " + str(lines["tspinsingles"]),
                                "T-Spin Doubles: " + str(lines["tspindoubles"])],

                               ["T-Spin Triples: " + str(lines["tspintriples"]),
                                "All Clears: " + str(lines["allclear"])]]

                clears_frame = ctk.CTkFrame(content_frame, fg_color=color, corner_radius=0)

                clears_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")
                clears_frame.columnconfigure((0, 1), weight=1, uniform="a")

                for row in range(4):
                    for column in range(2):
                        ctk.CTkLabel(clears_frame, text=str(clears_list[row][column]), font=smaller_font).grid(row=row,
                                                                                                               column=column,
                                                                                                               sticky="nsew",
                                                                                                               padx=20,
                                                                                                               pady=10)

                clears_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

                # GARBAGE

                garbage_frame = ctk.CTkFrame(content_frame, fg_color=color, corner_radius=0)

                garbage_frame.rowconfigure((0, 1, 2), weight=1, uniform="a")
                garbage_frame.columnconfigure((0, 1, 2), weight=1, uniform="a")

                garbage_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

                ctk.CTkLabel(garbage_frame, text="Garbage Statistics:", font=self.font).grid(row=0, column=0,
                                                                                             columnspan=3,
                                                                                             sticky="nsew")

                ctk.CTkLabel(garbage_frame, text="Sent: ",
                             font=self.font).grid(row=1, column=0, sticky="nsew")
                ctk.CTkLabel(garbage_frame, text="Received: ",
                             font=self.font).grid(row=1, column=1, sticky="nsew")
                ctk.CTkLabel(garbage_frame, text="Max Spike: ",
                             font=self.font).grid(row=1, column=2, sticky="nsew")

                ctk.CTkLabel(garbage_frame, text=str(rounds_values[round_].garbages[player]["sent"]),
                             font=self.font).grid(row=2, column=0, sticky="nsew")
                ctk.CTkLabel(garbage_frame, text=str(rounds_values[round_].garbages[player]["received"]),
                             font=self.font).grid(row=2, column=1, sticky="nsew")
                ctk.CTkLabel(garbage_frame, text=str(rounds_values[round_].garbages[player]["maxspike"]),
                             font=self.font).grid(row=2, column=2, sticky="nsew")

        ctk.CTkButton(new_info, text="Back", font=smaller_font, command=self.grid_forget).grid(row=0, column=1,
                                                                                               sticky="nsew", padx=10,
                                                                                               pady=(15, 450))


class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#242424")

        self.master1 = master
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=5, uniform="a")
        self.rowconfigure((2, 3, 4, 5), weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

        self.enable_all_rounds_button = ctk.CTkButton(self, text="Enable All Rounds", height=40,
                                                      command=master.enable_all_rounds)
        self.enable_all_rounds_button.grid(row=2, column=0, sticky="ew", padx=10)

        self.disable_all_rounds_button = ctk.CTkButton(self, text="Disable All Rounds", height=40,
                                                       command=master.disable_all_rounds)
        self.disable_all_rounds_button.grid(row=3, column=0, sticky="ew", padx=10)

        self.average_rounds_button = ctk.CTkButton(self, text="Average Stats From Selected Rounds", height=40,
                                                   command=self.build_average_stats)
        self.average_rounds_button.grid(row=4, column=0, sticky="ew", padx=10)

        self.load_new_file_button = ctk.CTkButton(self, text="Load New Replay (File)", height=40,
                                                  command=master.load_file)
        self.load_new_file_button.grid(row=5, column=0, sticky="ew", padx=10)

        # TODO:
        # ASK OSK ABOUT REPLAY DOWNLOADING

        # link_string = StringVar()
        #
        # self.load_new_file_link_button = ctk.CTkButton(self, text="Load New Replay (Link)", height=40,
        #                                                command=lambda: master.load_file(True, link_string.get()))
        # self.load_new_file_link_button.grid(row=6, column=0, sticky="ew", padx=10)
        #
        # self.load_new_file_link_entry = ctk.CTkEntry(self, height=40, textvariable=link_string)
        # self.load_new_file_link_entry.grid(row=7, column=0, sticky="ew", padx=10)

        self.grid(row=0, rowspan=2, column=1, sticky="nsew")

    def build_average_stats(self):
        average_stats = self.master1.average_stats_button()

        average = ctk.CTkFrame(self)
        average.grid(row=1, column=0, sticky="nsew")

        average.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")
        average.columnconfigure((0, 1), weight=1, uniform="a")

        ctk.CTkLabel(self, text="Average Stats (~0.02% Error):", fg_color="#333333", corner_radius=10).grid(row=0,
                                                                                                            column=0,
                                                                                                            columnspan=2,
                                                                                                            sticky="nsew",
                                                                                                            padx=15,
                                                                                                            pady=15)

        # player one
        # top left to bottom right:
        # apm, pps, vs, app
        ctk.CTkLabel(average, text=str(average_stats[0][0]) + " APM", fg_color="#256cca", corner_radius=10).grid(row=0,
                                                                                                                 column=0,
                                                                                                                 sticky="nsew",
                                                                                                                 padx=5,
                                                                                                                 pady=5)
        ctk.CTkLabel(average, text=str(average_stats[0][1]) + " PPS", fg_color="#256cca", corner_radius=10).grid(row=0,
                                                                                                                 column=1,
                                                                                                                 sticky="nsew",
                                                                                                                 padx=5,
                                                                                                                 pady=5)
        ctk.CTkLabel(average, text=str(average_stats[0][2]) + " VS", fg_color="#256cca", corner_radius=10).grid(row=1,
                                                                                                                column=0,
                                                                                                                sticky="nsew",
                                                                                                                padx=5,
                                                                                                                pady=5)
        ctk.CTkLabel(average, text=str(average_stats[0][3]) + " APP", fg_color="#256cca", corner_radius=10).grid(row=1,
                                                                                                                 column=1,
                                                                                                                 sticky="nsew",
                                                                                                                 padx=5,
                                                                                                                 pady=5)

        # player two
        ctk.CTkLabel(average, text=str(average_stats[1][0]) + " APM", fg_color="#cb2525", corner_radius=10).grid(row=2,
                                                                                                                 column=0,
                                                                                                                 sticky="nsew",
                                                                                                                 padx=5,
                                                                                                                 pady=5)
        ctk.CTkLabel(average, text=str(average_stats[1][1]) + " PPS", fg_color="#cb2525", corner_radius=10).grid(row=2,
                                                                                                                 column=1,
                                                                                                                 sticky="nsew",
                                                                                                                 padx=5,
                                                                                                                 pady=5)
        ctk.CTkLabel(average, text=str(average_stats[1][2]) + " VS", fg_color="#cb2525", corner_radius=10).grid(row=3,
                                                                                                                column=0,
                                                                                                                sticky="nsew",
                                                                                                                padx=5,
                                                                                                                pady=5)
        ctk.CTkLabel(average, text=str(average_stats[1][3]) + " APP", fg_color="#cb2525", corner_radius=10).grid(row=3,
                                                                                                                 column=1,
                                                                                                                 sticky="nsew",
                                                                                                                 padx=5,
                                                                                                                 pady=5)


class RoundSection(ctk.CTkFrame):
    def __init__(self, master, apm, pps, vs, app, color):
        super().__init__(master, fg_color="transparent")

        font = CTkFont(family="Calibiri", size=12, weight="bold")

        # init variables
        self.apm = StringVar(value=str(round(apm, 2)) + " APM")
        self.pps = StringVar(value=str(round(pps, 2)) + " PPS")
        self.vs = StringVar(value=str(round(vs, 2)) + " VS")
        self.app = StringVar(value=str(round(app, 2)) + " APP")
        self.color = color

        # setup
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")

        # creation of labels
        self.apm_label = CTkLabel(self, textvariable=self.apm, font=font, corner_radius=10, fg_color=self.color,
                                  height=40)
        self.pps_label = CTkLabel(self, textvariable=self.pps, font=font, corner_radius=10, fg_color=self.color,
                                  height=40)
        self.vs_label = CTkLabel(self, textvariable=self.vs, font=font, corner_radius=10, fg_color=self.color,
                                 height=40)
        self.app_label = CTkLabel(self, textvariable=self.app, font=font, corner_radius=10, fg_color=self.color,
                                  height=40)

        # place labels
        self.apm_label.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")
        self.pps_label.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")
        self.vs_label.grid(row=0, column=2, padx=3, pady=3, sticky="nsew")
        self.app_label.grid(row=0, column=3, padx=3, pady=3, sticky="nsew")


program = Program()
program.mainloop()
