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


#### so the only confusing part is that you need to run step 1 and 2 together before you add in step 3. Unless you somehow know your stationID before hand
