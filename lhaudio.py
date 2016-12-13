import hashlib
import os
import wave
import struct

def encode(files, container):
    outFile = wave.open(container, "wb")
    outFile.setnchannels(1) # Mono
    outFile.setsampwidth(1) # 8 bit sample size
    outFile.setframerate(8000) # 8000Hz sample rate
    print("Set parameters of " + container + ".")

    for file in files:
        inFile = open(file, "rb")
        # Store binary data from the input file in a list
        inData = inFile.read()
        print("Read " + str(len(inData)) + " bytes from " + os.path.basename(file) + ".")
        # Calculate a checksum of the data
        inSum = hashlib.sha1()
        inSum.update(inData)
        print("Calculated checksum of data.")

        for byte in range(255, -1, -1):
            # Write 1 byte to the output WAV
            outFile.writeframes(struct.pack('B', byte))
        print("Wrote first magic number.")

        for byte in str.encode(os.path.basename(file)):
            outFile.writeframes(struct.pack('B', byte))
        print("Wrote file name.")

        for byte in range(255, -1, -1):
            outFile.writeframes(struct.pack('B', byte))
        print("Wrote second magic number.")

        for byte in inSum.digest():
            outFile.writeframes(struct.pack('B', byte))
        print("Wrote checksum.")

        for byte in range(255, -1, -1):
            outFile.writeframes(struct.pack('B', byte))
        print("Wrote third magic number.")

        for byte in inData:
            outFile.writeframes(struct.pack('B', byte))
        print("Wrote data.")

        for byte in range(255, -1, -1):
            outFile.writeframes(struct.pack('B', byte))
        print("Wrote fourth magic number.")

        print("Encoded " + os.path.basename(file) + ".")

        for _ in range(0, 80):
            outFile.writeframes(struct.pack('B', 0))
        print("Added 10ms spacer.") # 80 frames / 8000 frames/second = 1/100 seconds

        inFile.close()

    outFile.close()

    print("Done.")
    return

def decode(container, outDir):
    magicNumber = []
    # The magic number is large enough that it is worth generating instead of writing manually
    for number in range(255, -1, -1):
        magicNumber.append(number)
    magicNumber = bytes(magicNumber)

    inFile = wave.open(container, "rb")

    # Check parameters of the input WAV
    if inFile.getnchannels() != 1:
        raise InvalidFileError("incorrect amount of channels")
    if inFile.getsampwidth() != 1:
        raise InvalidFileError("incorrect sample width")

    # Read the entire WAV into a list
    inData = inFile.readframes(inFile.getnframes())
    print("Read " + str(len(inData)) + " bytes from " + str(os.path.basename(container)) + ".")

    # There are 4 magic numbers in each encoded file, so an amount
    # of magic numbers not divisible by 4 is a bad sign
    if inData.count(magicNumber) % 4 != 0:
        raise InvalidFileError("incorrect amount of magic numbers")

    # For each encoded file in the WAV:
    for _ in range(0, int(inData.count(magicNumber) / 4)):
        # Seek through the data until we find a magic number
        for byte in range(0, len(inData)):
            if inData[byte:byte + len(magicNumber)] == magicNumber:
                print("Found first magic number.")
                # Discard everything up to and including the magic number
                inData = inData[byte + len(magicNumber):]
                break

        for byte in range(0, len(inData)):
            if inData[byte:byte + len(magicNumber)] == magicNumber:
                print("Found second magic number.")
                # Everything between the beginning of the remaining data
                # and the second magic number is the file name
                recoveredName = inData[:byte]
                print("File name recovered.")
                inData = inData[byte + len(magicNumber):]
                break

        for byte in range(0, len(inData)):
            if inData[byte:byte + len(magicNumber)] == magicNumber:
                print("Found third magic number.")
                # Everything between the beginning of the remaining data
                # and the third magic number is the checksum
                recoveredSum = inData[:byte]
                print("Checksum recovered.")
                inData = inData[byte + len(magicNumber):]
                break

        for byte in range(0, len(inData)):
            if inData[byte:byte + len(magicNumber)] == magicNumber:
                print("Found fourth magic number.")
                # Everything between the beginning of the remaining data
                # and the fourth magic number is the actual encoded data
                recoveredData = inData[:byte]
                print("Data recovered.")
                inData = inData[byte + len(magicNumber):]
                break

        # Calculate a checksum of the recovered data and compare it to the
        # recovered checksum
        inSum = hashlib.sha1()
        inSum.update(recoveredData)
        if inSum.digest() != recoveredSum:
            raise CorruptFileError("checksum mismatch")
        else:
            print("Checksum matched.")

        # The file name is currently a bytes object, we need to make it a string
        recoveredName = bytes.decode(recoveredName)
        outFile = open(os.path.join(outDir, recoveredName), "wb")
        outFile.write(recoveredData)
        print("Decoded " + recoveredName + ".")

        outFile.close()

    print("Done.")
    return

class LHAudioError(Exception):
    pass

class CorruptFileError(LHAudioError):
    # Raised when the checksum of the recovered data and the recovered checksum don't match
    def __init__(self, message):
        self.message = message

class InvalidFileError(LHAudioError):
    # Raised when the input WAV doesn't have the correct parameters or
    # contain a correct amount of magic numbers
    def __init__(self, message):
        self.message = message
