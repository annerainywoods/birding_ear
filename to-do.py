'''

MIX DETAIL
- figure out state filters
- move mix data out of view and into API
    for each mix ( mix nickname & description, drill settings, for each bird static and user data )
    can API hold calculated data? How many birds are learned, how many total
- use API to generate the bird list on the mix
- set classes of "favorite" and "excluded" on the bird links

MIX EDIT
- value for "All" should be NULL
- trigger color option selected without onload in body, and without flicker
- display an input for all selected state filters
- display an input for all selected bird types
- how to update database with form data
- get popovers functional for find other plugin

MIX NEW
- can this use the same template? Differences: no placeholder values, color should be theme grey
- how to save initial form data
- is there where userbird is created? User bird may also need to be created on bird detail page

BIRD DETAIL
- form for favorite and excluded needs to update via API
- need to find mixes with specific bird
- fix check box style on firefox (and other browsers?)

HOME
- use api to get learned and total numbers
- if learned = total, give mix the trophy class

BASE
- get menu js into external file

MODELS
- make mix nickname unique=True - will this be true for the user or for the system?
- Userbird, display bird name and user id. What about Drill and Mix?

'''