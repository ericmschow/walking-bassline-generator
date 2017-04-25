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
# dict holding numbers 0-11 and notes C-B ## replaced with NOTESLIST
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
            #print("Notes lookup for root in rootFinder is: ",root)    ## DEBUG
        elif len(chordListItem) == 2 and chordListItem[1] != 'm': #gets flats/sharps
            compoundRoot = '{}{}'.format(chordListItem[0].upper(),
                chordListItem[1].lower())
            #print("compoundRoot in rootFinder is: ",compoundRoot)                     ## DEBUG
            #print("Notes lookup for root is: ",NOTES[compoundRoot])              ## DEBUG
            return NOTES[compoundRoot]
        elif len(chordListItem) == 2 and chordListItem[1] == 'm': #eg Am, Em
            root = NOTES[chordListItem[0].upper()]
            #print("Notes lookup for minor root is: ", root)         ## DEBUG
        elif len(chordListItem) == 5:
            root = NOTES[chordListItem[0].upper()]
        elif len(chordListItem) == 6:
            compoundRoot = '{}{}'.format(chordListItem[0].upper(),
                chordListItem[1].lower())
        #    print("compoundRoot in rootFinder is: ",compoundRoot)                     ## DEBUG
        #    print("Notes lookup for root is: ",NOTES[compoundRoot])              ## DEBUG
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

# returns list of randomized notes
def noteFinder(tonesTupleList):
    timeSig = 4 #hardcode 4/4 until implementing variable time signature
    randomTonesTotal = []
    for chord in tonesTupleList:
        print('Chord tone tuple at start of noteFinder For loop is: ',chord)            ## DEBUG
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
                    print("While loop in noteFinder triggered on note ", note)         ## DEBUG
                    note = chord[randint(0, len(chord)-1)]
            randomTonesChord.append(note)
            print ('randomTonesChord in i loop is ', randomTonesChord)  ##DEBUG
        randomTonesTotal.append(randomTonesChord)
        print('randomTonesTotal in chord loop is ', randomTonesTotal)   ##DEBUG
    return randomTonesTotal

    # compare last tone in chord n with first tone in chord n+1

# returns tuple thirdsStack of chord tones via chordTuple lookup in FIFTHS
def chordToneFinder(chordTuple):
    quality = chordTuple[1]
    tones = CHORDS[quality]
    #print("tuple in chordToneFinder is: ", chordTuple)          ## DEBUG
    #print("tones in chordToneFinder is: ", tones)               ## DEBUG
    if quality == 'major' or quality == 'minor':
        root = (tones[0] + chordTuple[0] ) % 12
        third = ((tones[1] + chordTuple[0]) ) % 12
        fifth = ((tones[2] + chordTuple[0]) ) % 12
        octave = ((tones[3] + chordTuple[0]) ) % 12
        #print("Root, third, fifth, octave: ", root, third, fifth, octave)##DEBUG
        thirdsStack = (
        NOTESLIST[root],
        NOTESLIST[third],
        NOTESLIST[fifth],
        NOTESLIST[octave])
        #print("thirdsStack in chordToneFinder is: ", thirdsStack)  ##DEBUG
        return thirdsStack
    elif quality == 'min7' or quality == 'maj7' or quality == 'dom7':
        root = (tones[0] + chordTuple[0] ) % 12
        third = ((tones[1] + chordTuple[0]) ) % 12
        fifth = ((tones[2] + chordTuple[0]) ) % 12
        seventh = (tones[3] + chordTuple[0]) % 12
        octave = ((tones[4] + chordTuple[0]) ) % 12
        #print("Root, third, fifth, seventh octave: ", root, third, fifth, seventh octave)##DEBUG
        thirdsStack = (
        NOTESLIST[root],
        NOTESLIST[third],
        NOTESLIST[fifth],
        NOTESLIST[seventh],
        NOTESLIST[octave])
        #print("thirdsStack in chordToneFinder is: ", thirdsStack)  ##DEBUG
        return thirdsStack
    # etc with other qualities later

def main():
    chordList = chordParser(chordPrompter())
    #print("chordList is: ",chordList)                            ## DEBUG
    tupleList = listUnpacker(chordList)
    #print("tupleList is: ",tupleList)                            ## DEBUG
    tonesTupleList = []
    for chord in tupleList:
        #print("Chord tuple is: ",chord)                            ## DEBUG
        tones = chordToneFinder(chord) # returns tuple with chord tones
        #print('Tones output in main function is', tones)       ## DEBUG
        tonesTupleList.append(tones)
    print('tonesTupleList in main is ', tonesTupleList)         ## DEBUG
    # take list of tone tuples and send to noteFinder
    print('noteFinder call in main returned: ',noteFinder(tonesTupleList))





if __name__ == '__main__':
    main()
