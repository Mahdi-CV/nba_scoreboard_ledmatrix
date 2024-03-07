from nba_api.live.nba.endpoints import scoreboard
import requests
from datetime import datetime
from dateutil import parser, tz
import json
import pytz

def american_to_decimal(american_odds):
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return 1 - (100 / american_odds)
    

def convert_game_time_to_local(game_time_str):
    # Check if the format includes a timezone
    if 'ET' in game_time_str:
        # Extract the time part (assuming format '8:00 pm ET')
        time_str = game_time_str[:-3].strip()

        # Get the current date
        current_date = datetime.now().date()

        # Combine the current date with the extracted time
        datetime_str = current_date.strftime('%Y-%m-%d') + ' ' + time_str


        # Parse the datetime string
        game_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
        # Set the timezone to Eastern Time
        eastern = pytz.timezone('US/Eastern')
        game_datetime = eastern.localize(game_datetime)

        # Convert to local timezone
        local_tz = tz.tzlocal()
        local_datetime = game_datetime.astimezone(local_tz)

        # Return the local datetime as a string, excluding timezone information
        return local_datetime.strftime('%I:%M %p')
    else:
        # If no timezone is included, or for live game status, return the original string
        return game_time_str

def normalize_team_abbreviation(team_code):
    # Dictionary to map NBA API team codes to corrected ESPN team abbreviations
    abbreviation_mapping = {
        "ATL": "ATL",  # Atlanta Hawks
        "BOS": "BOS",  # Boston Celtics
        "BKN": "BKN",  # Brooklyn Nets
        "CHA": "CHA",  # Charlotte Hornets
        "CHI": "CHI",  # Chicago Bulls
        "CLE": "CLE",  # Cleveland Cavaliers
        "DAL": "DAL",  # Dallas Mavericks
        "DEN": "DEN",  # Denver Nuggets
        "DET": "DET",  # Detroit Pistons
        "GSW": "GS",  # Golden State Warriors, Note: Reverse mapping for consistency
        "HOU": "HOU",  # Houston Rockets
        "IND": "IND",  # Indiana Pacers
        "LAC": "LAC",  # LA Clippers
        "LAL": "LAL",  # Los Angeles Lakers
        "MEM": "MEM",  # Memphis Grizzlies
        "MIA": "MIA",  # Miami Heat
        "MIL": "MIL",  # Milwaukee Bucks
        "MIN": "MIN",  # Minnesota Timberwolves
        "NOP": "NO",  # New Orleans Pelicans, Note: Reverse mapping for consistency
        "NYK": "NY",  # New York Knicks
        "OKC": "OKC",  # Oklahoma City Thunder
        "ORL": "ORL",  # Orlando Magic
        "PHI": "PHI",  # Philadelphia 76ers
        "PHX": "PHX",  # Phoenix Suns
        "POR": "POR",  # Portland Trail Blazers
        "SAC": "SAC",  # Sacramento Kings
        "SAS": "SA",  # San Antonio Spurs, Note: Reverse mapping for consistency
        "TOR": "TOR",  # Toronto Raptors
        "UTA": "UTAH",  # Utah Jazz, Note: Reverse mapping for consistency with NBA API
        "WAS": "WSH",  # Corrected mapping for Washington Wizards
    }

    # Return the corrected ESPN abbreviation if it exists in the mapping, else return the original code
    return abbreviation_mapping.get(team_code, team_code)





