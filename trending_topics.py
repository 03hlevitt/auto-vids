import tweepy

api_key = "BIXCuwNrC21xFvpPDT0rgGT1e"
api_secret = "DKsxDgInV7fIikoH08WHqDQbTqSRy64UOTqEmUQVymMZyWkekl"
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAA%2BHkwEAAAAAYsmrkCzLfCy2nddCWxyKDEC1Ai0%3DSs612qboNgZss1m9d4IJz0LjXfJ59FugU37V52W9OpyvaEzuhC"
access_token = "1608133066458894339-oAjfYkmLfVwb7n6H38B0C5zwY1f2S6"
access_token_secret = "4ydTvxU3dC6w3b9OxVpuxoiOb8E3pByNIpM9T920rFFwS"

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

trends = api.get_place_trends(23424975, exclude='hashtags')

trend_names = [trend['name'] for trend in trends[0]['trends']]

i = 0
while i < len(trend_names):
    print(trend_names[i])
    i += 1
