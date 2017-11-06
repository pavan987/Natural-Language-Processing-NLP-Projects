import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    # Indicate initial and final states
    f.add_state('start')
    f.initial_state = 'start'
    f.add_state('znod1')
    f.add_state('znod2')
    f.add_state('0')
    f.add_state('units')
    f.add_state('tens')
    f.add_state('hundreds')
    f.add_state('unod1')
    f.add_state('unod2')
    f.add_state('1s')
    f.add_state('1e')
    f.add_state('2-9s')
    f.add_state('tnod1')
    f.add_state('11s')
    f.add_state('11e')
    f.add_state('10-60s')
    f.add_state('10-60e')
    f.add_state('11-16s')
    f.add_state('12-16e')
    f.add_state('7090s')
    f.add_state('80s')
    f.add_state('100-900s')
    f.add_state('100-900t')
    f.add_state('100-900e')

    # add arcs to first level
    f.add_arc('start', 'znod1', ('0'), ())
    f.add_arc('znod1', 'znod2', ('0'), ())
    f.add_arc('znod2', '0', ('0'), [kFRENCH_TRANS[0]])
    f.set_final('0')
    f.add_arc('start', 'units', (), ())
    f.add_arc('start', 'tens', (), ())
    f.add_arc('start', 'hundreds', (), ())

    # covers 1
    f.add_arc('units', 'unod1', ('0'), ())
    f.add_arc('unod1', 'unod2', ('0'), ())
    f.add_arc('unod2', '1s', (), ())
    f.add_arc('1s', '1e', ('1'), [kFRENCH_TRANS[1]])
    f.set_final('1e')

    # Covers 2-9
    for i in range(2,10):
        f.add_arc('unod2', '2-9s', (str(i)), [kFRENCH_TRANS[i]])
    f.set_final('2-9s')

    # covers 10-60
    f.add_arc('tens', 'tnod1', ('0'), ())
    for i in range(1,7):
        f.add_arc('tnod1', '10-60s', (str(i)), [kFRENCH_TRANS[i*10]])
    f.add_arc('10-60s', '10-60e', ('0'), ())
    f.add_arc('10-60s', 'unod2', (), ())
    f.add_arc('10-60s', '1s', (), [kFRENCH_AND])
    f.set_final('10-60e')

    # covers 11-16
    f.add_arc('tnod1', '11-16s', ('1'), ())
    #f.add_arc('11-16s', 'units', (), ())

    # covers 11
    f.add_arc('11-16s', '11s', (), ())
    f.add_arc('11s', '11e', ('1'), [kFRENCH_TRANS[11]])
    f.set_final('11e')

    # covers 12 - 19
    for i in range(2,7):
        f.add_arc('11-16s', '12-16e', (str(i)), [kFRENCH_TRANS[i+10]])
    f.set_final('12-16e')

    # covers 70-90
    f.add_arc('tnod1', '7090s', ('7'), [kFRENCH_TRANS[60]])
    f.add_arc('tnod1', '7090s', ('9'), [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]])
    f.add_arc('7090s', 'unod2', (), [kFRENCH_TRANS[10]])
    f.add_arc('7090s', '11-16s', (), ())
    f.add_arc('7090s', '10-60e', ('0'), [kFRENCH_TRANS[10]])
    f.add_arc('tnod1', '80s', ('8'), [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]])
    f.add_arc('80s', 'unod2', (), ())
    f.add_arc('80s', '10-60e', ('0'), ())

    # Covers 100 - 900

    f.add_arc('hundreds', '100-900s', ('1'), [kFRENCH_TRANS[100]])
    for i in range(2,10):
        f.add_arc('hundreds', '100-900s', (str(i)), [kFRENCH_TRANS[i]+" "+kFRENCH_TRANS[100]])
    f.add_arc('100-900s', 'tnod1', (), ())
    f.add_arc('100-900s', '100-900t', ('0'), ())
    f.add_arc('100-900t', 'unod2', (), ())
    f.add_arc('100-900t', '100-900e', ('0'), ())
    f.set_final('100-900e')

    return f

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
