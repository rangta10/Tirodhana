import codecs

def encode(payload):
    return codecs.encode(payload, 'rot_13')

def decode(payload):
    return codecs.decode(payload, 'rot_13')
