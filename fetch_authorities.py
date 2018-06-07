from opensearch import Client
from pymarc import MARCWriter, marcxml
from string import punctuation
from xml.sax._exceptions import SAXParseException
import argparse, os, re, sys, time, urllib

parser = argparse.ArgumentParser(description='Fetch MARC authority records from the Library of Congress')
parser.add_argument('filename', help='a file with headings on separate lines')
parser.add_argument('--matches', type=int, default=5, help='maximum number of matching records to download for each heading')
parser.add_argument('--output', '-o', default='authorities_to_load.mrc', help='name of the MARC file that you are downloading records into')
parser.add_argument('--exact', '-e', help='only download authority records that match the heading exactly', action='store_true')
vocabularies = parser.add_mutually_exclusive_group()
vocabularies.add_argument('--lcnaf-only', help='only download name authority records', action='store_true')
vocabularies.add_argument('--lcsh-only', help='only download subject authority records', action='store_true')
vocabularies.add_argument('--lcgft-only', help='only download genre/form authority records', action='store_true')
print_opts = parser.add_argument_group(title='Output options')
print_opts.add_argument('--print-matched-headings', '-m', help='Print headings that are matched and downloaded to STDOUT', action='store_true')
print_opts.add_argument('--print-unmatched-headings', '-u', help='Print headings that have no LC matches to STDOUT', action='store_true')
args = parser.parse_args()

try:
    search_client = Client('http://id.loc.gov/opensearch/')
    with open(args.filename) as authorized_terms:
        if args.lcnaf_only:
            heading_suffix = ' scheme:http://id.loc.gov/authorities/names'
        elif args.lcsh_only:
            heading_suffix = ' scheme:http://id.loc.gov/authorities/subjects'
        elif args.lcgft_only:
            heading_suffix = ' scheme:http://id.loc.gov/authorities/genreForms'
        else:
            heading_suffix = ''

        for term in authorized_terms:
            if args.exact:
                term_for_search = 'aLabel:"' + term.lstrip().rstrip() + '"'
            else:
                term_for_search = term.lstrip().rstrip('.,;')
            response = search_client.search(term_for_search + heading_suffix)
            if response.totalResults:
                if args.print_matched_headings:
                    print(term)
                i = 0
                for result in response:
                    if i < args.matches:
                        i = i + 1
                        if 'authorities' in result.link:
                            auth_id = re.search('.*\/authorities\/.*\/(.*)', result.link).group(1)
                            auth_file_url = 'http://lccn.loc.gov/' + auth_id + '/marcxml'
                            time.sleep(10)
                            urllib.urlretrieve (auth_file_url, 'tmp.marcxml')
                            try:
                                records = marcxml.parse_xml_to_array('tmp.marcxml')
                                writer = MARCWriter(file(args.output, 'ab'))
                                for r in records:
                                    writer.write(r)
                                    writer.close()
                                os.remove('tmp.marcxml')
                            except SAXParseException:
                                print('Could not parse MARCXML file')
                    else:
                        break
            elif args.print_unmatched_headings:
                print(term)
except IOError:
    print("File '%s' doesn't exist", args.filename)
    exit(1)
