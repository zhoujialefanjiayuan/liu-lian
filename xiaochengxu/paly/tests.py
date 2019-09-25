import hashlib
from django.test import TestCase

# Create your tests here.
list=['wnnn','123','swef']
shaa = hashlib.sha1()
map(shaa.update, list)
hashcode = shaa.hexdigest()
print( hashcode)