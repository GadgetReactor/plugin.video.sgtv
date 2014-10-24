import sys, xbmc, xbmcgui, xbmcplugin, urllib, urllib2, urlparse, re, string, os, traceback, time, datetime, xbmcaddon
import simplejson as json

__addon__ = "SG!TV"
__author__ = 'GadgetReactor'
__url__ = "http://www.gadgetreactor.com/portfolio/sgtv"

settings = xbmcaddon.Addon(id='plugin.video.sgtv')

THUMBNAIL_PATH = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media')
#channel-icons

def open_url(url):
	retries = 0
	while retries < 3:
		try:
			req = urllib2.Request(url)
			content = urllib2.urlopen(req)
			data=content.read()
			content.close()
			data = str(data).replace('\n','')
			return data
		except urllib2.HTTPError,e:
			print __addon__ + ' - Error code: ', e.code
			if e.code == 500:
				dialog = xbmcgui.Dialog()
				ok = dialog.ok(__addon__, 'Sorry, the server seems to be down. Please try again later')
				main()
				return "data"
			retries += 1
			print __addon__ + ' - Retries: ' + str(retries)
			time.sleep(2)
			continue
		else:
			break
	else:
		print 'Fetch of ' + url + ' failed after ' + str(retries) + 'tries.'


		
def main():
	
	li=xbmcgui.ListItem("1. Newest", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'newest.png'))
	u=sys.argv[0]+"?mode=4&channel=new&show=all"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)

	li=xbmcgui.ListItem("Channel 5", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'channel5.jpg'))
	u=sys.argv[0]+"?mode=3&channel=channel5"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)

	li=xbmcgui.ListItem("Channel 8",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'channel8.jpg'))
	u=sys.argv[0]+"?mode=3&channel=channel8"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)
	
	li=xbmcgui.ListItem("4. Channel U",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'channelu.jpg'))
	u=sys.argv[0]+"?mode=3&channel=channelu"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)

	li=xbmcgui.ListItem("5. Okto",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'okto.png'))
	u=sys.argv[0]+"?mode=3&channel=okto"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)

	li=xbmcgui.ListItem("6. Suria",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'suria.gif'))
	u=sys.argv[0]+"?mode=3&channel=suria"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)

	li=xbmcgui.ListItem("7. Vasantham",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'vasantham.jpg'))
	u=sys.argv[0]+"?mode=3&channel=vasantham"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)

	li=xbmcgui.ListItem("CNA",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'cna.png'))
	u=sys.argv[0]+"?mode=1&user=channelnewsasia"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)

	li=xbmcgui.ListItem("Viddsee",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'viddsee.png'))
	u=sys.argv[0]+"?mode=6&page=0&type=popular"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)

	li=xbmcgui.ListItem("WahBanana",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'wahbanana.jpg'))
	u=sys.argv[0]+"?mode=1&user=wahbanana"
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)
	
	xbmc.executebuiltin("Container.SetViewMode(500)")
	xbmcplugin.endOfDirectory(addon_handle)

def channel_shows(channel):
	data=open_url("http://xin.msn.com/en-sg/video/catchup/")		
	showlist  = re.compile('<div class="list"  data-module-id="homepage\|%s\|Tab\|(.*?)\|.+?:&quot;(.+?)&quot' % (channel)).findall(data)

	for show, thumb in showlist:
		image = 'http:'+ thumb.replace('&amp;','&')
		li=xbmcgui.ListItem(htmlParse(show), iconImage="DefaultFolder.png", thumbnailImage=image)
		u=sys.argv[0]+"?mode=4&channel="+urllib.quote_plus(channel)+"&show="+urllib.quote_plus(show)
		xbmcplugin.addDirectoryItem(addon_handle,u,li,True)
		
	xbmcplugin.setContent(addon_handle, 'tvshows')
	xbmc.executebuiltin("Container.SetViewMode(500)")
	xbmcplugin.endOfDirectory(addon_handle)

