import glob
import matplotlib.pyplot as plt
import re
import os
import numpy as np

# Album list to store song files
from collections import Counter
from math import log

FCDFK = []
IK = []
NSP = []
Skel = []
BT = []

for dir in glob.glob('lyrics/*'):
    dir = dir.split("lyrics/")[1]
    for song in glob.glob("lyrics/" + dir + '/*'):
        if dir == 'Impossible_Kid':
            IK.append(open(song, 'r'))
        if dir == 'Fast_Cars_Danger_Fire_and_Knives':
            FCDFK.append(open(song, 'r'))
        if dir == "None_Shall_Pass":
            NSP.append((open(song, 'r')))
        if dir == "Skelethon":
            Skel.append((open(song, 'r')))
        if dir == "Bazooka_Tooth":
            BT.append((open(song, 'r')))

'''
Clean up text. Want the text to be all one case so "Word" isn't counted differently than "word"
Also want to parse out parenthesis, blank lines and brackets.
'''


def strip_text(albums):
    for album in albums:
        current_dir = ""
        if album == IK:
            current_dir = "Impossible_Kid"
        if album == FCDFK:
            current_dir = "Fast_Cars_Danger_Fire_and_Knives"
        if album == NSP:
            current_dir = "None_Shall_Pass"
        if album == Skel:
            current_dir = "Skelethon"
        if album == BT:
            current_dir = "Bazooka_Tooth"

        for song in album:

            # create new file '<song_name>_cleaned.txt' to hold new, stripped lyrics
            with open(str(song.name.split('.txt')[0] + '_cleaned.txt'), 'w') as f:
                for line in song:
                    if line != "" and line != '\n' and '[' not in line and ']' not in line:
                        line = line.strip('\n')
                        line = re.sub('[\'\":*,.;()?!@#$\xe2\\x80\\x9c\x99]', '', line)
                        line = re.sub('[-]', ' ', line)
                        line = line.lower()
                        f.write(line + '\n')
            # replace the original song file with the data in <song>_cleaned.txt
            f.close()
            os.system("mv lyrics/" + current_dir + "/" +
                      str(song.name.split('.txt')[0].split(current_dir + "/")[1]) + "_cleaned.txt " + str(song.name))


all_albums = [BT, FCDFK, NSP, Skel, IK]

strip_text(all_albums)


def word_frequency(album):
    Songs = []
    Names = []
    for song in album:
        song_name = song.name.split('/')[2].split('.txt')[0]
        word_count = {}
        song.seek(0)
        for line in song:
            line = line.split('\n')[0]
            line = line.split(" ")
            for word in line:
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1
        Songs.append(word_count)
        Names.append(song_name)
    return Songs, Names


def plot_album_bars(list_name, album_name, fig_n):
    Songs = word_frequency(list_name)[0]

    trivial_words = ['a', 'the', 'i', 'of', 'in', 'to', 'and', 'for', 'is',
                     'was', 'w', 'im', 'this', 'thats', 'it', 'are', 'or',
                     'no', 'at', ' ', 'he', 'his', 'she', 'her', 'if']

    words = []
    counts = []
    for dictionary in Songs:
        for k in sorted(dictionary, key=lambda x: dictionary[x]):
            if k not in trivial_words:
                words.append(k)
                counts.append(dictionary[k])

    pairs = []
    for w, c in zip(words, counts):
        pairs.append((w, c))

    check = []
    for pair in reversed(sorted(set(pairs), key=lambda x: x[1])):
        if pair[0] not in [x[0] for x in check]:
            check.append(pair)
    words = []
    counts = []
    for c in (check[0:50]):
        words.append(c[0])
        counts.append(int(c[1]))

    #  plt.subplot(2, 2, fig_n)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    title = " "
    for string in album_name.split("_"):
        title = title + string + " "
    plt.title("'" + title + "' Word Frequency")

    indexes = np.arange(len(words))
    width = .8
    plt.bar(indexes, counts, width)
    plt.xticks(indexes + width * .5, words, rotation=55)
    # plt.legend()
    plt.tight_layout()
    plt.show()
    return words, counts


# plot_album_bars(IK, "Impossible_Kid", 1)
# plot_album_bars(FCDFK, "Fast_Cars_Danger_Fire_and_Knives", 2)
# plot_album_bars(NSP, "None_Shall_Pass", 3)
# plot_album_bars(Skel, "Skelethon", 3)
# plot_album_bars(BT, "Bazooka_Tooth", 5)
# all_albums = [IK, FCDFK, NSP, Skel, BT]

