# :control_knobs: fynesse

:seedling: Advanced recommendation and search web app for Spotify, written in pure Python.

:package: UI written in [Reflex](https://github.com/reflex-dev/reflex/), Spotify interaction via [Spotipy](https://github.com/spotipy-dev/spotipy)

![Screenshot](screenshot.png?raw=true 'fynesse UI')


## Features

- **Generate recommendations** based on seed tracks and artists from your library or search results + 5 tuneable parameters provided by rhe recommendation API
- **Browse** your Spotify library (liked songs, playlists, recently played) and see artist genres associated with each track
- **Fine-grained search** for artists and tracks — by name, genre, year
- **Play and queue new music** on your currently active Spotify device, or save recommendations to a playlist to lisen later


## Connecting to Spotify API and running the app

The core functionality of fynesse requires a connection to **Spotify's Web API**.

To set this up:
1. Go to the [Spotify developer dashboard](https://developer.spotify.com/dashboard/applications)
1. Click `Create app`
1. Enter a name and app description (these don't matter)
1. Enter `https://localhost:1234` as Redirect URI (or a port of your choice)
1. Tick `Web API` under `Which API/SDKs are you planning to use?`
1. Agree to terms and click `Save`
1. Click `Settings` in the top right
    - You now can see your `Client ID` and `Client Secret`
1. Add your `Client ID` and `Client Secret` to [sp_secrets.py](sp_secrets.py)
1. You are now ready to run the app. Do so by running `reflex init` followed by `reflex run` in the [parent directory](/) (you will need the packages listed in [requirements.txt](requirements.txt) installed)
1. On first run, a browser window will open to a spotify authentication page. When you click `Agree`, you will be redirected to a URL beginning `https://localhost:1234` (if you kept default port)
1. The terminal session in which reflex is running will prompt you to `Enter the URL you were redirected to`; copy-paste the redirect url from your browser's address bar into the terminal and press enter
1. The app should run, accessible at `http://localhost:3000` :sunglasses:

## Tips for use
- have a flick through your library for some bangers
- plant them and/or their artists into the seeds window
- germinate the seeds to produce a batch of tune recommendations
- experiment with the other generation parameters to fine tune your recommendations
- play/queue some/all of the recommended tunes
    - music is played via your active spotify device if you have one
    - **to play music from fynesse, you need to have a spotify client open somewhere - desktop, web, or mobile, and Spotify must consider it the 'active device'. To make a device active you can quickly play/pause from it**
- save recommended tunes to a playlist in your library to listen another time
- explore genres by showing them on your library and clicking to search
    - narrow down search to find similar tunes manually
- using a set of disparate seeds will produce a mixed playlist
- tunes can be played, queued or seeded from search results via each track's dropdown button
