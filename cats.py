"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    paragraphs = [word for word in paragraphs if select(word)]
    if k < len(paragraphs):
        return paragraphs[k]
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2

    def contains_word(paragraph):
        paragraph = split(remove_punctuation(lower(paragraph)))
        for word in topic:
            if word in paragraph:
                return True
        return False
    return contains_word
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    correct = 0
    total = len(typed_words)
    if not total:
        return 0.0
    for i in range(len(reference_words)):
        if i <= total-1:
            if typed_words[i] == reference_words[i]:
                correct += 1
        else:
            break
    percentage_correct = (correct / total) * 100
    return percentage_correct
    # END PROBLEM 3


accuracy("12345", "12345")


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    estimated_words = len(typed) / 5
    return estimated_words * (1 / (elapsed / 60))
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    else:
        # check for the word that has the lowest difference from the provided user word based off diff function
        closest_word = valid_words[0]
        smallest_difference = diff_function(user_word, valid_words[0], limit)
        for word in valid_words:
            current_difference = diff_function(user_word, word, limit)
            if current_difference < smallest_difference:
                smallest_difference = current_difference
                closest_word = word
        if smallest_difference <= limit:
            return closest_word
        else:
            return user_word
        # if lowest difference between user_word and any of the valid_words is greater than limit, return user_word

    # END PROBLEM 5


def sphinx_swap(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    # base case: if no letters left in start or goal, return limit
    if start == goal:
        return 0
    elif start == '' or goal == '':
        return len(start) + len(goal)
    elif limit == 0:
        return 1
    else:
        if start[0] != goal[0]:
            return sphinx_swap(start[1:], goal[1:], limit - 1) + 1
        else:
            return sphinx_swap(start[1:], goal[1:], limit)

    # def count_changes(start, goal):
    #     if start == '' or goal == '':
    #         return len(start) + len(goal)
    #     else:
    #         if start[0] != goal[0]:
    #             return count_changes(start[1:], goal[1:]) + 1
    #         else:
    #             return count_changes(start[1:], goal[1:])
    # number_of_changes = count_changes(start, goal)
    # if number_of_changes <= limit:
    #     return number_of_changes
    # else:
    #     return limit + 1

    # END PROBLEM 6


# sum([sphinx_swap('yond', 'yo', k) > k for k in range(4)])
sphinx_swap('car', 'cad', 0)
sum([sphinx_swap('pc', 'pc', k) > k for k in range(2)])


def feline_fixes(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    if start == goal:
        return 0
    elif start == '' or goal == '':
        return len(start) + len(goal)
    elif limit == 0:  # Feel free to remove or add additional cases
        # BEGIN
        return 1
        # END
    else:
        # Fill in these lines
        if start[0] != goal[0]:
            add_diff = feline_fixes(start[0:], goal[1:], limit-1) + 1
            remove_diff = feline_fixes(start[1:], goal[0:], limit-1) + 1
            substitute_diff = feline_fixes(start[1:], goal[1:], limit-1) + 1
            return min(add_diff, remove_diff, substitute_diff)
        else:
            return feline_fixes(start[1:], goal[1:], limit)
        # BEGIN
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    number_correct = 0
    for i in range(len(typed)):
        if typed[i] == prompt[i]:
            number_correct += 1
        else:
            break
    proportion_correct = number_correct / len(prompt)
    send({'id': id, 'progress': proportion_correct})
    return proportion_correct
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    # time_differences = [time[i+1] - time[i]
    #                     for time in times_per_player for i in range(len(time)-1)]
    # can i do this somehow?? ^^^^
    time_differences = []
    for times in times_per_player:
        times = [times[i+1] - times[i] for i in range(len(times)-1)]
        time_differences.append(times)
    return game(words, time_differences)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    players = range(len(all_times(game)))  # An index for each player
    words = range(len(all_words(game)))    # An index for each word
    times = all_times(game)
    # BEGIN PROBLEM 10
    # at every player index, see which one was fastest among all players
    # append that word to the list at the player index
    fastest_words_lst = []
    for x in players:
        fastest_words_lst.append([])
    for i in words:
        fastest = times[0][i]
        fastest_player = 0
        for j in players:  # this goes through each times list for every individual player
            if times[j][i] < fastest:
                fastest = times[j][i]
                fastest_player = j
        fastest_words_lst[fastest_player].append(word_at(game, i))
    return fastest_words_lst

    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]
               ), 'words should be a list of strings'
    assert all([type(t) == list for t in times]
               ), 'times should be a list of lists'
    assert all([isinstance(i, (int, float))
                for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]
               ), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    def select(p): return True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)


p0 = [2, 2, 3]
p1 = [6, 1, 2]
fastest_words(game(['What', 'great', 'luck'], [p0, p1]))
