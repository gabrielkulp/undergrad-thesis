# Padding and unpadding functions to reach the block size.
# Takes and returns bytearrays

# AES always operates on 16 bytes
length = 16

# Skip padding?
enable = False

def pad(data):
	if not enable:
		return data
	
	# truncate if too long
	if len(data) > length - 1:
		data = data[:(length-1)]
	
	# what byte to append?
	padder = length - len(data)

	# append until target reached
	while len(data) < length:
		data.append(padder)
	
	return data


def unpad(data):
	if not enable:
		return data
	
	# get amount to unpad
	padder = data[-1]

	# remove that many bytes
	return data[:-padder]
