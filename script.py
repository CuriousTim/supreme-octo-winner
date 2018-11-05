from user import *

# Create instance of user manager to interact with user table in database
userManager = UserManager('example.db')

# Insert a fake user
userManager.createUser('root', 'password')

# Find a user
print(userManager.findByUsername('root'))       # expected value ('root', 'password')
print(userManager.findByUsername('student'))    # expected value ()

# Verify a user's password
print(userManager.verifyPassword('root', 'password'))           # expected value True
print(userManager.verifyPassword('root', ''))                   # expected value False
print(userManager.verifyPassword('student', 'hacktheplanet'))   # expected value False
