import os

import requests
from flask import Flask, render_template, abort, request, Response, jsonify

from util import crossdomain

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
    return render_template('index.html')
    """
    if request.args.get('steamid', ''):
        return render_template('index.html', steamid=request.args.get('steamid', ''))
    else:
        return render_template('index.html', steamid='')
    """

@app.route('/games')
@app.route('/games/')
@app.route('/games/<steamid>')
def page_games(steamid=''):
    return render_template('games.html', steamid=steamid)

@app.route('/graph')
@app.route('/graph/')
@app.route('/graph/<steamid>')
def page_graph(steamid=''):
    return render_template('graph.html', steamid=steamid)

def get_friends(steamid):
    try:
        req = requests.get('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' 
                           + STEAM_API_KEY + '&steamid=' + steamid + '&relationship=friend&format=json')
        return req.json()['friendslist']['friends']
    except:
        return steamid + ' has no friends :('

def get_info(steamid):
    req = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' 
                           + STEAM_API_KEY + '&steamids=' + steamid + '&format=json')
    return req.json()['response']['players'][0]

def get_games(steamid):
    req = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' 
                       + STEAM_API_KEY + '&steamid=' + str(steamid) + 
                       '&include_appinfo=1&include_played_free_games=1&format=json')
    return req.json()['response']

def get_name(steamid):
    try:
        return get_info(steamid)['personaname']
    except:
        return 'Anonymous'

def graph_friends(steamid, depth=1):
    if depth == 1:
        friends = get_friends(steamid)
        if type(friends) is list:
            return [{'name': get_name(f['steamid']), 'steamid': f['steamid']} for f in friends]
        else:
            return []
    else:
        friends = get_friends(steamid)
        if type(friends) is list:
            return [{'name': get_name(f['steamid']),
                     'steamid': f['steamid'],
                     'friends': graph_friends(f['steamid'], depth - 1)} for f in friends]
        else:
            return [] # User has not exposed friends list to public.

@app.route('/api/graph/<steamid>')
@app.route('/api/graph/<steamid>/')
@app.route('/api/graph/<steamid>/<depth>')
@crossdomain(origin='*')
def graph(steamid, depth=1):
    if is_steamid(steamid):
        try:
            return jsonify({'steamid': steamid, 'friends': graph_friends(steamid, int(depth))})
        except:
            return abort(404)
    else:
        return abort(400)

@app.route('/api/friends/<steamid>')
@crossdomain(origin='*')
def friends(steamid):
    if is_steamid(steamid):
        return jsonify({'steamid': steamid, 'friends':get_friends(steamid)})
    else:
        return abort(400)

@app.route('/api/info/<steamid>')
@crossdomain(origin='*')
def info(steamid):
    if is_steamid(steamid):
        return jsonify(get_info(steamid))
    else:
        return abort(400)

@app.route('/api/games')
@app.route('/api/games/')
@app.route('/api/games/<steamid>')
@crossdomain(origin='*')
def games(steamid=None):
    games = None
    if not steamid:
        with open('steamdata.json', 'r') as f:
            resp = Response(f.read(), status=200, mimetype='application/json')
            resp.headers['Link'] = 'http://steamdata.herokuapp.com'
            return resp
    else:
        if is_steamid(steamid):
            return jsonify(get_games(steamid))
        else:
            return abort(400)
    
if __name__ == '__main__':
    app.run(debug=True)