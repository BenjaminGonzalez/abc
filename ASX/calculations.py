import pandas
import os
dirname = os.path.dirname(__file__)
stockFile = os.path.join(dirname, 'data.csv')

csv_data = pandas.read_csv(stockFile, parse_dates=True)
csv_data.dropna(inplace=True)
csv_data = csv_data[csv_data['adjusted close'] != 0]

finalCSV_data = pandas.DataFrame(columns=['Ticker','LstdDev', 'pChange10d', '30dG', '90dG', 'close'])

stocks = ["ABP","AX1","ABC","APT","AGL","ALQ","ALU","AJM","AWC","AMA","AYS","AMC","AMP","ANN","ANZ","APA","APX","ARB","AAD","ARF","ALL","ARQ","AHY","ASX","ALX","AIA","AMI","AZJ","ASL","AST","ASB","AAC","API","AHG","AVN","AOG","BOQ","BAP","BPT","BGA","BAL","BEN","BHP","BIN","BKL","BLA","BSL","BLD","BXB","BVS","BRG","BKW","BWP","BWX","CTX","CDD","CAR","CWP","CIP","CMA","CGF","CQE","CHC","CQR","CNU","CLW","CIM","CL1","CLQ","CWY","CUV","CCL","COH","COL","CKF","CBA","CPU","COE","CTD","CGC","CCP","CMW","CWN","CSL","CSR","CYB","DCN","DXS","DHG","DMP","DOW","DLX","ECX","ELD","EHL","EML","EPW","EHE","EVN","FAR","A2M","FBU","FLT","FMG","FNP","FPH","FXL","GDI","GEM","GMA","GMG","GNC","GOR","GOZ","GPT","GUD","GWA","GXL","GXY","HPI","HSN","HSO","HT1","HUB","HVN","IAG","IDR","IEL","IFL","IFM","IFN","IGL","IGO","ILU","IMD","IMF","INA","ING","INR","IOF","IPH","IPL","IRE","IRI","IVC","JBH","JHC","JHG","JHX","JMS","KAR","KDR","KGN","LLC","LNG","LNK","LOV","LYC","MFG","MGR","MIN","MLD","MLX","MMS","MND","MNY","MP1","MPL","MQG","MSB","MTS","MVF","MYO","MYR","MYS","MYX","NAB","NAN","NCK","NCM","NCZ","NEA","NEC","NGI","NHF","NSR","NST","NUF","NVT","NWH","NWL","NWS","NXT","OFX","OGC","OMH","OML","ORA","ORE","ORG","ORI","OSH","OZL","PDL","PGH","PLG","PLS","PME","PMV","PNI","PNV","PPS","PPT","PRU","PRY","PTM","QAN","QBE","QUB","REA","REG","RFF","RHC","RIC","RIO","RMD","RRL","RSG","RWC","S32","SAR","SBM","SCG","SCO","SCP","SDA","SDF","SEA","SEK","SFR","SGF","SGM","SGP","SGR","SHL","SHV","SIG","SIQ","SKC","SKI","SLC","SLK","SOL","SPK","SPL","SRV","SSM","STO","SUL","SUN","SVW","SWM","SXL","SXY","SYD","SYR","TAH","TCL","TGR","TLS","TME","TNE","TPM","TWE","URW","VCX","VEA","VLW","VOC","VRL","VRT","VVR","WBA","WBC","WEB","WES","WGN","WGX","WHC","WOR","WOW","WPL","WPP","WSA","WTC","XRO"]
print(len(stocks))
def getSingleStockData(ticker):
    print(" ==== Stats for " + ticker + " ==== ")
    global finalCSV_data
    csv_selected_data = csv_data.loc[csv_data['ticker'] == ticker]
    csv_selected_data.sort_values(by=['date'])
    csv_selected_data.reset_index(inplace=True, drop=True)
    if (len(csv_selected_data)>100):
        lifetimeSTD = csv_selected_data['adjusted close'].std()
        percentChange10d = (csv_selected_data['adjusted close'][len(csv_selected_data)-1]-csv_selected_data['adjusted close'][len(csv_selected_data)-11])/csv_selected_data['adjusted close'][len(csv_selected_data)-11]
        print("Lifetime Standard Deviation: " + str(round(lifetimeSTD, 2)))
        print(str(round(percentChange10d*100, 2)) + "% Change over the last 10d")
        MPA10 = csv_selected_data['adjusted close'].rolling(window=10).mean()
        MPA30 = csv_selected_data['adjusted close'].rolling(window=30).mean()
        Gradient30 = (MPA10[len(MPA10)-1]-MPA10[len(MPA10)-31])/30
        Gradient90 = (MPA30[len(MPA30)-1]-MPA30[len(MPA30)-91])/90
        RecentClosingPrice = csv_selected_data['adjusted close'][len(csv_selected_data)-1]
        print("30d Gradient: " + str(Gradient30))
        print("90d Gradient: " + str(Gradient90))
        print("Recent Closing Price: " + str(RecentClosingPrice))
        finalCSV_data = finalCSV_data.append({'Ticker':ticker,'LstdDev':lifetimeSTD, 'pChange10d':percentChange10d, '30dG':Gradient30, '90dG':Gradient90, 'close':RecentClosingPrice}, ignore_index=True)

##getSingleStockData("APTV")

for i in range(0, len(stocks)):
    getSingleStockData(stocks[i])

print("Saving to CSV...")
finalCSV_data.to_csv(os.path.join(dirname, 'finalOutput.csv'), index=False)
print("Saved to CSV successfully")







