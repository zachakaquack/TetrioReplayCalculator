import calculator

from tkinter import DoubleVar, StringVar, BooleanVar

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkFont


class Program(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        self.geometry("1280x720")
        self.bind("<Escape>", lambda x: self.quit())
        self.resizable(False, False)
        self.title("Zach's Replay Calculator")

        # extra
        self.font = CTkFont(family="Calibiri", size=12, weight="bold")
        self.enabled_rounds = []


        # outlines of the window
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=2, uniform="a")
        self.columnconfigure(0, weight=4, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")

        self.main_frame = CTkFrame(self, fg_color="#b2b2b2")
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.main_frame.rowconfigure(0, weight=1, uniform="a")

        self.main_frame.columnconfigure(0, weight=1, uniform="a")
        self.main_frame.columnconfigure(3, weight=1, uniform="a")
        self.main_frame.columnconfigure(6, weight=1, uniform="a")
        self.main_frame.columnconfigure((1, 2, 4, 5), weight=3, uniform="a")

        self.round_count_section = CTkFrame(self.main_frame)
        self.round_count_section.grid(row=0, column=0, sticky="nsew")

        self.left_rounds_section = CTkFrame(self.main_frame)
        self.left_rounds_section.grid(row=0, column=1, columnspan=2, sticky="nsew")

        self.round_timer_section = CTkFrame(self.main_frame)
        self.round_timer_section.grid(row=0, column=3, sticky="nsew")

        self.right_rounds_section = CTkFrame(self.main_frame)
        self.right_rounds_section.grid(row=0, column=4, columnspan=2, sticky="nsew")

        self.round_check_section = CTkFrame(self.main_frame)
        self.round_check_section.grid(row=0, column=6, sticky="nsew")

        # self.sidebar_frame = CTkFrame(self, fg_color="pink")
        # self.sidebar_frame.grid(row=0, column=1, sticky="nsew")

        self.sidebar = Sidebar(self)
        self.topbar = TopBar(self)


        self.create_all_rounds()

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

    def create_checkbox(self, value):
        ctk.CTkCheckBox(self.round_check_section, text="", variable=self.enabled_rounds[value]).grid(row=value, column=0, padx=20, sticky="nsew")


    def create_all_rounds(self):
        rounds = calculator.get_round_information()

        rows = []

        # generate amount of rows needed
        for i in range(len(rounds)):
            rows.append(i)
            self.enabled_rounds.append(BooleanVar(value=True))

        self.left_rounds_section.rowconfigure(rows, weight=1, uniform="a")
        self.right_rounds_section.rowconfigure(rows, weight=1, uniform="a")
        self.round_count_section.rowconfigure(rows, weight=1, uniform="a")
        self.round_timer_section.rowconfigure(rows, weight=1, uniform="a")
        self.round_check_section.rowconfigure(rows, weight=1, uniform="a")

        self.left_rounds_section.columnconfigure(0, weight=1, uniform="a")
        self.right_rounds_section.columnconfigure(0, weight=1, uniform="a")
        self.round_count_section.columnconfigure(0, weight=1, uniform="a")
        self.round_timer_section.columnconfigure(0, weight=1, uniform="a")
        self.round_check_section.columnconfigure(0, weight=1, uniform="a")


        for i in range(len(rounds)):
            RoundSection(self.left_rounds_section,
                         rounds[i].apms[0],
                         rounds[i].ppss[0],
                         rounds[i].vss[0],
                         rounds[i].apps[0], "#256cca").grid(row=i, column=0, sticky="nsew")

            RoundSection(self.right_rounds_section,
                         rounds[i].apms[1],
                         rounds[i].ppss[1],
                         rounds[i].vss[1],
                         rounds[i].apps[1], "#cb2525").grid(row=i, column=0, sticky="nsew")

            ctk.CTkLabel(self.round_count_section, text="Round " + str(rounds[i].round_number), font=self.font).grid(row=i, column=0, sticky="nsew")

            ctk.CTkLabel(self.round_timer_section, text=str(rounds[i].round_length) + "s", font=self.font).grid(row=i, column=0, sticky="nsew")

            self.create_checkbox(i)


class TopBar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color = "#b2b2b2")

        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.columnconfigure((0, 1), weight=1, uniform="a")

        self.grid(row=0, column=0, sticky="nsew")

        averages = calculator.get_player_data()
        player_one = averages[0]
        player_two = averages[1]
        print(averages)

        font=CTkFont(family="Calibiri", weight="bold", size=48)

        CTkLabel(self, text=player_one.username, font=font).grid(row=0, column=0, sticky="nsew", pady=20)
        CTkLabel(self, text=player_two.username, font=font).grid(row=0, column=1, sticky="nsew", pady=20)

        RoundSection(self, player_one.apm, player_one.pps, player_one.vs, player_one.app, "#256cca").grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        RoundSection(self, player_two.apm, player_two.pps, player_two.vs, player_two.app, "#cb2525").grid(row=1, column=1, sticky="nsew", padx=20, pady=10)


