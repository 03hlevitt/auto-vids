import openai

from videos import collate_media, create_movie, upload_and_clean
import click


@click.command()
@click.option('--length', help="video length", default=5)
@click.argument('subject')
def generate_upload_video(length, subject):
    try:
        mp3_list, jpg_list = collate_media(subject, length)
        thumb = jpg_list[0]
        movie_file_name, title = create_movie(mp3_list, jpg_list, subject)
        upload_and_clean(thumb, movie_file_name, title, subject)
    except openai.error.AuthenticationError as e:
        message = f"Update your api key ! \n{e}"
        click.echo(message)

if __name__ == "__main__":
    generate_upload_video()