class DataManager:
    def __init__(self):
        self.espn_url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
        self.cache_file = Path("./game_data_cache.json")  


    def fetch_nba_live_data(self):
        board = scoreboard.ScoreBoard()
        games_data = board.games.get_dict()
        return games_data
    
    def fetch_espn_data(self):
        response = requests.get(self.espn_url)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            data = None  # Assign None to data if request fails
        return data
    
    def combine_data(self, nba_live_data, espn_data):
        combined_data = []

        espn_events_by_gamecode = {event['shortName']: event for event in espn_data['events']}

        for game in nba_live_data:
            away_team_code = normalize_team_abbreviation(game['awayTeam']['teamTricode'])
            home_team_code = normalize_team_abbreviation(game['homeTeam']['teamTricode'])
            game_code = f"{away_team_code} @ {home_team_code}"

            # Extract the gameTime from nba_live_data and convert it to a datetime object
            game_time_nba = datetime.strptime(game['gameTimeUTC'], '%Y-%m-%dT%H:%M:%SZ')

            # Prepare the initial structure for game and team information
            game_information, team_information, odds_info = self.prepare_game_and_team_information(game)

            combined_game_data = {
                'game_information': game_information,
                'team_information': team_information,
                'odds': odds_info,  # Placeholder for odds
                'venue': game.get('venue', '')
            }

            espn_event = espn_events_by_gamecode.get(game_code)
            # print(espn_event)
            # print("\n\n")
            if espn_event:
                # Extract the gameTime from espn_data and convert it to a datetime object
                game_time_espn = datetime.strptime(espn_event['date'], '%Y-%m-%dT%H:%MZ')
                game_status = game.get('status', {})
                display_clock = game_status.get('displayClock', 'Not Available')
                # Update game and team information with ESPN data
                self.update_game_and_team_information_from_espn(combined_game_data, espn_event)

                # Fetch and fill odds data
                combined_game_data = self.update_odds_from_espn(combined_game_data, espn_event)

            combined_data.append(combined_game_data)

        return combined_data
    
    def prepare_game_and_team_information(self, game):
        # Game information
        game_information = {
            'gameId': game['gameId'],
            'gameStatus': game['gameStatus'],
            'gameStatusText': convert_game_time_to_local(game['gameStatusText']),
            'gameClock': game.get('gameClock', ''),
            'period': game.get('period', ''),
            'gameTimeUTC': game['gameTimeUTC'],
            'regulationPeriods': game.get('regulationPeriods', 4)
        }

        # Team information
        team_information = {
            'home': {
                'teamId': game['homeTeam']['teamId'],
                'teamTricode': game['homeTeam']['teamTricode'],
                'teamName': game['homeTeam']['teamName'],
                'score': game['homeTeam']['score'],
                'quarters': game['homeTeam'].get('quarters', []),
                'homeWinProbability': None
            },
            'away': {
                'teamId': game['awayTeam']['teamId'],
                'teamTricode': game['awayTeam']['teamTricode'],
                'teamName': game['awayTeam']['teamName'],
                'score': game['awayTeam']['score'],
                'quarters': game['awayTeam'].get('quarters', []),
                'awayWinProbability': None
            }
        }

        odds_info = {
            'spread': 0,
            'over_under': 0,
            'over_value': 0,
            'under_value': 0,
            'away_team_favorite': False,
            'home_team_favorite': False
        }

        
        return (game_information, team_information, odds_info)

    
    def update_game_and_team_information_from_espn(self, combined_game_data, espn_event):

        # Update scores
        combined_game_data['team_information']['home']['score'] = max(
            int(espn_event['competitions'][0]['competitors'][0]['score']), 
            int(combined_game_data['team_information']['home']['score'])
        )
        combined_game_data['team_information']['away']['score'] = max(
            int(espn_event['competitions'][0]['competitors'][1]['score']), 
            int(combined_game_data['team_information']['away']['score'])
        )

        game_data = espn_event["competitions"][0]
        if 'situation' in game_data and 'lastPlay' in game_data['situation'] and 'probability' in game_data['situation']['lastPlay']:
            probabilities = game_data['situation']['lastPlay']['probability']
            # home_win_percentage = probabilities.get('homeWinPercentage', None)
            # away_win_percentage = probabilities.get('awayWinPercentage', None)
            # print(f"Home Win Percentage: {home_win_percentage}")
            # print(f"Away Win Percentage: {away_win_percentage}")
            # Extract probabilities with defaults
            home_win_probability = int(round(probabilities.get('homeWinPercentage', 0), 2) * 100)
            away_win_probability = int(round(probabilities.get('awayWinPercentage', 0), 2) * 100)

            # Update combined game data
            combined_game_data['team_information']['home']['homeWinProbability'] = home_win_probability
            combined_game_data['team_information']['away']['awayWinProbability'] = away_win_probability

        return combined_game_data

    def update_odds_from_espn(self, combined_game_data, event):
        competition = event['competitions'][0]
        if 'odds' in competition and competition['odds']:
            odds_data = competition['odds'][0]
            current_odds = competition['odds'][0]['current']
            # Extract spread, over/under and favorite/underdog information
            spread = odds_data.get('spread')
            over_under = current_odds.get('total', {}).get('alternateDisplayValue')
            over_value = current_odds.get('over', {}).get('value')
            under_value = current_odds.get('under', {}).get('value')

            away_favorite = odds_data.get('awayTeamOdds', {}).get('favorite', False)
            home_favorite = odds_data.get('homeTeamOdds', {}).get('favorite', False)

            # Constructing the odds info dictionary
            combined_game_data['odds']['spread'] = spread
            combined_game_data['odds']['over_under'] = over_under
            combined_game_data['odds']['over_value'] = over_value
            combined_game_data['odds']['under_value'] = under_value
            combined_game_data['odds']['away_team_favorite'] = away_favorite
            combined_game_data['odds']['home_team_favorite'] = home_favorite
        return combined_game_data

    
    # def fetch_data(self):
    #     espn_data = self.fetch_espn_data()
    #     nba_live_data = self.fetch_nba_live_data()
    #     return self.combine_data(nba_live_data, espn_data)
    
    # Add methods to save data to and load data from cache
    def save_data_to_cache(self, data):
        try:
            with self.cache_file.open('w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Failed to save data to cache: {e}")

    def load_data_from_cache(self):
        try:
            if self.cache_file.exists():
                with self.cache_file.open() as f:
                    return json.load(f)
            else:
                return None
        except Exception as e:
            print(f"Failed to load data from cache: {e}")
            return None

    # Modify fetch_data to use cache
    def fetch_data(self):
        espn_data = self.fetch_espn_data()
        nba_live_data = self.fetch_nba_live_data()
        if espn_data and nba_live_data:
            combined_data = self.combine_data(nba_live_data, espn_data)
            self.save_data_to_cache(combined_data)  # Save the combined data to cache
            return combined_data
        else:
            print("Failed to fetch new data, loading from cache.")
            return self.load_data_from_cache()
       
if __name__ == '__main__':
    data_manager = DataManager()
    espn_data = data_manager.fetch_espn_data()
    nba_live_data = data_manager.fetch_nba_live_data()
    d = data_manager.combine_data(nba_live_data, espn_data)
    #print(d)
    #print('\n\n')
    # Process espn_data or perform further actions



