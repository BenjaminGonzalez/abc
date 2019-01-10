import numpy as np
import pandas as pd
import os
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

dirname = os.path.dirname(__file__)
read_file = os.path.join(dirname, 'StockDescriptions.csv')

ticks = ["ABP","AX1","ABC","APT","AGL","ALQ","ALU","AJM","AWC","AMA","AYS","AMC","AMP","ANN","ANZ","APA","APX","ARB","AAD","ARF","ALL","ARQ","AHY","ASX","ALX","AIA","AMI","AZJ","ASL","AST","ASB","AAC","API","AHG","AVN","AOG","BOQ","BAP","BPT","BGA","BAL","BEN","BHP","BIN","BKL","BLA","BSL","BLD","BXB","BVS","BRG","BKW","BWP","BWX","CTX","CDD","CAR","CWP","CIP","CMA","CGF","CQE","CHC","CQR","CNU","CLW","CIM","CL1","CLQ","CWY","CUV","CCL","COH","COL","CKF","CBA","CPU","COE","CTD","CGC","CCP","CMW","CWN","CSL","CSR","CYB","DCN","DXS","DHG","DMP","DOW","DLX","ECX","ELD","EHL","EML","EPW","EHE","EVN","FAR","A2M","FBU","FLT","FMG","FNP","FPH","FXL","GDI","GEM","GMA","GMG","GNC","GOR","GOZ","GPT","GUD","GWA","GXL","GXY","HPI","HSN","HSO","HT1","HUB","HVN","IAG","IDR","IEL","IFL","IFM","IFN","IGL","IGO","ILU","IMD","IMF","INA","ING","INR","IOF","IPH","IPL","IRE","IRI","IVC","JBH","JHC","JHG","JHX","JMS","KAR","KDR","KGN","LLC","LNG","LNK","LOV","LYC","MFG","MGR","MIN","MLD","MLX","MMS","MND","MNY","MP1","MPL","MQG","MSB","MTS","MVF","MYO","MYR","MYS","MYX","NAB","NAN","NCK","NCM","NCZ","NEA","NEC","NGI","NHF","NSR","NST","NUF","NVT","NWH","NWL","NWS","NXT","OFX","OGC","OMH","OML","ORA","ORE","ORG","ORI","OSH","OZL","PDL","PGH","PLG","PLS","PME","PMV","PNI","PNV","PPS","PPT","PRU","PRY","PTM","QAN","QBE","QUB","REA","REG","RFF","RHC","RIC","RIO","RMD","RRL","RSG","RWC","S32","SAR","SBM","SCG","SCO","SCP","SDA","SDF","SEA","SEK","SFR","SGF","SGM","SGP","SGR","SHL","SHV","SIG","SIQ","SKC","SKI","SLC","SLK","SOL","SPK","SPL","SRV","SSM","STO","SUL","SUN","SVW","SWM","SXL","SXY","SYD","SYR","TAH","TCL","TGR","TLS","TME","TNE","TPM","TWE","URW","VCX","VEA","VLW","VOC","VRL","VRT","VVR","WBA","WBC","WEB","WES","WGN","WGX","WHC","WOR","WOW","WPL","WPP","WSA","WTC","XRO"]
tickDesc = pd.read_csv(read_file)

nltk.download('punkt')

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

# remove punctuation
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


COLUMN_NAMES=['ticker', 'val']


for j in range(len(tickDesc.index)):
    finaldf = pd.DataFrame(columns=COLUMN_NAMES)
    focusTicker = tickDesc['ticker'][j]
    print("==== "+str(j+1)+"/"+str(len(tickDesc.index))+" == " + focusTicker)
    indexOfFocus = np.where(tickDesc.values == focusTicker)[0][0]
    focusDesc = tickDesc['desc'][j]
    file_name = os.path.join(dirname, "Sim/"+focusTicker+'_Sim.txt')
    print(focusDesc)
    if (focusDesc != "."):
        for i in range(len(tickDesc.index)):
            if (i != j):
                descCompare = tickDesc['desc'][i]
                val = cosine_sim(focusDesc, descCompare)
            else:
                val = -1

            finaldf = finaldf.append({'ticker':tickDesc['ticker'][i], 'val':val}, ignore_index=True)

        
        finaldf.to_csv(file_name, index=False)








    
