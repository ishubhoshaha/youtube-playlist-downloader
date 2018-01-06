import sys
import argparse
import os
import platform
import getpass
import requests
import pafy
from bs4 import BeautifulSoup
from pytube import YouTube,Stream

def get_formatted_video_url(utube_playlist_link = None):
    if utube_playlist_link is None:
        return
    #Todo check invalid utube url
    # https://www.youtube.com/playlist?list=PLk1kxccoEnNEtwGZW-3KAcAlhI_Guwh8x
    try:
        htmlpage = requests.get(utube_playlist_link).text
    except:
        sys.stdout.write("Parsing Error! Its seems that playlist url is invalid. ")

    my_soup = BeautifulSoup(htmlpage, 'html.parser')
    t = my_soup.find_all('a',{'class':'pl-video-title-link'})
    grab_all_video_link = []
    for each in t:
        grab_all_video_link.append('www.youtube.com'+each['href'].split('&')[0])

    return grab_all_video_link

def get_user_input():

    parser = argparse.ArgumentParser(description="Yoube Playlist Downloader")
    parser.add_argument('-l', '--link', type=str, help='Youtube Link', required=True)
    parser.add_argument('-t', '--type', type=str, help='Link type (Playlist/Single Video)', required=False)
    parser.add_argument('-o', '--output', type=str, help='Output Type ("a" for Audio / "v" for Video )', required=False)
    args = parser.parse_args()
    utube_link = args.link
    link_type = args.type
    output_type = args.output
    return utube_link, link_type, output_type

def get_output_directory():
    output_dir = ""
    if platform.system() == 'Linux':
        temp = os.path.join('/home',getpass.getuser(),'Downloads/')
        output_dir = temp if os.path.isdir(temp) else os.path.getcwd()
    elif platform.system() == 'Windows':
        pass
        #ToDo get windows Download folder
    elif platform.system() == 'darwin':
        pass 
        #ToDo get MacOS Download folder
    return output_dir

def fetch_video(video_url = None):
    if video_url is not None:
        try:
            # 'https://www.youtube.com/watch?v=VAUHZYf_aKY'
            video = pafy.new(video_url)
        except:
            sys.stdout.write("Couldn't get any video with this link: {x}".format(x = video_url))
        return video
    
def download_video(video_url = None):
    video = fetch_video(video_url)
    try:
        best_possible_video = video.getbestvideo(preftype="mp4")
        print('Downloading {x}'.format(x = video.title))
        best_possible_video.download(filepath = get_output_directory())
        print('Downloaded Size {y} MB'.format(y = (best_possible_video.get_filesize())/(1024*1024)))
    except:
        sys.stdout.write("Something went wrong!!! Skipping {x}".format(x = video.title))

def download_audio(video_url = None):

    video = fetch_video(video_url)
    try:
        best_possible_audio = video.getbestaudio()
        print('"{x}" Converting & Downloading into .mp3'.format(x = video.title))
        best_possible_audio.download(filepath = get_output_directory())
    except:
        print('"{x}" is not availabe in .mp3'.format(x = video.title))

#Todo Add audio codec
#Todo add appropriate msg and exception
#Todo Add thread base download

if __name__ == '__main__':
    utube_link, link_type, output_type = get_user_input()
    extracted_video_link = get_formatted_video_url(utube_link)
    if extracted_video_link:
        if output_type.lower() == 'v':
            for link in extracted_video_link:
                download_video(link)
        else:
            for link in extracted_video_link:
                download_audio(link)
    else:
        sys.stdout.write("Couldn't find any video against provided link")
