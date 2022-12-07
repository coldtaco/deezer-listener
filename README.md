# deezer-listener
 Listens to deezer tracks for you when you listen to it offline
 
 Requirements
 ```
 Selenium==4.1.2
 ```
 
 Run listen.py
 
 `PLAY_DURATION`: Adjusts how long to play if controlling play time is required (in seconds). Value of -1 means infinite play, rest of the arguments are ignored.
 `PAUSE_DURATION`: Adjusts duration of pause. If you don't to pretend to be listening 24/7 (for example only 'listen' 4 hours a day). Provide number in seconds. Value of -1 means to repeat once a day (listen to `PLAY_DURATION` seconds every day).
 `REPEAT`: Number of cycles of `PLAY_DURATION`, `PAUSE_DURATION` to repeat. Value of -1 means to repeat indefinitely.
