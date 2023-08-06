# Cryptous - The simplest encryption module for Python

*All our encryption method are resistant to attack by frequency analysis*

##### Example with the RSA algorithm

	import cryptous

	# Get public and private keys :
	keys = RSA.get_keys(503, 499)

	plain_text = "Hello World!" # Message to encrypt
	encrypted_text = RSA.Encryption(plain_text, keys["public_key"]) # Use public key for encrypt
	# -> "155736 128492 50025 134032 50694 58479 230367 136205 230858"

	decrypted_text = RSA.Decryption(encrypted_text, keys["private_key"]) # Use private key to decrypted_text
	# -> "Hello World!"

##### You can also do it with file

	import cryptous

	# Get public and private keys :
	keys = RSA.get_keys(503, 499)

	plain_text = "Hello World!" # Message to encrypt
	encrypted_text = RSA.Encryption("file.txt", keys["public_key"], type_of_entry="file") # Use public key for encrypt
	# -> Will encrypt the file

	decrypted_text = RSA.Decryption("file.txt", keys["private_key"], type_of_entry="file") # Use private key to decrypted_text
	# -> Will decrypt the fileù

## Changelog :

##### Encryption methods
- **RSA algorithm** ✔️
- **XOR algorithm** ✔️
- **CAESAR algorithm** ✔️

##### Tools :
- **prime numbers function** ✔️