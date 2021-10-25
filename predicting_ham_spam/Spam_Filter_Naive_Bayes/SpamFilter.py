import os
import glob
import math

hamDict = dict()
spamDict = dict()

hamEmailCount = 0
spamEmailCount = 0

hamWordCount = 0
spamWordCount = 0

alpha = .01
vocabulary = 170000

# populates dictionary with counts of words given a folder directory and dictionary to populate
def populateDict(path, d):
    numFiles = 0
    numWords = 0
    for filename in glob.glob(os.path.join(path, '*.words')):
        numFiles += 1
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            text = open(filename, "r")
            for word in text:
                word = word.strip().lower()
                if word in d:
                    d[word] = d[word] + 1
                    numWords += 1
                else:
                    d[word] = 1
                    numWords += 1

    return numFiles, numWords

# transforms dictionary counts to smoothed and log-transformed probalities
def countsToProbabilities(d, numWords):
    for k, v in d.items():
        d[k] = math.log2((v + alpha) / (numWords + alpha * vocabulary)) # avoid numeric underflow

    return math.log2(alpha / (numWords + alpha * vocabulary)) # log(P(unseenWord))

# predicts ham or spam for a given email
def classifyEmail(filename, p_ham, p_spam, p_unseenHam, p_unseenSpam):
    hamGuess = math.log2(p_ham) # transform to log-scale to match dict values
    spamGuess = math.log2(p_spam) # transform to log-scale to match dict values
    text = open(filename, "r")
    for word in text:
        word = word.strip().lower()
        if word in hamDict:
            hamGuess += hamDict[word]
        else:
            hamGuess += p_unseenHam
        if word in spamDict:
            spamGuess += spamDict[word]
        else:
            spamGuess += p_unseenSpam

    if hamGuess >= spamGuess:
        return 0 # classify as ham
    else:
        return 1 # classify as spam

# ouputs predictions for all test files in a directory
def guessTestFiles(path, p_ham, p_spam, p_unseenHam, p_unseenSpam):
    hamList = []
    spamList = []
    
    for filename in glob.glob(os.path.join(path, '*.words')):
        if classifyEmail(filename, p_ham, p_spam, p_unseenHam, p_unseenSpam) == 0:
            print(filename[13:] + " is ham")
            hamList.append(filename)
        else:
            print(filename[13:] + " is spam")
            spamList.append(filename)

    return hamList, spamList

# calculates model's performance
def getStats(hamList, spamList):
    trueSpam = []
    truth = open('HamSpam/truthfile', "r")
    for num in truth:
        wordsfile = "HamSpam/test/" + str(num.strip()) + ".words"
        trueSpam.append(wordsfile)

    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for email in hamList:
        if email not in trueSpam:
            TN += 1
        else:
            FN += 1

    for email in spamList:
        if email in trueSpam:
            TP += 1
        else:
            FP += 1

    P = TP / (TP + FP)
    R = TP / (TP + FN)

    F1 = 2 * P * R / (P + R)

    print("TP = " + str(TP) + "\n" +
          "FP = " + str(FP) + "\n" +
          "TN = " + str(TN) + "\n" +
          "FN = " + str(FN) + "\n" +
          "P = " + str(P) + "\n" +
          "R = " + str(R) + "\n" +
          "F1 = " + str(F1))


def main():
    # populate hamDict and count words
    hamEmailCount, hamWordCount = populateDict('HamSpam/ham', hamDict)

    # populate spamDict and count words
    spamEmailCount, spamWordCount = populateDict('HamSpam/spam', spamDict)

    # calculate P(ham) and P(spam), for our test data they are both 0.5, which is not representative
    p_ham = hamEmailCount / (hamEmailCount + spamEmailCount)
    p_spam = spamEmailCount / (hamEmailCount + spamEmailCount)

    # transform dictionary counts to smoothed probabilities and get P(unseenWord)
    p_unseenHam = countsToProbabilities(hamDict, hamWordCount)
    p_unseenSpam = countsToProbabilities(spamDict, spamWordCount)

    # make predictions
    hamList, spamList = guessTestFiles('HamSpam/test', p_ham, p_spam, p_unseenHam, p_unseenSpam)

    # performance (TP, FP, FN, TN, P, R, and F-score)
    getStats(hamList, spamList)


if __name__ == '__main__':
    main()
