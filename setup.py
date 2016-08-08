def setup():

	name	= 'GMDownloader'
	version	= '0.1'
	description = 'GM Playlist Downloader'
	long_description=README
	url = 'https://github.com/ceberous/GMDownloader'
	author = 'ceberous'
	author_email = 'cerbus.collin@gmail.com'

	packages = [ 'main.py' ]

	include_package_data = True

	install_requires[ 'gmusicapi' , 'tqdm' ]