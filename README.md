# TetrioReplayCalculator
Allows you to calculate certain things on a VS & 40 Line replay (.ttrm, .ttr) from tetrio.

## Automatically calculates: 

# VS:
- [x] APP
- [x] Player's Handling
- [x] Total / Per Round Lines Sent
- [x] Total / Per Round Lines Received
- [x] Total / Per Round Max Spike
- [x] Per Round Singles, Doubles, Triples, Quads, T-Spin Singles, T-Spin Doubles, T-Spin Triples, and Perfect Clears
- [x] Per Round Pieces Placed

You can also calculate average APM, PPS, VS, and APP for your choice of rounds.

# 40L:
- [x] Time, Date / Time Played, Replay ID
- [x] Played by, PPS, Pieces Placed, Total Inputs, Total Holds, Finesse Faults, Finesse Perfects
- [x] Clears (Singles, Doubles, Triples, Quads, Mini T-Spins, Mini T-Spin Singles, T-Spin Singles, Mini T-Spin Doubles, T-Spin Doubles, Mini T-Spin Triples, T-Spin Triples, All Clears

# Examples:
![Screenshot of the main page of the calculator, where the average stats for each round and the game as a whole are totaled.](/assets/zach_vs_agar_rounds.PNG)
![Screenshot of the handling and the extra information from the replay.](/assets/zach_vs_agar_handling_extrainfo.PNG)
![Screenshot of the extra info on the rounds, where many things are calculated.](/assets/zach_vs_agar_more_info_rounds.PNG)
![Screenshot of the 40L replay mode.](/assets/zach_sprint_overview.PNG)
![Screenshot of the pace calculator.](/assets/zach_pace_calculator.PNG)


If you have any ideas on anything else you want to be able to calculate in the program, message me on discord - @zachakaquack

# [HOW TO INSTALL AND USE TETRIO REPLAY CALCULATOR](https://www.youtube.com/watch?v=6544Zsfbkyo)
1. Go to [the releases page.](https://github.com/zachakaquack/TetrioReplayCalculator/releases)
2. Find the most recent release, then under **Assets**, click on **ReplayCalculator.exe** to download.
3. Upon loading the .exe, Windows may yell at you, but you can ignore it. The video linked [above](https://www.youtube.com/watch?v=6544Zsfbkyo) shows me downloading and opening this program, if you don't trust me.

## Extra
Works for replays after 11/26/24; Tetrio at some point changed their way of storing their replay files and it breaks this program. Sorry, I don't know when. If it breaks, it's _probably_ because of that.
Runs on py 3.12 w/ CustomTkinter and matplotlib.

dont bully me if anything goes wrong *but* message me on discord @zachakaquack if you want to report something

# Known Bugs
- Handling is sometimes reversed for each player in VS

# TODO:
- Blitz Mode
- Rework GUI to allow selecting replays dynamically again

<!--md docs https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax-->
