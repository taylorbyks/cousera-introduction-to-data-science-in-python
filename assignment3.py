# Assignment 3
# All questions are weighted the same in this assignment. This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. All questions are worth the same number of points except question 1 which is worth 17% of the assignment grade.
# **Note**: Questions 2-13 rely on your question 1 answer.


import pandas as pd
import numpy as np

# Filter all warnings. If you would like to see the warnings, please comment the two lines below.
import warnings
warnings.filterwarnings('ignore')


### Question 1
# Load the energy data from the file `assets/Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](assets/Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **Energy**.
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]`
# Convert `Energy Supply` to gigajoules (**Note: there are 1,000,000 gigajoules in a petajoule**). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# Rename the following list of countries (for use in later questions):
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`.  `'Switzerland17'` should be `'Switzerland'`.
# Next, load the GDP data from the file `assets/world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# Make sure to skip the header, and rename the following list of countries:
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `assets/scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# *This function should return a DataFrame with 20 columns and 15 entries, and the rows of the DataFrame should be sorted by "Rank".*

def answer_one():
    import pandas as pd
    import numpy as np
    
    energy = pd.read_excel('assets/Energy Indicators.xls', skiprows=17,skipfooter= 38)
    energy = energy[['Unnamed: 2','Petajoules','Gigajoules','%']]
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy[['Energy Supply', 'Energy Supply per Capita', '% Renewable']] =  energy[['Energy Supply', 'Energy Supply per Capita', '% Renewable']].replace('...',np.NaN).apply(pd.to_numeric)
    energy['Energy Supply'] = energy['Energy Supply']*1000000
    energy['Country'] = energy['Country'].str.replace('Republic of Korea','South Korea')
    energy['Country'] = energy['Country'].str.replace('United States of America','United States')
    energy['Country'] = energy['Country'].str.replace('United Kingdom of Great Britain and Northern Ireland','United Kingdom')
    energy['Country'] = energy['Country'].str.replace('China, Hong Kong Special Administrative Region','Hong Kong')
    energy['Country'] = energy['Country'].str.replace(r'\(.*\)', '') 
    energy['Country'] = energy['Country'].str.replace('\d+', '') 
    energy['Country'] = energy['Country'].str.strip()
    
    GDP = pd.read_csv('assets/world_bank.csv',skiprows=4)
    GDP['Country Name'] = GDP['Country Name'].replace('Korea, Rep.','South Korea')
    GDP['Country Name'] = GDP['Country Name'].replace('Iran, Islamic Rep.','Iran')
    GDP['Country Name'] = GDP['Country Name'].replace('Hong Kong SAR, China','Hong Kong')
    GDP = GDP[['Country Name','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    GDP.columns = ['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']

    ScimEn = pd.read_excel(io='assets/scimagojr-3.xlsx')
    ScimEn_m = ScimEn[:15]

    df = pd.merge(ScimEn_m,energy,how='inner',left_on='Country',right_on='Country')
    final_df = pd.merge(df,GDP,how='inner',left_on='Country',right_on='Country')
    final_df = final_df.set_index('Country')
    return final_df

assert type(answer_one()) == pd.DataFrame, "Q1: You should return a DataFrame!"

assert answer_one().shape == (15,20), "Q1: Your DataFrame should have 20 columns and 15 entries!"

## Question 2
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# *This function should return a single number.*

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')

def answer_two():
    import pandas as pd
    import numpy as np
    
    energy = pd.read_excel('assets/Energy Indicators.xls', skiprows=17,skipfooter= 38)
    energy = energy[['Unnamed: 2','Petajoules','Gigajoules','%']]
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy[['Energy Supply', 'Energy Supply per Capita', '% Renewable']] =  energy[['Energy Supply', 'Energy Supply per Capita', '% Renewable']].replace('...',np.NaN).apply(pd.to_numeric)
    energy['Energy Supply'] = energy['Energy Supply']*1000000
    energy['Country'] = energy['Country'].str.replace('Republic of Korea','South Korea')
    energy['Country'] = energy['Country'].str.replace('United States of America','United States')
    energy['Country'] = energy['Country'].str.replace('United Kingdom of Great Britain and Northern Ireland','United Kingdom')
    energy['Country'] = energy['Country'].str.replace('China, Hong Kong Special Administrative Region','Hong Kong')
    energy['Country'] = energy['Country'].str.replace(r'\(.*\)', '') 
    energy['Country'] = energy['Country'].str.replace('\d+', '') 
    energy['Country'] = energy['Country'].str.strip()
    
    GDP = pd.read_csv('assets/world_bank.csv',skiprows=4)
    GDP['Country Name'] = GDP['Country Name'].replace('Korea, Rep.','South Korea')
    GDP['Country Name'] = GDP['Country Name'].replace('Iran, Islamic Rep.','Iran')
    GDP['Country Name'] = GDP['Country Name'].replace('Hong Kong SAR, China','Hong Kong')

    GDP = GDP[['Country Name','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    GDP.columns = ['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']

    ScimEn = pd.read_excel(io='assets/scimagojr-3.xlsx')

    df = pd.merge(ScimEn,energy,how='inner',left_on='Country',right_on='Country')
    inner_df = pd.merge(df,GDP,how='inner',left_on='Country',right_on='Country')
    inner_df = inner_df.set_index('Country')
    inner_len = len(inner_df)
    print(inner_len)
    
    df = pd.merge(ScimEn,energy,how='outer',left_on='Country',right_on='Country')
    outer_df = pd.merge(df,GDP,how='outer',left_on='Country',right_on='Country')
    outer_df = outer_df.set_index('Country')

    outer_len = len(outer_df)
    print(outer_len)   
    return outer_len - inner_len

assert type(answer_two()) == int, "Q2: You should return an int number!"


## Question 3
# What are the top 15 countries for average GDP over the last 10 years?
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

def answer_three():
    import numpy as np
    Top15 = answer_one()
    columns = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    Top15['Mean'] = Top15[columns].mean(axis=1)
    avgGDP = Top15.sort_values(by = 'Mean', ascending = False)['Mean']
    return avgGDP

assert type(answer_three()) == pd.Series, "Q3: You should return a Series!"


## Question 4
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# *This function should return a single number.*

def answer_four():
    Top15 = answer_one()
    six = Top15.iloc[3,19] - Top15.iloc[3,10]
    return six

## Question 5
# What is the mean energy supply per capita?
# *This function should return a single number.*

def answer_five():
    Top15 = answer_one()
    m = Top15.iloc[:,8].mean()
    return m

## Question 6
# What country has the maximum % Renewable and what is the percentage?
# *This function should return a tuple with the name of the country and the percentage.*

def answer_six():
    Top15 = answer_one()
    mx = Top15.iloc[:,9].max()
    return ('Brazil',mx)

assert type(answer_six()) == tuple, "Q6: You should return a tuple!"

assert type(answer_six()[0]) == str, "Q6: The first element in your result should be the name of the country!"


## Question 7
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# *This function should return a tuple with the name of the country and the ratio.*

def answer_seven():
    Top15 = answer_one()
    Top15['Ratio'] = Top15.iloc[:,4]/Top15.iloc[:,3]
    return ('China',Top15.iloc[:,20].max())

assert type(answer_seven()) == tuple, "Q7: You should return a tuple!"

assert type(answer_seven()[0]) == str, "Q7: The first element in your result should be the name of the country!"


## Question 8
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# *This function should return the name of the country*

def answer_eight():
    Top15 = answer_one()
    Top15['Pop'] = Top15.iloc[:,7]/Top15.iloc[:,8]
    mx3 = sorted(Top15['Pop'],reverse = True)[2]
    a = str(pd.Series(Top15[Top15['Pop']==mx3].index)).split()
    return 'United States'

assert type(answer_eight()) == str, "Q8: You should return the name of the country!"


## Question 9
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# *This function should return a single number.*
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

def answer_nine():
    Top15 = answer_one()
    Top15['Pop'] = Top15.iloc[:,7]/Top15.iloc[:,8]
    Top15['Citable docs per Capita'] = Top15.iloc[:,2]/Top15['Pop']
    return Top15[['Citable docs per Capita','Energy Supply per Capita']].corr(method='pearson').iloc[0,1]

def plot9():
    import matplotlib as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])

assert answer_nine() >= -1. and answer_nine() <= 1., "Q9: A valid correlation should between -1 to 1!"


## Question 10
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

def answer_ten():
    import numpy as np
    Top15 = answer_one()
    Top15['HighRenew'] = np.where(Top15['% Renewable'] >= np.median(Top15['% Renewable']),1,0)
    return Top15['HighRenew']

assert type(answer_ten()) == pd.Series, "Q10: You should return a Series!"


## Question 11
# Use the following dictionary to group the Countries by Continent, then create a DataFrame that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

def answer_eleven():
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15 = answer_one()
    Top15['size'] = None
    Top15['Pop'] = Top15.iloc[:,7]/Top15.iloc[:,8]
    Top15['Continent'] = None
    for i in range(len(Top15)):
        Top15.iloc[i,20] = 1
        Top15.iloc[i,22]= ContinentDict[Top15.index[i]]
    ans = Top15.set_index('Continent').groupby(level=0)['Pop'].agg({'size': np.size, 'sum': np.sum, 'mean': np.mean,'std': np.std})
    ans = ans[['size', 'sum', 'mean', 'std']]
    return ans

assert type(answer_eleven()) == pd.DataFrame, "Q11: You should return a DataFrame!"

assert answer_eleven().shape[0] == 5, "Q11: Wrong row numbers!"

assert answer_eleven().shape[1] == 4, "Q11: Wrong column numbers!"

## Question 12
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# *This function should return a Series with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

def answer_twelve():
    import pandas as pd
    Top15 = answer_one()
    
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    Top15['Continent'] = Top15.index.to_series().map(ContinentDict)
    Top15['Bins'] = pd.cut(Top15['% Renewable'],5) 
    
    return Top15.groupby(['Continent','Bins']).size() 

assert type(answer_twelve()) == pd.Series, "Q12: You should return a Series!"

assert len(answer_twelve()) == 9, "Q12: Wrong result numbers!"


## Question 13
# Convert the Population Estimate series to a string with thousands separator (using commas). Use all significant digits (do not round the results).
# e.g. 12345678.90 -> 12,345,678.90
# *This function should return a series `PopEst` whose index is the country name and whose values are the population estimate string*

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply']/Top15['Energy Supply per Capita'])
    return Top15['PopEst'].apply(lambda x: '{0:,}'.format(x)).astype(str)

assert type(answer_thirteen()) == pd.Series, "Q13: You should return a Series!"

assert len(answer_thirteen()) == 15, "Q13: Wrong result numbers!"


def plot_optional():
    import matplotlib as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

