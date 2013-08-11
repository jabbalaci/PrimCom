try:
    import cPickle as pickle            # faster
except:
    import pickle
 

data1 = [ { 'a':'one', 'b':2, 'c':3.0 } ]
print 'DATA: ',
print(data1)

data1_string = pickle.dumps(data1)      # here: pickling
print 'PICKLE:', data1_string

data2 = pickle.loads(data1_string)      # here: unpickling
print 'UNPICKLED:',
print(data2)

print 'SAME?:', (data1 is data2)
print 'EQUAL?:', (data1 == data2)

# * By default, the pickled byte stream contains ASCII characters only.
# * The pickle format is specific to Python.
# * Never unpickle data received from an untrusted or unauthenticated source.
# * Only the data for the instance is pickled, not the class definition, thus
#     when you want to unpickle instances of a class, don’t forget to import 
#     the definition of this class!
