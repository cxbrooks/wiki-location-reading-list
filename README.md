# wiki-location-reading-list

Given a location, update a Wikipedia reading list for all nearby pages.

## TL;DR
This is a proof of concept about how Wikipedia reading lists could be updated with geographically nearby pages.

See [mw-createentry.py](mw-createentry.py) for detailed instructions.

mw-createentry.py uses [mwclient](https://github.com/mwclient/mwclient), which must be installed with
```
pip install mwclient
```

## The problem being solved

As a reader of Wikipedia pages, I would like to be able to access
pages that are nearby my location when I have no internet access.

In the perfect world, a user would be able to use the Wikipedia iOS or
Android app while they had connectivity and save pages within a
certain distance of a location.

## Reading Lists in Wikipedia
The Wikipedia iOS and Android apps have [synced reading lists](https://www.mediawiki.org/wiki/Wikimedia_Apps/Synced_Reading_Lists) that could be used.  A browser plugin that [supports reading lists](https://www.mediawiki.org/wiki/Wikimedia_Apps/Reading_list_browser_extension) can be added to Firefox and other browsers.  The downside here is that sharing these reading lists is not supported.

* [Reading Lists](https://www.mediawiki.org/wiki/Reading/Reading_Lists) (mediawiki) - The Reading Lists API

* Phabricator projects
  * [Reading list service component](https://phabricator.wikimedia.org/project/profile/2740/)
  * [Synchronized reading lists](https://phabricator.wikimedia.org/project/view/2483/)

* Phabricator tickets
  * [Reading lists on desktop and mobile web](https://phabricator.wikimedia.org/T194441)
  * [Shelve Offline Library code for now](https://phabricator.wikimedia.org/T195518)

* [Wikimedia Apps - Offline support](https://www.mediawiki.org/wiki/Wikimedia_Apps/Offline_support) - Mentions [[#Kiwix |Kiwix]]

### Reading Lists are private
A Mediawiki bot can read reading lists, but cannot update them.  This is because by design, bots don't have the `editmyprivateinfo` permission.  So, to add entries to a reading list, we must login as the user

## Bugs and limitations
* This code is a proof of concept, locations and list_ids are hardwired in and need to be updated.
* The method of getting the username and password is pathetic.  The username and password cannot have a colon in them.
* If there is no internet, will the Wikipedia app still show nearby locations?

Source: https://github.com/cxbrooks/wiki-location-reading-list
