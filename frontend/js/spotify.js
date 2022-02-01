let access_token = 'spotify token'

let _token = access_token;

window.onSpotifyPlayerAPIReady = () => {
    const player = new Spotify.Player({
      name: 'Web Playback SDK Template',
      getOAuthToken: cb => { cb(_token); }
    });
  
    // Error handling
    player.on('initialization_error', e => console.error(e));
    player.on('authentication_error', e => console.error(e));
    player.on('account_error', e => console.error(e));
    player.on('playback_error', e => console.error(e));
  
    // Playback status updates
    player.on('player_state_changed', state => {
      console.log(state)
      $('#current-track').attr('src', state.track_window.current_track.album.images[0].url);
      $('#current-track-name').text(state.track_window.current_track.name);
    });
  
    // Ready
    player.on('ready', data => {
      console.log('Ready with Device ID', data.device_id);
      
      // Play a track using our new device ID
      play(data.device_id);
    });
  
    // Connect to the player!
    player.connect();
  }
  
  // Play a specified track on the Web Playback SDK's device ID
function play(device_id) {
    $.ajax({
     url: "https://api.spotify.com/v1/me/player/play?device_id=" + device_id,
     type: "PUT",
     data: '{"uris": ["spotify:track:5ya2gsaIhTkAuWYEMB0nw5"]}',
     beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Bearer ' + _token );},
     success: function(data) { 
       console.log(data)
     }
    });
}