import json

def getDistribution(metricsData, metricsName):
    
    percentile = metricsData["loadingExperience"]["metrics"][metricsName]["percentile"]
    divider = 100
    unit = ""
    if metricsName in ["LARGEST_CONTENTFUL_PAINT_MS", "FIRST_CONTENTFUL_PAINT_MS", "EXPERIMENTAL_TIME_TO_FIRST_BYTE"]:
        divider = 1000
        unit = " s"
    elif metricsName in ["INTERACTION_TO_NEXT_PAINT"]:
        divider = 1
        unit = " ms"
    
    percentile = f'{percentile/divider}{unit}'
    
    good= metricsData["loadingExperience"]["metrics"][metricsName]["distributions"][0]["proportion"]
    needsImprov= metricsData["loadingExperience"]["metrics"][metricsName]["distributions"][1]["proportion"]
    bad= metricsData["loadingExperience"]["metrics"][metricsName]["distributions"][2]["proportion"]
    return [percentile, good, needsImprov, bad]  

def printMetrics(metricsData):
   l = ''
   for metric in metricsData:
      l+=f'{metric[0]},{",".join([str(round(x, 3)) for x in metric[1:]])}'+','
   return l

#"CLS", "LCP","INP", "FID", "FCP", "TTFB", "FID"
def parseData(final, url):
  try:
    clsMetrics = getDistribution(final, "CUMULATIVE_LAYOUT_SHIFT_SCORE")
    lcpMetrics = getDistribution(final, "LARGEST_CONTENTFUL_PAINT_MS")
    inpMetrics = getDistribution(final, 'INTERACTION_TO_NEXT_PAINT')
    fcpMetrics = getDistribution(final, 'FIRST_CONTENTFUL_PAINT_MS')
    ttfbMetrix = getDistribution(final, 'EXPERIMENTAL_TIME_TO_FIRST_BYTE')
    fidMetrics = getDistribution(final, 'FIRST_INPUT_DELAY_MS')
    
    analysisTime = final["analysisUTCTimestamp"]
  except KeyError:
      print(f'<KeyError> One or more keys not found {url}.')
        
  try:
    metrisStr = printMetrics([clsMetrics, lcpMetrics, inpMetrics, fcpMetrics, ttfbMetrix, fidMetrics])
    row = f'{url},{analysisTime},{metrisStr}\n'
    #print(f'Writing {row}...')
    return row
  except NameError:
    print(f'<NameError> Failing because of KeyError {url}.')
    return f'{url}\n'

# with open('./test-data.json', 'r') as f:
#     data = json.load(f)
#     parseData(data, 'test')