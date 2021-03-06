$.getJSON('/api/games', function(all_games) {
  document.querySelector('footer').innerHTML += 
      ' · Steam data last updated ' + all_games.last_updated.slice(0,10)
  function format_games_data(data) {
    function format_game_data(game) {
      var img_url = 'http://media.steampowered.com/steamcommunity/public/images/apps/'
                           + game.appid + '/'
      function get_details() {
        function same_game(element, index, array) {
          return element.appid === game.appid
        }
        var same_game_list = all_games.games.filter(same_game)
        if(same_game_list.length < 1) {
          return null
        }
        return same_game_list[0]
      }
      var output = '<tr>'
      var details = get_details()
      if(game.img_icon_url) {
        output += '<td class="game_icon"><img src="' + img_url + game.img_icon_url + '.jpg"</img></td>'
      } else output += '<td class="game_icon"><img src="http://placehold.it/34x34"></td>'
      if(details) {
        output += '<td><a href="' + details.url + '">' + game.name + '</a></td>'
        output += '<td class="game_price">' + details.price + '</td>'
        output += '<td class="game_released">' + details.released + '</td>'
        if(details.score)
          output += '<td class="game_score">' + details.score + '</td>'
        else
          output += '<td class="game_score">No data.</td>'
        output += '<td class="game_platforms">' + details.platforms.join(', ') + '</td>'
      } else {
        output += '<td class="game_name">' + game.name + '</td>'
        output += '<td class="game_platforms">No data.</td>'  
      }
      output += '</tr>'
      return output
    }
    var games = data.games
    var table_header = '<table id="games"><thead><tr>' + 
                       '<th class="game_icon"></th>' + 
                       '<th class="game_name">Name</th>' +
                       '<th class="game_price">Price ($)</th>' +
                       '<th class="game_released">Release Date</th>' +
                       '<th class="game_score">Metascore</th>' +
                       '<th class="game_platforms">Platforms</th>' +
                       '</tr></thead>'
    return table_header + '<tbody>' + games.map(format_game_data).join('') + '</tbody></table>'
  }
  function is_steamid(steamid) {
    var steamid = String(steamid)
    return steamid && /^\d+$/.test(steamid) && steamid.length === 17 && steamid.indexOf("7656119") === 0;    
  }
  function load_steam_data(steamid) {
    if(steamid.indexOf('/') !== -1) {
      steamid = steamid.slice(steamid.lastIndexOf('/')+1)
    }
    if(is_steamid(steamid)) {
      try {
        $.getJSON('/api/info/' + steamid, function(data) {
          try {
            var name = data.realname || data.personaname || 'Anonymous'
            var profileurl = data.profileurl
            document.querySelector('header').innerHTML =
                '<h1><a href="' + profileurl + '">' + name + '\'s Steam Library</a></h1>'
          } catch(e) {}
        })
        $.getJSON('/api/games/' + steamid, function(data) {
          document.getElementById('container').innerHTML =
              '<p id="info">You own <strong>' + data.game_count 
               + '</strong> out of <strong>' + all_games.game_count 
               + '</strong> total Steam games.</p>'
          document.getElementById('container').innerHTML += format_games_data(data)
          $('#floatingBarsG').hide()
          $('section').show()
        })
      } catch(e) {
        alert('Please enter a valid Steam ID.')
      }

    }
    else {
      alert('Please enter a valid Steam ID.')
    }
  }
  $('#loadgames').click(function() {
    var steamid = document.getElementById('steamidinput').value
    if(steamid.indexOf('/') !== -1) {
      steamid = steamid.slice(steamid.lastIndexOf('/')+1)
    }
    if(is_steamid(steamid)) {
      window.location = '/games/' + steamid
    } else {
      alert('Please enter a valid Steam ID.')
    }
  }) 
  if(steamid) {
    load_steam_data(String(steamid))
  }
})