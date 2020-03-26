import interp

# Get text from source file
f = open("tests/example.jordie", "r")
source_string = f.read()
f.close()

interp.run(source_string)