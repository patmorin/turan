#!/usr/bin/python3

#coding=utf-8
import itertools

# copied from python itertools documentation
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) \
            for r in range(len(s)+1))

names = ["bat", "crossing", "taco", "nested",
         "mariposa", "david", "ears", "swords"]
for i in range(len(names)):
    globals()[names[i]] = i
#taco, mariposa, bat, nested, crossing, swords, david, ears = range(8)

def pack_set(iterable):
    x = 0
    for y in iterable:
        x |= 1 << y
    return x

def pack(*args):
    return pack_set(args)

def unpack(x):
    stuff = list()
    i = 0
    while x > 0:
        if x & 1:
            stuff.append(i)
        i += 1
        x >>= 1
    return set(stuff)

def tostring(x):
    return [names[i] for i in unpack(x)]

def format_exponent(c):
    if c == -1:
        return "0"
    if c == 0:
        return "1"
    if c == 1:
        return "n"
    return "n^{{{}}}".format(c)

def print_everything(upper_bounds, lower_bounds):
    print("="*60)
    tight = 0
    for x in range(2**8):
        if x in upper_bounds and x in lower_bounds \
            and upper_bounds[x] == lower_bounds[x]:
            print("ex(n,{{{}}}) = Θ({})".format(",".join(tostring(x)),
                                                format_exponent(upper_bounds[x])))
            tight += 1
        else:
            if x in upper_bounds:
                print("ex(n,{{{}}}) = O({})".format(",".join(tostring(x)),
                                                    format_exponent(upper_bounds[x])))
            if x in lower_bounds:
                print("ex(n,{{{}}}) = Ω({})".format(",".join(tostring(x)),
                                                    format_exponent(lower_bounds[x])))
    print("Found {} tight results".format(tight))

def n2s(i, cfgs):
    if i in unpack(cfgs):
        return r'\{}'.format(names[i])
    return ''

def make_table(fp, upper_bounds, lower_bounds, old_upper_bounds=None,
               old_lower_bounds=None):
    if not old_upper_bounds: old_upper_bounds = upper_bounds
    if not old_lower_bounds: old_lower_bounds = lower_bounds
    colcfgs = [swords, david, ears]
    rowcfgs = [taco, bat, nested, crossing]
    cols = sorted([pack_set(s) for s in powerset(colcfgs)])[::-1]
    rows = sorted([pack_set(s) for s in powerset(rowcfgs)])[::-1]
    tight = 0
    fp.write(r'\begin{{tabular}}{{|c@{{\,}}c@{{\,}}c@{{\,}}c{}|}}\hline'.format('|C'*8) + '\n')
    for i in colcfgs:
        fp.write("&&&&")
        fp.write("&".join([n2s(i, c) for c in cols]))
        if i == colcfgs[-1]:
            fp.write(r' \\ ' + '\n')
        else:
            fp.write(r' \\[-1mm] ' + '\n')
    fp.write(r'\hline')

    for r in rows:
        fp.write("&".join([n2s(i, r) for i in rowcfgs]))
        fp.write(r'$\rule{0mm}{1em}$')
        for c in cols:
            x = r|c
            if upper_bounds[x][0] == lower_bounds[x][0]:
                colour = 'green'
                tight += 1
            else:
                colour = 'red'

            modifier = ''
            if old_upper_bounds[x][0] == upper_bounds[x][0] \
                  and old_lower_bounds[x][0] == lower_bounds[x][0]:
                opacity = 10
            else:
                opacity = 40
                if old_upper_bounds[x][0] > 1 and upper_bounds[x][0] == 1:
                    modifier='^*'

            if 1 < lower_bounds[x][0] < 2:
                fp.write(r'&\cellcolor{{{}!{}}}tripods'.format(colour, opacity))
            elif upper_bounds[x][0] == lower_bounds[x][0]:
                fp.write(r'&\cellcolor{{{}!{}}}${}{}$\newline {}:{}'.format(colour, opacity,
                                                            format_exponent(upper_bounds[x][0]),
                                                            modifier,
                                                            lower_bounds[x][1],
                                                            upper_bounds[x][1]))
            else:
                fp.write(r'&\cellcolor{{{}!{}}}${}:{}$\newline {}:{}'.format(colour, opacity,
                                                         format_exponent(lower_bounds[x][0]),
                                                         format_exponent(upper_bounds[x][0]),
                                                         lower_bounds[x][1],
                                                         upper_bounds[x][1]))
        fp.write(r'\\ \hline' + '\n')
    fp.write(r'\end{tabular}')
    print("Found {} tight bounds".format(tight))


