# Radio2Spotify
If you ever listen to radio, you have certainly been in a situation when you wanted to add the song you've just heard into your playlist on Spotify, YouTube, or any other service where you store your favourite music. 

The problem is, you probably don't always have time for that, or don't even have the ability to check out the name of the song.

Alternatively, maybe you've recently stumbled upon a radio station which you love for music they play and wish to have a playlist of what they are playing because the style fits you so well?

Well, all of these are the case for me, which is why (and for training myself) I've started this project, allowing me to export music from two of my favourite radio stations. In one case [LRT Opus](https://www.lrt.lt/mediateka/tiesiogiai/lrt-opus) only **now playing** songs are exported, as no playlist history is available, and for another one [Shonan Beach FM](https://www.beachfm.co.jp/) **historical playlist** for ca. latest hour is used.

## Acknowledgements
I would really like to thank TheComeUpCode for her YouTube tutorial about [generating Spotify playlist based on YouTube liked videos](https://www.youtube.com/watch?v=7J_qcttfnJA) and, as to understand it, required some understanding of OOP, CoreyMSchafer for his [Python OOP tutorial](https://www.youtube.com/watch?v=ZDa-Z5JzLYM). 

## Spotify API
Using an expirable Spotify token is impractical, as it expires after 1 hour. Therefore, this code is using refresh tokens (token_refresher class), a request inside this class returns an access token to be used in the next request and a refresh token to be used when token refresher is used next time. More information about using Spotify API can be found [here](https://developer.spotify.com/documentation/general/guides/)
*add more info about using Spotify API*

## Scraping: one song versus a playlist
The code of this project covers both scenarios: radio station (or a third-party service) providing a whole playlist `shonanscraper.py` as well as only single-song scenario in `opusscraper.py`. Note that some tweaks are made to resulting string in order to separate songs from artists' names, remove a release year (always added to the end of song name in LRT Opus case) and/or some other unneccessary characters. 

## TODO
- Automate tasks to be executed ca. every 5 minutes for now playing case and every 1 hour for historical playlist.
- Use a headless browser for Selenium scraping.
- Ignore unneccessary characters in scraping Shonan Beach FM.
- Implement a check for duplicates.
- General cleanup.
- Clearer readme.
