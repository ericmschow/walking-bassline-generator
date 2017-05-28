# program intended to generate walking basslines using chord tones and chromatic
# approach tones.
# outputs scale degrees relative to tonic, not root of each chord.

# this is probably something that could be done better with classes
# but I don't know how to use classes yet
# e.g. a chord has a third, has a fifth, has an octave
# i.e. a major third is the root shifted up by 5 fifths
# but for now it will be functional programming

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

sample_rate = 44100

class Info():
    # dict holding chord quality and tuple as number of semitones above root
    # circle of fifths for reference : https://i.imgur.com/ZwMH969.png
    CHORDS = {
        'major' : (0, 4, 7, 12),
        'minor' : (0, 3, 7, 12),
        'maj7' : (0, 4, 7, 11, 12),
        'min7' : (0, 3, 7, 10, 12),
        'dom7' : (0, 4, 7, 10, 12)
    }

    # dict holding note names and number 0-11 for later calculating distance
    NOTESTONUMS = {
        'C' : 0,
        'C#' : 1,
        'Db' : 1,
        'D' : 2,
        'D#' : 3,
        'Eb' : 3,
        'E' : 4,
        'F' : 5,
        'F#' : 6,
        'Gb' : 6,
        'G' : 7,
        'G#' : 8,
        'Ab' : 8,
        'A' : 9,
        'A#' : 10,
        'Bb' : 10,
        'B' : 11
    }

    # dict holding note names and frequencies for sample generation
    FREQS = {
        'C' : 32.7,
        'C#/Db' : 34.65,
        'Db' : 34.65,
        'D' : 36.71,
        'D#/Eb' : 38.89,
        'Eb' : 38.89,
        'E' : 41.20,
        'F' : 43.65,
        'F#/Gb' : 46.25,
        'Gb' : 45.25,
        'G' : 49,
        'G#/Ab' : 51.91,
        'Ab' : 51.91,
        'A' : 55,
        'A#/Bb' : 58.27,
        'Bb' : 58.27,
        'B' : 61.74
    }

    # empty dict to be initialized by toneDictGenerator with audio data
    TONEDICT = {}

    # dict holding circle of fifths starting with 0 : C for calculating thirds
    FIFTHS = {
        0 : 'C',
        1 : 'G',
        2 : 'D',
        3 : 'A',
        4 : 'E',
        5 : 'B',
        6 : 'Gb/F#',
        7 : 'Db/C#',
        8 : 'Ab/G#',
        9 : 'Eb/D#',
       10 : 'Bb/A#',
       11 : 'F'
    }

    # list of notes in order with C at 0 index
    NOTESLIST = [
    "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"
    ]

