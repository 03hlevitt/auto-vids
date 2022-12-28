from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo


def upload(file, title, description, category, keywords,
       privacyStatus, thumb):
    # loggin into the channel
    channel = Channel()
    channel.login("client_secret.json", "credentials.storage")

    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path=file)

    # setting snippet
    video.set_title(title)
    video.set_description(description)
    video.set_tags([keywords.split(",")])
    video.set_category(category)
    video.set_default_language("en-US")

    # setting status
    video.set_embeddable(True)
    video.set_license("creativeCommon")
    video.set_privacy_status(privacyStatus)
    video.set_public_stats_viewable(True)

    # setting thumbnail
    video.set_thumbnail_path(thumb)

    # uploading video and printing the results
    video = channel.upload_video(video)
    print(video.id)
    print(video)

    # liking video
    video.like()