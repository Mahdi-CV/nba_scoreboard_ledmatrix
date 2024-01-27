from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import os
import json
import datetime as dt
import time
import sys
# from NBA_Standings import NBA_Standings
from dateutil import tz
###
from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from PIL import Image

class Render:
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.hardware_mapping = 'adafruit-hat'
        self.options.gpio_slowdown = 3
        self.options.rows = 32
        self.options.cols = 64
        self.options.drop_privileges = False

        # Initialize and load fonts
        self.font = graphics.Font()
        self.font.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/6x12.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/4x6.bdf")

        # Initialize and load medium font
        self.font_medium = graphics.Font()
        self.font_medium.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/7x13.bdf")  

        # Initialize and load small font
        self.font_small = graphics.Font()
        self.font_small.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/5x8.bdf") 
        
        self.path = './nba_scoreboard_ledmatrix'
        
        self.font = graphics.Font()
        self.font.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/6x12.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/4x6.bdf")
        self.team_colors = {'ATL': [[225, 58, 62], [100, 100, 100]], 'BOS': [[0, 131, 72], [187, 151, 83]], 'BKN': [[100, 100, 100], [100, 100, 100]], 'CHA': [[29, 17, 96], [0, 140, 168]], 'CHI': [[206, 17, 65], [206, 17, 65]], 'CLE': [[134, 0, 56], [253, 187, 48]], 'DAL': [[0, 125, 197], [196, 206, 211]], 'DEN': [[77, 144, 205], [253, 185, 39]], 'DET': [[237, 23, 76], [0, 107, 182]], 'GSW': [[253, 185, 39], [0, 107, 182]], 'HOU': [[206, 17, 65], [206, 17, 65]], 'LAL': [[253, 185, 39], [85, 37, 130]], 'MEM': [[15, 88, 108], [190, 212, 233]], 'MIA': [[152, 0, 46], [152, 0, 46]], 'MIL': [[0, 71, 27], [240, 235, 210]], 'MIN': [[0, 80, 131], [0, 169, 79]], 'NOP': [[0, 43, 92], [227, 24, 55]], 'NYK': [[0, 107, 182], [245, 132, 38]], 'OKC': [[0, 125, 195], [240, 81, 51]], 'ORL': [[0, 71, 27], [0, 71, 27]], 'PHI': [[237, 23, 76], [0, 107, 182]], 'PHX': [[229, 96, 32], [29, 17, 96]], 'POR': [[224, 58, 62], [186, 195, 201]], 'SAC': [[114, 76, 159], [142, 144, 144]], 'SAS': [[0, 71, 27], [0, 71, 27]], 'TOR': [[255, 0, 0], [255, 0, 0]], 'UTA': [[0, 43, 92], [249, 160, 27]], 'WAS': [[0, 43, 92], [227, 24, 55]], 'IND': [[255, 198, 51], [0, 39, 93]], 'LAC': [[237, 23, 76], [0, 107, 182]]}
            
    
    def Render_Games(self, printer=False):
        matrix = RGBMatrix(options=self.options)
        canvas = matrix.CreateFrameCanvas()

        # Load a larger font for team names
        self.font_large = graphics.Font()
        self.font_large.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/10x20.bdf")

        # Assuming 'games' is the JSON string you got from the NBA API
        board = scoreboard.ScoreBoard()
        print("ScoreBoardDate: " + board.score_board_date)
        games_data = board.games.get_dict()
        for game in games_data:
            hometeam = game['homeTeam']['teamTricode']
            awayteam = game['awayTeam']['teamTricode']
            homescore = game['homeTeam']['score']
            awayscore = game['awayTeam']['score']
            game_status = game['gameStatus']
            print(hometeam + " vs " + awayteam)

            # Clear the canvas
            canvas.Clear()

            logo_width, logo_height = 10, 10
            gap = 1  # Gap between away and home team sections
            # Away team logo and text
            away_logo_y = 0  # Y position for away team logo
            away_text_y = logo_height  # Y position for away team text

            # Home team logo and text
            home_logo_y = away_logo_y + logo_height + gap  # Y position for home team logo
            home_text_y = home_logo_y + logo_height  # Y position for home team text

            away_logo_path = f'./assets/logos_16x16/{awayteam}.png'
            home_logo_path = f'./assets/logos_16x16/{hometeam}.png'
            if os.path.exists(away_logo_path) and os.path.exists(home_logo_path):
                away_logo = Image.open(away_logo_path).convert('RGB').resize((logo_width, logo_height))
                home_logo = Image.open(home_logo_path).convert('RGB').resize((logo_width, logo_height))
                canvas.SetImage(away_logo, 0, away_logo_y)
                canvas.SetImage(home_logo, 0, home_logo_y)
            else:
                print(f"Logo not found for teams {awayteam} or {hometeam}")

            text_start_x = logo_width + 2  # Small gap after logo
            graphics.DrawText(canvas, self.font_medium, text_start_x, away_text_y, graphics.Color(self.team_colors[awayteam][1][0], self.team_colors[awayteam][1][1], self.team_colors[awayteam][1][2]), awayteam)
            graphics.DrawText(canvas, self.font_medium, text_start_x + (len(awayteam) * 8), away_text_y, graphics.Color(100, 100, 100), str(awayscore))

            # Display home team name and score
            graphics.DrawText(canvas, self.font_medium, text_start_x, home_text_y, graphics.Color(self.team_colors[hometeam][1][0], self.team_colors[hometeam][1][1], self.team_colors[hometeam][1][2]), hometeam)
            graphics.DrawText(canvas, self.font_medium, text_start_x + (len(hometeam) * 8), home_text_y, graphics.Color(100, 100, 100), str(homescore))

            game_status = game['gameStatus']
            game_status_text = game['gameStatusText']

            if game_status == 2:  # Game is live
                # Extract and format game clock (convert from ISO 8601 duration)
                game_clock = game['gameClock']
                if game_clock:  # Check if game clock is not empty
                    try:
                        minutes, seconds = game_clock.lstrip('PT').split('M')
                        seconds = seconds.rstrip('S').split('.')[0]  # Removing '.00S'
                        game_clock_text = f"{minutes}:{seconds}"
                    except ValueError:
                        # Handle cases where game clock format is unexpected
                        game_clock_text = "Live"
                else:
                    game_clock_text = "Live"

                quarter_text = f"Q{game['period']}" if game['period'] <= 4 else "OT"
                game_status_text = f"{quarter_text} {game_clock_text}"

            elif game_status == 3:  # Game has finished
                game_status_text = "Final"

            elif game_status == 1:  # Game is scheduled for later
                # Format and display the scheduled start time
                game_time_utc = game['gameTimeUTC']
                start_time = parser.parse(game_time_utc)
                local_time = start_time.astimezone(tz.tzlocal()).strftime("%H:%M")
                game_status_text = f"Starts {local_time}"

            # Example coordinates for displaying game status
            clock_x = 2
            clock_y = 28

            # Render the game status text
            graphics.DrawText(canvas, self.font_small, clock_x, clock_y, graphics.Color(255, 255, 255), game_status_text)

            # # Render the quarter-by-quarter scores
            # score_x = quarter_x  # Starting x position for scores
            # for period in range(1, game['regulationPeriods'] + 1):  # Loop through each quarter
            #     # Find the score for the away team in this quarter
            #     away_score = next((p['score'] for p in game['awayTeam']['periods'] if p['period'] == period), 0)
            #     # Find the score for the home team in this quarter
            #     home_score = next((p['score'] for p in game['homeTeam']['periods'] if p['period'] == period), 0)

            #     # Format and render the score for this quarter
            #     quarter_score_text = f"{away_score}-{home_score}"
            #     graphics.DrawText(canvas, self.font_small, score_x, ..., graphics.Color(255, 255, 255), quarter_score_text)
            #     score_x += ...  # Increment x position for the next quarter score



            # Update the display
            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(6)  # Adjust the timing as needed
    
if __name__=='__main__':
    while True:
        Render().Render_Games()
