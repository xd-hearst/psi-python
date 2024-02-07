import requests
from dotenv import load_dotenv
import os
from dataparse import parseData

load_dotenv()
apiKey = os.getenv("API_KEY")

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# Documentation: https://developers.google.com/speed/docs/insights/v5/get-started

# JSON paths: https://developers.google.com/speed/docs/insights/v4/reference/pagespeedapi/runpagespeed

def printMetrics(metricNames):
    l=''
    for metric in metricNames:
        names = [f'{metric}', f'{metric}-good', f'{metric}-needsImprov', f'{metric}-bad']
        l += ','.join(names)+','
    return l

filename = 'pagespeed-results-mobile.csv'
metricNames= ["CLS", "LCP","INP", "FID", "FCP", "TTFB"]
columnTitleRow = f'URL,analysisUTCTimestamp,{printMetrics(metricNames)}\n'

if not os.path.exists(filename):
    with open(filename, 'w', newline='') as f:
        f.write(columnTitleRow)


# Populate 'pagespeed.txt' file with URLs to query against API.
with open('./pagespeed.txt') as pagespeedurls:
    download_dir = './pagespeed-results-mobile.csv'
    file = open(download_dir, 'a')
    content = pagespeedurls.readlines()
    content = [line.rstrip('\n') for line in content]
  
    # This is the google pagespeed api url structure, using for loop to insert each url in .txt file
    for line in content:
        # If no "strategy" parameter is included, the query by default returns desktop data.
        x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={line}&strategy=mobile&key={apiKey}'
        print(f'Requesting {x}...')
        r = requests.get(x)
        final = r.json()
        
        try:
            row = parseData(final, line)
            file.write(row)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')
            file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')
