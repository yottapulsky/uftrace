import sys

func = ''
unit = 'b'
histo = None

divider = {
    'b': 1,
    'k': 1000,
    'K': 1000,
    'm': 1000000,
    'M': 1000000,
    'g': 1000000000,
    'G': 1000000000,
}

def create_histogram():
    h = []
    for i in range(12):
        h.append(0)
    return h

def get_histogram_index(val):
    if val < 0:
        return 0
    val = int(val / divider[unit])
    for i in range(10):
        if val < (1 << (i+1)):
            return i+1
    return 11

def print_histogram():
    total = sum(histo)
    if total == 0:
        print("no value")
        return

    print(" <  %4d%s  : %10d  (%5.1f %%)" % (0, unit, histo[0], 100.0 * histo[0] / total))
    for i in range(10):
        print(" <  %4d%s  : %10d  (%5.1f %%)" % (1 << (i+1), unit, histo[i+1], 100.0 * histo[i+1] / total))
    print(" >= %4d%s  : %10d  (%5.1f %%)" % (1024, unit, histo[11], 100.0 * histo[11] / total))

def parse_args(args):
    global func, unit
    if args[0] == '-u' or args[0] == '--unit':
        unit = args[1]
        func = args[2]
    else:
        unit = 'b'
        func = args[0]
#
# uftrace interface functions
#
def uftrace_begin(ctx):
    global histo
    if len(ctx["cmds"]) == 0:
        print("Usage: retval-histogram.py [-- -u <unit>] <function>")
        print("  Unit is one of b, k, m, g")
        return
    parse_args(ctx["cmds"])
    if unit not in divider:
        print("Usage: invalid unit: %s" % unit)
        return
    histo = create_histogram()

def uftrace_entry(ctx):
    pass

def uftrace_exit(ctx):
    global histo
    if histo is None:
        return
    if ctx["name"] != func:
        return
    if "retval" not in ctx:
        return
    retval = int(ctx["retval"])
    idx = get_histogram_index(retval)
    histo[idx] += 1

def uftrace_end():
    if histo is None:
        return
    print("histogram of return value of '%s'\n" % func)
    print_histogram()
