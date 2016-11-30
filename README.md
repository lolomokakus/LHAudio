# LHAudio
Stores binary data as WAV audio, for whatever reason

## Background
This program/library is the result of two classmates' collaboration for the final task of their programming class. It is actually not what they are supposed to do, but their programming teacher is pretty chill. 

It was Ludvig who had the idea for the project. He has long been fascinated by 1980's computers, and in particular their methods of storing data on casette tapes in an audible format.

## Format
LHAudio uses a special, homebrew format for data storage inside of "regular" (more on that later) WAV files. It is structured as follows:

- [Magic number](https://en.wikipedia.org/wiki/File_format#Magic_number)
- SHA1 checksum of the data
- Magic number
- The data
- Magic number (again)

### Magic number
LHAudio's magic number is simply 256 bytes containing the numbers 255 to 0. This is very large for a magic number, and the reason for that is that because of our design, the data **can not contain the magic number**. Originally we were planning to use the numbers `0 255 0 255` as a magic number, but when we tested the program with a PNG image, we discovered the image contained this number multiple times.

### Limitations
Apart from the previously mentioned limitations of the magic number, there are a number of other limitations of our format:

- Only works with 8-bit audio
- Only works with mono audio
- Doesn't work with recordings of the original sound (i.e. you can not extract the data from a recording of a speaker playing the original WAV file)
- Only supports having one set of data encoded within one WAV file

## The Python module
The LHAudio Python module contains two functions, `encode()` and `decode()`. They both take two arguments, `inFile` and `outFile`. For the `encode()` function, `inFile` could be any type of file, where as `outFile` should be a `.wav`. For `decode()`, `inFile` should be a `.wav` and `outFile` could be anything your little heart desires.
`
## Status
The Python module, written by Ludvig, is currently usable, even though it could use some tweaking.

The GUI, to be written by Hugo, is only in the planning stages so far.

For more detailed information, check TODO.md.

