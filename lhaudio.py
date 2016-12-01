import hashlib
import wave
import struct

def encode(inFile, outFile):
    inData = open(inFile, "rb").read()
    print("Read " + str(len(inData)) + " bytes from " + inFile + ".")
    inSum = hashlib.sha1()
    inSum.update(inData)
    print("Calculated checksum of read data.")
    outData = wave.open(outFile, "wb")

    outData.setnchannels(1)
    outData.setsampwidth(1)
    outData.setframerate(8000)
    print("Set parameters of " + outFile + ".")

    for byte in range(255, -1, -1):
        outData.writeframes(struct.pack('B', byte))

    print("Wrote first magic number.")

    for byte in inSum.digest():
        outData.writeframes(struct.pack('B', byte))

    print("Wrote checksum.")

    for byte in range(255, -1, -1):
        outData.writeframes(struct.pack('B', byte))

    print("Wrote second magic number.")

    for byte in inData:
        outData.writeframes(struct.pack('B', byte))

    print("Wrote data.")

    for byte in range(255, -1, -1):
        outData.writeframes(struct.pack('B', byte))

    print("Wrote third magic number.")

    outData.close()

    print("Done.")
    return

def decode(inFile, outFile):
    magicNumber = []
    for number in range(255, -1, -1):
        magicNumber.append(number)

    magicNumber = bytes(magicNumber)

    inData = wave.open(inFile, "rb")
    outData = open(outFile, "wb")

    if inData.getnchannels() != 1:
        raise InvalidFileError("incorrect amount of channels")
    if inData.getsampwidth() != 1:
        raise InvalidFileError("incorrect sample width")

    audioList = inData.readframes(inData.getnframes())
    print("Read " + str(len(audioList)) + " bytes from " + inFile + ".")

    if audioList.count(magicNumber) != 3:
        raise InvalidFileError("incorrect amount of magic numbers")

    for byte in range(0, len(audioList)):
        if audioList[byte:byte + len(magicNumber)] == magicNumber:
            print("Found first magic number.")
            audioList = audioList[byte + len(magicNumber):]
            break

    for byte in range(0, len(audioList)):
        if audioList[byte:byte + len(magicNumber)] == magicNumber:
            print("Found second magic number.")
            recoveredSum = audioList[:byte]
            print("Checksum recovered.")
            audioList = audioList[byte + len(magicNumber):]
            break

    for byte in range(0, len(audioList)):
        if audioList[byte:byte + len(magicNumber)] == magicNumber:
            print("Found third magic number.")
            recoveredData = audioList[:byte]
            print("Data recovered.")
            break

    audioList[:] = []

    outSum = hashlib.sha1()
    outSum.update(recoveredData)

    if outSum.digest() != recoveredSum:
        raise CorruptFileError("checksum mismatch")
    else:
        print("Checksum matched.")

    outData.write(recoveredData)
    print("Wrote recovered data to " + outFile + ".")

    inData.close()
    outData.close()

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
