import numpy as np 
import pandas as pd 
import warnings
import datetime as dt
from tensorflow.keras.models import load_model
import joblib
warnings.filterwarnings("ignore")

###Function For Segmentation
def RfmSegmentation(inputPath,modelPath,labelEncoderPath):
    #load the dataset
    retail_df = pd.read_csv(inputPath,encoding="ISO-8859-1",dtype={'CustomerID': str,'InvoiceID': str})

    #remove canceled orders
    retail_uk = retail_df[retail_df['Quantity']>0]
    #remove rows where customerID are NA
    retail_uk.dropna(subset=['CustomerID'],how='all',inplace=True)
    #restrict the data to one full year because it's better to use a metric per Months or Years in RFM
    retail_uk = retail_uk[retail_uk['InvoiceDate']>= "2010-12-09"]

    ##First Result
    summary_stats = {
    "Number of transactions": retail_uk['InvoiceNo'].nunique(),
    "Number of products bought": retail_uk['StockCode'].nunique(),
    "Number of customers": retail_uk['CustomerID'].nunique(),
    "Percentage of customers NA": round(retail_uk['CustomerID'].isnull().sum() * 100 / len(retail_df),2)
    }
    summaryDF = pd.DataFrame([summary_stats])
    summaryDF.to_csv('summary_stats.csv', index=False) ##IMP

    ##RFM analysis Start
    now = dt.date(2011,12,9)
    #create a new column called date which contains the date of invoice only
    retail_uk['date'] = pd.DatetimeIndex(retail_uk['InvoiceDate']).date

    #Recency
    recency_df = retail_uk.groupby(by='CustomerID', as_index=False)['date'].max()
    recency_df.columns = ['CustomerID','LastPurshaceDate']
    #calculate recency
    recency_df['Recency'] = recency_df['LastPurshaceDate'].apply(lambda x: (now - x).days)
    #drop LastPurchaseDate as we don't need it anymore
    recency_df.drop('LastPurshaceDate',axis=1,inplace=True)
    #Recency Done

    #Frequency
    # drop duplicates
    retail_uk_copy = retail_uk
    retail_uk_copy.drop_duplicates(subset=['InvoiceNo', 'CustomerID'], keep="first", inplace=True)
    #calculate frequency of purchases
    frequency_df = retail_uk_copy.groupby(by=['CustomerID'], as_index=False)['InvoiceNo'].count()
    frequency_df.columns = ['CustomerID','Frequency']
    #Frequency Done

    #Monetary Value
    #create column total cost
    retail_uk['TotalCost'] = retail_uk['Quantity'] * retail_uk['UnitPrice']
    monetary_df = retail_uk.groupby(by='CustomerID',as_index=False).agg({'TotalCost': 'sum'})
    monetary_df.columns = ['CustomerID','Monetary']
    #Monetary done

    #Create RFM table
    temp_df = recency_df.merge(frequency_df,on='CustomerID')
    #merge with monetary dataframe to get a table with the 3 columns
    rfm_df = temp_df.merge(monetary_df,on='CustomerID')
    #use CustomerID as index
    rfm_df.set_index('CustomerID',inplace=True)
    temp = rfm_df.copy()

    #Model
    model = load_model(modelPath)
    predictions = model.predict(temp)

    # Load the label encoder
    le = joblib.load(labelEncoderPath)

    # Get the index of the maximum probability
    max_prob_indices = np.argmax(predictions, axis=1)

    # Transform the indices back to original form
    original_labels = le.inverse_transform(max_prob_indices)

    temp['Labels'] =original_labels

    ##Second result
    temp.to_csv('RFM_Table.csv',index = False) #IMP

    ##Third IMP
    unique_counts = temp['Labels'].value_counts()
    unique_counts_df = unique_counts.reset_index()
    unique_counts_df.columns = ["Labels", "Count"]
    unique_counts_df.to_csv('Unique_Counts_Of_Labels.csv')##IMP

if __name__ == "__main__":
    labelEncoderPath = "A:\MegaProject\Segmentation\RFM\label_encoder.pkl"
    modelPath = "A:\MegaProject\Segmentation\RFM\RFMSegmentationModel.keras"
    input = "A:\MegaProject\Segmentation\RFM\data.csv"
    RfmSegmentation(input,modelPath,labelEncoderPath)
