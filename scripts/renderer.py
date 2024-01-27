from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time 
import os
from datetime import datetime
from dateutil import parser, tz
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
        self.skip_count = {}  # Dictionary to keep track of skip counts for each game

        # Initialize and load fonts
        self.font = graphics.Font()
        self.font.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/6x12.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/4x6.bdf")
        self.font_medium = graphics.Font()
        self.font_medium.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/7x13.bdf")  
        self.font_small = graphics.Font()
        self.font_small.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/5x7.bdf") 
        self.team_colors = {
            'ATL': [[225, 68, 52], [196, 214, 0]],  # Atlanta Hawks
            'BOS': [[0, 122, 51], [139, 111, 78]],  # Boston Celtics
            'BKN': [[33, 33, 33], [119, 125, 132]],     # Brooklyn Nets
            'CHA': [[29, 17, 96], [0, 120, 140]],    # Charlotte Hornets
            'CHI': [[206, 17, 65], [33, 33, 33]],     # Chicago Bulls
            'CLE': [[134, 0, 56], [255, 184, 28]],   # Cleveland Cavaliers
            'DAL': [[0, 83, 188], [0, 43, 92]],      # Dallas Mavericks
            'DEN': [[13, 34, 64], [255, 198, 39]],   # Denver Nuggets
            'DET': [[200, 16, 46], [29, 66, 138]],   # Detroit Pistons
            'GSW': [[29, 66, 138], [255, 199, 44]],  # Golden State Warriors
            'HOU': [[206, 17, 65], [33, 33, 33]],     # Houston Rockets
            'IND': [[0, 45, 98], [253, 187, 48]],    # Indiana Pacers
            'LAC': [[200, 16, 46], [29, 66, 138]],   # Los Angeles Clippers
            'LAL': [[85, 37, 130], [253, 185, 39]],  # Los Angeles Lakers
            'MEM': [[93, 118, 169], [18, 23, 63]],   # Memphis Grizzlies
            'MIA': [[152, 0, 46], [249, 160, 27]],   # Miami Heat
            'MIL': [[0, 71, 27], [240, 235, 210]],   # Milwaukee Bucks
            'MIN': [[12, 35, 64], [35, 97, 146]],    # Minnesota Timberwolves
            'NOP': [[0, 22, 65], [225, 58, 62]],     # New Orleans Pelicans
            'NYK': [[0, 107, 182], [245, 132, 38]],  # New York Knicks
            'OKC': [[0, 125, 195], [239, 59, 36]],   # Oklahoma City Thunder
            'ORL': [[0, 125, 197], [196, 206, 211]], # Orlando Magic
            'PHI': [[0, 107, 182], [237, 23, 76]],   # Philadelphia 76ers
            'PHX': [[29, 17, 96], [229, 95, 32]],    # Phoenix Suns
            'POR': [[224, 58, 62], [186, 195, 201]], # Portland Trail Blazers
            'SAC': [[91, 43, 130], [99, 113, 122]],  # Sacramento Kings
            'SAS': [[33, 33, 33], [196, 206, 211]],   # San Antonio Spurs
            'TOR': [[206, 17, 65], [33, 33, 33]],     # Toronto Raptors
            'UTA': [[0, 43, 92], [0, 71, 27]],       # Utah Jazz
            'WAS': [[0, 43, 92], [227, 24, 55]],     # Washington Wizards
        }

    def Render_Games(self, printer=False):
        matrix = RGBMatrix(options=self.options)
        canvas = matrix.CreateFrameCanvas()
        board = scoreboard.ScoreBoard()
        print("ScoreBoardDate: " + board.score_board_date)
        games_data = board.games.get_dict()

        for game in games_data:
            game_id = game['gameId']
            if game['gameStatus'] != 2:  # If the game is not live
                self.skip_count[game_id] = self.skip_count.get(game_id, 0) + 1
                if self.skip_count[game_id] < 10:
                    continue
                else:
                    self.skip_count[game_id] = 0
            hometeam = game['homeTeam']['teamTricode']
            awayteam = game['awayTeam']['teamTricode']
            homescore = game['homeTeam']['score']
            awayscore = game['awayTeam']['score']
            game_status = game['gameStatus']
            
            print(hometeam + " vs " + awayteam + " " + str(game_id))

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

            # Example coordinates for displaying game status
            clock_x = 0
            clock_y = 30  

            if game_status == 2:
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
                # Render the quarter-by-quarter scores

                quarter_text = f"Q{game['period']}" if game['period'] <= 4 else "OT"
                game_clock_text = f"{minutes}:{seconds}"

                # Since each character in 4x6 font typically occupies 4 pixels in width
                char_width = 5

                # Render the quarter and game clock text with reduced space
                graphics.DrawText(canvas, self.font_small, clock_x, clock_y, graphics.Color(255, 255, 255), quarter_text)
                graphics.DrawText(canvas, self.font_small, clock_x + (len(quarter_text) * char_width), clock_y, graphics.Color(255, 255, 255), game_clock_text)

                # Render the quarter-by-quarter scores
                quarter_scores_start_x = clock_x + (len(quarter_text) * char_width) + 1 + (len(game_clock_text) * char_width) + 1
                quarter_width = 5  # Adjusted for 4x6 font

                for period in range(1, game['regulationPeriods'] + 1):
                    score_x = quarter_scores_start_x + (period - 1) * quarter_width
                    # Find and render the scores for each team in this quarter
                    away_score = next((p['score'] for p in game['awayTeam']['periods'] if p['period'] == period), 0)
                    home_score = next((p['score'] for p in game['homeTeam']['periods'] if p['period'] == period), 0)

                    graphics.DrawText(canvas, self.font2, score_x, 26, graphics.Color(0, 0, 255), str(away_score))
                    graphics.DrawText(canvas, self.font2, score_x, 32, graphics.Color(0, 0, 255), str(home_score))

            elif game_status == 3:  # Game has finished
                game_status_text = "Final"
                # Render the game status text
                graphics.DrawText(canvas, self.font_small, clock_x, clock_y, graphics.Color(255, 255, 255), game_status_text)

            elif game_status == 1:  # Game is scheduled for later
                # Calculate the time remaining until the game starts
                current_time = datetime.now(tz.tzlocal())
                game_time_utc = parser.parse(game['gameTimeUTC'])
                time_difference = game_time_utc - current_time
                hours, remainder = divmod(int(time_difference.total_seconds()), 3600)
                minutes, _ = divmod(remainder, 60)
                game_status_text = f"Starts in {hours}h {minutes}m" if time_difference.total_seconds() > 0 else "Starting Soon"
                # Render the game status text
                graphics.DrawText(canvas, self.font_small, clock_x, clock_y, graphics.Color(255, 255, 255), game_status_text)
            
            
  
            # Update the display
            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(6)  # Adjust the timing as needed
    
if __name__=='__main__':
    while True:
        Render().Render_Games()
