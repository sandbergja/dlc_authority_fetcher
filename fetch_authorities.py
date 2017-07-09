from opensearch import Client
from pymarc import MARCWriter, marcxml
from string import punctuation
from xml.sax._exceptions import SAXParseException
import os, re, sys, time, urllib

if len(sys.argv) < 2:
    print("Please include the filename")
    exit(1)

fname = sys.argv[1]
try:
    search_client = Client('http://id.loc.gov/opensearch/')
    with open(fname) as authorized_terms:
        for term in authorized_terms:
            print term
            response = search_client.search(term.lstrip().rstrip('.,;'))
            i = 0
            for result in response:
                if i < 6:
                    i = i + 1
                    print("fetching record " + str(i))
                    if 'authorities' in result.link:
                        auth_id = re.search('.*\/authorities\/.*\/(.*)', result.link).group(1)
                        auth_file_url = 'http://lccn.loc.gov/' + auth_id + '/marcxml'
                        time.sleep(20)
                        urllib.urlretrieve (auth_file_url, 'tmp.marcxml')
                        try:
                            records = marcxml.parse_xml_to_array('tmp.marcxml')
                            writer = MARCWriter(file('authorities_to_load.mrc', 'ab'))
                            for r in records:
                                writer.write(r)
                                writer.close()
                            os.remove('tmp.marcxml')
                        except SAXParseException:
                            print('Could not parse MARCXML file')
                else:
                    break
except IOError:
    print("File '%s' doesn't exist", fname)
    exit(1)
