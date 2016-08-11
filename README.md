# Google Music RadioStation/Playlist Downloader Using https://github.com/simon-weber/gmusicapi

# GPMDownloader

pip3 install gDownloader

from gDownloader import Downloader

## 1.) Fill in Login Details with "all-access" google-play-music account

myD = Downloader( "username" , "password" , customLibrarySavePATH=None , customLibraryPickleFilePATH=None  )

## 2.) Get User's RadioStations/Playlists

myD.getMyStations()

myD.printAvailableStations()

## 3.) Download and Save to Folder

wStationID = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

myD.downloadStationToPOOL( wStationID )

myD.extractSinglePlaylistFromPOOL( wStationID , os.path.join( myD.libDIR , wStationID  )  )
