# Steam Data
Steam Data is an unofficial, enhanced API for [Steam](http://www.steampowered.com/).

## Usage
Make a GET request to:
* `/api/games`: list of all games on Steam
* `/api/info/<steamid>`: public profile info about `<steamid>`
* `/api/games/<steamid>`: list of all games owned by `<steamid>`
* `/api/friends/<steamid>`: list of all friends of `<steamid>`
* `/api/graph/<steamid>/<depth>`: graph of friends of friends of `<steamid>` (with depth `<depth>`)
  * `<depth>` is optional and defaults to 1
  * currently very slow (> 30 seconds) for depths greater than 1

All results returned in the JSON format.

## Example apps

### Steam Game Library
Available at `/games`. Enter your Steam ID to view a list of your Steam games, with
associated metadata.

### Steam Friend Graph
Available at `/graph`. Currently under development.