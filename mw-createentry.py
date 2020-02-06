#!/opt/local/bin/python3.7

"""mw-createentry.py

    Add a list of Wikipedia pages to a pre-existing Wikipedia reading list.

    Usage:

    1) Create a file called user-config.txt that has a single line with
    your Wikipedia account name and password, separated by a colon,
    followed by a newline.  The username and password cannot have a
    colon in them.

    For example:

       Jimbo:myunguessablepassword

    2) Update wiki-geosearch.py with the latitude and longitude of the
    location of interest.  Also update the radius of the area of distance.

    3) Run wiki-geosearch.py and save the output in a file called pages.txt
       python3 wiki-geosearch.py > pages.txt

    4) Run this file once to determine the id of the reading list to
    be updated.  If you don't have any reading lists, then use the
    Wikipedia iOS or Android client to create one.
       python3 mw-createentry.py

    5) Update the mw-createentry.py with the list_id and run it again:
       python3 mw-createentry.py

    MIT License

"""

from mwclient import Site
import logging
logging.basicConfig(level=logging.WARNING)

# The reading list id of the list to be updated.  To get this value, run this file once.
list_id = 2016297

ua = 'LocationReadingList/0.1 (User:Cxbrx)'
print("About to call site")
site = Site('en.wikipedia.org', clients_useragent=ua)

#print("About to get authmanagerinfo");
#result = site.api('query', meta='authmanagerinfo', amirequestsfor='login')
#print(result)

print("About to get login token")
result = site.api('query', meta='tokens', type='login', format='json')
login_token = result['query']['tokens']['logintoken']

# Get the username and password.
# FIXME: This assumes no : in either username or password.
with open('user-config.txt') as f:
    pieces = [x.strip().split(':', 1) for x in f]
username = pieces[0][0]
password = pieces[0][1]

print("About to call login")
result = site.api('clientlogin', username=username, password=password, logintoken=login_token, loginreturnurl='https://wn.wikipedia.org/')
print(result)

print("About to get reading lists")
result = site.api('query', http_method='GET', meta='readinglists', format='json')
print(result)
reading_lists = result['query']['readinglists']
RLE_LIST=[]
print("Here are your reading list ids and numbers.")
print("Edit mw-createentry.py with the id of the reading list you would like to update.")
for reading_list in reading_lists:
    print(reading_list['id'], reading_list['name'])
    RLE_LIST.append(reading_list['id'])

# Below is some test code that gets the reading list entries, adds an entry and then gets the reading list entries again.
#
#print(RLE_LIST)
#RLE_LIST2="|".join(map(str, RLE_LIST))                    
#print(RLE_LIST2)

# Get the reading list entries.
#result = site.api('query', http_method='GET', list='readinglistentries', rlelists=RLE_LIST2, format='json')
#print(result)

# print("About to get a CSRF token")
# result = site.api('query', http_method='GET', meta='tokens', format='json')
#print(result)

# csrf_token = result['query']['tokens']['csrftoken']
# print(csrf_token)

# print("About to create an entry")
# result = site.api('readinglists', command='createentry', list=list_id, project='https://www.mediawiki.org', title='Gerlach Water Tower', token=csrf_token)

# print("About to get the contents of a reading list")
# result = site.api('query', http_method='GET', list='readinglistentries', rlelists='1983196', format='json')
# print(result)

# Read the page names from pages.txt and add them to the list with the id of list_id
from io import StringIO
batch = StringIO()
batch.write('[')
total_length = 0
filepath = 'pages.txt'
with open(filepath) as fp:
    line = fp.readline()
    while line:
        while total_length < 400 and line:
            total_length = total_length + len(line)
            batch.write('{"project":"https://en.wikipedia.org","title":"')
            batch.write(line[0:len(line)-1])
            batch.write('"},')
            line = fp.readline()
        total_length = 0
        # Remove the trailing ,
        batch2 = batch.getvalue()
        batch = StringIO()
        batch.write('[')

        batch3 = batch2[0:len(batch2) - 1] + ']'
        print(batch3)

        result = site.api('query', http_method='GET', meta='tokens', format='json')
        csrf_token = result['query']['tokens']['csrftoken']

        result = site.api('readinglists', command='createentry', list=list_id, batch=batch3, token=csrf_token)
        print(result)

