import openai

import requests

from gtts import gTTS

import os

import glob

from moviepy.editor import *
from upload import upload

openai.api_key = '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'

# Animals= "Alligator,Anteater,Ape,Armadillo,Baboon,Bat,Bear,Beetle,Bongo,Camel,Centipede,Chameleon,Cheetah,Clownfish,Coati,Cockatoo,Crane,Crocodile,Deer,Drill,Duck,Eagle,Echidna,Elephant,Elk,Flamingo,Fox,Frigatebird,Gila monster,Giraffe,Gorilla,Guanaco,Hamster,Hawk,Hedgehog,Hermit crab,Hippo,Hippopotamus,Horse,Hummingbird,Hyena,Iguana,Impala,Jaguar,Kangaroo,Kingfisher,Kite,Kiwi,Koala,Komodo dragon,Kudu,Lemur,Leopard,Lion,Lionfish,Lizard,Lynx,Mole,Monkey,Newt,Nilgai,Numbat,Okapi,Opossum,Orangutan,Ostrich,Owl,Panda,Panther,Parrot,Peacock,Pelican,Penguin,Pigeon,Platypus,Puffin,Quail,Rabbit,Rattlesnake,Red panda,Reindeer,Rhinoceros,Rooster,Scorpion,Seal,Skunk,Snake,Sparrow,Squirrel,Swan,Toucan,Tiger,Turkey,Turtle,Vulture,Walrus,Wolf,Woodpecker,Yak,Zebra"

# AnimalList = Animals.split(",")

subject = 'Bear'


def create_script(subject):
    text = openai.Completion.create(

        model='text-davinci-003',

        prompt='Write a 200 word Youtube video script about a ' + subject + ' with voiceovers and 5 short scene descriptions',

        temperature=0.7,

        max_tokens=500,

        top_p=1,

        frequency_penalty=0,

        presence_penalty=0

    )

    script = text['choices'][0]['text']

    return script


def parse_script(script):
    script_dict = {}

    split_script = script.split('\n')

    image_blurb = ''

    script_text = ''

    for number in range(len(split_script)):

        if 'Voiceover' in split_script[number]:

            if len(split_script[number]) > 15:

                script_text = split_script[number][11:]

            else:

                script_text = split_script[number + 1]

        elif 'Scene' in split_script[number]:

            if len(split_script[number]) > 15:

                image_blurb = split_script[number][9:]

            else:

                image_blurb = split_script[number + 1]

        script_dict[script_text] = image_blurb

    script_dict.pop('')

    return script_dict


def image_creator(script_dict):
    block_token = 1

    while block_token == 1:

        try:

            for text, blurb in script_dict.items():

                print(blurb + '\n')

                if blurb != '':
                    image = openai.Image.create(

                        prompt=blurb,

                        n=1,

                        size="1024x1024"

                    )

                    image_url = image['data'][0]['url']

                    script_dict[text] = image_url

                block_token = 0

        except:

            print('Word blocked by OpenAI; trying again...\n')

            block_token = 1

    return script_dict


def text_to_speech(mytext, topic, count):
    language = 'en'

    filename = topic + str(count) + '.mp3'

    myobj = gTTS(text=mytext, lang=language, slow=False)

    myobj.save(filename)

    print(filename, 'saved!\n')

    return filename


def save_image(url, topic, count):
    filename = topic + str(count) + '.jpg'

    img_data = requests.get(url).content

    with open(filename, 'wb') as handler:
        handler.write(img_data)

    print(filename, 'saved!\n')

    return filename


def create_movie(mp3_list, jpg_list, topic):
    audio_len_list = []

    clips = [AudioFileClip(c) for c in mp3_list]

    for item in clips:
        audio_len_list.append(item.duration)

    audioclip = concatenate_audioclips(clips)

    jpg_len_dict = dict(zip(jpg_list, audio_len_list))

    frames = []

    for key, value in jpg_len_dict.items():
        frames.append(ImageClip(key, duration=value))

    videoclip = concatenate_videoclips(frames, method="chain")

    videoclip.audio = audioclip
    file_name = f"final_{topic}.mp4"
    print(file_name)
    videoclip.write_videofile(file_name, fps=24)
    return file_name, topic


script = image_creator(parse_script(create_script(subject)))

print(script)

jpg_list = []

mp3_list = []

for number in range(len(script)):
    mp3_list.append(text_to_speech(list(script.keys())[number], subject, number + 1))
    try:
        jpg_list.append(save_image(list(script.values())[number], subject, number + 1))
    except Exception as e:
        print(f"failed to take image {e}")
movie_file_name, title = create_movie(mp3_list, jpg_list, subject)

upload(file=movie_file_name, title=title, description="title", category="animals", keywords=["animals"],
       privacyStatus="public", thumb=jpg_list[0])

files = glob.glob(subject + '*')

for file in files:
    os.remove(file)

print('Subject files removed!')
