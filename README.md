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

By default, it should append all downloaded authority records to a file called authorities_to_load.mrc.  You can change this with the `-o` or `--output` flag.  For example, you could run `python fetch_authorities.py -o records.mrc list_of_headings_to_search` if you want the authority records to go into a file called records.mrc.

There are several options regarding searching specific thesauri, etc.  You can get a complete list of options by running `python fetch_authorities.py -h`

## Restrictions

By default, this script waits 10 seconds between each request (the Library of Congress "recommends that software programs submit a total of no more than 10 requests per minute").

For this reason, it is strongly recommended that you only run one instance of this script at once.

## Acknowledgments

Special thanks to Josh Stompro for all your help with the specifics of id.loc.gov searching!
