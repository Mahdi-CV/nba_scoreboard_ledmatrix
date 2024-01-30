from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from data_manager import DataManager
#from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions
import time 
import os
from datetime import datetime
from dateutil import parser, tz
from nba_api.live.nba.endpoints import scoreboard
from PIL import Image



# class Render:
#     def __init__(self):
#         self.options = RGBMatrixOptions()
#         self.options.hardware_mapping = 'adafruit-hat'
#         self.options.gpio_slowdown = 3
#         self.options.rows = 32
#         self.options.cols = 64
#         self.options.drop_privileges = False
#         self.skip_count = {}  # Dictionary to keep track of skip counts for each game

#         # Initialize and load fonts
#         self.font = graphics.Font()
#         self.font.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/6x12.bdf")
#         self.font2 = graphics.Font()
#         self.font2.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/4x6.bdf")
#         self.font_medium = graphics.Font()
#         self.font_medium.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/7x13.bdf")  
#         self.font_small = graphics.Font()
#         self.font_small.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/5x7.bdf") 
#         self.team_colors = {
#             'ATL': [[225, 68, 52], [196, 214, 0]],  # Atlanta Hawks
#             'BOS': [[0, 122, 51], [139, 111, 78]],  # Boston Celtics
#             'BKN': [[33, 33, 33], [119, 125, 132]],     # Brooklyn Nets
#             'CHA': [[29, 17, 96], [0, 120, 140]],    # Charlotte Hornets
#             'CHI': [[206, 17, 65], [33, 33, 33]],     # Chicago Bulls
#             'CLE': [[134, 0, 56], [255, 184, 28]],   # Cleveland Cavaliers
#             'DAL': [[0, 83, 188], [0, 43, 92]],      # Dallas Mavericks
#             'DEN': [[13, 34, 64], [255, 198, 39]],   # Denver Nuggets
#             'DET': [[200, 16, 46], [29, 66, 138]],   # Detroit Pistons
#             'GSW': [[29, 66, 138], [255, 199, 44]],  # Golden State Warriors
#             'HOU': [[206, 17, 65], [33, 33, 33]],     # Houston Rockets
#             'IND': [[0, 45, 98], [253, 187, 48]],    # Indiana Pacers
#             'LAC': [[200, 16, 46], [29, 66, 138]],   # Los Angeles Clippers
#             'LAL': [[85, 37, 130], [253, 185, 39]],  # Los Angeles Lakers
#             'MEM': [[93, 118, 169], [18, 23, 63]],   # Memphis Grizzlies
#             'MIA': [[152, 0, 46], [249, 160, 27]],   # Miami Heat
#             'MIL': [[0, 71, 27], [240, 235, 210]],   # Milwaukee Bucks
#             'MIN': [[12, 35, 64], [35, 97, 146]],    # Minnesota Timberwolves
#             'NOP': [[0, 22, 65], [225, 58, 62]],     # New Orleans Pelicans
#             'NYK': [[0, 107, 182], [245, 132, 38]],  # New York Knicks
#             'OKC': [[0, 125, 195], [239, 59, 36]],   # Oklahoma City Thunder
#             'ORL': [[0, 125, 197], [196, 206, 211]], # Orlando Magic
#             'PHI': [[0, 107, 182], [237, 23, 76]],   # Philadelphia 76ers
#             'PHX': [[29, 17, 96], [229, 95, 32]],    # Phoenix Suns
#             'POR': [[224, 58, 62], [186, 195, 201]], # Portland Trail Blazers
#             'SAC': [[91, 43, 130], [99, 113, 122]],  # Sacramento Kings
#             'SAS': [[33, 33, 33], [196, 206, 211]],   # San Antonio Spurs
#             'TOR': [[206, 17, 65], [33, 33, 33]],     # Toronto Raptors
#             'UTA': [[0, 43, 92], [0, 71, 27]],       # Utah Jazz
#             'WAS': [[0, 43, 92], [227, 24, 55]],     # Washington Wizards
#         }

