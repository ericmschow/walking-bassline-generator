# walking-bassline-generator
Command line Python program to generate randomized walking basslines from user-inputted chord progressions.

This is my personal project to apply the concepts learned at DigitalCrafts to create a useful practice tool for my bass playing. (How useful it will be remains to be seen.)

As of this writing (4/25/17), this program, when run from the command line, does the following:
  * prompts the user for a list of chords
  * parses that list into individual chords
  * parses the chords further for their root and quality (e.g. major or minor)
  * generates a random list of notes from each chord
  * outputs list to terminal in readable format
  * plays sound for each note using simpleaudio module (pip install simpleaudio) and numpy module

Future plans include:
  * chromatic approach tones, common tones, etc. to make output more musical
  * GUI to bypass ugly parsing functions
  * better sound samples to minimize load times as well as improve user experience
  * web hosting
  * tempo and time signature selection support
