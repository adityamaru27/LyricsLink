import requests
import webbrowser
import spotipy
import spotipy.util as util
import sys


def dedup(list1):
    new_list = []
    for x in list1:
        if (x not in new_list) and (x != ''):
            new_list.append(x)
    return new_list


def init():
    id_list = []
    for items in filtered_data:
        spotify_id = (items['track']['track_spotify_id'])
        id_list.append(spotify_id)
    else:
        spotify_list = (dedup(id_list))
        previewer(spotify_list)


def selector(lst_2, pr_num, lst_3):
    while not(pr_num.isdigit()) or int(pr_num) > len(preview_url_list):
        pr_num = input('Please enter a valid serial number of the song whose preview you would like to '
                           'hear! : ')
    else:
        preview_url1 = lst_2[int(pr_num) - 1][0]
        if preview_url1 is None:
            print('Sorry there is no preview to this song!')
            decision2 = input('To see the list again press y, to quit press n: ')
            if decision2 == 'y':
                print()
                previewer(lst_3)
            elif decision2 == 'n':
                print()
                print('Sorry we couldn\'t help!')
                sys.exit()
        else:
            webbrowser.open(preview_url1)
            decider(pr_num, lst_3)


def previewer(lst_1):
    serial_num = 0
    for item in lst_1:
        urlfinal = url2 + item
        r2 = requests.get(urlfinal)
        data2 = r2.json()
        serial_num += 1
        print()
        print(str(serial_num) + ".")
        print('Artist Name: ', data2['artists'][0]['name'])
        print('Song Name: ', (data2['name']))
        url_link = [(data2['preview_url']), data2['id'], serial_num]
        preview_url_list.append(url_link)
        print()
    else:
        if len(preview_url_list) == 0:
            print()
            print('Sorry! No songs were found with these lyrics!')
            sys.exit()
        else:
            preview_number = input('Please enter the serial number of the song whose preview you would like '
                                   'to hear! : ')
            selector(preview_url_list, preview_number, lst_1)


def decider(p_num, lst_4):
    song_found = input('Please press y, if this is the song you were looking for or press n: ')
    while (song_found != 'y') and (song_found != 'n'):
        print('That\'s an invalid input, try again')
        print()
        song_found = input('Please press y, if this is the song you were looking for or press n: ')
    else:
        while song_found == 'n':
            decision1 = input('To see the list again press y, to quit press n: ')
            if decision1 == 'y':
                print()
                previewer(lst_4)
            elif decision1 == 'n':
                print()
                print('Sorry we couldn\'t help!')
                break
        else:
            authorization_function(p_num)


def authorization_function(p_num):
    username = input('Please input your Spotify Username: ')
    client_id = '5a36c4ca0cc242afa61597624a485c0d'
    redirect_uri = 'http://adityamaru27.github.io'
    scope = 'playlist-read-private playlist-modify-public playlist-modify-private user-read-email ' \
            'user-read-private user-read-birthdate'
    client_secret = 'ef7d481d52034dd3a1c3b85e7aba298c'
    token = util.prompt_for_user_token(username, scope=scope, client_id=client_id,
                                       client_secret=client_secret, redirect_uri=redirect_uri)
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer %s' % token}
    data3 = requests.get(url_user, headers=headers)
    user_info = data3.json()
    user_id = user_info['id']
    if token:
        instance = spotipy.Spotify(auth=token)
        data_playlists = instance.user_playlists(user_id, limit=5, offset=0)
        play_list = data_playlists['items']
        play_list_1 = []
        serial_n = 0
        for parameters in play_list:
            print()
            serial_n += 1
            print(str(serial_n) + '.')
            print(parameters['name'])
            id_playlist = parameters['id']
            play_list_1.append([parameters['name'], serial_n, id_playlist])
            print()
        else:
            playlist_number = input('Please choose which playlist you wish to add the song to: ')
            while not (playlist_number.isdigit()) or int(playlist_number) > len(play_list_1):
                print()
                print('That is not a valid serial number, try again!')
                playlist_number = input('Please choose which playlist you wish to add the song to: ')
            else:
                track_id = [preview_url_list[int(p_num) - 1][1]]
                instance.user_playlist_add_tracks(user_id, play_list_1[int(int(playlist_number)) - 1][2], track_id)
                print('The song has been added!')
                print()
                print('Would you like to add another song?')
                repeat = input('Please press y, if you want to add another song from the list: ')
                while (repeat != 'y') and (repeat != 'n'):
                    print('That\'s an invalid input, try again')
                    print()
                    repeat = input('Please press y, if you want to add another song from the list: ')
                else:
                    while repeat == 'n':
                        print()
                        print('Thanks for using LyricsLink, see you soon!')
                        sys.exit()
                    else: init()




apikey = '425cebdbe74fbb9dea718acdb613e0e8'
url = 'http://api.musixmatch.com/ws/1.1/track.search'
url2 = 'https://api.spotify.com/v1/tracks/'
url_user = 'https://api.spotify.com/v1/me'
lyrics = input('Please enter the partial lyrics of the song you know! : ')
search_extent = int(input('Please enter the number of pages of results you wish to see: '))
params = {'apikey': '425cebdbe74fbb9dea718acdb613e0e8', 'q_lyrics': lyrics, 'page': search_extent,
          's_track_rating': 'desc', 's_artist_rating': 'desc', 'format': 'json'}
r = requests.get(url, params=params)
data = r.json()
filtered_data = (data['message']['body']['track_list'])
preview_url_list = []
init()