class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master1 = master

        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=5, uniform="a")
        self.rowconfigure((2, 3, 4), weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

        self.average_rounds_button = ctk.CTkButton(self, text="Average Stats From Selected Rounds", height=40,
                                                   command=self.build_average_stats)
        self.average_rounds_button.grid(row=4, column=0, sticky="ew", padx=10)


        self.enable_all_rounds_button = ctk.CTkButton(self, text="Enable All Rounds", height=40,
                                                      command=master.enable_all_rounds)
        self.enable_all_rounds_button.grid(row=2, column=0, sticky="ew", padx=10)


        self.disable_all_rounds_button = ctk.CTkButton(self, text="Disable All Rounds", height=40,
                                                      command=master.disable_all_rounds)
        self.disable_all_rounds_button.grid(row=3, column=0, sticky="ew", padx=10)



        self.grid(row=0, rowspan=2, column=1, sticky="nsew")

    def build_average_stats(self):

        average_stats = self.master1.average_stats_button()


        average = ctk.CTkFrame(self)
        average.grid(row=1, column=0, sticky="nsew")


        average.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")
        average.columnconfigure((0, 1), weight=1, uniform="a")

        ctk.CTkLabel(self, text="Average Stats (Not 1000% Accurate):", fg_color="#333333", corner_radius=10).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=15)

        # player one
        # top left to bottom right:
        # apm, pps, vs, app
        ctk.CTkLabel(average, text=str(average_stats[0][0]) + " APM", fg_color="#256cca", corner_radius=10).grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(average, text=str(average_stats[0][1]) + " PPS", fg_color="#256cca", corner_radius=10).grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(average, text=str(average_stats[0][2]) + " VS", fg_color="#256cca", corner_radius=10).grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(average, text=str(average_stats[0][3]) + " APP", fg_color="#256cca", corner_radius=10).grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # player two
        ctk.CTkLabel(average, text=str(average_stats[1][0]) + " APM", fg_color="#cb2525", corner_radius=10).grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(average, text=str(average_stats[1][1]) + " PPS", fg_color="#cb2525", corner_radius=10).grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(average, text=str(average_stats[1][2]) + " VS", fg_color="#cb2525", corner_radius=10).grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(average, text=str(average_stats[1][3]) + " APP", fg_color="#cb2525", corner_radius=10).grid(row=3, column=1, sticky="nsew", padx=5, pady=5)




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
        self.apm_label = CTkLabel(self, textvariable=self.apm, font=font, corner_radius=10, fg_color=self.color)
        self.pps_label = CTkLabel(self, textvariable=self.pps, font=font, corner_radius=10, fg_color=self.color)
        self.vs_label = CTkLabel(self, textvariable=self.vs, font=font, corner_radius=10, fg_color=self.color)
        self.app_label = CTkLabel(self, textvariable=self.app, font=font, corner_radius=10, fg_color=self.color)

        # place labels
        self.apm_label.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")
        self.pps_label.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")
        self.vs_label.grid(row=0, column=2, padx=3, pady=3, sticky="nsew")
        self.app_label.grid(row=0, column=3, padx=3, pady=3, sticky="nsew")



program = Program()
program.mainloop()
