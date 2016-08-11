from gmusicapi import Mobileclient

from tqdm import tqdm
import os , pickle , threading , requests , shutil 

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mutagen.id3

class Downloader:

	def __init__( self , username1=None ,  password1=None , baseDirectory=None , pickleLIBFilePath=None ):

		self.api = Mobileclient()
		if username1 is not None:
			if password1 is not None:
				self.login( username1 , password1 )

		if self.isLoggedIn() == True:
			print("Logged In")
		else:
			raise Exception


		# Setup Default Save Location
		if baseDirectory is not None:
			self.homeDIR = baseDirectory
			self.libDIR = os.path.join( self.homeDIR , 'GMusicLocalLibraryPOOL' )
		else:
			self.homeDIR = os.path.expanduser("~")
			self.libDIR = os.path.join( self.homeDIR , 'GMusicLocalLibraryPOOL' )
		

		if not os.path.exists(self.libDIR):
			os.makedirs(self.libDIR)


		self.stations = {}
		self.workingPlaylistOBJ = {}
		self.needToDownloadSongs = None	

		self.Full = True

		#self.playlists = None
		self.localLibrary = None
		#self.initializePlaylists()
		if pickleLIBFilePath is not None:
			self.initializeLocalLibrary(pickleLIBFilePath)
		else:
			self.initializeLocalLibrary()


	def isLoggedIn(self):

		x = self.api.is_authenticated()
		return x

	def login(self , userN , passW ):

		self.api.login( userN , passW , Mobileclient.FROM_MAC_ADDRESS )

	def initializePlaylists(self):

		try:
			self.playlists = pickle.load( open( libDIR + "libPlaylists.p" , "rb" ) )
		except:
			print("Recreating Playlists Save File")
			self.playlists = {}
			playlists['EDM'] = []
			playlists['Relaxing'] = []
			playlists['EDM'].append('4b40425b-2e11-388f-aeed-ea736b88662c')
			pickle.dump( playlists , open( libDIR + "libPlaylists.p" , "wb" ) )

	def initializeLocalLibrary(self , pickleLIBFilePath=None):

		defaultPath = os.path.join( self.libDIR , "libDatabasePOOL.p" )

		if pickleLIBFilePath is not None:
			defaultPath = pickleLIBFilePath
			print("DefaultPath .p file = " + defaultPath)

		try:
			self.localLibrary = pickle.load( open( os.path.join( self.libDIR , "libDatabasePOOL.p" ) , "rb" ) )
			print("Loaded libDatabasePOOL.p")
		except:
			self.localLibrary = {}
			pickle.dump( self.localLibrary , open( defaultPath , "wb" ) )
			print("Recreated LibraryPOOL Save File")

		print( "LocalLibary Size = " + str( len( self.localLibrary ) ) )

	def getMyStations(self):

		stations = self.api.get_all_stations()
		for x in stations:
			self.stations[x['id']] = x['name']

	def printAvailableStations(self):

		for x in self.stations:
			print( str(x) + " = " + self.stations[x] )

	def downloadStationToPOOL( self , stationID ):

		rawPlaylist = self.api.get_station_tracks( stationID , 25 )

		self.needToDownloadSongs = {}

		for x in rawPlaylist:
			if x['nid'] in self.localLibrary:
				print("Already in LibraryPOOL")
			else:
				self.Full = False
				print( str(x['nid']) + " == Not in library ... need to download" )
				self.needToDownloadSongs[x['nid']] = { 'stationID': stationID , 'trackName': x['title'] , 'artistName': x['artist'] , 'albumID': x['albumId'] , 'artURL': x['albumArtRef'][0]['url'] }
				

		p1 = threading.Thread( target=self.getMP3FromSongIDS , args=( stationID , ) )
		p1.start()
		p1.join()

		if self.Full == False:
			self.Full = True
			print( "LocalLibary Size = " + str( len( self.localLibrary ) ) )
			self.downloadStationToPOOL( stationID )

	def getMP3FromSongIDS( self , stationID ):
		
		a1 = 1
		for x in self.needToDownloadSongs:

			self.saveMP3ToLibraryPOOL( x , self.needToDownloadSongs[x]['trackName'] , self.needToDownloadSongs[x]['artistName'] , stationID )
			self.localLibrary[x] = self.needToDownloadSongs[x]
			pickle.dump( self.localLibrary , open( os.path.join( self.libDIR , "libDatabasePOOL.p" ) , "wb" ) )
			print("added [" + str(a1) + " of " + str(len(self.needToDownloadSongs)) + "] songs to localLibrary")
			a1 = a1 + 1
			
	def saveMP3ToLibraryPOOL( self , songID , name , artist , stationID ):

		albumName = self.stations[stationID]
		
		wURL = self.api.get_stream_url( songID , self.api.android_id , 'hi' )
		fN = os.path.join( self.libDIR , songID + ".mp3" )

		response1 = requests.get( wURL , stream=True )
		with open( fN , 'wb' ) as f:
			for data in tqdm( response1.iter_content(chunk_size=524288) ):
				f.write(data)		


		m3 = MP3( fN , ID3=EasyID3 )
		m3.add_tags( ID3=EasyID3 )
		m3["title"] = name
		m3['artist'] = artist
		m3['album'] = albumName
		m3['organization'] = stationID 
		m3.save()

	def extractSinglePlaylistFromPOOL( self , stationID , destinationDIR , onlyCopyNotExtract=False ):

		if not os.path.exists(destinationDIR):
			os.makedirs(destinationDIR)

		if onlyCopyNotExtract == True:
			for key , value in self.localLibrary.items():
				try:
					if value['stationID'] == stationID:
						#print( "found --> " + self.localLibrary[key]['trackName'] + " in ... " + str(stationID) )
						fN = str(key) + ".mp3" 
						shutil.copy( os.path.join( self.libDIR , fN ) , os.path.join( destinationDIR , fN ) )
				except:
					pass		

		else:
			for key , value in self.localLibrary.items():
				try:
					if value['stationID'] == stationID:
						#print( "found --> " + self.localLibrary[key]['trackName'] + " in ... " + str(stationID) )
						fN = str(key) + ".mp3" 
						shutil.move( os.path.join( self.libDIR , fN ) , os.path.join( destinationDIR , fN ) )
				except:
					pass



