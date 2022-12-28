from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
import ffmpeg
import os


def compress_video(video_full_path, output_file_name, target_size=1.5):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()
    return output_file_name


def upload(file, title, description, category, keywords,
           privacyStatus, thumb):
    # loggin into the channel
    channel = Channel()
    channel.login("client_secrets.json", "credentials.storage")

    # setting up the video that is going to be uploaded
    # compressed_file_name = "c_" + file
    # compressed_file = compress_video(file, compressed_file_name)
    video = LocalVideo(file_path=file)

    # setting snippet
    video.set_title(title)
    video.set_description(description)
    video.set_tags(keywords)
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
