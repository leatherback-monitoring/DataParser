def readfiles(filenames):
    for f in filenames:
        for line in open(f):
            yield line
fil = readfiles("timetest.txt")
fil.next()