def close_bounds(upper_bounds, lower_bounds):
    # Mariposas don't matter
    for k in list(upper_bounds.keys()):
        s = unpack(k)
        x = pack_set(s ^ {mariposa})
        if x in upper_bounds and upper_bounds[x][0] < upper_bounds[k][0]:
            upper_bounds[k] = upper_bounds[x]
        upper_bounds[x] = upper_bounds[k]

    for k in list(lower_bounds.keys()):
        s = unpack(k)
        x = pack_set(s ^ {mariposa})
        if x in lower_bounds and lower_bounds[x][0] > lower_bounds[k][0]:
            lower_bounds[k] = lower_bounds[x]
        lower_bounds[x] = lower_bounds[k]

    # Create all upper bounds inherited by superset relationships
    for k in list(upper_bounds.keys()):
        these = set(unpack(k))
        others = set(range(8)) - these
        for s in powerset(others):
            x = pack_set(these|set(s))
            if x not in upper_bounds or upper_bounds[x][0] > upper_bounds[k][0]:
                upper_bounds[x] = upper_bounds[k]

    # Create all lower bounds inherited by subset relationship
    for k in list(lower_bounds.keys()):
        these = set(unpack(k))
        for s in powerset(these):
            x = pack_set(s)
            if x not in lower_bounds or lower_bounds[x][0] < lower_bounds[k][0]:
                lower_bounds[x] = lower_bounds[k]


