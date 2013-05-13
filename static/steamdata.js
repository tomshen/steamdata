$.getJSON('/games', function(all_games) {
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
        output += '<td class="game_platforms">' + details.platforms.join(', ') + '</td>'
      } else {
        output += '<td class="game_name">' + game.name + '</td>'
        output += '<td class="game_platforms">No data.</td>'  
      }
      output += '</tr>'
      return output
    }
    var games = data.response.games
    var table_header = '<table id="games"><thead><tr>' + 
                       '<th class="game_icon"></th>' + 
                       '<th class="game_name">Name</th>' +
                       '<th class="game_platforms">Platforms</th>' +
                       '</tr></thead>'
    return table_header + '<tbody>' + games.map(format_game_data).join('') + '</tbody></table>'
  }
  $('#loadgames').click(function() {
    var steamid = document.getElementById('steamid').value
    if(steamid && /^\d+$/.test(steamid) && steamid.length === 17 && steamid.indexOf("7656119") === 0) {
      try {
        $.getJSON('/info/' + steamid, function(data) {
          try {
            var name = data.response.players[0].realname
            var profileurl = data.response.players[0].profileurl
            document.querySelector('header').innerHTML =
                '<a href="' + profileurl + '">' + name + '\'s Steam Library</a>'
          } catch(e) {}
        })
        $.getJSON('/games/' + steamid, function(data) {
          document.getElementById('info').innerHTML =
              '<p>You own <strong>' + data.response.game_count 
               + '</strong> out of <strong>' + all_games.game_count 
               + '</strong> total Steam games.</p>'
          document.getElementById('info').innerHTML += format_games_data(data)
        })
      } catch(e) {
        alert('Please enter a valid Steam ID.')
      }

    }
    else {
      alert('Please enter a valid Steam ID.')
    }
  })
})