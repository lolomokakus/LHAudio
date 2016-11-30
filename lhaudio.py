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
    outData.setnframes(0)
    outData.setcomptype("NONE", "not compressed")
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

    if not inData.getnchannels() == 1 or not inData.getsampwidth() == 1:
        raise ValueError("Not a valid LHAudio file.")

    audioList = inData.readframes(inData.getnframes())
    print("Read " + str(len(audioList)) + " bytes from " + inFile + ".")

    if audioList.count(magicNumber) != 3:
        raise ValueError("Not a valid LHAudio file.")

    for byte in range(0, len(audioList)):
        if audioList[byte:byte + 256] == magicNumber:
            print("Found first magic number.")
            audioList = audioList[byte + 256:]
            break

    for byte in range(0, len(audioList)):
        if audioList[byte:byte + 256] == magicNumber:
            print("Found second magic number.")
            recoveredSum = audioList[:byte]
            print("Checksum recovered.")
            audioList = audioList[byte + 256:]
            break

    for byte in range(0, len(audioList)):
        if audioList[byte:byte + 256] == magicNumber:
            print("Found third magic number.")
            recoveredData = audioList[:byte]
            print("Data recovered.")
            break

    outSum = hashlib.sha1()
    outSum.update(recoveredData)

    if outSum.digest() != recoveredSum:
        raise ValueError("Checksum mismatch.")
    else:
        print("Checksum matched.")

    outData.write(recoveredData)
    print("Wrote recovered data to " + outFile + ".")

    inData.close()
    outData.close()

    print("Done.")
    return
