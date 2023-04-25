import hashlib

"""
The purpose of this code is to encrypt a files using hashing by first breaking up the 
code into Blocks of size 1024(or specified as something else)
and strarting from the last block, hash it and conatenate it to the 
end of the block before it. Repeat this process until you get the hash of the first block. 

The functions only generate a hash and verify it. 

No function available for decryption. 
"""

# define the file path and block size 
file_path = '/home/burhan/Downloads/c.mp4'

block_size = 1024  # block size in bytes


def generateBlocks(file_path,block_size):
    """
    Computes a list that stores bytes of size 1KB in each cell representing chunks of the mp4 file

    :param file_path: The assciated path to the mp4 file
    :param block_size: The size of each chunk
    :return: The list of chunks
    """
    with open(file_path, 'rb') as f:
        mp4_bytes = f.read()  # read the entire mp4 file as bytes

    blocks = [mp4_bytes[i:i+block_size] for i in range(0, len(mp4_bytes), block_size)]
    return blocks

def hashing(chunks):
    """
    Compute the hash for the mp4 file using  SHA256

    :param chunks: A list of chunks of the mp4 file
    :return: a list containing all thre previus hashes upto h0
    """
    prev_hash = b''
    arr = []
    arr.append(prev_hash)    
    for chunk in reversed(chunks):
        prev_hash = hashlib.sha256(chunk+prev_hash).digest()
        arr.insert(0,prev_hash)
    return arr

def compHash(c,h):
    """
    Compute hash for a given block
    :param c: the chunk in bytes
    :param h: the hash being concatenated
    return: the computed hash 
    """
    comp_hash = hashlib.sha256(c+h).digest()
    return comp_hash

def verification(chunks, h0):
    """
    Verify if all blocks are hashed correctly

    :param chunks: A list that contains chunks of the mp4 file
    :param h0: a list of hashes 
    :return: False if even one block is not hashed correctly otherwise True
    """ 
    i = len(h0)-2
    for c in reversed(chunks):
        if not h0[i]== compHash(c,h0[i+1]):
            return "Hashin Rejected"
        i-=1
    return "Hashing Acccepted"


#Generating the hash and verifying it
chunks = generateBlocks(file_path,block_size)
h0 = hashing(chunks)

print("h0: ", h0[0].hex(),"\n")
print(verification(chunks,h0))