def channel_youtube(user):
	youtube_url = "https://www.youtube.com/user/" + user + "/videos"
	data=open_url(youtube_url)
	showlist  = re.compile('dir="ltr" title="(.+?)".+?watch\?v=(.+?)&amp;.+?">(.+?)</a>.+?<li>(.+?)</li><li class="yt-lockup-deemphasized-text">(.+?)</li>').findall(data)
	
	if user is "channelnewsasia":
		li=xbmcgui.ListItem("CNA @ Live Broadcast", iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'cna.png'))
		li.setInfo( type="Video", infoLabels={ "Title": "CNA @ Live Broadcast" } )
		li.setProperty('IsPlayable', 'true')
		u='http://cna_hls-lh.akamaihd.net/i/cna_en@8000/index_584_av-b.m3u8?sd=10&dw=50&rebase=on&e=870c0c22a42f4c5a'
		xbmcplugin.addDirectoryItem(addon_handle,u,li)
	
	for title, video_id, desc, views, air_date in showlist:
		image = "http://img.youtube.com/vi/" + video_id + "/0.jpg"
		#image = "http://i.ytimg.com/vi_webp/" + video_id + "/mqdefault.webp"
		li=xbmcgui.ListItem(htmlParse(title), iconImage="DefaultVideo.png", thumbnailImage=image)
		li.setInfo( type="Video", infoLabels={ "Title": title , "Plot" : desc + "\n" + air_date + "\n" + views } )
		li.setProperty('IsPlayable', 'true')
		u="plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=" + video_id
		xbmcplugin.addDirectoryItem(addon_handle,u,li)
		
	xbmcplugin.endOfDirectory(addon_handle)

def playVimeo(url):
	videodata=open_url(url)
	match=re.compile('"profile".+?"url":"(.+?)",.+?bitrate":(.+?),"').findall(videodata)
	x=0
	for url_quality, bitrate in match:
		if int(bitrate) > x: 
			video_url=url_quality
			x=int(bitrate)	
	listitem = xbmcgui.ListItem(path=video_url)
	listitem.setInfo(type='Video', infoLabels= xbmc.getInfoLabel("ListItem.InfoLabel"))
	xbmcplugin.setResolvedUrl(addon_handle, succeeded=True, listitem=listitem)

def channel_viddsee(page, type):
#	type examples: | popular | genre/drama | genre/comedy |  
	viddsee_url = "https://www.viddsee.com/v1/browse/"+type+"?current_page="+page+"&per_page=12"
	req = urllib2.Request(viddsee_url, None, {'user-agent':'Mozilla/Firefox'})
	opener = urllib2.build_opener()
	f = opener.open(req)
	data = json.load(f)	
	i = 0
	while (i < 12):		
		image = data["videos"][i]["thumbnail_url"]
		li=xbmcgui.ListItem(data["videos"][i]["title"], iconImage="DefaultVideo.png", thumbnailImage=image)
		li.setInfo( type="Video", infoLabels=	{
												"title": data["videos"][i]["title"], 
												"plot": htmlParse(data["videos"][i]["description_long"]),
												"plotoutline": data["videos"][i]["description_short"],
												"genre": data["videos"][i]["genres"],
												"year": data["videos"][i]["year"],
												"votes": data["videos"][i]["rating"]["ext_likes"],
												"rating": data["videos"][i]["rating"]["rating_like"],
												"duration": data["videos"][i]["duration"],													
												})
		video_url = data["videos"][i]["embed_url"];
		li.setProperty('IsPlayable', 'true')
		li.setProperty('Fanart_Image', data["videos"][i]["photo_large_url"])
		
		if "vimeo" in video_url:
			u=sys.argv[0]+"?mode=7&url="+urllib.quote_plus(video_url)
		elif "youtube" in video_url:
			video_url = video_url.split('embed/')[1]
			u="plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=" + video_url
		else:
			u = ""
		xbmcplugin.addDirectoryItem(addon_handle,u,li)			
		i = i + 1
		
	li=xbmcgui.ListItem("Next Page", iconImage="DefaultFolder.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, "viddsee.png"))
	page = str(int(page)+1)
	u=sys.argv[0]+"?mode=6&page="+page+"&type="+type
	xbmcplugin.addDirectoryItem(addon_handle,u,li,True)
	xbmcplugin.endOfDirectory(addon_handle)	
	
def channel_episodes(channel, show):
	data=open_url("http://xin.msn.com/en-sg/video/catchup/")
	if "new" in channel:
		episodelist = re.compile('<li.+?href="(.+?)".+?:&quot;(.+?)&quot.+?<h4>(.+?)</h4>.+?"duration">(.+?)<.+?</li>').findall(data)	

	else:
		episodechunk  = re.compile('<div class="list"  data-module-id="homepage\|%s\|Tab\|%s(.+?)(<div data-tabkey|</main>)' % (channel, show)).search(data).group(1)
		episodelist = re.compile('<li.+?href="(.+?)".+?:&quot;(.+?)&quot.+?<h4>(.+?)</h4>.+?"duration">(.+?)<.+?</li>').findall(episodechunk)	

	for episode_url, thumb, title, time in episodelist:
		episode_url = "http://xin.msn.com" + episode_url
		title=title.strip()
		title=htmlParse(title)									
		
		image = 'http:'+ thumb.replace('&amp;','&')
		li=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=image)
		li.setInfo('Video', infoLabels={'Title': title, 'Duration':time})
		u=sys.argv[0]+"?mode=0&title="+urllib.quote_plus(title)+"&url="+urllib.quote_plus(episode_url)+"&channel="+urllib.quote_plus(channel)
		xbmcplugin.addDirectoryItem(addon_handle,u,li,False)

	xbmc.executebuiltin("Container.SetViewMode(500)")	
	xbmcplugin.endOfDirectory(addon_handle)		