#     def Render_Games(self, games_data, printer=False):
#         matrix = RGBMatrix(options=self.options)
#         canvas = matrix.CreateFrameCanvas()


#         scroll_position = 0  # Position for scrolling text
#         scroll_step = 1      # Amount to scroll each frame
#         scroll_interval = 0.1  # Time between scroll steps in seconds


#         for game in games_data:
#             game_id = game['gameId']
#             if game['gameStatus'] != 2:  # If the game is not live
#                 self.skip_count[game_id] = self.skip_count.get(game_id, 0) + 1
#             hometeam = game['homeTeam']['teamTricode']
#             awayteam = game['awayTeam']['teamTricode']
#             homescore = game['homeTeam']['score']
#             awayscore = game['awayTeam']['score']
#             game_status = game['gameStatus']
            
#             print(hometeam + " vs " + awayteam + " " + str(game_id))

#             # Clear the canvas
#             #canvas.Clear()

#             logo_width, logo_height = 10, 10
#             gap = 1  # Gap between away and home team sections
#             # Away team logo and text
#             away_logo_y = 0  # Y position for away team logo
#             away_text_y = logo_height  # Y position for away team text

#             # Home team logo and text
#             home_logo_y = away_logo_y + logo_height + gap  # Y position for home team logo
#             home_text_y = home_logo_y + logo_height  # Y position for home team text

#             away_logo_path = f'./assets/logos_16x16/{awayteam}.png'
#             home_logo_path = f'./assets/logos_16x16/{hometeam}.png'
#             if os.path.exists(away_logo_path) and os.path.exists(home_logo_path):
#                 away_logo = Image.open(away_logo_path).convert('RGB').resize((logo_width, logo_height))
#                 home_logo = Image.open(home_logo_path).convert('RGB').resize((logo_width, logo_height))
#                 canvas.SetImage(away_logo, 0, away_logo_y)
#                 canvas.SetImage(home_logo, 0, home_logo_y)
#             else:
#                 print(f"Logo not found for teams {awayteam} or {hometeam}")



#             game_status = game['gameStatus']
#             game_status_text = game['gameStatusText']

#             # Example coordinates for displaying game status
#             clock_x = 5
#             clock_y = 30  

#             if game_status == 2:
#                 # Extract and format game clock (convert from ISO 8601 duration)
#                 game_clock = game['gameClock']
#                 # Initialize default values for minutes and seconds
#                 minutes = '00'
#                 seconds = '00'

#                 if game_clock:  # Check if game clock is not empty
#                     try:
#                         minutes, seconds = game_clock.lstrip('PT').split('M')
#                         seconds = seconds.rstrip('S').split('.')[0]  # Removing '.00S'
#                         game_clock_text = f"{minutes}:{seconds}"
#                     except ValueError:
#                         # Handle cases where game clock format is unexpected
#                         game_clock_text = "Live"
#                 else:
#                     game_clock_text = "Live"
#                 # Render the quarter-by-quarter scores

#                 quarter_text = f"Q{game['period']}" if game['period'] <= 4 else "OT"
#                 game_clock_text = f"{minutes}:{seconds}"

#                 # Since each character in 4x6 font typically occupies 4 pixels in width
#                 char_width = 5

#                 # Render the quarter and game clock text with reduced space
#                 graphics.DrawText(canvas, self.font_small, clock_x - scroll_position, clock_y, graphics.Color(100, 120, 100), quarter_text)
#                 graphics.DrawText(canvas, self.font_small, clock_x - scroll_position + (len(quarter_text) * char_width), clock_y, graphics.Color(255, 255, 255), game_clock_text)

#                 # Update scroll position
#                 scroll_position += scroll_step
#                 if scroll_position > matrix.width:  # Once scrolled off, reset position and show quarterly scores
#                     scroll_position = 0

#                 quarter_scores_start_x = clock_x + (len(quarter_text) * char_width) + (len(game_clock_text) * char_width) + 2
#                 quarter_width = 9  # Adjust this based on the available space and font size

