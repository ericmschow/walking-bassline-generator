# program intended to generate walking basslines using chord tones and chromatic
# approach tones.
# outputs scale degrees relative to tonic, not root of each chord.

# this is probably something that could be done better with classes
# but I don't know how to use classes yet
# e.g. a chord has a third, has a fifth, has an octave
# i.e. a major third is the root shifted up by 5 fifths
# but for now it will be functional programming

# NEED IMPLEMENT FIFTHS -> NOTES USING INVERSE DICT
# OR BRING CHORD NAME FROM STRING

from random import randint

# dict holding chord quality and tuple as number of fifths above root for tones
# circle of fifths for reference : https://i.imgur.com/ZwMH969.png
CHORDS = {
    'major' : (0, 4, 1, 0),
    'minor' : (0, 9, 1, 0),
    'maj7' : (0, 4, 1, 5, 0),
    'min7' : (0, 9, 1, 10, 0),
    'dom7' : (0, 4, 1, 10, 0)
}

# dict holding note names and number 1-12 for later calculating distance
NOTES = {
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

INVERSE = {
    0 : 'C',
    1 : 'C#/Db',
    2 : 'D',
    3 : 'D#/Eb',
    4 : 'E',
    5 : 'F',
    6 : 'F#/Gb',
    7 : 'G',
    8 : 'G#/Ab',
    9 : 'A',
    10 : 'A#/Bb',
    11 : 'B'
}

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

# parses user string for desired chords, places into list and returns
def chordParser(arg):
    chords = []
    chords = arg.split(' ')
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

# reads list item and returns chord root as semitones from C
def rootFinder(chordListItem):
    print("chordListItem in rootFinder is: ", chordListItem)    ##DEBUG
    if type(chordListItem == str):
        if len(chordListItem) == 1:
            root = NOTES[chordListItem[0].upper()]
            print("Notes lookup for root in rootFinder is: ",root)    ## DEBUG
        elif len(chordListItem) == 2:
            compoundRoot = '{}{}'.format(chordListItem[0].upper(),
                chordListItem[1].lower())
            print("compoundRoot in rootFinder is: ",compoundRoot)                     ## DEBUG
            print("Notes lookup for root is: ",NOTES[compoundRoot])              ## DEBUG
            return NOTES[compoundRoot]
        else:
            print("Error in rootFinder function string block.")
    if type(chordListItem == tuple):
        return NOTES[chordListItem[0]]

# reads list item and returns chord quality
def qualityFinder(chordListItem):
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

# returns random note in chord from tuple
def randomizer(chordTuple):
    pass

# calls randomizer and returns
def notePrinter(chordTuple):
    timeSig = 4 # hardcode 4/4 until implementing variable time signature

# returns tuple thirdsStack of chord tones via chordTuple lookup in FIFTHS
def chordToneFinder(chordTuple):
    quality = chordTuple[1]
    tones = CHORDS[quality]
    print("tuple in chordToneFinder is: ", chordTuple)          ## DEBUG
    print("tones in chordToneFinder is: ", tones)               ## DEBUG
    if quality == 'major':
        root = (tones[0] + chordTuple[0] ) % 12
        third = ((tones[1] + chordTuple[0]) ) % 12
        fifth = ((tones[2] + chordTuple[0]) ) % 12
        octave = ((tones[3] + chordTuple[0]) ) % 12
        print("Root, third, fifth, octave: ", root, third, fifth, octave)##DEBUG
        thirdsStack = (FIFTHS[root], FIFTHS[third], FIFTHS[fifth], FIFTHS[octave])
        print("thirdsStack in chordToneFinder is: ", thirdsStack)  ##DEBUG
        return thirdsStack
    if quality == 'minor':
        print("Minor not yet implemented.")
    if quality == 'min7':
        print("Extensions not yet implemented.")
    # etc with other qualities later

def main():
    chordList = chordParser(chordPrompter())
    print("chordList is: ",chordList)                            ## DEBUG
    tupleList = listUnpacker(chordList)
    print("tupleList is: ",tupleList)                            ## DEBUG
    for chord in tupleList:
        print("Chord tuple is: ",chord)                            ## DEBUG
        chordToneFinder(chord)
        print(chordToneFinder(chord))





if __name__ == '__main__':
    main()
