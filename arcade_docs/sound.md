# Sound
This page will help you get started by covering the essentials of sound.
In addition each section’s concepts, there may also be links to example code and documentation.
  1. [Why Is Sound Important?](#sound-why-important)
  2. [Sound Basics](#sound-basics)
     * [Loading Sounds](#sound-basics-loading)
     * [Playing Sounds](#sound-basics-playing)
     * [Stopping Sounds](#sound-basics-stopping)
  3. [Streaming or Static Loading?](#sound-loading-modes)
  4. [Intermediate-Level Playback Control](#sound-intermediate-playback)
  5. [Cross-Platform Compatibility](#sound-compat)
  6. [Other Sound Libraries](#sound-other-libraries) (for advanced users)


I’m Impatient!
Users who want to skip to example code should consult the following:
  1. [Sound Demo](../example_code/sound_demo.html#sound-demo)
  2. [Sound Speed Demo](../example_code/sound_speed_demo.html#sound-speed-demo)
  3. [Music Control Demo](../example_code/music_control_demo.html#music-control-demo)
  4. [Platformer Tutorial - Step 9 - Adding Sound](../tutorials/platform_tutorial/step_09.html#platformer-part-nine)


## Why Is Sound Important?
Sound helps players make sense of what they see.
For example, have you ever run into one of these common problems?
  * Danger you never knew was there
  * A character whose reaction seemed unexpected or out of place
  * Items or abilities which appeared similar, but were very different
  * An unclear warning or confirmation dialog


How much progress did it cost you? A few minutes? The whole playthrough? More importantly, how did you feel? You probably didn’t want to keep playing.
You can use sound to prevent moments like these. In each example above, the right audio can provide the information players need for the game to feel fair.
## Sound Basics
### Loading Sounds
To play audio, you must first load its data into a [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound") object.
Arcade has two ways to do this:
  * [`arcade.load_sound()`](../api_docs/api/sound.html#arcade.load_sound "arcade.load_sound")
  * [`arcade.Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.Sound")


Both provide a [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound") instance and accept the same arguments:  
| Argument  | Type  | Meaning  |  
| --- | --- | --- |  
| `path`  | [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)") **|** [`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "\(in Python v3.14\)")  | A sound file (may use [Resource Handles](resource_handlers.html#resource-handles))  |  
| `streaming`  | [`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")  | 
  * `True` streams from disk
  * `False` loads the whole file

 |  
The simplest option is to use [`arcade.load_sound()`](../api_docs/api/sound.html#arcade.load_sound "arcade.load_sound"):

```
from pathlib import Path
import arcade

# The path argument accepts paths prefixed with resources handle,
from_handle_prefix = arcade.load_sound(":resources:sounds/hurt1.wav")
# Windows-style backslash paths,
from_windows_path = arcade.load_sound(Path(r"sounds\windows\file.wav"))
# or pathlib.Path objects:
from_pathlib_path = arcade.load_sound(Path("imaginary/mac/style/path.wav"))

```

For an object-oriented approach, create [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound") instances directly:

```
from arcade import Sound  # You can also use arcade.Sound directly

# For music files and ambiance tracks, streaming=True is usually best
streaming_music_file = Sound(":resources:music/1918.mp3", streaming=True)

```

To learn more, please see the following:
  1. [Built-In Resources](../api_docs/resources.html#resources)
  2. Python’s built-in [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "\(in Python v3.14\)")
  3. [Streaming or Static Loading?](#sound-loading-modes)


### Playing Sounds
Arcade has two easy ways to play loaded [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound") data.
Imagine you’ve loaded the following built-in sound file:

```
COIN_SOUND = arcade.load_sound(":resources:sounds/coin1.wav")

```

The first way to play it is passing it to [`arcade.play_sound()`](../api_docs/api/sound.html#arcade.play_sound "arcade.play_sound"):

```
self.coin_playback = arcade.play_sound(COIN_SOUND)

```

We store the return value because it is a special object which lets us control this specific playback of the [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound") data.
Important
You **must** pass a [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.Sound"), not a path!
If you pass [`arcade.play_sound()`](../api_docs/api/sound.html#arcade.play_sound "arcade.play_sound") anything other than a [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound") or `None`, it will raise a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)").
To avoid making this mistake, you can call the [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.Sound") data’s [`play()`](../api_docs/api/sound.html#arcade.Sound.play "arcade.Sound.play") method instead:

```
self.coin_playback = COIN_SOUND.play()

```

In each case, the returned object allows stopping and changing a specific playback of a sound before it finishes. We’ll cover this in depth below.
### Stopping Sounds
#### Sound data vs Playbacks
Arcade uses the pyglet multimedia library to handle sound.
Each playback of a [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound") has its own pyglet [`Player`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player "\(in pyglet v2.1\)") object to control it:

```
# We can play the same Sound one, two, or many more times at once
self.coin_playback_1 = arcade.play_sound(COIN_SOUND)
self.coin_playback_2 = COIN_SOUND.play()
self.coin_playback_3 = COIN_SOUND.play()
...

```

We can create and control a very large number of separate playbacks. Although there is a platform-dependent upper limit, it is high enough to be irrelevant for most games.
#### Stopping a Specific Playback
There are two easy ways of stopping a playback of a [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound").
The first is to choose which function we’ll pass its [`Player`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player "\(in pyglet v2.1\)") object to:
  * [`arcade.stop_sound()`](../api_docs/api/sound.html#arcade.stop_sound "arcade.stop_sound"):

```
arcade.stop_sound(self.coin_playback_1)

```

  * The [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.Sound") data’s [`stop()`](../api_docs/api/sound.html#arcade.Sound.stop "arcade.Sound.stop") method:

```
self.COIN_SOUND.stop(self.coin_playback_1)

```



The last step is to clean up by removing all remaining references to it:

```
# Overwriting them with None is the clearest option
self.current_playback = None

```

By default, Python automatically counts how many places use an object. When there are zero of these “references” left, Python will mark an object as “garbage” and delete it automatically. This is called “garbage collection.” We’ll cover it further in the advanced sections below.
To learn more about playback limits and stopping, please see the following:
  * [The Most Reliable Formats & Features](#sound-compat-easy)
  * [Intermediate-Level Playback Control](#sound-intermediate-playback)
  * [Sound Demo](../example_code/sound_demo.html#sound-demo)


## Intermediate Loading and Playback
Arcade also offers more advanced options for controlling loading and playback.
These allow loading files in special modes best used for music. They also allow controlling volume, speed, and spatial aspects of playback.
### Streaming or Static Loading?
The streaming option is best for long-playing music and ambiance tracks.  
| Streaming  | Best [[1]](#meaningbestformatheader) Format  | Decompressed  | Best Uses  |  
| --- | --- | --- | --- |  
| `False` (Default)  | `.wav`  | Whole file  | 2+ overlapping playbacks, short, repeated, unpredictable  |  
| `True`  | `.mp3`  | Predicted data  | 1 copy & file at a time, long, uninterrupted  |  
Arcade uses **static** loading by default. It is called static loading because it decompresses the whole audio file into memory once and then never changes the data. Since the data never changes, it has multiple benefits like allowing multiple playbacks at once.
The alternative is streaming. Although it saves memory for long music and ambiance tracks, it has downsides:
  * Only one playback of the [`Sound`](../api_docs/api/sound.html#arcade.Sound "arcade.sound.Sound") permitted
  * Moving around in the file can cause buffering issues
  * Looping is not supported


Enable it by passing `True` through the `streaming` [keyword argument](https://docs.python.org/3/glossary.html#term-argument) when [loading sounds](#sound-basics-loading):

```
# Both loading approaches accept the streaming keyword.
classical_music_track = arcade.load_sound(":resources:music/1918.mp3", streaming=True)
funky_music_track = arcade.Sound(":resources:music/funkyrobot.mp3", streaming=True)

```

To learn more about streaming, please see:
  * The [Music Control Demo](../example_code/music_control_demo.html#music-control-demo) for runnable example code
  * The [Sound Performance in Depth](performance_tips.html#loading-performance-sound) guide for extensive discussion


### Intermediate-Level Playback Control
#### Stopping via the Player Object
Arcade’s [Stopping Sounds](#sound-basics-stopping) functions wrap pyglet [`Player`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player "\(in pyglet v2.1\)") features.
For additional finesse or less functional call overhead, some users may want to access its functionality directly.
Pausing
There is no stop method. Instead, call [`Player.pause()`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player.pause "\(in pyglet v2.1\)"):

```
# Assume this is inside a class which stores a pyglet Player
self.current_player.pause()

```

Stopping Permanently
After you’ve paused a player, you can stop playback permanently as follows:
  1. Call the player’s [`delete()`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player.delete "\(in pyglet v2.1\)") method:

```
# Permanently deletes the operating system half of this playback.
self.current_player.delete()

```

This specific playback is now permanently over, but you can start new ones.
  2. Make sure all references to the player are replaced with `None`:

```
# Python will delete the pyglet Player once there are 0 references to it
self.current_player = None

```



Note
This is how [`Sound.stop`](../api_docs/api/sound.html#arcade.Sound.stop "arcade.Sound.stop") works internally.
For a more in-depth explanation of references and auto-deletion, skim the start of Python’s page on [garbage collection](https://devguide.python.org/internals/garbage-collector/). Reading the Abstract section of this page should be enough to get started.
#### Advanced Playback Arguments
There are more ways to alter playback than stopping. Some are more qualitative. Many of them can be applied to both new and ongoing sound data playbacks, but in different ways.
Both [`arcade.play_sound()`](../api_docs/api/sound.html#arcade.play_sound "arcade.play_sound") and [`arcade.Sound.play()`](../api_docs/api/sound.html#arcade.Sound.play "arcade.Sound.play") support the following advanced arguments:  
| Argument  | Values  | Meaning  |  
| --- | --- | --- |  
| volume  | [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)") between `0.0` (silent) and `1.0` (full volume)  | A scaling factor for the original audio file.  |  
| pan  | A [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)") between `-1.0` (left) and `1.0` (right)  | The left / right channel balance  |  
| loop  | [`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)") (`True` / `False`)  | Whether to restart playback automatically after finishing. [[2]](#streamingnoloop)  |  
| speed  | [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)") greater than `0.0`  | The scaling factor for playback speed (and pitch)
  * Lower than `1.0` slows speed and lowers pitch
  * Exactly `1.0` is the original speed (default)
  * Higher than `1.0` plays faster with higher pitch

 |  
#### Change Ongoing Playbacks via Player Objects
[`Player.pause()`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player.pause "\(in pyglet v2.1\)") is one of many method and property members which change aspects of an ongoing playback. It’s impossible to cover them all here, especially given the complexity of [positional audio](#sound-other-libraries-pyglet-positional).
Instead, the table below summarizes a few of the most useful members in the context of Arcade. Superscripts link info about potential issues, such as name differences between properties and equivalent keyword arguments to Arcade functions.  
| [`Player`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player "\(in pyglet v2.1\)") Member  | Type  | Default  | Purpose  |  
| --- | --- | --- | --- |  
| [`pause()`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player.pause "\(in pyglet v2.1\)")  | method  | N/A  | Pause playback resumably.  |  
| [`play()`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player.play "\(in pyglet v2.1\)")  | method  | N/A  | Resume paused playback.  |  
| [`seek()`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player.seek "\(in pyglet v2.1\)")  | method  | N/A  |  Warning [Using this option with streaming can cause freezes!](performance_tips.html#sound-loading-modes-streaming-freezes) Skip to the passed [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)") timestamp measured as seconds from the audio’s start.  |  
| [`volume`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player.volume "\(in pyglet v2.1\)")  | [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)") property  | `1.0`  | A scaling factor for playing the audio between `0.0` (silent) and `1.0` (full volume).  |  
| [`loop`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player.loop "\(in pyglet v2.1\)")  | [`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)") property  | `False`  | Whether to restart playback automatically after finishing. [[3]](#streamingnoloop2)  |  
| [`pitch`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player.pitch "\(in pyglet v2.1\)") [[4]](#inconsistencyspeed)  | [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)") property  | `1.0`  | How fast to play the sound data; also affects pitch.  |  
#### Configure New Playbacks via Keyword Arguments
Arcade’s helper functions for playing sound also accept keyword arguments for configuring playback. As mentioned above, the names of these keywords are similar or identical to those of properties on [`Player`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player "\(in pyglet v2.1\)"). See the following to learn more:
  * [`arcade.play_sound()`](../api_docs/api/sound.html#arcade.play_sound "arcade.play_sound")
  * [`arcade.Sound.play()`](../api_docs/api/sound.html#arcade.Sound.play "arcade.Sound.play")
  * [Sound Speed Demo](../example_code/sound_speed_demo.html#sound-speed-demo)


## Cross-Platform Compatibility
The sections below cover the easiest approach to compatibility.
You can try other options if you need to. Be aware that doing so requires grappling with the many factors affecting audio compatibility:
  1. The formats which can be loaded
  2. The features supported by playback
  3. The hardware, software, and settings limitations on the first two
  4. The interactions of project requirements with all of the above


### The Most Reliable Formats & Features
For most users, the best approach to formats is:
  * Use 16-bit PCM Wave (`.wav`) files for [sound effects](performance_tips.html#sound-loading-modes-static)
  * Use MP3 files for [long background audio like music](performance_tips.html#sound-loading-modes-streaming)


As long as a user has working audio hardware and drivers, the following basic features should work:
  1. [Loading Sounds](#sound-basics-loading) sound effects from Wave files
  2. [Playing Sounds](#sound-basics-playing) and [Stopping Sounds](#sound-basics-stopping)
  3. [Adjusting playback volume and speed of playback](#sound-intermediate-playback)


Advanced functionality or subsets of it may not, especially [positional audio](#sound-other-libraries-pyglet-positional). To learn more, see the rest of this page and [pyglet’s guide to supported media types](https://pyglet.readthedocs.io/en/latest/programming_guide/media.html#supported-media-types).
#### Why 16-bit PCM Wave for Effects?
Storing sound effects as 16-bit PCM `.wav` ensures all users can load them:
  1. pyglet [has built-in in support for this format](#sound-compat-loading)
  2. [Some platforms can only play 16-bit audio](#sound-compat-playback)


The files must also be mono rather than stereo if you want to use [positional audio](#sound-other-libraries-pyglet-positional).
Accepting these limitations is usually worth the compatibility benefits, especially as a beginner.
#### Why MP3 For Music and Ambiance?
  1. Nearly every system which can run Arcade has a supported MP3 decoder.
  2. MP3 files are much smaller than Wave equivalents per minute of audio, which has multiple benefits.


See the following to learn more:
  * [Loading In-Depth](#sound-compat-loading)
  * [Pyglet’s Supported Media Types](https://pyglet.readthedocs.io/en/latest/programming_guide/media.html#supported-media-types)


#### Converting Audio Formats
Don’t worry if you have a great sound in a different format.
There are multiple free, reliable, open-source tools you can use to convert existing audio. Two of the most famous are summarized below.  
| Name & Link for Tool  | Difficulty  | Summary  |  
| --- | --- | --- |  
| [Audacity](https://www.audacityteam.org/)  | Beginner [[5]](#linuxlame)  | A free GUI application for editing sound  |  
| [FFmpeg](https://ffmpeg.org/)’s command line tool  | Advanced  | Powerful media conversion tool included with the library  |  
Most versions of these tools should handle the following common tasks:
  * Converting audio files from one encoding format to another
  * Converting from stereo to mono for use with [positional audio](#sound-other-libraries-pyglet-positional).


To integrate FFmpeg with Arcade as a decoder, you must use FFmpeg version 4.X, 5.X, or 6.X. See [Loading In-Depth](#sound-compat-loading) to learn more.
### Loading In-Depth
There are 3 ways Arcade can read audio data through pyglet:
  1. The built-in pyglet `.wav` loading features
  2. Platform-specific components or nearly-universal libraries
  3. Supported cross-platform media libraries, such as PyOgg or [FFmpeg](https://ffmpeg.org/)


To load through FFmpeg, you must install FFmpeg 4.X, 5.X, or 6.X. This is a requirement imposed by pyglet. See [pyglet’s notes on installing FFmpeg](https://pyglet.readthedocs.io/en/latest/programming_guide/media.html#ffmpeg-installation) to learn more.
#### Everyday Usage
In practice, Wave is universally supported and MP3 nearly so. [[6]](#mp3linux)
Limiting yourself to these formats is usually worth the increased compatibility doing so provides. Benefits include:
  1. Smaller download & install sizes due to having fewer dependencies
  2. Avoiding binary dependency issues common with PyInstaller and Nuitka
  3. Faster install and loading, especially when using MP3s on slow drives


These benefits become even more important during game jams.
### Backends Determine Playback Features
As with formats, you can maximize compatibility by only using the lowest common denominators among features. The most restrictive backends are:
  * Mac’s only backend, an OpenAL version limited to 16-bit audio
  * PulseAudio on Linux, which lacks support for common features such as [positional audio](#sound-other-libraries-pyglet-positional).


On Linux, the best way to deal with the PulseAudio backend’s limitations is to [install OpenAL](https://pyglet.readthedocs.io/en/latest/programming_guide/media.html#openal). It will often already be installed as a dependency of other packages.
Other differences between backends are less drastic. Usually, they will be things like the specific positional features supported and the maximum number of simultaneous sounds.
See the following to learn more:
  * [Pyglet’s Audio Backends](https://pyglet.readthedocs.io/en/latest/programming_guide/media.html#choosing-the-audio-driver)
  * [Other Sound Libraries](#sound-other-libraries)


### Choosing the Audio Backend
By default, Arcade will try pyglet audio back-ends in the following order until it finds one which loads:
  1. `"openal"`
  2. `"xaudio2"`
  3. `"directsound"`
  4. `"pulse"`
  5. `"silent"`


You can override through the `ARCADE_SOUND_BACKENDS` [environment variable](https://www.twilio.com/blog/environment-variables-python). The following rules apply to its value:
  1. It must be a comma-separated string
  2. Each name must be an audio back-ends supported by pyglet
  3. Spaces do not matter and will be ignored


For example, you could need to test OpenAL on a specific system. This example first tries OpenAL, then gives up instead using fallbacks.

```
ARCADE_SOUND_BACKENDS="openal,silent" python mygame.py

```

Please see the following to learn more:
  * [pyglet’s audio driver documentation](https://pyglet.readthedocs.io/en/latest/programming_guide/media.html#choosing-the-audio-driver)
  * [Working with Environment Variables in Python](https://www.twilio.com/blog/environment-variables-python)


## Other Sound Libraries
Advanced users may have reasons to use other libraries to handle sound.
### Using Pyglet
The most obvious external library for audio handling is pyglet:
  * It’s guaranteed to work wherever Arcade’s sound support does.
  * It offers far better control over media than Arcade
  * You may have already used parts of it directly for [Intermediate-Level Playback Control](#sound-intermediate-playback)


Note that the [`arcade.Sound.source`](../api_docs/api/sound.html#arcade.Sound.source "arcade.Sound.source") attribute holds a [`pyglet.media.Source`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.Source "\(in pyglet v2.1\)"). This means you can start off by cleanly using Arcade’s resource and sound loading with pyglet features as needed.
#### Notes on Positional Audio
Positional audio is a set of features which automatically adjust sound volumes across the channels for physical speakers based on in-game distances.
Although pyglet exposes its support for this through its [`Player`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player "\(in pyglet v2.1\)"), Arcade does not currently offer integrations. You will have to do the setup work yourself.
If you already have some experience with Python, the following sequence of links should serve as a primer for trying positional audio:
  1. [Why 16-bit PCM Wave for Effects?](#sound-compat-easy-best-effects)
  2. [Backends Determine Playback Features](#sound-compat-playback)
  3. The following sections of pyglet’s media guide:
    1. [Controlling playback](https://pyglet.readthedocs.io/en/latest/programming_guide/media.html#controlling-playback)
    2. [Positional audio](https://pyglet.readthedocs.io/en/latest/programming_guide/media.html#positional-audio)
  4. [`pyglet.media.player.Player`](https://pyglet.readthedocs.io/en/latest/modules/media.html#pyglet.media.player.Player "\(in pyglet v2.1\)")’s full documentation


### External Libraries
Some users have reported success with using [PyGame CE](https://pyga.me/) or [SDL2](https://www.libsdl.org/) to handle sound. Both these and other libraries may work for you as well. You will need to experiment since this isn’t officially supported.
