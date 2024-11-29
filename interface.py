import math
import webbrowser
from tokenize import Double

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)

import calculator

from tkinter import StringVar, BooleanVar, IntVar, DoubleVar

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkScrollableFrame

from calculator import get_pps_values


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

        # extra
        self.font = CTkFont(family="Calibiri", size=12, weight="bold")

        if calculator.get_gamemode() == "40l":

            self.rowconfigure(0, weight=1, uniform="a")
            self.columnconfigure(0, weight=1, uniform="a")

            self.main_frame = ctk.CTkScrollableFrame(self, fg_color="#242424")
            self.main_frame.rowconfigure(0, weight=1, uniform="a")
            self.main_frame.columnconfigure(0, weight=1, uniform="a")
            self.main_frame.grid(row=0, column=0, sticky="nsew")

            self.create_40l_mode()

        elif calculator.get_gamemode() is None or calculator.get_gamemode() == "league":  # vs sometimes is null for some reason

            # variables
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

            self.create_vs_mode()

    def load_file(self, type):
        calculator.load_file(type)
        self.create_vs_mode()

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

    def create_40l_mode(self):
        self.create_40l_mode_information()
        self.create_40l_mode_timer()

    def create_40l_mode_timer(self):
        fl_values = calculator.get_round_information()

        font = ctk.CTkFont(family="Calibri", size=48, weight="bold")
        big_font = ctk.CTkFont(family="Calibri", size=120, weight="bold")
        tiny_font = ctk.CTkFont(family="Calibri", size=16, weight="bold")

        # full container
        full_time_frame = ctk.CTkFrame(self.main_frame, fg_color="#2b2b2b")

        full_time_frame.rowconfigure(0, weight=1, uniform="a")
        full_time_frame.rowconfigure(1, weight=4, uniform="a")
        full_time_frame.columnconfigure(0, weight=1, uniform="a")

        full_time_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # "Final Time" text
        ctk.CTkLabel(full_time_frame, text="Final Time", font=font).grid(row=0, column=0, sticky="nsw", padx=25)

        # inset frame
        inset_time_frame = ctk.CTkFrame(full_time_frame, fg_color="#4b4b4b")

        inset_time_frame.rowconfigure((0, 2), weight=1, uniform="a")
        inset_time_frame.rowconfigure(1, weight=2, uniform="a")
        inset_time_frame.columnconfigure(0, weight=1, uniform="a")

        inset_time_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=(15, 25))

        # date played
        date = fl_values.date_played
        year = date[0]
        month = date[1]
        day = date[2]

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # date and timeplayed
        ctk.CTkLabel(inset_time_frame,
                     text="Played " + str(months[int(month) - 1]) + " " + str(day) + ", " + str(year) + "\n@ " +
                          str(fl_values.time_played[0]) + ":" +
                          str(fl_values.time_played[1]) + ":" +
                          str(fl_values.time_played[2]),
                     font=tiny_font).grid(row=0, column=0, sticky="nw", padx=10, pady=5)
        #ctk.CTkLabel(inset_time_frame, text="test").grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        # time value
        time = fl_values.finaltime

        # so time doesnt end up like "1:0" when it's meant to be "1:00"
        minutes = math.floor(time / 60)
        seconds = time % 60

        # adds zeros to complete the three decimals (turns 13.34 into 13.340)
        possible_zeros = "0" * (3 - len(str(seconds)[3:]))

        # actual time
        formatted_time = f"{minutes}:{seconds}{possible_zeros}"

        # time text
        ctk.CTkLabel(inset_time_frame, text=formatted_time, font=big_font).grid(row=1, column=0, sticky="nsew")

        def on_enter(e):
            replay_button.configure(text_color="#2b2b2b")

        def on_exit(e):
            replay_button.configure(text_color="#dce4ee")

        def send_to_replay():
            webbrowser.open(f"https://tetr.io/#R:{fl_values.replay_id}")

        # replay text
        replay_button = ctk.CTkButton(inset_time_frame, text="Replay ID: " + str(fl_values.replay_id), font=tiny_font,
                                      fg_color="#4b4b4b", hover_color="#4b4b4b", command=send_to_replay)
        replay_button.grid(row=2, column=0, sticky="sw", padx=10, pady=5)

        replay_button.bind("<Enter>", on_enter)
        replay_button.bind("<Leave>", on_exit)

    def create_40l_mode_information(self):
        font = ctk.CTkFont(family="Calibri", size=36, weight="bold")

        full_information_frame = ctk.CTkFrame(self.main_frame, fg_color="#2b2b2b")

        full_information_frame.rowconfigure(0, weight=1, uniform="a")
        full_information_frame.columnconfigure(0, weight=1, uniform="a")

        full_information_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        # stats text
        ctk.CTkLabel(full_information_frame, text="Stats", font=font).grid(row=0, column=0, sticky="nsw", padx=25)

        button_changer_frame = ctk.CTkFrame(full_information_frame, fg_color="#4b4b4b", corner_radius=0)

        button_changer_frame.rowconfigure(0, weight=1, uniform="a")
        button_changer_frame.columnconfigure((0, 1, 2), weight=1, uniform="a")

        button_changer_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=10)

        overview_frame = ctk.CTkFrame(full_information_frame, fg_color="#4b4b4b", corner_radius=0)
        clears_frame = ctk.CTkFrame(full_information_frame, fg_color="#4b4b4b", corner_radius=0)
        pace_frame = ctk.CTkFrame(full_information_frame, fg_color="#4b4b4b", corner_radius=0)

        overview_button = ctk.CTkButton(button_changer_frame, text="Overview", fg_color="#6b6b6b",
                                        hover_color="#8b8b8b", height=50,
                                        command=lambda: self.create_overview(overview_frame, clears_frame, pace_frame))
        overview_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        full_button = ctk.CTkButton(button_changer_frame, text="Clears", fg_color="#6b6b6b", hover_color="#8b8b8b",
                                    height=50,
                                    command=lambda: self.create_clears(overview_frame, clears_frame, pace_frame))
        full_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        pace_button = ctk.CTkButton(button_changer_frame, text="Pace", fg_color="#6b6b6b", hover_color="#8b8b8b",
                                    height=50,
                                    command=lambda: self.create_pace(overview_frame, clears_frame, pace_frame))
        pace_button.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.create_overview(overview_frame, clears_frame, pace_frame)

    def create_pace(self, overview_frame, clear_frame, pace_frame):

        font = ctk.CTkFont(family="Calibri", size=36, weight="bold")

        fl_values = calculator.get_round_information()

        overview_frame.grid_forget()
        clear_frame.grid_forget()
        pace_frame.grid_forget()

        pace_frame.grid(row=2, column=0, sticky="ew", padx=25, pady=10)

        pace_frame.rowconfigure(0, weight=1, uniform="a")
        pace_frame.rowconfigure(1, weight=5, uniform="a")
        pace_frame.columnconfigure(0, weight=1, uniform="a")

        pace_frame_info = ctk.CTkFrame(pace_frame, fg_color="#6b6b6b")

        pace_frame_info.rowconfigure((0, 1), weight=1, uniform="a")
        pace_frame_info.columnconfigure((0, 1, 2), weight=1, uniform="a")

        pace_frame_info.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(pace_frame_info, text="Time Chosen", font=font).grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(pace_frame_info, text="Predicted Pace", font=font).grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(pace_frame_info, text="PPS @ Time", font=font).grid(row=0, column=2, sticky="nsew")

        time_chosen = StringVar(value="0.0 Seconds")
        predicted_pace = StringVar(value="0.0 Seconds")
        pps_at_time = StringVar(value="0.0 PPS")

        ctk.CTkLabel(pace_frame_info, textvariable=time_chosen, font=font).grid(row=1, column=0, sticky="nsew")
        ctk.CTkLabel(pace_frame_info, textvariable=predicted_pace, font=font).grid(row=1, column=1, sticky="nsew")
        ctk.CTkLabel(pace_frame_info, textvariable=pps_at_time, font=font).grid(row=1, column=2, sticky="nsew")

        # PLOTTING ------------------------
        # configuring the font that doenst even work lol
        plt.rcParams["font.size"] = 24
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = "Calibri"

        # the figure that will contain the plot
        fig, ax = plt.subplots(facecolor="#6b6b6b")

        # plot points
        x = calculator.get_pps_values()[1]
        y = calculator.get_pps_values()[0]

        # x label
        plt.xlabel("Time (Seconds)")
        # y label
        plt.ylabel("PPS")
        # title
        plt.title("Click on Graph to Find Pace for that PPS")

        # turn on the grid
        ax.grid(which='major', color='#DDDDDD', linewidth=0.8)
        ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)

        # enable the tiny ticks
        plt.minorticks_on()

        # enable the tiny ticks pt 2
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.tick_params(axis='both', which='minor', labelsize=8)

        # how often the ticks appear
        tick_frequency = 1

        # make the ticks appear more often
        plt.xticks(np.arange(min(x), max(x) + 1, tick_frequency))
        plt.yticks(np.arange(min(y), max(y) + 1, tick_frequency))

        # create canvas
        canvas = FigureCanvasTkAgg(fig, master=pace_frame)

        # Plot data on Matplotlib Figure
        ax.plot(x, y, c="black")

        # lim called here because of autoplotting
        plt.xlim((0, math.ceil(max(x))))
        plt.ylim((0, 10))

        # draw the plot
        canvas.draw()

        # gridding
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        def calc_pace(e):
            temp = []
            if e.xdata is not None:
                for i in range(len(x)):
                    if x[i] < e.xdata:
                        temp.append(x[i])
                time = temp[-1]

                info = calculator.calculate_pace(0, time * 60)
                time_chosen.set(str(round(info[0], 2)) + " Seconds")
                predicted_pace.set(str(round(info[1], 2)) + " Seconds")
                pps_at_time.set(str(round(info[2], 2)) + " PPS")

        # getting the x position of your cursor to determine where the pace should start
        fig.canvas.callbacks.connect('button_press_event', calc_pace)

    def create_overview(self, overview_frame, clear_frame, pace_frame):

        font = ctk.CTkFont(family="Calibri", size=36, weight="bold")

        fl_values = calculator.get_round_information()

        overview_frame.grid_forget()
        clear_frame.grid_forget()
        pace_frame.grid_forget()

        overview_frame.grid(row=2, column=0, sticky="ew", padx=25, pady=10)

        stats_name = [
            "Played By",
            "Pieces Per Second",
            "Pieces Placed",
            "Total Inputs",
            "Total Holds",
            "Finesse Faults",
            "Finesse Perfects"
        ]

        stats = [
            fl_values.username,
            fl_values.pps,
            fl_values.piecesplaced,
            fl_values.inputs,
            fl_values.holds,
            fl_values.finessefaults,
            fl_values.finesseperfects
        ]

        rows = [0, 1, 2, 3, 4, 5, 6]

        overview_frame.rowconfigure(0, weight=1, uniform="a")
        overview_frame.columnconfigure((0, 1), weight=1, uniform="a")
        val = ctk.IntVar(value=1)
        for i in range(len(rows)):
            ctk.CTkLabel(overview_frame, text=str(stats_name[i]), font=font).grid(row=i, column=0, sticky="nsw",
                                                                                  padx=15)
            if i != len(rows) - 1:
                ctk.CTkLabel(overview_frame, text=str(stats[i]), font=font).grid(row=i, column=1, sticky="nse",
                                                                                 padx=15)

                ctk.CTkProgressBar(overview_frame, progress_color="#dce4ee", variable=val, corner_radius=50,
                                   height=5).grid(row=i, column=0, columnspan=2, sticky="ew", padx=15,
                                                  pady=(100, 0))
            else:
                ctk.CTkLabel(overview_frame, text=str(stats[i]), font=font).grid(row=i, column=1, sticky="nse",
                                                                                 padx=15, pady=(35, 35))

    def create_clears(self, overview_frame, clears_frame, pace_frame):

        font = ctk.CTkFont(family="Calibri", size=36, weight="bold")

        fl_values = calculator.get_round_information()

        overview_frame.grid_forget()
        clears_frame.grid_forget()
        pace_frame.grid_forget()

        clears_frame.grid(row=2, column=0, sticky="ew", padx=25, pady=10)

        clears_name = [
            "Singles",
            "Doubles",
            "Triples",
            "Quads",
            "Mini T-Spins",
            "Mini T-Spin Singles",
            "T-Spin Singles",
            "Mini T-Spin Doubles",
            "T-Spins Doubles",
            "Mini T-Spin Triples",
            "T-Spin Triples",
            "All Clears",
        ]

        clears = [
            fl_values.clears["singles"],
            fl_values.clears["doubles"],
            fl_values.clears["triples"],
            fl_values.clears["quads"],
            fl_values.clears["minitspins"],
            fl_values.clears["minitspinsingles"],
            fl_values.clears["tspinsingles"],
            fl_values.clears["minitspindoubles"],
            fl_values.clears["tspindoubles"],
            fl_values.clears["minitspintriples"],
            fl_values.clears["tspintriples"],
            fl_values.clears["allclear"]
        ]

        rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        clears_frame.rowconfigure(0, weight=1, uniform="a")
        clears_frame.columnconfigure((0, 1), weight=1, uniform="a")
        val = ctk.IntVar(value=1)
        for i in range(len(rows)):
            ctk.CTkLabel(clears_frame, text=str(clears_name[i]), font=font).grid(row=i, column=0, sticky="nsw",
                                                                                 padx=15)
            if i != len(rows) - 1:
                ctk.CTkLabel(clears_frame, text=str(clears[i]), font=font).grid(row=i, column=1, sticky="nse",
                                                                                padx=15)

                ctk.CTkProgressBar(clears_frame, progress_color="#dce4ee", variable=val, corner_radius=50,
                                   height=5).grid(row=i, column=0, columnspan=2, sticky="ew", padx=15,
                                                  pady=(100, 0))
            else:
                ctk.CTkLabel(clears_frame, text=str(clears[i]), font=font).grid(row=i, column=1, sticky="nse",
                                                                                padx=15, pady=(35, 35))

    def create_vs_mode(self):

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
        self.rowconfigure((2, 3, 4), weight=1, uniform="a")
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

        self.load_new_file_button = ctk.CTkButton(self, text="Load New !!VS!! Replay (File)", height=40,
                                                  command=lambda: master.load_file("vs"))
        #self.load_new_file_button.grid(row=5, column=0, sticky="ew", padx=10)

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
