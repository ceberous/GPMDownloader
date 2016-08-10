from distutils.core import setup

setup(

	name	= 'GMDownloader',
	packages = [ 'GMDownloader' ],
	version	= '0.1',
	description = 'GM Playlist Downloader',
	author = 'ceberous',
	author_email = 'cerbus.collin@gmail.com',
	url = 'https://github.com/ceberous/GPMDownloader.git',
	download_url = 'https://github.com/ceberous/GPMDownloader/tarball/0.1',
	keywords = [ 'google' , 'play' , 'music' , 'gmusicapi' , 'downloader' , 'playlist' ],
	classifier = [],
	install_requires = [ 'gmusicapi' , 'tqdm' ]

)