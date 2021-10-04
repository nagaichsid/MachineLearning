USAGE:

Simply run the SpamFilter.py file to see the output on the test data found in /HamSpam/test/

Model Hyperparameters:

Alpha = 0.01 (anything below this value did not seem to change performance, anything above this value decreased the quality of  performance)

Vocabulary = 170000 (this value did not affect performance except under extreme cases that could not be reasonably justified in the English language, and those cases caused poorer performance)


Model Statistics:

TP = 37
FP = 13
TN = 50
FN = 0
P = 0.74
R = 1.0
F1 = 0.8505747126436781


The model has perfect recall, meaning that it captures all instances of spam. However, this is because the model is probably too cautious in its predictions, which results in its lower precision. This means that it calls more emails spam than it should. In the case of a spam filter, it may be beneficial to have high recall for the safety of the user (viruses, phishing, etc.), though I would like to see higher precision as well so that the user does not miss potentially relevant (ham) emails.