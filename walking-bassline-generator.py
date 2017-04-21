# program intended to generate walking basslines using chord tones and chromatic
# approach tones

# this is probably something that could be done better with classes
# but I don't know how to use classes yet


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

# prompts user for chords and returns string in format 'C Am F G'
def chordPrompter():
    chords = input("Please enter the chords, in format e.g. C Am F G\n> ")
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
    print(chords)
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
        chordInfo = (root, quality)
        chordList.append(chordInfo)
    return chordList

# reads list item and returns chord root as semitones
def rootFinder(chord):
    return NOTES[chord[0]]

# reads list item and returns chord quality
def qualityFinder(chord):
    if 'maj7' in chord.lower():
        return 'maj7'
    elif 'min7' in chord.lower():
        return 'min7'
    elif 'dom7' in chord.lower():
        return 'dom7'
    elif 'm' in chord.lower():
        return 'minor'
    else:
        return 'major'



def main():
    chordList = chordParser(chordPrompter())
    print(listUnpacker(chordList))





if __name__ == '__main__':
    main()