def htmlParse(str):
	str=str.replace('\\x3a', ':')
	str=str.replace('\\x2f', '/')	
	str=re.sub('&amp;','&',str)
	str=re.sub('&#39;',"'",str)
	str=str.replace('&quot;', '"')
	str=str.replace('&#187;', '-')
	str=str.replace('&#160;', ':')
	str=re.sub(r'<.*?>','', str)
	return str
			
def playVideo(url, title):
		progress = xbmcgui.DialogProgress()
		progress.create('SG!TV', 'Finding Stream')
		progress.update(0, "SG!TV", "Loading link")
		videodata=open_url(url)
		progress.update(25, "SG!TV", "Loading link")
		match=re.compile("{&quot;formatCode&quot;:&quot;(...)&quot;,&quot;url&quot;:&quot;(.+?)&quot;,").findall(videodata)
		max = len(match)
		progress.update(50, "SG!TV", "Processing information")
		x=0
		for formatcode, url_quality in match:
			if int(formatcode) > x: 
				video_url=url_quality
				x=int(formatcode)
		progress.update(70, "SG!TV", "Finding best quality link" )		
		video_url=htmlParse(video_url)
		listitem = xbmcgui.ListItem(title, iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ))
		progress.update(100, "", "Preparing to play" )
		progress.close()
		xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play(video_url, listitem)
		
def timecheck():
	from datetime import datetime
	from datetime import timedelta
	start_time = datetime.now()

	# function
	
	dt = datetime.now() - start_time
	ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
	return ms

	
args = urlparse.parse_qs(sys.argv[2][1:])

mode = args.get('mode', None)
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'tvshows')

if mode==None:
	name = 'Channels'
	main()
	
elif mode[0]=='0':
	url = args['url'][0]
	title = args['title'][0]
	playVideo(url, title)
elif mode[0]=='1':
	user = args['user'][0]
	channel_youtube(user)
elif mode[0] =='3':
	channel = args['channel'][0]
	channel_shows(channel)
elif mode[0]=='4':
	channel = args['channel'][0]
	show = args['show'][0]
	channel_episodes(channel, show)
elif mode[0]=='6':
	page = args['page'][0]
	type = args['type'][0]
	channel_viddsee(page, type)
elif mode[0]=='7':
	url = args['url'][0]
	playVimeo(url)