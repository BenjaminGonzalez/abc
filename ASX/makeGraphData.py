import pandas
import os
import math

dirname = os.path.dirname(__file__)
stockFile = os.path.join(dirname, 'data.csv')

csv_data = pandas.read_csv(stockFile, parse_dates=True)
csv_data.dropna(inplace=True)
csv_data = csv_data[csv_data['adjusted close'] != 0]

resolution = 50

finalCSV_data = pandas.DataFrame(columns=['Ticker','Index', 'Close'])

stocks = ["ABP","AX1","ABC","APT","AGL","ALQ","ALU","AJM","AWC","AMA","AYS","AMC","AMP","ANN","ANZ","APA","APX","ARB","AAD","ARF","ALL","ARQ","AHY","ASX","ALX","AIA","AMI","AZJ","ASL","AST","ASB","AAC","API","AHG","AVN","AOG","BOQ","BAP","BPT","BGA","BAL","BEN","BHP","BIN","BKL","BLA","BSL","BLD","BXB","BVS","BRG","BKW","BWP","BWX","CTX","CDD","CAR","CWP","CIP","CMA","CGF","CQE","CHC","CQR","CNU","CLW","CIM","CL1","CLQ","CWY","CUV","CCL","COH","COL","CKF","CBA","CPU","COE","CTD","CGC","CCP","CMW","CWN","CSL","CSR","CYB","DCN","DXS","DHG","DMP","DOW","DLX","ECX","ELD","EHL","EML","EPW","EHE","EVN","FAR","A2M","FBU","FLT","FMG","FNP","FPH","FXL","GDI","GEM","GMA","GMG","GNC","GOR","GOZ","GPT","GUD","GWA","GXL","GXY","HPI","HSN","HSO","HT1","HUB","HVN","IAG","IDR","IEL","IFL","IFM","IFN","IGL","IGO","ILU","IMD","IMF","INA","ING","INR","IOF","IPH","IPL","IRE","IRI","IVC","JBH","JHC","JHG","JHX","JMS","KAR","KDR","KGN","LLC","LNG","LNK","LOV","LYC","MFG","MGR","MIN","MLD","MLX","MMS","MND","MNY","MP1","MPL","MQG","MSB","MTS","MVF","MYO","MYR","MYS","MYX","NAB","NAN","NCK","NCM","NCZ","NEA","NEC","NGI","NHF","NSR","NST","NUF","NVT","NWH","NWL","NWS","NXT","OFX","OGC","OMH","OML","ORA","ORE","ORG","ORI","OSH","OZL","PDL","PGH","PLG","PLS","PME","PMV","PNI","PNV","PPS","PPT","PRU","PRY","PTM","QAN","QBE","QUB","REA","REG","RFF","RHC","RIC","RIO","RMD","RRL","RSG","RWC","S32","SAR","SBM","SCG","SCO","SCP","SDA","SDF","SEA","SEK","SFR","SGF","SGM","SGP","SGR","SHL","SHV","SIG","SIQ","SKC","SKI","SLC","SLK","SOL","SPK","SPL","SRV","SSM","STO","SUL","SUN","SVW","SWM","SXL","SXY","SYD","SYR","TAH","TCL","TGR","TLS","TME","TNE","TPM","TWE","URW","VCX","VEA","VLW","VOC","VRL","VRT","VVR","WBA","WBC","WEB","WES","WGN","WGX","WHC","WOR","WOW","WPL","WPP","WSA","WTC","XRO"]

def getSingleStockData(ticker):
    print(" ==== Stats for " + ticker + " ==== ")
    global finalCSV_data
    csv_selected_data = csv_data.loc[csv_data['ticker'] == ticker]
    csv_selected_data.sort_values(by=['date'])
    csv_selected_data.reset_index(inplace=True, drop=True)
    for j in range(0, resolution+1):
        alpha = j/resolution
        index = math.floor((len(csv_selected_data)-1)*alpha)
        selectedClose = csv_selected_data['adjusted close'][index]
        finalCSV_data = finalCSV_data.append({'Ticker':ticker,'Index':resolution-j, 'Close':selectedClose}, ignore_index=True)
    print("Data processed!")

for i in range(0, len(stocks)):
    getSingleStockData(stocks[i])

print("Saving to CSV...")
finalCSV_data.to_csv(os.path.join(dirname, 'finalStockHistorical.csv'), index=False)
print("Saved to CSV successfully")







