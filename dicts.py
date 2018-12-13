# dict holding chord quality and tuple as number of semitones above root
# circle of fifths for reference : https://i.imgur.com/ZwMH969.png
CHORDS = {
    'major' : ('OC', 'M3', 'P5'),
    'minor' : ('OC', 'm3', 'P5'),
    'maj7' : ('OC', 'M3', 'P5', 'M7'),
    'min7' : ('OC', 'm3', 'P5', 'm7'),
    'dom7' : ('OC', 'M3', 'P5', 'm7')
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
