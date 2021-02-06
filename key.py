try:
	with open('../../.password/google-maps/api', 'r') as fp:
		key = fp.readlines()

	key = ''.join(key)

except:
	# Insert your API key here
	key = 'AIzaSyDxydKN7Yt54JNmVw9opg9EcibCghjetgw'

