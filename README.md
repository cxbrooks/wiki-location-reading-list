# wiki-location-reading-list

Given a location, update a Wikipedia reading list for all nearby pages.

## TL;DR
This is a proof of concept about how Wikipedia reading lists could be updated with nearby pages.

See mw-createentry.py for detailed instructions.

mw-createentry.py uses [mwclient](https://github.com/mwclient/mwclient), which must be installed with
```
pip install mwclient
```

## The problem being solved

As a reader of Wikipedia pages, I would like to be able to access
pages that are nearby my location when I have no internet access.

## Bugs and limitations
* This code is a proof of concept, locations and list_ids are hardwired in and need to be updated.
* The method of getting the username and password is pathetic.  The username and password cannot have a colon in them.
