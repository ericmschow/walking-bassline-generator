# program intended to generate walking basslines using chord tones and chromatic
# approach tones.
# outputs scale degrees relative to tonic, not root of each chord.

#### TODO:
#### create proper output
#### implement common tones
#### implement chromatic approach tones
#### implement tempo and timesig
####    * tempo function needs to generate dict with note samples
#### refactor into classes
####    * chord has quality, third/fifth/seventh
#### implement sound library
####    * one sound w/ transpose? 12 sound files? generate sin waves?
#### host on website
#### develop gui

from random import randint
import numpy as np
import simpleaudio as sa
import dicts
import json
import graphs

sample_rate = 44100

class Song:
    def __init__(self, tempo, timesig):
        self.tempo = tempo
        self.timesig = timesig
        self.chords = []
        self.measures = []

    def makeMeasures(self):
        print('Making measures from chords: ', self.chords)
        measures = []
        for chord in self.chords:
            measures.append(Measure(chord, self.timesig))
        self.measures = measures

class Chord:

    def __init__(self, chordListItem):

        self.rootname = self.rootFinder(chordListItem)
        self.quality = self.qualityFinder(chordListItem)
        self.name = "{} {}".format(self.rootname, self.quality)
        self.chordTones = list()
        for note in self.chordToneFinder():
            self.chordTones.append(note)
    #
    # #    print('chordlistitem in class is ',chordListItem)
    #     self.rootname = self.rootFinder(chordListItem)
    # #    print('rootname in class is ',self.rootname)
    #     self.rootnum = info.NOTESTONUMS[self.rootname]
    #     self.quality = self.qualityFinder(chordListItem)
    #     self.notes = info.CHORDS[self.quality]
    #     self.thirdnum = self.notes[1]
    #     self.fifthnum = self.notes[2]
    #     if self.quality != 'major' and self.quality != 'minor':
    #         self.seventhnum = self.notes[3]
    #     self.name = "{} {}".format(self.rootname, self.quality)
    #     self.namedNotesTuple = self.chordToneFinder()
    # #    print('self.notes in class is ',self.notes)
    # #    print('self.namedNotesTuple is ', self.namedNotesTuple)
    #     self.namedNotesList = list()
    #     for note in self.namedNotesTuple:
    #         self.namedNotesList.append(note)
    #     self.thirdname = self.namedNotesList[1]
    #     self.fifthname = self.namedNotesList[2]
    #     if self.quality != 'major' and self.quality != 'minor':
    #         self.seventhname = self.namedNotesList[3]
    #     self.outputNotes = []
    # #    print('self.namednotesList is ', self.namedNotesList)
    # #    print('rootnum in class is ',self.rootnum)
    #     print("thirdnum, fifthnum, seventhnum for {} chord are, {}, {}".format(self.rootname, self.thirdnum, self.fifthnum))
    #     print("thirdname, fifthname, seventhname for {} chord are, {}, {}".format(self.rootname, self.thirdname, self.fifthname))



    def __repr__(self):
        return self.name

    # rootFinder reads list item and returns chord root letter w/ accidental
    # options in format of C, C#, Cm, C#m, Cmin7, C#min7
    # 2 options for 2 chars
    def rootFinder(self, chordListItem):
        print('chordListItem in rootFinder is ',chordListItem)
        if type(chordListItem == str):
            if len(chordListItem) == 1:
                root = chordListItem[0].upper()
       #         print("Notes lookup for root in rootFinder is: ",root)    ## DEBUG
                return root
            elif len(chordListItem) == 2 and chordListItem[1] != 'm': #gets flats/sharps
                compoundRoot = '{}{}'.format(chordListItem[0].upper(),
                    chordListItem[1].lower())
       #         print("compoundRoot in rootFinder is: ",compoundRoot)                     ## DEBUG
       #         print("Notes lookup for root is: ",info.NOTES[compoundRoot])              ## DEBUG
                return compoundRoot
            elif len(chordListItem) == 2 and chordListItem[1].lower() == 'm': #eg Am, Em
                root = chordListItem[0].upper()
       #         print("Notes lookup for minor root is: ", root)         ## DEBUG
                return root
            elif len(chordListItem) == 3 and chordListItem[2].lower() == 'm':  # e.g. G#m
                compoundRoot = '{}{}'.format(chordListItem[0].upper(),
                    chordListItem[1].lower())
                return compoundRoot
            elif len(chordListItem) == 5:
                root = chordListItem[0].upper()
                return root
            elif len(chordListItem) == 6:
                compoundRoot = '{}{}'.format(chordListItem[0].upper(),
                    chordListItem[1].lower())
       #         print("compoundRoot in rootFinder is: ",compoundRoot)                     ## DEBUG
       #         print("Notes lookup for root is: ",info.NOTES[compoundRoot])              ## DEBUG
                return compoundRoot

            else:
                print("Error in rootFinder function string block, cLI =", chordListItem)
       # print("chordListItem in rootFinder is: ", chordListItem)    ##DEBUG

    # reads list item and returns chord quality
    def qualityFinder(self, chordListItem):
        if 'maj7' in chordListItem.lower():
            return 'maj7'
        elif 'min7' in chordListItem.lower():
            return 'min7'
        elif 'dom7' in chordListItem.lower():
            return 'dom7'
        elif 'm' in chordListItem.lower():
            return 'minor'
        else:
            return 'major'

    # returns tuple thirdsStack of chord tones via lookup in notes graph
    def chordToneFinder(self):
        intervals = dicts.CHORDS[self.quality]
        notes = []
        for i in intervals:
            # eg notesgraph[C][P5] returns G
            notes.append(graphs.notesgraph[self.rootname][i])
        return tuple(notes)



    # returns note a half-step below given note takes string input
    def chromaticFlat(self, note):
        approachTone = info.NOTESLIST[(info.NOTESTONUMS[note]+11) % 12]
        print("flat approach tone is: ", approachTone)      ##DEBUG

    # returns note a half-step below given note takes string input
    def chromaticSharp(self, note):
        approachTone = info.NOTESLIST[(info.NOTESTONUMS[note]+1) % 12]
        print("sharp approach tone is: ", approachTone)     ##DEBUG

    # checks whether target note is more than X notes away from last
    def rangeChecker(self, note1, note2):
        pass

    # makes note objects from chord namedNotesList
    def noteObjectMaker(self):
        for note in self.namedNotesList:
            n = Note(note, info)
            self.notesObjectsList.push(n)

