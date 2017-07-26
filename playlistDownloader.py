from gmusicapi import Mobileclient
import gMusicLogin

from tqdm import tqdm
import sys , os , time , requests

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mutagen.id3

api = Mobileclient()
try:
	api.login( gMusicLogin.getUser() , gMusicLogin.getPass() , Mobileclient.FROM_MAC_ADDRESS )		
except:
	sys.exit("Login Failed")

while api.is_authenticated() == False:
	time.sleep(.1)

wPlaylists = None

def removeNonASCII(text):
    return ''.join(i for i in text if ord(i)<128)

def getPlaylists():
	global wPlaylists
	wPlaylists = api.get_all_playlists()
	for idx , x in enumerate( wPlaylists ):
		x['name'] = removeNonASCII( x['name'] )
		print( str( idx ) + " = " + x['name'] )

def getSelection():
	global wPlaylists
	wSel = int( input( "\nchoose a number --> " ) )
	downloadPlaylist( wSel )

def downloadPlaylist( wSel ):
	
	global wPlaylists

	wContents = api.get_shared_playlist_contents( wPlaylists[ wSel ]['shareToken'] )
	for x in wContents:
		wTID = removeNonASCII( x['track']['title'] )
		print( str( x['trackId'] ) + " = " + wTID )

	w_Album = {}
	w_Album['name'] = removeNonASCII( wPlaylists[ wSel ]['name'] )
	print("\n")
	print(w_Album['name'])
	w_Album['songs'] = []

	wIDX = 1
	for item in wContents:
		w_Item = {}
		w_Item['nid'] = item['trackId']
		w_Item['trackNumber'] = str( wIDX ) 
		w_Item['title'] = removeNonASCII( item['track']['title'])
		w_Item['artist'] = removeNonASCII(item['track']['artist'])
		w_Item['artURL'] = item['track']['albumArtRef'][0]['url']
		w_Album['songs'].append( w_Item )
		wIDX = wIDX + 1

	c_Length = len(w_Album['songs'])
	w_Index = 1
	for item in w_Album['songs']:

		print( "Downloading [" + str(w_Index) + "] of " + str(c_Length ) )

		w_URL = api.get_stream_url( item['nid'] , api.android_id , 'hi' )
		fN = os.path.join( os.getcwd() , item['title'] + ".mp3" )

		response1 = requests.get( w_URL , stream=True )
		
		with open( fN , 'wb' ) as f:
			for data in tqdm( response1.iter_content(chunk_size=524288) ):
				f.write(data)		

		m3 = MP3( fN , ID3=EasyID3 )

		EasyID3.RegisterTXXXKey("comment", "comment")
		EasyID3.RegisterTXXXKey("albumartist", "albumartist")

		m3.add_tags( ID3=EasyID3 )

		print( w_Item['trackNumber'] )

		m3['title'] = item['title']
		m3['trackNumber'] = item['trackNumber']
		m3['artist'] = item['artist']
		m3['albumartist'] = item['artist']
		m3['album'] = w_Album['name']
		m3['comment'] = item['artURL'] 
		m3.save()

		w_Index = w_Index + 1



getPlaylists()
getSelection()
