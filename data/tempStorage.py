
#all parsed node data is stored here.
#the reason we do this is because we shouldn't pass blender's `context` around as it's a bad practice
#instead we store all the data we need in this global dictionary and read it when exporting

#this is only written to in `materialParser.py` and read inside `jsonSaver.py`
GLOBAL_DATA_STORE = {}
