from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """
    # Let's define our first FST
    f1 = FST('soundex-generate')
    num_maps = ["aehiouwy","bfpv","cgjkqsxz","dt","l","mn","r"]

    for state in '12345678':
        f1.add_state(state)
    f1.initial_state = '1'

    # Set all the final states
    for letter in '2345678':
        f1.set_final(letter)

    # Add the arcs for step 1
    for letter in string.ascii_letters:
        f1.add_arc('1', '2', (letter), (letter))

    # add the arcs for step 2 and step 3
    states = "2345678"
    value = '0'
    index=0
    # for each sequence in ["aehiouwy","bfpv","cgjkqsxz","dt","l","mn","r"]
    for key in num_maps:
        # for each letter  in "aehiouwy"
        for letter in key:
            # for each state node in "2345678"
            for state in states:
                # add arcs from 2->3, 2->4 with letter,value
                if(state != states[index]):
                    # if dest node state is '2', arc should be letter, empty
                    if(value =='0'):
                        f1.add_arc(state,states[index], (letter), ())
                    else:
                        f1.add_arc(state,states[index], (letter), (value))
                # add arc to itself 2->2 with letter, empty
                else:
                    f1.add_arc(state,state, (letter), ())
        index+=1
        value = chr(ord(value) + 1)

    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('1')
    f2.add_state('2a')
    f2.add_state('2b')
    f2.add_state('3')
    f2.add_state('4')
    f2.add_state('5')
    f2.initial_state = '1'
    f2.set_final('2a')
    f2.set_final('2b')
    f2.set_final('3')
    f2.set_final('4')
    f2.set_final('5')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('1', '2a', (letter), (letter))

    for n in range(10):
        f2.add_arc('1', '3', (str(n)), (str(n)))
        f2.add_arc('2a', '2b', (str(n)), (str(n)))
        f2.add_arc('3', '4', (str(n)), (str(n)))
        f2.add_arc('2b', '4', (str(n)), (str(n)))
        f2.add_arc('4', '5', (str(n)), (str(n)))
        f2.add_arc('5', '5', (str(n)), ())
    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    # Indicate initial and final states
    f3.add_state('0')
    f3.add_state('1')
    f3.add_state('1a')
    f3.add_state('1b')
    f3.add_state('1c')
    f3.add_state('2')
    f3.add_state('3a')
    f3.add_state('3b')
    f3.add_state('4')
    f3.initial_state = '0'
    f3.set_final('4')

    # Add the arcs
    for letter in string.letters:
        f3.add_arc('0', '1', (letter), (letter))

    for n in range(10):
        f3.add_arc('1', '1a', (str(n)), (str(n)))
        f3.add_arc('1a', '1b', (str(n)), (str(n)))
        f3.add_arc('1b', '4', (str(n)), (str(n)))
        f3.add_arc('1', '2', (str(n)), (str(n)))
        f3.add_arc('1', '3a', (str(n)), (str(n)))
        f3.add_arc('3a', '3b', (str(n)), (str(n)))
    f3.add_arc('0', '1', (), ())
    f3.add_arc('1', '4', (), ('000'))
    f3.add_arc('2', '4', (), ('00'))
    f3.add_arc('3b', '4', (), ('0'))
    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()
    #
    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
    #trace(f3,user_input)
