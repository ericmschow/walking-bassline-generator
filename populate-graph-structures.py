import dicts
import json

NOTESLIST = dicts.NOTESLIST

INTERVALS = {
    'm2': 1,
    'M2': 2,
    'm3': 3,
    'M3': 4,
    'P4': 5,
    'TT': 6,
    'P5': 7,
    'm6': 8,
    'M6': 9,
    'm7': 10,
    'M7': 11
}

def getNextNote(inpt):
    if inpt == 'B':
        return 'C'
    else:
        index = NOTESLIST.index(inpt)
        return NOTESLIST[index + 1]

def getTargetNote(inpt, interval):
    for i in range(interval):
        inpt = getNextNote(inpt)
    return inpt

def generateGraph():

    graphs = {}

    for (note) in NOTESLIST:
        graphs[note] = {}

    for (key, interval) in INTERVALS.items():
        # graphs[key] = {}
        for (note) in NOTESLIST:
            target = getTargetNote(note, interval)
            graphs[note][key] = target
            # graphs[key][note] = target


        with open('./graphs.py', 'w') as graphsFile:
            graphsFile.write(json.dumps(graphs))


    print('all done')

def main():
    import graphs
    print(graphs.notesgraph['C']['P5'])

if __name__ == '__main__':
    main()
