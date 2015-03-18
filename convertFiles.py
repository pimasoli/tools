""" Module convert.
Convert a single text-file or multiple text-files from source-encoding to target-encoding.
"""
import sys
import os
import argparse
import codecs

BUFFER_SIZE = 1024


def convert_files(input_dir, output_dir, src_encoding, target_encoding, root_dir=None):
    count = 0
    if root_dir is None:
        root_dir = input_dir
    for dirpath, dirnames, filenames in os.walk(input_dir):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            relative_path = os.path.relpath(file_path, root_dir)
            count += convert_file(file_path, os.path.join(output_dir, relative_path), src_encoding, target_encoding)
        for d in dirnames:
            count += convert_files(d, output_dir, src_encoding, target_encoding, root_dir)
    return count


def convert_file(input_file, output_file, src_encoding, target_encoding):
    try:
        with codecs.open(input_file, "r", src_encoding) as fin:
            if not os.path.exists(os.path.dirname(output_file)):
                os.makedirs(os.path.dirname(output_file))
            with codecs.open(output_file, "w", target_encoding) as fout:
                while True:
                    content = fin.read(BUFFER_SIZE)
                    if not content:
                        break
                    fout.write(content)
            print 'file %s converted to UTF-8 and written to %s' % (input_file, output_file)
        return 1
    except Exception, err:
        sys.stderr.write('ERROR converting file %s: %s\n' % (input_file, str(err)))
        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Convert a single text-file or multiple text-files from source-encoding to target-encoding.')
    # TODO make args required
    parser.add_argument('-i', '--input', help='the input file or directory', dest='input', required=True)
    parser.add_argument('-o', '--output', help='the output file or directory', dest='output', required=True)
    parser.add_argument('-s', '--src-encoding', help='the source encoding', dest='src_encoding', required=True)
    parser.add_argument('-t', '--target-encoding', default='UTF-8', help='the target encoding (default=UTF-8)',
                        dest='target_encoding', required=True)
    parser.add_argument('-r', '--recursive', default=False,
                        help='recursively convert a directory instead of a single file', action='store_true',
                        dest='recursive')
    args = parser.parse_args()
    print
    if args.recursive:
        count = convert_files(args.input, args.output, args.src_encoding, args.target_encoding)
    else:
        count = convert_file(args.input, args.output, args.src_encoding, args.target_encoding)
    print 'converted %d files' % count

if __name__ == "__main__":
    main()
