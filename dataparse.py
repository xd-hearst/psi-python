import json

def getDistribution(metricsData, metricsName):
    percentile = metricsData["loadingExperience"]["metrics"][metricsName]["percentile"]/100
    good= metricsData["loadingExperience"]["metrics"][metricsName]["distributions"][0]["proportion"]
    needsImprov= metricsData["loadingExperience"]["metrics"][metricsName]["distributions"][1]["proportion"]
    bad= metricsData["loadingExperience"]["metrics"][metricsName]["distributions"][2]["proportion"]
    return [percentile, good, needsImprov, bad]  

def printMetrics(metricsData):
   l = ''
   for metric in metricsData:
      l+=f'{metric[0]},{",".join([str(round(x, 3)) for x in metric[1:]])}'
   return l

#"CLS", "LCP", "FID", "FCP", "TTFB", "fid"
def parseData(final, url):
  try:
    clsMetrics = getDistribution(final, "CUMULATIVE_LAYOUT_SHIFT_SCORE")
    lcpMetrics = getDistribution(final, "LARGEST_CONTENTFUL_PAINT_MS")
    inpMetrics = getDistribution(final, 'INTERACTION_TO_NEXT_PAINT')
    fcpMetrics = getDistribution(final, 'FIRST_CONTENTFUL_PAINT_MS')
    ttfbMetrix = getDistribution(final, 'EXPERIMENTAL_TIME_TO_FIRST_BYTE')
    fidMetrics = getDistribution(final, 'FIRST_INPUT_DELAY_MS')
    analysisTime =final["analysisUTCTimestamp"]
  except KeyError:
      print(f'<KeyError> One or more keys not found {url}.')
        
  try:
    metrisStr = printMetrics([clsMetrics, lcpMetrics, inpMetrics, fcpMetrics, ttfbMetrix, fidMetrics])
    row = f'{url},{analysisTime},{metrisStr}\n'
    return row
  except NameError:
    print(f'<NameError> Failing because of KeyError {url}.')
    return f'{url}\n'

# with open('./test-data.json', 'r') as f:
#     data = json.load(f)
#     parseData(data, 'test')