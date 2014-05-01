"""
Copyright (c) 2013, Sam Dodrill
All rights reserved.

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

    1. The origin of this software must not be misrepresented; you must not
    claim that you wrote the original software. If you use this software
    in a product, an acknowledgment in the product documentation would be
    appreciated but is not required.

    2. Altered source versions must be plainly marked as such, and must not be
    misrepresented as being the original software.

    3. This notice may not be removed or altered from any source
    distribution.
"""

phrases = [" in your pants", "... ladies", " in bed", " at night",
        " with your mother", "... that's what she said", " #420", " #swag",
        " #yolo", " LE MAYMAY", " so edgy", " #yoloswag"]

from random import choice
from utils import *

NAME="Immature phrase appender"
DESC="Makes anything people say immature."

def initModule(cod):
    cod.addBotCommand("IMMATURE", commandIMMATURE)

def destroyModule(cod):
    cod.delBotCommand("IMMATURE")

def rehash():
    pass

def commandIMMATURE(cod, line, splitline, source, destination):
    return immature(" ".join(splitline[1:]))

def immature(tweet, no_url=True):
    """A very childish function. Takes any string input (assumes a sentence) and appends "in your pants" to it, preserving case if nessecary."""
    conditions = [tweet.endswith("!"), tweet.endswith("."), tweet.endswith("?")]
    valid = reduce(lambda x,y: (x or y), conditions)
    #print valid

    if "http" in tweet.split()[-1]:
        return in_your_url(tweet, no_url)
    #jump to the special condition!
    elif ":" in tweet:
        return in_your_colon(tweet)

    if valid:
        split_tweet = tweet.split()

        derp = True

        if len(split_tweet) == 1:
            derp = False

        if derp and split_tweet[-2].isupper() and split_tweet[-1].isupper():
            return tweet[:-1] + choice(phrases).upper() + tweet[-1]
        else:
            return tweet[:-1] + choice(phrases) + tweet[-1]
    else:
        split_tweet = tweet.split()

        derp = True

        if len(split_tweet) == 1:
            derp = False

        if derp and split_tweet[-2].isupper() and split_tweet[-1].isupper():
            return tweet + choice(phrases).upper()
        else:
            return tweet + choice(phrases)

def in_your_url(tweet, no_url):
    """
    Deals with URLs
    """
    split_tweet = tweet.split()
    urlAtEnd = split_tweet[-1].startswith("http")

    if urlAtEnd:
        return immature(rejoin(split_tweet[:-1])) + " " + split_tweet[-1]
    else:
        return split_tweet[0] + " " + immature(split_tweet[1:])

def in_your_colon(tweet):
    return immature(str(tweet.split(":")[0])) + ":" + rejoin(tweet.split(":")[1:])

def rejoin(string_ara, delim=" "):
    try:
        r = str(reduce(lambda x,y: x + delim + y, string_ara))
    except:
        r = ""
    return r

def count(string, pattern):
    r = 0

    for n in string:
        if n == pattern:
            r = r + 1

    return r

def test():
    print immature("I am awesome.")
    print immature("SO COOL DRAGONITE!")
    print immature("check out my site! http://herp.derp")
    print immature("OPERATION SIMPLISTIC SALTY GREAT GRAPE RAPE APE")
    print immature("OPERATION EXPECT NO MERCY FROM OUR JUMBLED DISCOVERY")
    print immature("OPERATION TWISTING ADAPTABLE BREATH")

if __name__ == "__main__":
    test()
