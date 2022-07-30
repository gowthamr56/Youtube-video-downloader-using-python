# YouTube video and audio downloader using Python

import streamlit as st
import pytube
import pytube.exceptions as py_exp
import requests

# containers
header = st.container() 
body = st.container()

# checking internet is available or not
def checkingInternet(url='https://pynerds.blogspot.com/'):
    try:
        req = requests.get(url)
        return True
    except:
        return False

# downloads the file
def downlaod(format):
    format.download()

with header:
    st.title('YouTube audio & video downloader')

try:
    with body:
        if checkingInternet():
            # get input from the user
            link = st.text_input(label='Enter YouTube URL',placeholder='Paste your link here')

            if link:
                # checks the link is valid or not
                is_link_valid = (not 'Video unavailable' in requests.get(link).text) and ('youtube.com' in link or 'youtu.be' in link)

                if is_link_valid:
                    
                    yt = pytube.YouTube(link)
                    streams = yt.streams

                    # avail_res = []
                    # for stream in streams:
                    #     res = stream.resolution
                    #     if (res in avail_res) or (res == None):
                    #         continue
                    #     else:
                    #         avail_res.append(res)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.video(link)
                    with col2:
                        formats = ['Video', 'Audio']
                        format = st.radio(label='Choose Format', options=formats)

                        avail_res = ['Select', 'Highest resolution', 'Lowest resolution']

                        if format == formats[0]:
                            res = st.selectbox(label='Resolution', options=avail_res)
                            # res = res.replace('p', '')
                            if res == avail_res[1]:
                                video = streams.get_highest_resolution()
                                size = round((video.filesize / 1024) / 1024, 2)
                                d = st.button(f'Download - {size}MB', on_click=downlaod(video))
                                if d:
                                    with body:
                                        st.success('Download was successfull')
                            elif res == avail_res[2]:
                                video = streams.get_lowest_resolution()
                                size = round((video.filesize / 1024) / 1024, 2)
                                d = st.button(f'Download - {size}MB', on_click=downlaod(video))
                                if d:
                                    with body:
                                        st.success('Download was successfull')
                        else:
                            audio = streams.filter(only_audio=True).first()
                            size = round((audio.filesize / 1024) / 1024, 2)
                            d = st.button(f'Download - {size}MB', on_click=downlaod(audio))
                            if d:
                                with body:
                                    st.success('Download was successfull')
                else:
                    st.warning('Enter a valid YouTube URL')
        else:
            st.error('Cannot access internet. Kindly, connect to internet')

except py_exp.AgeRestrictedError:
    st.error('Video is age resticted, and cannot be accessed without OAuth')
except py_exp.ExtractError:
    st.error('Data extraction based error')
except py_exp.HTMLParseError:
    st.error('HTML could not be parsed')
except py_exp.LiveStreamError:
    st.error('Video is live stream, can not download')
except py_exp.MaxRetriesExceeded:
    st.error('Maximun number of retries exceeded')
except py_exp.MembersOnly:
    st.error('Video is members-only. YouTube has special videos that are only viewable to users who have subscribed to a content creator')
# except py_exp.PytubeError:
#     st.error('Base pytube exception that all others inherit. This is done to not pollute the built-in exceptions, which could result in unintended errors being unexpectedly and incorrectly handled within implementers code.')
except (py_exp.VideoPrivate, py_exp.VideoRegionBlocked, py_exp.VideoUnavailable) as e:
    st.error('Base video unavailable error')