class Note:
    def __init__(self, note, value, octave):
        self.name = '{}{}'.format(note, octave)
        self.value = value
        self.octave = octave
    def __repr__(self):
        return self.name

class Measure:
    def __init__(self, chord, timeSig):
        self.maxNotes = timeSig
        self.chord = chord
        self.notes = self.noteRandomizer()

    def __repr__(self):
        return str(self.chord)

    # noteRandomizer returns list of randomized notes  CURRENTLY UNUSED AGAIN
    def noteRandomizer(self):
        timeSig = 4 #hardcode 4/4 until implementing variable time signature
        octave = 4 # same
        randomTonesTotal = []

        numberOfNotes = len(self.chord.chordTones)

        for beat in range(timeSig):
            r = randint(0, numberOfNotes - 1)
            randomTonesTotal.append('{}{}'.format(self.chord.chordTones[r], octave))

        return randomTonesTotal

# prompts user for chords and returns string in format 'C Am F G'
def chordPrompter():
    chords = input("Please enter the chords, in format e.g. C Am F G:\n> ")
    return chords

# prompts user for time signature and returns string in format '4/4'
# currently unused
#def timeSigPrompter():
#    timeSig = input("Please enter the time signature, in format e.g. 4/4.\n< ")
#    return timeSig

# prompts user for tempo in int format 1 - 240
# currently unused
#def tempoPrompter():
#    pass

# takes tempo in BPM and generates sample library
def toneDictGenerator(tempo):
    # get timesteps for each sample, T is note duration in seconds
    octaver = 4 # adjusts octave of playback by factor of octaver
    T = 60/tempo # gets length of note in seconds, e.g. 120 bpm * 1m/60s
    t = np.linspace(0, T, T * sample_rate, False)
    for octave in range(1, 8):
        for note in info.NOTESLIST:
            print('Generating sample for ', note, octave)
            # generate sine wave notes
            tone = np.sin(info.FREQS[note] * octaver * t * 2 * np.pi)
            # concatenate notes
            audio = np.hstack((tone))
            # normalize to 16-bit range
            audio *= 32767 / np.max(np.abs(audio))
            # convert to 16-bit data
            audio = audio.astype(np.int16)
            # print('audio is', audio)
            info.TONEDICT['{}{}'.format(note, octave)] = audio

# parses user string for desired chords, places into list and returns
def chordParser(inpt):
    chords = []
    chords = inpt.split(' ')
    chords = list(filter(None, chords))
    # print(chords)
    return chords

# parses user string for desired time signature and returns
# currently unused
#def timeSigParser(arg):
#    pass

# calls ___finder functions for each chord in list and returns list of tuples
def listUnpacker(arg):
    chordList = []
    for chord in arg:
        root = rootFinder(chord)
        quality = qualityFinder(chord)
        name = chord[0]
        chordInfo = (root, quality, name) # stores root & chord quality in tuple
        chordList.append(chordInfo)
    return chordList

# takes note name input and plays sound
def tonePlayer(note):
    # start playback
    play_obj = sa.play_buffer(info.TONEDICT[note], 1, 2, sample_rate)
    # wait for playback to finish before exiting
    play_obj.wait_done()

def main():
    timeSig = 4 #hardcode to 4 for now, later get from call to timeSigParser
    tempo = 120 #hardcode to 120 for now
    song = Song(tempo, timeSig)
    # info = Info()
    print("Generating audio samples...")
    # toneDictGenerator(song.tempo)
    # with open('./tones.py', 'w') as f:
        # np.savetxt(f, np.column_stack(dicts.TONEDICT), fmt='%U6f')
        # print('wrote tones')
    chordList = chordParser(chordPrompter())
    print("chordList is: ",chordList)                            ## DEBUG
    #tupleList = listUnpacker(chordList)
    #print("tupleList is: ",tupleList)
    for ch in chordList:
    #    print('Appending {} to chordList'.format(ch))
        song.chords.append(Chord(ch))
    print (song.chords)
    song.makeMeasures()
    if timeSig == 4:
        print(song.measures)
        for measure in song.measures:
            print("|| {} | {} | {} | {} |".format(*measure.notes))
            # for note in chord.namedNotesList:
        #    for i in range(timeSig):
        #        tonePlayer(chord.namedNotesList[i], info)
    again = input("Would you like enter more chords? Y/N > ")
    if 'y' in again.lower():
        main()
    if 'n' in again.lower():
        print("Goodbye!")
        quit()





if __name__ == '__main__':
    info = dicts
    main()
