# dlc_authority_fetcher
Given a file of headings, it will return matching MARC authorities from Library of Congress

## Dependencies

Requires Python 2.X.  It relies on the opensearch library, which does not yet support Python 3.

You can install the opensearch and pymarc libraries with `pip install opensearch pymarc`

## Running the script

Your file should be formatted like so:

    Moran, Peggy, 1960-
    Golden retriever
    Dogs
    Our best friends

Run the script by calling `python fetch_authorities.py list_of_headings_to_search`, where list_of_headings_to_search is a file formatted as in the example above.

There are several options regarding searching specific thesauri, etc.  You can get a complete list of options by running `python fetch_authorities.py -h`

## Restrictions

By default, this script waits 10 seconds between each request (the Library of Congress "recommends that software programs submit a total of no more than 10 requests per minute").

## Acknowledgments

Special thanks to Josh Stompro for all your help with the specifics of id.loc.gov searching!
