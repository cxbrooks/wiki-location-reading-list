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

Ideally, it would be possible to use this facility with non-Wikipedia wikis.
However, the
[Wikipedia app supports only Wikipedia and not other MediaWikis](https://phabricator.wikimedia.org/T107042)

## Reading Lists in Wikipedia
The Wikipedia iOS and Android apps have [synced reading lists](https://www.mediawiki.org/wiki/Wikimedia_Apps/Synced_Reading_Lists) that could be used.  A browser plugin that [supports reading lists](https://www.mediawiki.org/wiki/Wikimedia_Apps/Reading_list_browser_extension) can be added to Firefox and other browsers.  The downside here is that sharing these reading lists is not supported.

* Mediawiki pages
  * [Reading Lists](https://www.mediawiki.org/wiki/Reading/Reading_Lists) - The Reading Lists API
  * [Wikimedia Apps - Offline support](https://www.mediawiki.org/wiki/Wikimedia_Apps/Offline_support) - Mentions [[#Kiwix |Kiwix]]

* Phabricator projects
  * [Reading list service component](https://phabricator.wikimedia.org/project/profile/2740/)
  * [Synchronized reading lists](https://phabricator.wikimedia.org/project/view/2483/)
  * [iOS-app-feature-Places](https://phabricator.wikimedia.org/project/profile/2008/)

* Phabricator tickets
  * [Reading lists on desktop and mobile web](https://phabricator.wikimedia.org/T194441)
  * [Shelve Offline Library code for now](https://phabricator.wikimedia.org/T195518)
  * [Generic version of Wikipedia mobile apps that other MediaWikis could reuse](https://phabricator.wikimedia.org/T107042)

### Reading Lists are private
A Mediawiki bot can read reading lists, but cannot update them.  This is because by design, bots don't have the `editmyprivateinfo` permission.  So, to add entries to a reading list, we must login as the user

### Places requires an internet connection
The Wikipedia app requires an internet connection to show nearby pages in the places map.  Ideally, if there was no internet connection, then the app would query any saved pages.

## Bugs and limitations
* This code is a proof of concept, locations and list_ids are hardwired in and need to be updated.
* The method of getting the username and password is pathetic.  The username and password cannot have a colon in them.


Source: https://github.com/cxbrooks/wiki-location-reading-list