class Chord:

    def __init__(self, chordListItem, info):
        self.info = info
    #    print('chordlistitem in class is ',chordListItem)
        self.rootname = self.rootFinder(chordListItem)
    #    print('rootname in class is ',self.rootname)
        self.rootnum = info.NOTESTONUMS[self.rootname]
        self.quality = self.qualityFinder(chordListItem)
        self.notes = info.CHORDS[self.quality]
        self.thirdnum = self.notes[1]
        self.fifthnum = self.notes[2]
        if self.quality != 'major' and self.quality != 'minor':
            self.seventhnum = self.notes[3]
        self.name = "{} {}".format(self.rootname, self.quality)
        self.namedNotesTuple = self.chordToneFinder()
    #    print('self.notes in class is ',self.notes)
    #    print('self.namedNotesTuple is ', self.namedNotesTuple)
        self.namedNotesList = list()
        for note in self.namedNotesTuple:
            self.namedNotesList.append(note)
        self.thirdname = self.namedNotesList[1]
        self.fifthname = self.namedNotesList[2]
        if self.quality != 'major' and self.quality != 'minor':
            self.seventhname = self.namedNotesList[3]
        self.outputNotes = []
    #    print('self.namednotesList is ', self.namedNotesList)
    #    print('rootnum in class is ',self.rootnum)
        print("thirdnum, fifthnum, seventhnum for {} chord are, {}, {}".format(self.rootname, self.thirdnum, self.fifthnum))
        print("thirdname, fifthname, seventhname for {} chord are, {}, {}".format(self.rootname, self.thirdname, self.fifthname))



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

    # returns tuple thirdsStack of chord tones via lookup in NOTESLIST
    def chordToneFinder(self):
        quality = self.quality
        tones = self.info.CHORDS[quality]
        #print("tuple in chordToneFinder is: ", chordTuple)          ## DEBUG
        #print("tones in chordToneFinder is: ", tones)               ## DEBUG
        if quality == 'major' or quality == 'minor':
            root = (self.notes[0] + self.rootnum) % 12
            third = (self.notes[1] + self.rootnum) % 12
            fifth = (self.notes[2] + self.rootnum) % 12
            octave = (self.notes[3] + self.rootnum) % 12
        #    print("Root, third, fifth, octave: ", root, third, fifth, octave)##DEBUG
            thirdsStack = (
            self.info.NOTESLIST[root],
            self.info.NOTESLIST[third],
            self.info.NOTESLIST[fifth],
            self.info.NOTESLIST[octave])
        #    print("thirdsStack in chordToneFinder is: ", thirdsStack)  ##DEBUG
            return thirdsStack
        elif quality == 'min7' or quality == 'maj7' or quality == 'dom7':
            root = (self.notes[0] + self.rootnum ) % 12
            third = (self.notes[1] + self.rootnum) % 12
            fifth = (self.notes[2] + self.rootnum) % 12
            seventh = (self.notes[3] + self.rootnum) % 12
            octave = (self.notes[4] + self.rootnum) % 12
            print("Root, third, fifth, seventh, octave: ", root, third, fifth, seventh, octave)##DEBUG
            thirdsStack = (
            self.info.NOTESLIST[root],
            self.info.NOTESLIST[third],
            self.info.NOTESLIST[fifth],
            self.info.NOTESLIST[seventh],
            self.info.NOTESLIST[octave])
            print("thirdsStack in chordToneFinder is: ", thirdsStack)  ##DEBUG
            return thirdsStack
        # etc with other qualities later

    # noteRandomizer returns list of randomized notes  CURRENTLY UNUSED AGAIN
    def noteRandomizer(self,tonesTupleList):
        timeSig = 4 #hardcode 4/4 until implementing variable time signature
        randomTonesTotal = []
        for chord in tonesTupleList:
            #print('Chord tone tuple at start of noteFinder For loop is: ',chord)            ## DEBUG
            randomTonesChord = []
            for i in range(timeSig):  #iterate for number of beats in measure
                note = chord[randint(0, len(chord)-1)] # randomly pick from notes in chord
                # if block here is to prevent notes from being repeated
                if len(randomTonesChord) == 0:  # if no tone in list already
                    pass # no need to check anything
                # except IndexError:
                #     randomTonesChord.append(note)
                #     print("while loop in noteFinder triggered.")        ##DEBUG
                else:
                    while note == randomTonesChord[i-1]:
                        #print("While loop in noteFinder triggered on note ", note)         ## DEBUG
                        note = chord[randint(0, len(chord)-1)]
                randomTonesChord.append(note)
                #print ('randomTonesChord in i loop is ', randomTonesChord)  ##DEBUG
            randomTonesTotal.append(randomTonesChord)
            #print('randomTonesTotal in chord loop is ', randomTonesTotal)   ##DEBUG
        return randomTonesTotal

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
    def __init__(self, note, info):
        self.name = note.

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
    global info
    octaver = 4 # adjusts octave of playback by factor of octaver
    T = 60/tempo # gets length of note in seconds, e.g. 120 bpm * 1m/60s
    t = np.linspace(0, T, T * sample_rate, False)
    for note in info.NOTESLIST:
        print('Generating sample for ', note)
        # generate sine wave notes
        tone = np.sin(info.FREQS[note] * octaver * t * 2 * np.pi)
        # concatenate notes
        audio = np.hstack((tone))
        # normalize to 16-bit range
        audio *= 32767 / np.max(np.abs(audio))
        # convert to 16-bit data
        audio = audio.astype(np.int16)
        info.TONEDICT[note] = audio

# parses user string for desired chords, places into list and returns
def chordParser(inpt):
    global info
    chords = []
    chords = inpt.split(' ')
    # print(chords)
    return chords

# parses user string for desired time signature and returns
# currently unused
#def timeSigParser(arg):
#    pass

# calls ___finder functions for each chord in list and returns list of tuples
def listUnpacker(arg):
    global info
    chordList = []
    for chord in arg:
        root = rootFinder(chord)
        quality = qualityFinder(chord)
        name = chord[0]
        chordInfo = (root, quality, name) # stores root & chord quality in tuple
        chordList.append(chordInfo)
    return chordList

# takes note name input and plays sound
def tonePlayer(note, info):
    info = info
    # start playback
    play_obj = sa.play_buffer(info.TONEDICT[note], 1, 2, sample_rate)
    # wait for playback to finish before exiting
    play_obj.wait_done()

def main():
    timeSig = 4 #hardcode to 4 for now, later get from call to timeSigParser
    tempo = 120 #hardcode to 120 for now
    info = Info()
    chordList = chordParser(chordPrompter())
    print("chordList is: ",chordList)                            ## DEBUG
    #tupleList = listUnpacker(chordList)
    #print("tupleList is: ",tupleList)
    chordclasses = list()
    for ch in chordList:
        print('Appending {} to chordList'.format(ch))
        chordclasses.append(Chord(ch, info))
    print (chordclasses)
    if timeSig == 4:
        for chord in chordclasses:
            print("|| {} | {} | {} | {} |".format(chord.namedNotesList[0], chord.namedNotesList[1], chord.namedNotesList[2], chord.namedNotesList[3]))
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
    info = Info()
    #print("Generating audio samples...")
    #toneDictGenerator(80)
    main()
