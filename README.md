# dlc_authority_fetcher
Given a file of headings, it will return matching MARC authorities from Library of Congress

Requires Python 2.X.  It relies on the opensearch library, which does not yet support Python 3.

By default, it waits 10 seconds between each request (the Library of Congress "recommends that software programs submit a total of no more than 10 requests per minute").

Your file should be formatted like so:

    Moran, Peggy, 1960-
    Golden retriever
    Dogs
    Our best friends

You can get a complete list of options by running `python fetch_authorities.py -h`

Special thanks to Josh Stompro for all your help with the specifics of id.loc.gov searching!