#                 # for period in range(1, game['regulationPeriods'] + 1):
#                 #     score_x = quarter_scores_start_x + (period - 1) * quarter_width

#                 #     # Find and render the scores for each team in this quarter
#                 #     away_score = next((p['score'] for p in game['awayTeam']['periods'] if p['period'] == period), 0)
#                 #     home_score = next((p['score'] for p in game['homeTeam']['periods'] if p['period'] == period), 0)

#                 #     # Format and render scores with fixed width
#                 #     formatted_away_score = f"{away_score:2d}"  # Formats score with 2-digit width, right-aligned
#                 #     formatted_home_score = f"{home_score:2d}"

#                 #     graphics.DrawText(canvas, self.font2, score_x, 26, graphics.Color(100, 100, 255), formatted_away_score)
#                 #     graphics.DrawText(canvas, self.font2, score_x, 32, graphics.Color(100, 100, 255), formatted_home_score)

#             elif game_status == 3:  # Game has finished
#                 game_status_text = "Final"
#                 # Render the game status text
#                 graphics.DrawText(canvas, self.font_small, clock_x, clock_y, graphics.Color(255, 255, 255), game_status_text)

#             elif game_status == 1:  # Game is scheduled for later
#                 # Calculate the time remaining until the game starts
#                 current_time = datetime.now(tz.tzlocal())
#                 game_time_utc = parser.parse(game['gameTimeUTC'])
#                 time_difference = game_time_utc - current_time
#                 hours, remainder = divmod(int(time_difference.total_seconds()), 3600)
#                 minutes, _ = divmod(remainder, 60)
#                 game_status_text = f"Starts in {hours}h {minutes}m" if time_difference.total_seconds() > 0 else "Starting Soon"
#                 # Render the game status text
#                 graphics.DrawText(canvas, self.font_small, clock_x, clock_y, graphics.Color(255, 255, 255), game_status_text)
            
