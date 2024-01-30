from render_nba import NBARenderer
from data_manager import DataManager

if __name__ == '__main__':
    data_manager = DataManager()
    renderer = NBARenderer()

    while True:
        games_data = data_manager.fetch_data()
        renderer.render_games(games_data)
