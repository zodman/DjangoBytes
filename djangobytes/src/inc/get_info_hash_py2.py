#!/usr/bin/env python3

# imports
from benc import bdecode, bencode
import hashlib

# args:         torrentfile (str)... path to the torrent file
# return:       the info hash of the specified torrent file
def get_info_hash(torrentfile):
    f = open(torrentfile, 'rb')
    try:
        bencoded_data = bdecode(f.read())
    except ValueError:
        print('ERR: Invalid File')
        return
    # encode the value of the info key of the dictionary with the metainfo 
    # in sha1; encode the sha1 hash into hex.
    info_hash = hashlib.sha1(bencode(bencoded_data['info'])).hexdigest()
    return info_hash


if __name__ == '__main__':
 
    # imports
    import os, sys
    
    if len(sys.argv) == 2:
        fp = sys.argv[1]
	
        if not os.path.isfile(fp):
            print('no such file or directory: %s' % fp)
            sys.exit(1)

        info_hash = get_info_hash(fp)
        if not info_hash:
            sys.exit(1)
        print(info_hash)
        sys.exit(0)
   
    else:
        print("Usage: %s [torrentfile]" % sys.argv[0])
        sys.exit(1)
