from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option('-i', type='string',
                      help='input corpus',
                      dest='input')
    parser.add_option('-s', type='int', default=3,
                      help='number of letters to base the chain on',
                      dest='size')
    parser.add_option('-n', type='int', default=5,
                      help='number of generated words',
                      dest='num')
    (options, args) = parser.parse_args()

    # required parameter
    if not options.input:
        parser.error('no input file is specified')

    ng = NameGen(options.input, size=options.size)
    # ...