#             # Update the display
#             canvas = matrix.SwapOnVSync(canvas)
#             time.sleep(6)  # Adjust the timing as needed

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
        self.font_medium.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/6x13.bdf")
        self.font_medium_height = 9
        self.font_medium_width = 7
        self.font_small = graphics.Font()
        self.font_small.LoadFont("./submodules/rpi-rgb-led-matrix/fonts/5x7.bdf")
        self.font_small_height = 7
        self.font_small_width = 5
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

    def render_team_logos(self, canvas, awayteam, hometeam, logo_height, logo_width):
        gap = 1  # Gap between away and home team sections
        # Away team logo and text
        away_logo_y = 0  # Y position for away team logo
        away_text_y = logo_height  # Y position for away team text

        # Home team logo and text
        home_logo_y = away_logo_y + logo_height # Y position for home team logo
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

        return
    
    # def render_team_scores(self, canvas, awayteam, hometeam, awayscore, homescore, logo_height, logo_width):
    #     gap = 1  # Gap between away and home team sections
    #     # Away team logo and text
    #     away_logo_y = 0  # Y position for away team logo
    #     away_text_y = logo_height  # Y position for away team text

    #     # Home team logo and text
    #     home_logo_y = away_logo_y + logo_height + gap  # Y position for home team logo
    #     home_text_y = home_logo_y + logo_height  # Y position for home team text

    #     text_start_x = logo_width + 2  # Small gap after logo
    #     graphics.DrawText(canvas, self.font_medium, text_start_x, away_text_y, graphics.Color(self.team_colors[awayteam][1][0], self.team_colors[awayteam][1][1], self.team_colors[awayteam][1][2]), awayteam)
    #     graphics.DrawText(canvas, self.font_medium, text_start_x + (len(awayteam) * 8), away_text_y, graphics.Color(255, 255, 255), str(awayscore))

    #     # Display home team name and score
    #     graphics.DrawText(canvas, self.font_medium, text_start_x, home_text_y, graphics.Color(self.team_colors[hometeam][1][0], self.team_colors[hometeam][1][1], self.team_colors[hometeam][1][2]), hometeam)
    #     graphics.DrawText(canvas, self.font_medium, text_start_x + (len(hometeam) * 8), home_text_y, graphics.Color(255, 255, 255), str(homescore))

    #     return

    def render_team_names(self, canvas, awayteam, hometeam, logo_height, logo_width):
        gap = 6 # Gap between top of screen and text

        # Assuming logos are at the top of the screen, start text right below the logos
        away_name_y = self.font_medium_height + 2  # Y position for away team name
        home_name_y = away_name_y + logo_height   # Y position for home team name, below the away name

        text_start_x = logo_height + gap  # X position for text, assuming logos are square

        # Render team names
        graphics.DrawText(canvas, self.font_medium, text_start_x, away_name_y, graphics.Color(self.team_colors[awayteam][1][0], self.team_colors[awayteam][1][1], self.team_colors[awayteam][1][2]), awayteam)
        graphics.DrawText(canvas, self.font_medium, text_start_x, home_name_y, graphics.Color(self.team_colors[hometeam][1][0], self.team_colors[hometeam][1][1], self.team_colors[hometeam][1][2]), hometeam)
        
    def render_team_scores(self, canvas, awayteam, hometeam, awayscore, homescore, logo_height, logo_width):

        gap = 6  # Gap between text elements

        # Calculate Y positions based on logo height, slightly below the names
        away_score_y = self.font_medium_height + 2  # Y position for away team score
        home_score_y = away_score_y + logo_height # Y position for home team score

        # Calculate X positions for scores based on the length of team names
        away_score_x = logo_width + (len(awayteam) * self.font_medium_width) + gap
        home_score_x = logo_width + (len(hometeam) * self.font_medium_width) + gap

        # Render away team score
        graphics.DrawText(canvas, self.font_medium, away_score_x, away_score_y, graphics.Color(255, 255, 255), str(awayscore))
        # Render home team score
        graphics.DrawText(canvas, self.font_medium, home_score_x, home_score_y, graphics.Color(255, 255, 255), str(homescore))

    
    # def render_team_scores(self, canvas, awayteam, hometeam, awayscore, homescore, logo_height, logo_width):
    #     gap = 1  # Gap between away and home team sections
    #     char_width = 7  # Width per character for the medium font

    #     # Y positions for team names and scores based on logo height
    #     away_name_y = logo_height  # Y position for away team name
    #     home_name_y = away_name_y + logo_height + gap  # Y position for home team name

    #     # X positions for team names and scores
    #     text_start_x = logo_width + 2  # Start text right after logo

    #     # Calculate X position for scores based on team name length
    #     # Estimating the width of the team name based on character width
    #     away_score_x = text_start_x + len(awayteam) * char_width + gap
    #     home_score_x = text_start_x + len(hometeam) * char_width + gap

    #     # Render team names
    #     graphics.DrawText(canvas, self.font_medium, text_start_x, away_name_y, graphics.Color(self.team_colors[awayteam][1][0], self.team_colors[awayteam][1][1], self.team_colors[awayteam][1][2]), awayteam)
    #     graphics.DrawText(canvas, self.font_medium, text_start_x, home_name_y, graphics.Color(self.team_colors[hometeam][1][0], self.team_colors[hometeam][1][1], self.team_colors[hometeam][1][2]), hometeam)

    #     # Render scores next to team names
    #     graphics.DrawText(canvas, self.font_medium, away_score_x, away_name_y, graphics.Color(255, 255, 255), str(awayscore))
    #     graphics.DrawText(canvas, self.font_medium, home_score_x, home_name_y, graphics.Color(255, 255, 255), str(homescore))




    def render_win_probabilities(self, canvas, awayteam, hometeam, away_prob, home_prob, logo_height, logo_width):
        char_width = 6  # Use the widest character for width estimation
        char_height = 10
        gap = 1
        text_start_x = logo_width + (len(awayteam) * char_width) + gap
        away_text_y = char_height
        home_text_y = away_text_y + logo_height + gap   # considering gap

        # Format probabilities as percentages
        away_prob_text = f"{away_prob * 100:.0f}%"
        home_prob_text = f"{home_prob * 100:.0f}%"

        # Draw probabilities
        graphics.DrawText(canvas, self.font_medium, text_start_x, away_text_y, graphics.Color(255, 255, 255), away_prob_text)
        graphics.DrawText(canvas, self.font_medium, text_start_x, home_text_y, graphics.Color(255, 255, 255), home_prob_text)


    def render_quarterly_scores(self, canvas, game, logo_height, logo_width):
        # Example of how you might want to structure this method
        # You need to fetch the quarterly scores from the game data
        char_width_team_name = 6  # Use the widest character for width estimation
        char_height = 5
        gap = 1
        text_start_x = logo_width + (3 * char_width_team_name) + gap
        away_text_y = 0
        home_text_y = away_text_y + logo_height + 1  # considering gap

        # Assuming game['quarters'] contains the quarter scores
        for idx, quarter in enumerate(game['team_information']['away']['quarters']):
            away_score = game['team_information']['away']['quarters'][idx]
            home_score = game['team_information']['home']['quarters'][idx]
            quarter_text = f"Q{idx+1}: {away_score}-{home_score}"

        graphics.DrawText(canvas, self.font_small, text_start_x, away_text_y + idx * 8, graphics.Color(255, 255, 255), quarter_text)

    def render_game_status(self, canvas, game_status, game, logo_height, logo_width):
        # Adjust the vertical position
        gap = 1
        status_text_y = self.options.rows - gap  # Place it near the top but leaving some margin
        # Start from left side a bit to the right to account for the logo width
        status_text = game['game_information']['gameStatusText']
        status_text_x = self.options.cols - len(status_text) * self.font_small_width - gap # Start right after the logoa
        graphics.DrawText(canvas, self.font_small, status_text_x, status_text_y, graphics.Color(255, 255, 255), status_text)


    def render_spread(self, canvas, game, logo_height, logo_width):
        spread_text_y = logo_height * 2 + 2  # Adjust as needed
        odds = game['odds']
        print(odds)
        if odds == None:
            spread_text = f"Spread: {0}"
        else:
            spread_text = f"Spread: {odds['spread']}"  # Example, adjust based on your data structure

        graphics.DrawText(canvas, self.font_small, logo_width + 2, spread_text_y, graphics.Color(255, 255, 255), spread_text)


    def render_game_clock(self, canvas, game, clock_x, clock_y):
        game_status = game['game_information']['gameStatus']
        game_clock = game['game_information']['gameClock']
        print(game_status)
        if game_status == 2:  # Live games
            # Default values for minutes and seconds
            minutes, seconds = '00', '00'

            if game_clock:  # Check if game clock is not empty
                try:
                    minutes, seconds = game_clock.lstrip('PT').split('M')
                    seconds = seconds.rstrip('S').split('.')[0]  # Removing '.00S'
                except ValueError:
                    # Handle cases where game clock format is unexpected
                    pass  # Keeping minutes and seconds as '00'

            quarter_text = f"Q{game['game_information']['period']}" if game['game_information']['period'] <= 4 else "OT"
            game_clock_text = f"{minutes}:{seconds}"

            # Render the quarter and game clock text
            graphics.DrawText(canvas, self.font_small, clock_x, clock_y, graphics.Color(100, 120, 100), quarter_text)
            graphics.DrawText(canvas, self.font_small, clock_x + (len(quarter_text) * 5), clock_y, graphics.Color(255, 255, 255), game_clock_text)
  
    def Render_Games(self, games_data, printer=False):
        matrix = RGBMatrix(options=self.options)
        canvas = matrix.CreateFrameCanvas()
        display_counter = 0  # Counter to switch between scores, probabilities, and quarterly scores

        logo_height, logo_width = 13, 17  # Set your logo dimensions
        clock_x = 5  # Position for the game clock
        clock_y = 30  # Position for the game clock

        for game in games_data:
            print(game)
            print('/n/n')
            # Extract game details
            game_status = game['game_information']['gameStatus']
            awayteam = game['team_information']['away']['teamTricode']
            hometeam = game['team_information']['home']['teamTricode']
            awayscore = game['team_information']['away']['score']
            homescore = game['team_information']['home']['score']

            self.render_team_logos(canvas, awayteam, hometeam, logo_height, logo_width)

            # Alternating between scores, probabilities, and quarterly scores
            if game_status == 2:  # Live games
                if display_counter < 4:
                    self.render_team_names(canvas, awayteam, hometeam,  logo_height, logo_width)
                    self.render_team_scores(canvas, awayteam, hometeam, awayscore, homescore, logo_height, logo_width)
                elif display_counter < 8:
                    # Example probabilities, replace with real values
                    away_prob, home_prob = 0.5, 0.5  # Fetch win probabilities here
                    self.render_win_probabilities(canvas, awayteam, hometeam, away_prob, home_prob, logo_height, logo_width)
                else:
                    self.render_quarterly_scores(canvas, game, logo_height, logo_width)
                if display_counter >= 12:
                    display_counter = 0
            elif game_status == 1:  # Scheduled games
                self.render_team_names(canvas, awayteam, hometeam,  logo_height, logo_width)
                # self.render_spread(canvas, game, logo_height, logo_width)
            else:  # Post game or other statuses
                self.render_team_names(canvas, awayteam, hometeam,  logo_height, logo_width)
                self.render_team_scores(canvas, awayscore, homescore, logo_height, logo_width)

            # Render the game clock and game status
            #self.render_game_clock(canvas, game, clock_x, clock_y)
            self.render_game_status(canvas, game_status, game, logo_height, logo_width)

            # Update the display and counter
            canvas = matrix.SwapOnVSync(canvas)
            display_counter += 1
            time.sleep(4)  # Adjust as needed
            canvas.Clear()




    # def Render_Games(self, games_data, printer=False):
    #     matrix = RGBMatrix(options=self.options)
    #     canvas = matrix.CreateFrameCanvas()
    #     display_counter = 0  # Counter to switch between scores and probabilities

    #     logo_height, logo_width = 10, 10  # Set your logo dimensions

    #     for game in games_data:
    #         # Extract game details
    #         game_status = game['gameStatus']
    #         awayteam = game['awayTeam']['teamTricode']
    #         hometeam = game['homeTeam']['teamTricode']
    #         awayscore = game['awayTeam']['score']
    #         homescore = game['homeTeam']['score']
    #         # Extract or calculate away_prob and home_prob here

    #         self.render_team_logos(canvas, awayteam, hometeam, logo_height, logo_width)

    #         # Alternating between scores, probabilities, and quarterly scores
    #         if game_status == 2:  # Live games
    #             if display_counter < 4:
    #                 self.render_team_scores(canvas, awayteam, hometeam, awayscore, homescore, logo_height, logo_width)
    #             elif display_counter < 8:
    #                 # Example probabilities, replace with real values
    #                 away_prob, home_prob = 0.5, 0.5  # Fetch win probabilities here
    #                 self.render_win_probabilities(canvas, awayteam, hometeam, away_prob, home_prob, logo_height, logo_width)
    #             else:
    #                 self.render_quarterly_scores(canvas, game, logo_height, logo_width)
    #             if display_counter >= 12:
    #                 display_counter = 0
    #         elif game_status == 1:  # Scheduled games
    #             self.render_spread(canvas, game, logo_height, logo_width)
    #         else:  # Post game or other statuses
    #             self.render_team_scores(canvas, awayteam, hometeam, awayscore, homescore, logo_height, logo_width)

    #         self.render_game_status(canvas, game_status, game, logo_height, logo_width)

    #         # Update the display and counter
    #         canvas = matrix.SwapOnVSync(canvas)
    #         display_counter += 1
    #         time.sleep(4)  # Adjust as needed


    
if __name__=='__main__':
    while True:
        data_manager = DataManager()
        games_data = data_manager.fetch_data()  # Assuming this method returns the data as shown

        renderer = Render()
        renderer.Render_Games(games_data)


