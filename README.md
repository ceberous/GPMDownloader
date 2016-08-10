# GPMDownloader

## 1.) Login
myD = GMDownloader()

## 2.) Fetch User's Stations
myD.getMyStations()
myD.printAvailableStations()

## 3.) Download a Station
wID = '9673a6e8-de88-3c98-b81e-b3a1a4d30c89'
myD.downloadStationToPOOL( wID )
myD.extractSinglePlaylistFromPOOL( wID , os.path.join( myD.libDIR , wID  )  )
