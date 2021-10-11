# Shuxuan Liu
import pandas as pd

def existing_CDCData():
    # Read data from textfile into dataframe
    df = pd.read_json('/Users/liushuxuan/Desktop/Grad School/21Fall/DFP/Final Project/CDCData.txt')
    df.submission_date = df.submission_date.replace({'T00:00:00.000':''}, regex=True)
    
    print(df)
    
    # Clean the data and retireve based on state
    stateName = 'MO'
    stateData = df.loc[df['state'] == stateName][['submission_date', 'state', 'tot_cases', 'new_case', 
                                                  'tot_death', 'new_death']]
    stateData = stateData.sort_values(by=['submission_date'])
    index = pd.Series(range(len(stateData)))
    stateData = stateData.set_index(index)
    stateData['score'] = stateData.index * (stateData.new_case + abs(stateData.new_death)) / 10000
    
    score = sum(stateData['score']) / 50
    
    print(stateData[['submission_date', 'state', 'tot_cases', 'new_case', 
                                                  'tot_death', 'new_death']])
    print(score)
