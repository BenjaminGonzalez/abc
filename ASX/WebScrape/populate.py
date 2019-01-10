import requests
import pandas as pd
import json
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import random
import os
dirname = os.path.dirname(__file__)
file_name = os.path.join(dirname, 'cuck.csv')


COLUMN_NAMES=['ticker', 'desc']
finaldf = pd.DataFrame(columns=COLUMN_NAMES)

ticks = ["ABP","AX1","ABC","APT","AGL","ALQ","ALU","AJM","AWC","AMA","AYS","AMC","AMP","ANN","ANZ","APA","APX","ARB","AAD","ARF","ALL","ARQ","AHY","ASX","ALX","AIA","AMI","AZJ","ASL","AST","ASB","AAC","API","AHG","AVN","AOG","BOQ","BAP","BPT","BGA","BAL","BEN","BHP","BIN","BKL","BLA","BSL","BLD","BXB","BVS","BRG","BKW","BWP","BWX","CTX","CDD","CAR","CWP","CIP","CMA","CGF","CQE","CHC","CQR","CNU","CLW","CIM","CL1","CLQ","CWY","CUV","CCL","COH","COL","CKF","CBA","CPU","COE","CTD","CGC","CCP","CMW","CWN","CSL","CSR","CYB","DCN","DXS","DHG","DMP","DOW","DLX","ECX","ELD","EHL","EML","EPW","EHE","EVN","FAR","A2M","FBU","FLT","FMG","FNP","FPH","FXL","GDI","GEM","GMA","GMG","GNC","GOR","GOZ","GPT","GUD","GWA","GXL","GXY","HPI","HSN","HSO","HT1","HUB","HVN","IAG","IDR","IEL","IFL","IFM","IFN","IGL","IGO","ILU","IMD","IMF","INA","ING","INR","IOF","IPH","IPL","IRE","IRI","IVC","JBH","JHC","JHG","JHX","JMS","KAR","KDR","KGN","LLC","LNG","LNK","LOV","LYC","MFG","MGR","MIN","MLD","MLX","MMS","MND","MNY","MP1","MPL","MQG","MSB","MTS","MVF","MYO","MYR","MYS","MYX","NAB","NAN","NCK","NCM","NCZ","NEA","NEC","NGI","NHF","NSR","NST","NUF","NVT","NWH","NWL","NWS","NXT","OFX","OGC","OMH","OML","ORA","ORE","ORG","ORI","OSH","OZL","PDL","PGH","PLG","PLS","PME","PMV","PNI","PNV","PPS","PPT","PRU","PRY","PTM","QAN","QBE","QUB","REA","REG","RFF","RHC","RIC","RIO","RMD","RRL","RSG","RWC","S32","SAR","SBM","SCG","SCO","SCP","SDA","SDF","SEA","SEK","SFR","SGF","SGM","SGP","SGR","SHL","SHV","SIG","SIQ","SKC","SKI","SLC","SLK","SOL","SPK","SPL","SRV","SSM","STO","SUL","SUN","SVW","SWM","SXL","SXY","SYD","SYR","TAH","TCL","TGR","TLS","TME","TNE","TPM","TWE","URW","VCX","VEA","VLW","VOC","VRL","VRT","VVR","WBA","WBC","WEB","WES","WGN","WGX","WHC","WOR","WOW","WPL","WPP","WSA","WTC","XRO"]
random.shuffle(ticks)


print(finaldf)

for i, ticker in enumerate(ticks):
    delay = random.uniform(3, 10)
    print("==== "+str(i+1)+"/"+str(len(ticks))+" == "+ticker+" == Delaying For: "+str(delay))
    time.sleep(delay)
    print("GRABBING")
    try:
        dataA = requests.get("https://www.asx.com.au/asx/1/company/"+ticker+"?fields=primary_share,latest_annual_reports,last_dividend,primary_share.indices&callback=angular.callbacks._0")
        formattedTextA = dataA.text[21:-2]
        if (formattedTextA != ""):
            dataA = json.loads(formattedTextA)
            text = dataA['principal_activities']
            finaldf = finaldf.append({'ticker':ticker, 'desc':text}, ignore_index=True)
            print("GRABBED!")
            finaldf.to_csv(file_name, index=False)
        else:
            print("EMPTY!")
    except requests.exceptions.RequestException as e:
        print("FAILED TO GRAB!")


finaldf.to_csv(file_name, index=False)
