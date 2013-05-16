import os
import json
from flask import Flask, render_template, abort, request, Response, url_for
import requests
app = Flask(__name__)
try:
    from config import STEAM_API_KEY
except:
    STEAM_API_KEY = os.environ['STEAM_API_KEY']

def update_game_data():
    from steamscraper.steamscraper import SteamScraper
    SteamScraper().outputJSON('steamdata.json')
    return 'Steam game data updated.'

def is_steamid(id):
    return id and id.isdigit() and len(id) == 17 and ('7656119' in id)

@app.route('/')
def home():
    if request.args.get('steamid', ''):
        return render_template('index.html', steamid=request.args.get('steamid', ''))
    else:
        return render_template('index.html', steamid='')

@app.route('/graph')
@app.route('/graph/<steamid>')
def page_graph(steamid=''):
    return render_template('graph.html', steamid=steamid)

"""
REQUIRES: is_steamid(steamid)
ENSURES: returns a list of friends for `steamid`
"""
def get_friends(steamid):
    try:
        req = requests.get('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' 
                           + STEAM_API_KEY + '&steamid=' + steamid + '&relationship=friend&format=json')
        return req.json()['friendslist']['friends']
    except:
        return steamid + ' has no friends :('

"""
REQUIRES: is_steamid(steamid)
ENSURES: returns an info dictionary for `steamid`
"""
def get_info(steamid):
    req = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' 
                           + STEAM_API_KEY + '&steamids=' + steamid + '&format=json')
    return req.json()['response']['players'][0]

"""
REQUIRES: is_steamid(steamid)
ENSURES: returns an game object (with `game_count`, list of `games`) for `steamid`
"""
def get_games(steamid):
    req = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' 
                       + STEAM_API_KEY + '&steamid=' + str(steamid) + 
                       '&include_appinfo=1&include_played_free_games=1&format=json')
    return req.json()['response']

def graph_friends(friends, depth=1):
    def get_name(steamid):
        return get_info(steamid)['personaname']
        try:
            return get_info(steamid)['personaname']
        except:
            return 'Anonymous'
    if depth == 0:
        return friends
    else:
        return dict([(f['steamid'], {'name': get_name(f['steamid']),
                    'friends': graph_friends(get_friends(f['steamid']), depth - 1)}) for f in friends])

@app.route('/api/graph/<steamid>')
@app.route('/api/graph/<steamid>/<depth>')
def graph(steamid, depth=1):
    if is_steamid(steamid):
        info = get_info(steamid)
        friends = get_friends(steamid)
        resp = Response(json.dumps(graph_friends(friends, int(depth)), indent=4), status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://steamdata.herokuapp.com'
        return resp
        try:
            friends = get_friends(steamid)
            return str(friends)
            """
            resp = Response(req.text, status=200, mimetype='application/json')
            resp.headers['Link'] = 'http://steamdata.herokuapp.com'
            return resp
            """
        except:
            return abort(404)
    else:
        return abort(404)

@app.route('/api/friends/<steamid>')
def friends(steamid):
    if is_steamid(steamid):
        resp = Response(json.dumps(get_friends(steamid), indent=4), status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://steamdata.herokuapp.com'
        return resp
    else:
        return abort(404)

@app.route('/api/info/<steamid>')
def info(steamid):
    if is_steamid(steamid):
        resp = Response(json.dumps(get_info(steamid), indent=4), status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://steamdata.herokuapp.com'
        return resp
    else:
        return abort(404)

@app.route('/api/games')
@app.route('/api/games/<steamid>')
def games(steamid=None):
    games = None
    if not steamid:
        with open('steamdata.json', 'r') as f:
            games = f.read()
    else:
        if is_steamid(steamid):
            games = json.dumps(get_games(steamid), indent=4)
        else:
            return abort(404)
    resp = Response(games, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://steamdata.herokuapp.com'
    return resp

if __name__ == '__main__':
    app.run(debug=True)