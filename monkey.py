import random
import pprint
import argparse

pp = pprint.PrettyPrinter(indent=4)
parser = argparse.ArgumentParser(description='Monkey generated words.')
parser.add_argument('-p', metavar='probability', type=float, required=True,
                   help='probability that a letter will be chosen')
parser.add_argument('-i', metavar="iterations", type=int, default=100000,
                   help='number of iterations')
args = parser.parse_args()


def make_word(p):
    """Generates a word with len > 0 by accumulating random letters a-z.
    p is the probability that a certain letter will be chosen.
    Probability of word ending is 1 - 26p."""
    word = ""
    while(True):
        r = random.uniform(0, 1);
        if r < 26 * p:
            word += str(unichr(int(r / p) + 97))
        elif len(word):
            return word

def distribution_map(p, iters):
    """Generates words, stores in map keyed by word length, then word,
    with the value being the frequency of the word"""
    words = {};
    for i in xrange(iters):
        word = make_word(p);
        length = str(len(word))
        if length not in words:
            words[length] = {word: 0}
            found = False
        elif word not in words[length]:
            words[length][word] = 0
        words[length][word] += 1
    return words

def length_counts(dmap):
    """Counts # of unique words per word length"""
    counts = {}
    [counts.update({length.zfill(3): len(dmap[length])}) for length in dmap]
    return counts


def bar_graph(counts):
    """Builds a bar graph using a dict of strings, keyed by word length"""
    # Build map of percentage distribution
    total_count = sum(counts.values())
    highest_count = max(counts.values())
    percentages = {}
    for length in counts:
        per = float("{0:.2f}".format(
            counts[length] / float(total_count) * 100))
        # Only keep top 90% of results to avoid long tails
        if counts[length] >= float(highest_count / 10):
            percentages[length.zfill(3)] = per
    highest_percent = max(percentages.values())

    # Build horizontal bar graph with strings
    graph = {}
    for length in percentages:
        graph[length] = "".join(
            ["*" for i in xrange(int(percentages[length] * 50 / highest_percent))]) \
            + " {} ({}%)".format(counts[length], percentages[length])
    return graph

def start(p, iters):
    print("\nMonkey typing on keyboard, inventing words by typing random letters")
    print("\t- Probability of typing a letter: 26 * {} = {}%".format(args.p, args.p * 26 * 100))
    print("\t- Probability of ending word:               = {}%".format(100 - (args.p * 26 * 100)))
    print("\t- Iterations: {}\n".format(args.i))

    dmap = distribution_map(p, iters)
    counts = length_counts(dmap)
    print("Word length: # of unique words")
    print("------------------------------")
    pp.pprint(counts)

    print("\n\n")
    print("Word length: % of total unique words (top 90%)")
    print("------------------------------------------------")
    pp.pprint(bar_graph(counts))

    # Average length of unique word
    total_unique_words = sum(counts.values())
    tot = 0
    for length in dmap:
        tot += int(length) * len(dmap[length])
    avg = tot / total_unique_words

    print("\nTotal unique words created: {} (Avg length: {})".format(total_unique_words, avg))

    # Average length of all words
    total_all_words = sum([sum(dmap[length].values()) for length in dmap])
    tot = 0
    for length in dmap:
        tot += int(length) * sum(dmap[length].values())
    avg = tot / total_all_words

    print("\nTotal all words created: {} (Avg length: {})".format(total_all_words, avg))

    # Print some word that was created
    some_word = dmap[dmap.keys()[-1]]
    some_word = some_word.keys()[-1]
    print("\nOne of those crazy words is '{}'\n".format(some_word))

start(args.p, args.i)
