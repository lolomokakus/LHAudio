# LHAudio
Stores binary data as WAV audio, for whatever reason

## Background
This program/library is the result of two classmates' collaboration for the final task of their programming class. It is actually not what they are supposed to do, but their programming teacher is pretty chill.

It was Ludvig who had the idea for the project. He has long been fascinated by 1980's computers, and in particular their methods of storing data on casette tapes in an audible format.

## Format
LHAudio uses a special, homebrew format for file storage inside of "regular" (more on that later) WAV files. It is structured as follows:

- [Magic number](https://en.wikipedia.org/wiki/File_format#Magic_number)
- File name
- Magic number
- SHA1 checksum of the file
- Magic number
- The file data
- Magic number (again)

The format is structured in such a way that storage of multiple files in one WAV file is possible.

### Magic number
LHAudio's magic number is simply 256 bytes containing the numbers 255 to 0. This is very large for a magic number, and the reason for that is that because of our design, the data *can not contain the magic number*. Originally we were planning to use the numbers `0 255 0 255` as a magic number, but when we tested the program with a PNG image, we discovered the image contained this number multiple times.

### Limitations
Apart from the previously mentioned limitations of the magic number, there are a number of other limitations of our format:

- Only works with 8-bit audio
- Only works with mono audio
- Doesn't work with recordings of the original sound (i.e. you can not extract the data from a recording of a speaker playing the original WAV file)

## The Python module
The LHAudio Python module contains two functions, `encode()` and `decode()`.

The `encode()` function takes at least two arguments, the first is the WAV file to store the data in and the second is the file to store. If more than two arguments are specified, the other arguments are interpreted as more files to store.

The `decode()` function takes one argument, the WAV file to decode. The output files are stored in the current working directory.

## Status
The Python module, written by Ludvig, is currently usable, even though it could use some tweaking.

The GUI, in the progress of being written by Hugo, is still in an early phase. All we can say for certain is that it will use [PyQt](https://www.riverbankcomputing.com/software/pyqt/intro). ***I sure hope an intial version is uploaded soon.***

For more detailed information, check TODO.md.
