import hashlib
import os
import wave
import struct

def encode(container, *files):
    if len(files) == 0:
        raise InvalidArgumentError("no input files specified")

    outFile = wave.open(container, "wb")
    outFile.setnchannels(1)
    outFile.setsampwidth(1)
    outFile.setframerate(8000)
    print("Set parameters of " + container + ".")

    for file in files:
        inFile = open(file, "rb")
        inData = inFile.read()
        print("Read " + str(len(inData)) + " bytes from " + os.path.basename(file) + ".")
        inSum = hashlib.sha1()
        inSum.update(inData)
        print("Calculated checksum of data.")

        for byte in range(255, -1, -1):
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
        print("Added 10ms spacer.")

        inFile.close()

    outFile.close()

    print("Done.")
    return

def decode(container, outDir):
    magicNumber = []
    for number in range(255, -1, -1):
        magicNumber.append(number)

    magicNumber = bytes(magicNumber)

    inFile = wave.open(container, "rb")

    if inFile.getnchannels() != 1:
        raise InvalidFileError("incorrect amount of channels")
    if inFile.getsampwidth() != 1:
        raise InvalidFileError("incorrect sample width")

    inData = inFile.readframes(inFile.getnframes())
    print("Read " + str(len(inData)) + " bytes from " + str(os.path.basename(container)) + ".")

    if inData.count(magicNumber) % 4 != 0:
        raise InvalidFileError("incorrect amount of magic numbers")

    for _ in range(0, int(inData.count(magicNumber) / 4)):
        for byte in range(0, len(inData)):
            if inData[byte:byte + len(magicNumber)] == magicNumber:
                print("Found first magic number.")
                inData = inData[byte + len(magicNumber):]
                break

        for byte in range(0, len(inData)):
            if inData[byte:byte + len(magicNumber)] == magicNumber:
                print("Found second magic number.")
                recoveredName = inData[:byte]
                print("File name recovered.")
                inData = inData[byte + len(magicNumber):]
                break

        for byte in range(0, len(inData)):
            if inData[byte:byte + len(magicNumber)] == magicNumber:
                print("Found third magic number.")
                recoveredSum = inData[:byte]
                print("Checksum recovered.")
                inData = inData[byte + len(magicNumber):]
                break

        for byte in range(0, len(inData)):
            if inData[byte:byte + len(magicNumber)] == magicNumber:
                print("Found fourth magic number.")
                recoveredData = inData[:byte]
                print("Data recovered.")
                inData = inData[byte + len(magicNumber):]
                break

        inSum = hashlib.sha1()
        inSum.update(recoveredData)
        if inSum.digest() != recoveredSum:
            raise CorruptFileError("checksum mismatch")
        else:
            print("Checksum matched.")

        outFile = open(os.path.join(outDir, bytes.decode(recoveredName)), "wb")
        outFile.write(recoveredData)
        print("Decoded " + bytes.decode(recoveredName) + ".")

        outFile.close()

    print("Done.")
    return

class LHAudioError(Exception):
    pass

class CorruptFileError(LHAudioError):
    def __init__(self, message):
        self.message = message

class InvalidFileError(LHAudioError):
    def __init__(self, message):
        self.message = message

class InvalidArgumentError(LHAudioError):
    def __init__(self, message):
        self.message = message
