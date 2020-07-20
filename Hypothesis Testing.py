import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

#'''Returns a DataFrame of towns and the states they are in from the
    #university_towns.txt list. The format of the DataFrame should be:
    #DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    #  )

    #The following cleaning needs to be done:

    #1. For "State", removing characters from "[" to the end.
    #2. For "RegionName", when applicable, removing every character from " (" to the end.
    #3. Depending on how you read the data, you may need to remove newline character '\n'. '''

def get_list_of_university_towns():
    university_towns = pd.read_csv('university_towns.txt', sep="\t",encoding='utf-8', header=None)
    region = pd.DataFrame(columns=["State", "RegionName"])

    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    State = pd.Series(states)   #change to series


    i = 0
    for i in range(567):
        x = university_towns.iloc[i][0]
        if '[edit]' in x:
            region.set_value(i,'State',x)
        else:
            split_string = x.split("(", 1)
            x = split_string[0]
            region.set_value(i,'RegionName',x)
            if region.iloc[i]['State'] != region.iloc[i-1]['State']:
                region.set_value(i,'State',region.iloc[i-1]['State'])



    region = region.dropna()

    region['State'] = region['State'].str.replace(r'\[.*\]','')
    region['RegionName'] = region['RegionName'].str.replace(r"\(.*\)","")    #delete everything in () region['RegionName'] = region['RegionName'].str.replace(r"\[.*\]","")    #delete everything in []
    region['RegionName'] = region['RegionName'].str.replace(r"\n","")
    region['RegionName'] = region['RegionName'].str.rstrip()


    region.reset_index(drop=True, inplace=True)

    return region
get_list_of_university_towns()

################################################
 # '''Returns the year and quarter of the recession start time as a
   # string value in a format such as 2005q3'''

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def get_recession_start():
    GDP = pd.read_excel('gdplev.xls', header=None)
    GDP.columns = GDP.iloc[5]
    GDP = GDP.iloc[:, 4:7]
    GDP.columns = ['Quarter','GDP in billions of current dollars','GDP in billions of chained 2009 dollars']
    GDP = GDP[GDP['Quarter']>= '2000q1'].dropna().drop(['GDP in billions of current dollars'], axis=1)
    GDP.reset_index(drop=True, inplace=True)
    GDP.set_index('Quarter',inplace=True)
    # shift the column down by 1 period and calcualte the change in GDP
    GDP['GDP change'] = GDP['GDP in billions of chained 2009 dollars'] - GDP['GDP in billions of chained 2009 dollars'].shift(1)
    GDP['RecessionStart'] = (GDP['GDP change'] < 0) & (GDP['GDP change'].shift(-1) < 0)

    recession_start = GDP.index[GDP['RecessionStart']].tolist()[0]

    return recession_start
get_recession_start()

#################################################

def get_recession_bottom():


    GDP = pd.read_excel('gdplev.xls', header=None)
    GDP.columns = GDP.iloc[5]
    GDP = GDP.iloc[:, 4:7]
    GDP.columns = ['Quarter','GDP in billions of current dollars','GDP in billions of chained 2009 dollars']
    GDP = GDP[GDP['Quarter']>= '2000q1'].dropna().drop(['GDP in billions of current dollars'], axis=1)
    GDP.reset_index(drop=True, inplace=True)
    GDP.set_index('Quarter',inplace=True)
    # shift the column down by 1 period and calcualte the change in GDP
    GDP['GDP change'] = GDP['GDP in billions of chained 2009 dollars'] - GDP['GDP in billions of chained 2009 dollars'].shift(1)
    GDP['RecessionStart'] = (GDP['GDP change'] < 0) & (GDP['GDP change'].shift(+1) < 0)  #compare the next

    recession_bottom = GDP.index[GDP['RecessionStart']].tolist()[-1]


    return recession_bottom

get_recession_bottom()


##################################################