def album_name_map(index):
    if index == 0:
        return "Bazooka Tooth"
    elif index == 1:
        return "Fast Cars Danger Fire and Knives"
    elif index == 2:
        return "None Shall Pass"
    elif index == 3:
        return "Skelethon"
    elif index == 4:
        return "The Impossible Kid"


def all_unique_words():
    check = []
    for a, album in enumerate(all_albums):
        songs, names = word_frequency(album)
        words = []
        counts = []
        song = []
        for i, dictionary in enumerate(songs):
            for k in sorted(dictionary, key=lambda x: dictionary[x]):
                print i, names[i], k, dictionary[k]
                song.append(names[i])
                words.append(k)
                counts.append(dictionary[k])

        pairs = []
        for s, w, c in zip(song, words, counts):
            pairs.append((s, w, c, album_name_map(a)))

        for pair in reversed(sorted(set(pairs), key=lambda x: x[2])):
            if pair[1] not in [x[1] for x in check]:
                check.append(pair)

    unique_words_per_song = [(i[0], i[1], i[3]) for i in check if i[2] == 1]
    unique_words = [(i[1], i[3]) for i in check if i[2] == 1]
    return unique_words, len(unique_words), unique_words_per_song


def unique_words_per_song_bar_plot():
    unique_word_song_pairs = all_unique_words()[2]
    songs_word_count = Counter([(name[0], name[2]) for name in unique_word_song_pairs])
    songs_word_count = [x for x in reversed(sorted(songs_word_count.iteritems(), key=lambda x: songs_word_count[x[0]]))]
    plt.xlabel('Song')
    plt.ylabel('Number of Unique Words')
    plt.title("Number of Unique Words per Song")

    indexes = np.arange(len(songs_word_count))
    width = .8
    plt.bar(indexes, [i[1] for i in songs_word_count], width)
    plt.xticks(indexes + width * .5, [x[0] for x in songs_word_count], rotation=80)
    # plt.legend()
    plt.tight_layout()
    plt.show()


def cumulative_unique_words():
    words_contributed_by_song = {}
    word_count = []
    for a, album in enumerate(all_albums):

        for song in album:
            song_name = song.name.split('/')[2].split('.txt')[0]
            song.seek(0)

            for line in song:
                line = line.split('\n')[0]
                line = line.split(" ")
                for word in line:
                    if word not in word_count:
                        word_count.append(word)
            words_contributed_by_song[(album_name_map(a), song_name)] = len(word_count)
    return words_contributed_by_song


def unique_words_per_song_cumulative():
    cumulative_word_frequency = cumulative_unique_words()

    x_pos = 0
    x = []
    y = []
    percent_changes = []
    album_break_points = []
    first = "Bazooka Tooth"
    pos = 0
    for k, v in sorted(cumulative_word_frequency.iteritems(), key=lambda k: cumulative_word_frequency[k[0]]):
        x.append(x_pos)
        y.append(v)
        if k[0] != first:
            album_break_points.append(x_pos)
            first = k[0]

        percent_changes.append(100*(y[pos]-y[pos-1])/y[pos-1])
        pos+=1

        x_pos += 1

    z = np.polyfit(x, y, 2, full = True)
    p = np.poly1d(z[0])
    plt.figure(figsize=(10, 12))
    plt.xticks([i for i in range(0, x_pos)], [k[0][1] for k in sorted(cumulative_word_frequency.iteritems(),
                                                                      key=lambda k: cumulative_word_frequency[k[0]])],
               rotation=80)
    # plt.plot(x,p(x),'k')
    plt.plot(x[0:album_break_points[0]], percent_changes[0:album_break_points[0]], 'r', label="Bazooka Tooth")
    plt.plot(x[album_break_points[0]:album_break_points[1]],
             percent_changes[album_break_points[0]:album_break_points[1]], 'b',
             label="Fast Cars Danger Fire and Knives")
    plt.plot(x[album_break_points[1]:album_break_points[2]],
             percent_changes[album_break_points[1]:album_break_points[2]], 'y',
             label="None Shall Pass")
    plt.plot(x[album_break_points[2]:album_break_points[3]],
             percent_changes[album_break_points[2]:album_break_points[3]], 'm',
             label="Skelethon")
    plt.plot(x[album_break_points[3]:], percent_changes[album_break_points[3]:], 'c', label="The Impossible Kid")
    plt.xlabel('Songs, listed chronologically by album')
    plt.ylabel('Percent Change')
    plt.title("Percent Change to Total Number of Unique Words")

    plt.legend(loc='upper center')
    plt.tight_layout()
    plt.show()


unique_words_per_song_cumulative()
