## Simple Discord Bot

### Version: 1.2.1

Discord bot that plays audio from youtube videos in the discord voice channel
the user is in. 

#### List of commands:

* !play [search]: Plays audio from youtube video in voice channel (Needs "")  
  Adds search to a queue when audio is already playing or paused
* !pause: Pauses audio currently playing
* !resume: Resumes audio that is paused
* !skip: Skips audio that is currently playing or paused 
* !leave: Forces bot to leave voice channel and cleans queue
* !options: Posts list of commands

#### Update Log

* Version 1.2.2
  *  Fixed bug where sometimes .webm files would be left in the directory
* Version 1.2.1
  *  Removed need for quotations when using command !play
  *  Fixed bug with !leave command where it wouldn't clean the queue
* Version 1.2
  *  Bot now adds searches to a queue when audio is playing or paused
  *  Added skip command that skips audio currently playing or paused
* Version 1.1 
  *  Bot now posts what audio is playing in the text channel