def get_recession_end():


    GDP = pd.read_excel('gdplev.xls', header=None)
    GDP.columns = GDP.iloc[5]
    GDP = GDP.iloc[:, 4:7]
    GDP.columns = ['Quarter','GDP in billions of current dollars','GDP in billions of chained 2009 dollars']
    GDP = GDP[GDP['Quarter']>= '2000q1'].dropna().drop(['GDP in billions of current dollars'], axis=1)
    GDP.reset_index(drop=True, inplace=True)
    GDP.set_index('Quarter',inplace=True)
    # shift the column down by 1 period and calcualte the change in GDP
    GDP['GDP change'] = GDP['GDP in billions of chained 2009 dollars'] - GDP['GDP in billions of chained 2009 dollars'].shift(1)
    GDP['RecessionStart'] = (GDP['GDP change'] < 0) & (GDP['GDP change'].shift(+1) < 0)  #compare the next

    recession_bottom = GDP.index[GDP['RecessionStart']].tolist()[-1]

    list = GDP.index.tolist() #make the index to list
    index = list.index(recession_bottom)   #set the recession bottom as the starting point

    recession_end = list[index + 2] #get the second index after recession bottom

    return recession_end

get_recession_end()

#################################################

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


def convert_housing_data_to_quarters():

    #'''Converts the housing data to quarters and returns it as mean
    # values in a dataframe. This dataframe should be a dataframe with
    #columns for 2000q1 through 2016q3, and should have a multi-index
    #in the shape of ["State","RegionName"].

    #Note: Quarters are defined in the assignment description, they are
    # not arbitrary three month periods. The resulting dataframe should have 67 columns, and 10,730 rows.

    newstate = pd.Series(states)   #change to series


    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    housing = housing.drop(['RegionID','Metro','CountyName','SizeRank'], axis=1)

    housing_copy = housing.copy()
    copy = housing_copy[['State','RegionName' ]] # keep the regionName and state

    housing = housing.iloc[:,-200::]


    housing.rename(columns=lambda x: pd.Period(x,'q'),inplace=True)    #change timestamp to quarter

    # In order to group by column names, transpose first and then group by index
    df = housing.transpose()
    df = df.reset_index()
    df = df.groupby("index").median().transpose()
    df.columns = df.columns.to_series().astype(str) #converting the periodIndex to string


    df[['State','RegionName']] = copy   #append regionName and state

    df.replace({'State':states},inplace=True)  #replace a column with the dictionary

    df.set_index(['State','RegionName'],inplace=True)  #set multiIndex
    df.columns = map(str.lower, df.columns)

    return df

convert_housing_data_to_quarters()

#######################################################

recession_start = get_recession_start()
recession_bottom = get_recession_bottom()
recession_end = get_recession_end()
housing = convert_housing_data_to_quarters()
region_list = get_list_of_university_towns()



def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''

    newhousing = housing[['2008q2','2008q3','2008q4','2009q1','2009q2']]

    newhousing_copy = newhousing.copy()


    university_towns = pd.merge(region_list,newhousing, how='inner', left_on= ['State','RegionName'],right_index=True)
    #merge the 2 dataframes (multiple-index dataframe needs both columns to merge)
    university_towns.set_index(['State','RegionName'],inplace=True)   #set as multiple index

    #first get a new column to find out the merge and filter the right_only rows
    non_university_towns = pd.merge(region_list,newhousing, how='right', left_on= ['State','RegionName'],right_index=True,indicator=True)
    non_university_towns = non_university_towns[non_university_towns['_merge']=='right_only']
    non_university_towns.drop(['_merge'],axis=1,inplace=True)
    non_university_towns.set_index(['State','RegionName'],inplace=True)     #reorganize to multipleindex




    '''Hypothesis: University towns have their mean housing prices less effected by recessions.
    Run a t-test to compare the ratio of the mean price of houses in university towns
    the quarter before the recession starts compared to the recession bottom.
    (price_ratio=quarter_before_recession/recession_bottom)
    '''

    university_towns['ratio'] = university_towns['2008q2'] / university_towns['2009q2']
    non_university_towns['ratio'] = non_university_towns['2008q2'] / non_university_towns['2009q2']

    #run ttest to find the pvalue
    tstat, pvalue = ttest_ind(university_towns['ratio'], non_university_towns['ratio'],nan_policy = "omit")

    if pvalue < 0.01:
        different=True
    else:
        different=False


    if university_towns['ratio'].mean()<non_university_towns['ratio'].mean():
        better ="university town"
    else:
        better = "non-university town"
   
    result = (different,pvalue,better)

    return result
run_ttest()