if __name__ == "__main__":

    upper_bounds = dict()
    lower_bounds = dict()

    # Trivial stuff
    upper_bounds[pack_set([])] = (3, 'F')  # empty set is Theta(n^3)
    upper_bounds[pack_set(range(8))] = (0, 'F')  # complete set is Theta(1)

    # These are all due to Brass
    upper_bounds[pack(mariposa)] = (3, r'\cite{brass:turan}')
    upper_bounds[pack(taco)] = (2, r'\cite{brass:turan}')

    upper_bounds[pack(bat)] = (3, r'\cite{brass:turan}')
    upper_bounds[pack(nested)] = (2, r'\cite{brass:turan}')
    upper_bounds[pack(crossing)] = (2, r'\cite{brass:turan}')

    upper_bounds[pack(ears)] = (3, r'\cite{brass:turan}')
    upper_bounds[pack(swords)] = (2, r'\cite{brass:turan}')
    upper_bounds[pack(david)] = (2, r'\cite{brass:turan}')

    upper_bounds[pack(bat, nested)] = (2, r'\cite{brass:turan}')
    upper_bounds[pack(nested, crossing)] = (2, r'\cite{brass:turan}')
    upper_bounds[pack(bat, crossing)] = (2, r'\cite{brass:turan}')

    # This is Brass, Rote, and Swanepoel
    upper_bounds[pack(ears, swords, bat, nested)] = (1, r'\cite{brass.rote.ea:triangles}')

    # These are inherited from hypergraphs
    upper_bounds[pack(bat, nested, crossing)] = (1, 'H')
    upper_bounds[pack(taco)] = (2, 'H')
    upper_bounds[pack(ears, swords, david)] = (2, ('H'))

    # Up to here, everything is tight, so copy this to the lower bounds
    for k in upper_bounds:
        lower_bounds[k] = upper_bounds[k]

    # We have Omega(n) lower bounds for most everything
    s = set(range(8))-{mariposa}
    upper_bounds[pack_set(s)] = (0, 'F')
    for t in s:
        lower_bounds[pack_set(s-{t})] = (1, r'T\ref{thm:linear-lower}')

    close_bounds(upper_bounds, lower_bounds)
    fp = open("oldbounds.tex", "w")
    make_table(fp, upper_bounds, lower_bounds)
    fp.close()

    old_upper_bounds = dict(upper_bounds)
    old_lower_bounds = dict(lower_bounds)

    # New Upper bounds based on swords
    upper_bounds[pack(taco, swords)] = (1, r'T\ref{thm:taco-swords}')
    upper_bounds[pack(nested, swords)] = (1, r'T\ref{thm:nested-swords}')
    upper_bounds[pack(crossing, swords)] = (1, r'T\ref{thm:crossing-swords}')

    # New linear upper bounds
    upper_bounds[pack(taco, nested, crossing)] = (1, r'T\ref{thm:taco-nested-crossing}')
    upper_bounds[pack(nested, crossing, ears)] = (1, r'T\ref{thm:nested-crossing-ears}')
    upper_bounds[pack(taco, nested, david)] = (1, r'T\ref{thm:taco-nested-david}')
    upper_bounds[pack(nested, ears, david)] = (1, r'T\ref{thm:nested-ears-david}') # (2)
    upper_bounds[pack(nested, bat, david)] = (1, r'T\ref{thm:nested-bat-david}')  # new, replaces (1)

    # Upper bounds based on tripod packing
    lower_bounds[pack(taco, nested, bat, ears)] = (1.546, r'\cite{gowers.long:length}')  # Gowers and Long
    upper_bounds[pack(taco, nested)] = (2, r'\cite{ruzsa.szemeredi:triple}') # Induced matchings

    # New lower bounds
    lower_bounds[pack(ears, bat)] = (3, r'T\ref{thm:pairwise-crossing}')
    lower_bounds[pack(taco, david, crossing, bat, ears)] = (2, r'T\ref{dilwad}')
    lower_bounds[pack(swords, bat, ears, david)] = (2, r'T\ref{thm:swords-bat-ears-david}')
    # lower_bounds[pack(nested, ears, david)] = 2 # incorrect, replaced by (2)
    lower_bounds[pack(david, nested, crossing)] = (2, r'T\ref{thm:david-nested-crossing}')
    #lower_bounds[pack(nested, bat, david)] = 2  # (1)
    lower_bounds[pack(bat, nested, ears)] = (2, r'T\ref{thm:bat-nested-ears}')

    saved_ubs = dict(upper_bounds)
    saved_lbs = dict(lower_bounds)

    extremal_ubs = set()
    for k in upper_bounds:
        if k in old_upper_bounds and upper_bounds[k] != old_upper_bounds[k]:
            extremal_ubs.add(k)
    extremal_lbs = set()
    for k in lower_bounds:
        if k in old_lower_bounds and lower_bounds[k] != old_lower_bounds[k]:
            extremal_lbs.add(k)

    close_bounds(upper_bounds, lower_bounds)

    # Highlight extremal new bounds
    for k in extremal_ubs:
        if saved_ubs[k][1].startswith('T'):
            upper_bounds[k] = (upper_bounds[k][0],
                               r'\textbf{{{}}}'.format(upper_bounds[k][1]))
    for k in extremal_lbs:
        if saved_lbs[k][1].startswith('T'):
            lower_bounds[k] = (lower_bounds[k][0],
                               r'\textbf{{{}}}'.format(lower_bounds[k][1]))

    fp = open("bounds.tex", "w")
    make_table(fp, upper_bounds, lower_bounds, old_upper_bounds, old_lower_bounds)
    fp.close()
