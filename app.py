import os
from flask import Flask, render_template, abort
import requests
app = Flask(__name__)
try:
    from secrets import STEAM_API_KEY
except:
    STEAM_API_KEY = os.environ['STEAM_API_KEY']

def update_game_data():
    from steamscraper.steamscraper import SteamScraper
    SteamScraper().outputJSON('steamdata.json')
    return 'Steam game data updated.'

def is_steam_id(id):
    return id and id.isdigit() and len(id) == 17 and ('7656119' in id)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/info/<steamid>')
def info(steamid):
    if is_steam_id(steamid):
        req = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' 
                           + STEAM_API_KEY + '&steamids=' + steamid + '&format=json')
        return req.text
    else:
        return abort(404)

@app.route('/games')
@app.route('/games/<steamid>')
def games(steamid=None):
    if not steamid:
        with open('steamdata.json', 'r') as f:
            return f.read()
    else:
        if is_steam_id(steamid):
            req = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' 
                               + STEAM_API_KEY + '&steamid=' + steamid + 
                               '&include_appinfo=1&include_played_free_games=1&format=json')
            return req.text
        else:
            return abort(404)

if __name__ == '__main__':
    app.run(debug=True)