spotify_client_id = # your client ID, unique for every app created in Spotify Developer Dashboard
spotify_user_id = # your user ID, found in your profile link
spotify_secret = # your client secret, unique for every app created in Spotify Developer Dashboard

# This is used for Authorization header for POST request for refresh token
authstring = spotify_client_id + ":" + spotify_secret
authstring_encoded = base64.b64encode(authstring.encode())
authstring = authstring_encoded.decode("utf-8")
