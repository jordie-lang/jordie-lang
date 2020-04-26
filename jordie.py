import interp
import sys


if len(sys.argv) < 1:
    print("Need to provide filename")

fn = sys.argv[1]

# Get text from source file
f = open(fn, "r")
source_string = f.read()
f.close()

interp.run(source_string)