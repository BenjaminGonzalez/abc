import requests
import multiprocessing
import time
import pandas as pd
import json
from functools import partial
import math

baseurl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=ASX:IFN&outputsize=full&apikey='
start = time.clock()

stocks = ["ABP","AX1","ABC","APT","AGL","ALQ","ALU","AJM","AWC","AMA","AYS","AMC","AMP","ANN","ANZ","APA","APX","ARB","AAD","ARF","ALL","ARQ","AHY","ASX","ALX","AIA","AMI","AZJ","ASL","AST","ASB","AAC","API","AHG","AVN","AOG","BOQ","BAP","BPT","BGA","BAL","BEN","BHP","BIN","BKL","BLA","BSL","BLD","BXB","BVS","BRG","BKW","BWP","BWX","CTX","CDD","CAR","CWP","CIP","CMA","CGF","CQE","CHC","CQR","CNU","CLW","CIM","CL1","CLQ","CWY","CUV","CCL","COH","COL","CKF","CBA","CPU","COE","CTD","CGC","CCP","CMW","CWN","CSL","CSR","CYB","DCN","DXS","DHG","DMP","DOW","DLX","ECX","ELD","EHL","EML","EPW","EHE","EVN","FAR","A2M","FBU","FLT","FMG","FNP","FPH","FXL","GDI","GEM","GMA","GMG","GNC","GOR","GOZ","GPT","GUD","GWA","GXL","GXY","HPI","HSN","HSO","HT1","HUB","HVN","IAG","IDR","IEL","IFL","IFM","IFN","IGL","IGO","ILU","IMD","IMF","INA","ING","INR","IOF","IPH","IPL","IRE","IRI","IVC","JBH","JHC","JHG","JHX","JMS","KAR","KDR","KGN","LLC","LNG","LNK","LOV","LYC","MFG","MGR","MIN","MLD","MLX","MMS","MND","MNY","MP1","MPL","MQG","MSB","MTS","MVF","MYO","MYR","MYS","MYX","NAB","NAN","NCK","NCM","NCZ","NEA","NEC","NGI","NHF","NSR","NST","NUF","NVT","NWH","NWL","NWS","NXT","OFX","OGC","OMH","OML","ORA","ORE","ORG","ORI","OSH","OZL","PDL","PGH","PLG","PLS","PME","PMV","PNI","PNV","PPS","PPT","PRU","PRY","PTM","QAN","QBE","QUB","REA","REG","RFF","RHC","RIC","RIO","RMD","RRL","RSG","RWC","S32","SAR","SBM","SCG","SCO","SCP","SDA","SDF","SEA","SEK","SFR","SGF","SGM","SGP","SGR","SHL","SHV","SIG","SIQ","SKC","SKI","SLC","SLK","SOL","SPK","SPL","SRV","SSM","STO","SUL","SUN","SVW","SWM","SXL","SXY","SYD","SYR","TAH","TCL","TGR","TLS","TME","TNE","TPM","TWE","URW","VCX","VEA","VLW","VOC","VRL","VRT","VVR","WBA","WBC","WEB","WES","WGN","WGX","WHC","WOR","WOW","WPL","WPP","WSA","WTC","XRO"]

api_keys = ["EX3EX8U1TBQEQD8M",
"YYSQHZ10U8MZ6RMP",
"DLIP7Y6GZQW0D3WX",
"7UOE15F2UJHVZZA5",
"GQX8LN1W2VCI879M"]

CPM = 5

http_proxy  = ["http://190.108.192.97:58021", "http://194.187.217.18:43521", "http://36.89.181.11:51813", "http://103.111.55.142:55055"]
proxyIndex = 0
globalIndex = 295


def internet_resource_getter(index, prox, stock):
    global stockIndex
    ticker = stocks[stock+index]
    key = api_keys[index]
    proxyDict = {
        "http": http_proxy[proxyIndex%len(http_proxy)],
    }
    session = requests.Session()
    stuff_got = []

    #print('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=ASX:'+ticker+'&outputsize=full&apikey='+key)
    response = session.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=ASX:'+ticker+'&outputsize=full&apikey='+key, proxies = proxyDict)
    if 'Time Series (Daily)' in response.json():
        df = pd.read_json(json.dumps(response.json()['Time Series (Daily)'])).transpose()
        df['ticker'] = ticker
        return df
    else:
        print(ticker+" FAILED TO GRAB!")
        return pd.DataFrame({'A' : []})

if __name__ == '__main__':
    #time.sleep(60)
    for i in range(math.floor(len(stocks)/5)):
        print("FETCHING")
        pool = multiprocessing.Pool(processes=4)
        pool_outputs = pool.map(partial(internet_resource_getter, prox=proxyIndex, stock=globalIndex), range(0, 5))
        pool.close()
        pool.join()
        print("FETCHED")
        timeBefore = time.time()
        if not (pool_outputs[0].empty):
            total_append = pool_outputs[0]
            for j in range(1, len(pool_outputs)):
                if not (pool_outputs[j].empty):
                    total_append = total_append.append(pool_outputs[j])

            total_append.reset_index(inplace=True);
            with open('xd.csv', 'a') as fd:
                fd.write(total_append.to_csv(header=(i == 0), index=False))
            print("SAVED! - "+str(i*5)+"/"+str(len(stocks))+" - DELAYING FOR " + str(60-(time.time()-timeBefore)))
        else:
            print("Batch "+str(i*5)+" FAILED!")
        time.sleep(60-(time.time()-timeBefore))
        proxyIndex += 1
        globalIndex += 5