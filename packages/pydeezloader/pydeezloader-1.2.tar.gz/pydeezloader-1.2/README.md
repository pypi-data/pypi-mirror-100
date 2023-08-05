# pydeezloader

This project has been created to download songs, albums or playlists with Spotify or Deezer link from Deezer.

# Disclaimer

- I am not responsible for the usage of this program by other people.
- I do not recommend you doing this illegally or against Deezer's terms of service.

* ### OS's Supported ###
	![Linux Support](https://img.shields.io/badge/Linux-Support-brightgreen.svg)
	![macOS Support](https://img.shields.io/badge/macOS-Support-brightgreen.svg)
	![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)

* ### Installation ###
```bash
$ pip install git+https://github.com/TheDeezLoader/pyDeezloader.git
```

# CLI interface

```bash
$ deez-dw -h
```
	usage: deez-dw [-h] [-l LINK] [-s SONG] [-a ARTIST] [-o OUTPUT]
                     [-q QUALITY] [-rq RECURSIVE_QUALITY]
                     [-rd RECURSIVE_DOWNLOAD] [-g NOT_GUI] [-z ZIP]
                     setting

## OPTIONS
	-h, --help            show this help message and exit
  	-l LINK, --link LINK  Deezer or Spotify link for download
  	-s SONG, --song SONG  song name
  	-a ARTIST, --artist ARTIST
                       	artist song
  	-o OUTPUT, --output OUTPUT
                        Output folder
  	-q QUALITY, --quality QUALITY
                        Select download quality between FLAC, 320, 256, 128
  	-rq RECURSIVE_QUALITY, --recursive_quality RECURSIVE_QUALITY
                        If choosen quality doesn't exist download with best
                        possible quality (True or False)
  	-rd RECURSIVE_DOWNLOAD, --recursive_download RECURSIVE_DOWNLOAD
                        If the song has already downloaded skip (True or
                        False)
  	-g NOT_GUI, --not_gui NOT_GUI
                        Show the little not_gui (True or False)
  	-z ZIP, --zip ZIP     If is an album or playlist link create a zip archive
                        (True or False)

# WEB interface

```bash
$ deez-web
```

## SETTINGS
	[login]
	token = deezer_arl_token

Use the setting.ini file for deez-dw and deez-web only

# Library

### Initialize

```python
import pydeezloader

download = pydeezloader.Login("YOUR ARL TOKEN")
```

### Download song
Download track by Spotify link

```python
download.download_trackspo(
	"Insert the Spotify link of the track to download",
	output = "Output folder, ending with /",
	quality = "MP3_320",
	recursive_quality = False,
	recursive_download = False
	not_interface = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality=True if selected quality isn't avalaible download with best quality possible
#recursive_download=True if song has already been downloaded don't ask for download it again
#not_interface=False if you want too see no download progress
```

Download track by Deezer link
```python
download.download_trackdee(
	"Insert the Deezer link of the track to download",
	output = "Output folder, ending with /",
	quality = "MP3_320",
	recursive_quality = False,
	recursive_download = False,
	not_interface = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
```

### Download album
Download album by Spotify link
```python
download.download_albumspo(
	"Insert the Spotify link of the album to download",
	output = "Output folder, ending with /",
	quality = "MP3_320",
	recursive_quality = True,
	recursive_download = True,
	not_interface = False,
	zips = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
#zips = True create a zip with all album songs
```

Download album from Deezer link
```python
download.download_albumdee(
	"Insert the Deezer link of the album to download",
	output = "Output folder, ending with /",
	quality = "MP3_320",
	recursive_quality = True,
	recursive_download = True,
	not_interface = False,
	zips = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
#zips = True create a zip with all album songs
```

### Download playlist

Download playlist by Spotify link
```python
download.download_playlistspo(
	"Insert the Spotify link of the album to download",
	output = "Output folder, ending with /",
	quality = "MP3_320",
	recursive_quality = True,
	recursive_download = True,
	not_interface = False,
	zips = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
#zips = True create a zip with all album songs
```

Download playlist from Deezer link
```python
download.download_playlistdee(
	"Insert the Deezer link of the album to download",
	output = "Output folder, ending with /",
	quality = "MP3_320",
	recursive_quality = True,
	recursive_download = True,
	not_interface = False,
	zips = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
#zips = True create a zip with all album songs
```

### Download name

Download by name
```python
download.download_name(
	artist = "Eminem",
	song = "Berzerk",
	output = "Output folder, ending with /",
	quality = "MP3_320",
	recursive_quality = False,
	recursive_download = False,
	not_interface = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
```
