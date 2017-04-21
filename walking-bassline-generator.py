# program intended to generate walking basslines using chord tones and chromatic
# approach tones.
# outputs scale degrees relative to tonic, not root of each chord.

# this is probably something that could be done better with classes
# but I don't know how to use classes yet

from random import randint

# dict holding chord quality and tuple for semitones above root
CHORDS = {
    'major' : (1, 5, 8, 13),
    'minor' : (1, 4, 8, 13)
    #'maj7' :
    #'min7' :
    #'dom7' :
}

# dict holding note names and number 1-12 for later calculating distance
NOTES = {
    'C' : 1,
    'C#' : 2,
    'Db' : 2,
    'D' : 3,
    'D#' : 4,
    'Eb' : 4,
    'E' : 5,
    'F' : 6,
    'F#' : 7,
    'Gb' : 7,
    'G' : 8,
    'G#' : 9,
    'Ab' : 9,
    'A' : 10,
    'A#' : 11,
    'Bb' : 11,
    'B' : 12
}

# dict holding circle of fifths starting with 1 : C for calculating thirds
FIFTHS = {
    1 : 'C',
    2 : 'G',
    3 : 'D',
    4 : 'A',
    5 : 'E',
    6 : 'B',
    7 : 'Gb/F#',
    8 : 'Db/C#',
    9 : 'Ab/G#',
   10 : 'Eb/D#',
   11 : 'Bb/A#',
   12 : 'F'
}

# prompts user for chords and returns string in format 'C Am F G'
def chordPrompter():
    chords = input("Please enter the chords, in format e.g. C Am F G:\n> ")
    return chords

# prompts user for time signature and returns string in format '4/4'
# currently unused
def timeSigPrompter():
    timeSig = input("Please enter the time signature, in format e.g. 4/4.\n< ")
    return timeSig

# prompts user for tempo in int format 1 - 240
# currently unused
def tempoPrompter():
    pass

# parses user string for desired chords, places into list and returns
def chordParser(arg):
    chords = []
    chords = arg.split(' ')
    # print(chords)
    return chords

# parses user string for desired time signature and returns
# currently unused
def timeSigParser(arg):
    pass

# calls ___finder functions for each chord in list and returns list of tuples
def listUnpacker(arg):
    chordList = []
    for chord in arg:
        root = rootFinder(chord)
        quality = qualityFinder(chord)
        chordInfo = (root, quality) # stores root and chord quality in tuple
        chordList.append(chordInfo)
    return chordList

# reads list item and returns chord root as semitones
def rootFinder(chordListItem):
    return NOTES[chordListItem[0].upper()]

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

# returns tuple of chord tones given chord tuple checking dictionary
def chordToneFinder(chordTuple):
    quality = chordTuple[1]
    tones = CHORDS[quality]
    if quality == 'major':
        for tone in tones:
            root = int(tones[0])
            third = root + 4
            fifth = root + 1
            return (FIFTHS[root], FIFTHS[third], FIFTHS[fifth])
    if quality == 'minor':
        pass
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
