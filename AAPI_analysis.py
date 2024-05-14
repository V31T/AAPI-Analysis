import marimo

__generated_with = "0.5.2"
app = marimo.App(app_title="AAS 1 - AAPI Data Analysis")


@app.cell
def __(mo):
    mo.md(
        f"""
        # AAPI/SWANA HATE CRIME DATA ANALYSIS
        **Made by**: Henry Pham   
        **Class**: AAS 1 - Saugher Nojan
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        f'''
        ## AAPI Dataset was provided by:  
        **Stop AAPI Hate. “Hate Act Data.” Accessed [May 10th, 2024]. stopaapihate/org/explore-our-data**  
        ## Notes about the data:  
        - **Hate act numbers from our reporting center should not be used in isolation to represent the full prevalence of anti-Asian or anti-Pacific Islander hate at any given time.** Like all datasets that rely on voluntarily submitted reports, our numbers are just the tip of the iceberg. For every act of hate that is reported, there are many more that go unreported. The volume of reports to Stop AAPI Hate is subject to numerous factors, including but not limited to: awareness of and access to the reporting center, current events that spur reporting, and reporting fatigue.  
        - **We caution against making claims about hate crimes based on our data.** For an act to constitute a hate crime, it must be formally investigated and declared so by law enforcement. Therefore, while a portion of the hate acts reported to us may constitute potential hate crimes, it would be inaccurate to describe our data as hate crime data since these cases may or may not have been reported to law enforcement and investigated. Further, the majority of hate acts that our communities experience are non-criminal acts.
        - **Data was collected post Covid-19, from 2020 - 2022**
        
        '''
    )
    return


@app.cell
def __():
    # -*- coding: utf-8 -*-
    # @Date    : 2020-07-29 22:00:00
    # @Author  : Henry Pham


    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.express as px
    return np, pd, plt, px


@app.cell
def __(pd):
    ## import dataset

    # Read the first xlsx file
    county_df = pd.read_excel('2020-2022-county-level-totals.xlsx', sheet_name = ['type', 'site', 'bias','scope','age','gender','race_ethnicity','offender', 'reporting for'])

    # Read the second xlsx file
    state_df = pd.read_excel('2020-2022-state-level-totals.xlsx', sheet_name = ['type', 'site', 'bias','scope','age','gender','race_ethnicity','offender', 'reporting for'])
    return county_df, state_df


@app.cell
def __(mo):
    mo.md(
        f"""
        This data analysis will focus on the type of hatecrime and the age/race/gender that was afflicted. The 3 states that we will be looking at are California, New York, and Texas since they had the highest records of AAPI hate crimes.
        """
    )
    return


@app.cell
def __(county_df, state_df):
    # gather the type, age, gender, and race_ethnicty data
    state_type = state_df['type']
    state_age = state_df['age']
    state_gender = state_df['gender']
    state_race = state_df['race_ethnicity']

    # county will be used mainly for California and New York since those have the greatest portion of hate crimes towards AAPI
    county_type = county_df['type']
    county_age = county_df['age']
    county_gender = county_df['gender']
    county_race = county_df['race_ethnicity']
    return (
        county_age,
        county_gender,
        county_race,
        county_type,
        state_age,
        state_gender,
        state_race,
        state_type,
    )


@app.cell
def __(pd, state_age, state_gender, state_race, state_type):
    # take only the California, New York, and Texas data from the state level data
    california_type = state_type[state_type['state'] == 'California']
    new_york_type = state_type[state_type['state'] == 'New York']
    texas_type = state_type[state_type['state'] == 'Texas']

    california_age = state_age[state_age['state'] == 'California']
    new_york_age = state_age[state_age['state'] == 'New York']
    texas_age = state_age[state_age['state'] == 'Texas']

    california_gender = state_gender[state_gender['state'] == 'California']
    new_york_gender = state_gender[state_gender['state'] == 'New York']
    texas_gender = state_gender[state_gender['state'] == 'Texas']

    california_race = state_race[state_race['state'] == 'California']
    new_york_race = state_race[state_race['state'] == 'New York']
    texas_race = state_race[state_race['state'] == 'Texas']

    # concat data for each sheet
    data_type = pd.concat([california_type, new_york_type, texas_type], axis = 0).reset_index(drop = True)
    data_age = pd.concat([california_age, new_york_age, texas_age], axis = 0).reset_index(drop = True)
    data_gender = pd.concat([california_gender, new_york_gender, texas_gender], axis = 0).reset_index(drop = True)
    data_race = pd.concat([california_race, new_york_race, texas_race], axis = 0).reset_index(drop = True)

    # concat the dataframes for California, New York, and Texas
    california = pd.concat([california_type, california_age, california_gender, california_race], axis = 1)
    new_york = pd.concat([new_york_type, new_york_age, new_york_gender, new_york_race], axis = 1)
    texas = pd.concat([texas_type, texas_age, texas_gender,texas_race], axis = 1)

    # display data
    data = pd.concat([california, new_york, texas], axis = 0).reset_index(drop = True)
    return (
        california,
        california_age,
        california_gender,
        california_race,
        california_type,
        data,
        data_age,
        data_gender,
        data_race,
        data_type,
        new_york,
        new_york_age,
        new_york_gender,
        new_york_race,
        new_york_type,
        texas,
        texas_age,
        texas_gender,
        texas_race,
        texas_type,
    )


@app.cell
def __(data_type):
    # combine and rename columns into Harassment, Physical harm or contact, Institutional discrimination, Property harm, and Other
    data_type['Harassment'] = data_type[['Verbal harassment',
           'Threat of harm to person', 'Behavioral harassment',
           'Written, visual, or auditory materials', 'Following or stalking',
           'Call ICE or police', 'Other or unspecified harassment',
           'Threat of harm to property']].sum(axis = 1)

    data_type['Physical harm or contact'] = data_type[['Attempted physical injury or contact', 'Physical contact',
           'Physical injury', 'Coughed at or spat on',
           'Unspecified physical assault or harassment']].sum(axis = 1)

    data_type['Institutional discrimination'] = data_type[['Government services discrimination',
           'Business discrimination', 'Housing discrimination',
           'Job discrimination', 'Other unfair treatment']].sum(axis = 1)

    data_type['Property harm'] = data_type[['Property damage or abuse', 'Robbery or theft']].sum(axis = 1)

    # sum of new columns by state
    data_type['total harrassment'] = data_type[['Harassment', 'Physical harm or contact', 'Institutional discrimination', 'Property harm']].sum(axis = 1)
    return


@app.cell
def __(mo):
    mo.md(
        f'''
        ## **NOTES ABOUT THIS WEBSITE/DATA ANALYSIS**  
        - Analysis will seek to explain visualizations and relate the graphs with **CLO2** (addresses how SWANA/Asian Pacific Islander Desi/Americans have shared experiences that link them together).  
        - ***DATA LIMITATION***: I could not find a usable/workable dataset file for SWANA groups, instead I will be pulling data from [FBI HATECRIME DATA](https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/explorer/crime/hate-crime) 
            - SWANA hatecrime amount from 2020-2022 totals to be 3,078

        
        '''
    )
    return


@app.cell
def __(mo, type_hist, type_pie):
    mo.md(
        f"""
        -----
        ## **HARASSMENT**
        {mo.ui.tabs( tabs = dict({'Pie Chart': type_pie, 'Histogram': type_hist}.items()))} 
        ### **Analysis**
        AAPI harassment has been recorded the most in California, this is due to the high AAPI presence in California, especially in counties like San Diego, Los Angelas, and San jose. Preceiding that, New york also contains a large Asian Demographic. These 2 occurances are not the same for Texas. This is due to the large Anti-Asian Sentiment that exists in Texas. When relating these experiences to SWANA groups, Both groups had the highest number of hate crimes commited through general harassment. According to the FBI database, more than half of the recorded hate crimes targeted towards SWANA groups is in the form of Intimidation. Furthermore physical harm/simple asault is second for the most common hate crime type towrads AAPI/SWANA groups. Why is this the case? This is most likely due to targeted Racism after the Covid-19 outbreak. Further more the war in the middle east could fuel hate towards SWANA groups. This goes to show the overall sentiment towards AAPI/SWANA groups that have no real connection to why their is anti-sentiment towards them.
        """
    )
    return


@app.cell(disabled=True)
def __(mo, type_hist, type_pie):
    type_tabs = mo.ui.tabs( tabs = dict({'Pie Chart': type_pie, 'Histogram': type_hist}.items()))
    return type_tabs,


@app.cell
def __(mo, px, state_type):
    # pie chart for data_type to show harasment amount per state
    pie1 = state_type.copy()
    pie1['Harassment'] = pie1[['Verbal harassment',
           'Threat of harm to person', 'Behavioral harassment',
           'Written, visual, or auditory materials', 'Following or stalking',
           'Call ICE or police', 'Other or unspecified harassment',
           'Threat of harm to property']].sum(axis = 1)

    pie1 = pie1[['state', 'Harassment']].drop(index = 20, axis = 0)

    #make pie chart
    _fig = px.pie(pie1, values='Harassment', names='state', title='Harassment Amount per State')
    #make pie chart pretty
    _fig.update_traces(textposition='inside', textinfo='percent+label')

    type_pie = mo.ui.plotly(_fig)
    return pie1, type_pie


@app.cell
def __(data_type, mo, px):
    # bar plot for harassment, physical harm, institutional discrimination, and property harm
    # sort by total amount of hate crimes
    _fig = px.histogram(data_type, x = 'state', y = ['Harassment', 'Physical harm or contact', 'Institutional discrimination', 'Property harm'], barmode = 'group', title = 'Type of hate crimes in California, New York, and Texas')

    #make bar plot pretty
    _fig.update_layout(xaxis={'categoryorder':'total descending'}) 

    type_hist = mo.ui.plotly(_fig)

    # fig = px.bar(data_type, x = 'state', y = 'Harassment', barmode = 'group', title = 'Type of hate crimes in California, New York, and Texas')
    # fig.show()

    #make chart pretty
    return type_hist,


@app.cell
def __(data_type, px):
    # make each column into a percentage based on self-reported data
    data_type['Harassment_percent'] = data_type['Harassment']/data_type['total harrassment']
    data_type['Physical harm or contact_percent'] = data_type['Physical harm or contact']/data_type['total harrassment']
    data_type['Institutional discrimination_percent'] = data_type['Institutional discrimination']/data_type['total harrassment']
    data_type['Property harm_percent'] = data_type['Property harm']/data_type['total harrassment']

    # bar plot for harassment, physical harm, institutional discrimination, and property harm
    _fig = px.bar(data_type, x = 'state', y = ['Harassment_percent', 'Physical harm or contact_percent', 'Institutional discrimination_percent', 'Property harm_percent'], barmode = 'group', title = 'Type of hate crimes in California, New York, and Texas')
    return


@app.cell
def __(age_hist, age_pie, mo):
    mo.md(
        f"""
        -----
        ## **AGE**

        {mo.ui.tabs( tabs = dict({'Pie Chart': age_pie, 'Histogram': age_hist}.items()))}
        ### **Analysis**
        Middle aged groups were targeted the most. This is most likely due to the Age Group's presence in the work force. Common to how Chinese Americans got hate by Automobile workers. Anti-AAPI sentiment was mostly targetted towards coworkers/working force. 
        There was no data on SWANA hate crime victim ages.
        """
    )
    return


@app.cell
def __(data_age, mo, px):
    _fig = px.histogram(data_age, x = 'state', y = ['Under 18', '18-25', '26-35', '36-45', '46-60', '60+', 'Unknown'], barmode = 'group', title = 'Age of victims in California, New York, and Texas')
    age_hist = mo.ui.plotly(_fig)
    return age_hist,


@app.cell
def __(data_age, px):
    data_age['total'] = data_age[['Under 18', '18-25', '26-35', '36-45', '46-60', '60+', 'Unknown']].sum(axis = 1)

    #same thing as above but for age
    data_age['Under 18_percent'] = data_age['Under 18']/data_age['total']
    data_age['18-25_percent'] = data_age['18-25']/data_age['total']
    data_age['26-35_percent'] = data_age['26-35']/data_age['total']
    data_age['36-45_percent'] = data_age['36-45']/data_age['total']
    data_age['46-60_percent'] = data_age['46-60']/data_age['total']
    data_age['60+_percent'] = data_age['60+']/data_age['total']
    data_age['Unknown_percent'] = data_age['Unknown']/data_age['total']

    # bar plot for age
    _fig = px.bar(data_age, x = 'state', y = ['Under 18_percent', '18-25_percent', '26-35_percent', '36-45_percent', '46-60_percent', '60+_percent', 'Unknown_percent'], barmode = 'group', title = 'Age of victims in California, New York, and Texas')
    return


@app.cell
def __(data_age, mo, px):
    # pie chart for age
    pie2 = data_age.copy()
    pie2 = pie2.drop([0])
    pie2 = pie2.drop(columns = ['state', 'total', 'self-reported hate acts', 'Under 18_percent', '18-25_percent', '26-35_percent', '36-45_percent', '46-60_percent', '60+_percent', 'Unknown_percent'])
    pie2 = pie2.sum(axis = 0)

    _fig = px.pie(pie2, values=pie2.values, names=pie2.index, title='Age of victims in California, New York, and Texas')
    _fig.update_traces(textposition='inside', textinfo='percent+label')

    age_pie = mo.ui.plotly(_fig)
    return age_pie, pie2


@app.cell
def __(gender_hist, mo):
    mo.md(
        f"""
        -----
        ## **GENDER**

        {gender_hist}
          
        ### **Analysis**
        According to the FBI data, SWANA females were also the most targetted Gender during 2020-2022. 
        """
    )
    return


@app.cell
def __(data_gender, mo, px):
    _fig = px.histogram(data_gender, x = 'state', y = ['Female', 'Nonbinary', 'Male',
           'Unknown'], barmode = 'group', title = 'Gender of victims in California, New York, and Texas')
    gender_hist = mo.ui.plotly(_fig)
    return gender_hist,


@app.cell
def __(data_gender, px):
    # do the same for gender
    data_gender['total'] = data_gender[['Female', 'Nonbinary', 'Male',
           'Unknown']].sum(axis = 1)

    #same thing as above but for age
    data_gender['Female_percent'] = data_gender['Female']/data_gender['total']
    data_gender['Nonbinary_percent'] = data_gender['Nonbinary']/data_gender['total']
    data_gender['Male_percent'] = data_gender['Male']/data_gender['total']
    data_gender['Unknown_percent'] = data_gender['Unknown']/data_gender['total']

    # bar plot for age
    _fig = px.bar(data_gender, x = 'state', y = ['Female_percent', 'Nonbinary_percent', 'Male_percent',
           'Unknown_percent'], barmode = 'group', title = 'Gender of victims in California, New York, and Texas')
    return


@app.cell
def __(mo, race_hist):
    mo.md(
        f"""
        -----
        ## RACE

        {race_hist}
        ### **Analysis**
        Chinese Americans were the victims of most hate crimes in the United States in general. This is largely due to sentiments after the COVID-19 outbreak. From 2020-2022 there was a large spread of misinformation and hate towards Chinese Americans as being the cause of COVID-19. This same genre of misinformation can be used to describe the hate towards Islam in the United States.
        """
    )
    return


@app.cell
def __(data_race, mo, px):
    _fig = px.histogram(data_race, x = 'state', y = ['Cambodian',
           'Central Asian_grouped', 'Chinese', 'P/Filipinx', 'Latinx', 'Hmong',
           'Indian', 'Japanese', 'Korean', 'Lao', 'Pacific Islander', 'Taiwanese',
           'Thai', 'Vietnamese', 'White', 'Other East Asian', 'Other South Asian',
           'Other Southeast Asian', 'Other non-AA/PI',
           'Other or unknown_ethnicity'], barmode = 'group', title = 'Race of Victims in California, New York, and Texas')
    race_hist = mo.ui.plotly(_fig)
    return race_hist,


@app.cell
def __(data_race, px):
    # same thing for race
    # do the same for gender
    wow = data_race.copy()
    wow['total'] = wow[['Cambodian',
           'Central Asian_grouped', 'Chinese', 'P/Filipinx', 'Latinx', 'Hmong',
           'Indian', 'Japanese', 'Korean', 'Lao', 'Pacific Islander', 'Taiwanese',
           'Thai', 'Vietnamese', 'White', 'Other East Asian', 'Other South Asian',
           'Other Southeast Asian', 'Other non-AA/PI',
           'Other or unknown_ethnicity']].sum(axis = 1)

    #same thing as above but for age
    wow['Cambodian_percent'] = wow['Cambodian']/wow['total']
    wow['Central Asian_grouped_percent'] = wow['Central Asian_grouped']/wow['total']
    wow['Chinese_percent'] = wow['Chinese']/wow['total']
    wow['P/Filipinx_percent'] = wow['P/Filipinx']/wow['total']
    wow['Latinx_percent'] = wow['Latinx']/wow['total']
    wow['Hmong_percent'] = wow['Hmong']/wow['total']
    wow['Indian_percent'] = wow['Indian']/wow['total']
    wow['Japanese_percent'] = wow['Japanese']/wow['total']
    wow['Korean_percent'] = wow['Korean']/wow['total']
    wow['Lao_percent'] = wow['Lao']/wow['total']
    wow['Pacific Islander_percent'] = wow['Pacific Islander']/wow['total']
    wow['Taiwanese_percent'] = wow['Taiwanese']/wow['total']
    wow['Thai_percent'] = wow['Thai']/wow['total']
    wow['Vietnamese_percent'] = wow['Vietnamese']/wow['total']
    wow['White_percent'] = wow['White']/wow['total']
    wow['Other East Asian_percent'] = wow['Other East Asian']/wow['total']
    wow['Other South Asian_percent'] = wow['Other South Asian']/wow['total']
    wow['Other Southeast Asian_percent'] = wow['Other Southeast Asian']/wow['total']
    wow['Other non-AA/PI_percent'] = wow['Other non-AA/PI']/wow['total']
    wow['Other or unknown_ethnicity_percent'] = wow['Other or unknown_ethnicity']/wow['total']

    # bar plot for age
    _fig = px.bar(wow, x = 'state', y = ['Cambodian_percent',
           'Central Asian_grouped_percent', 'Chinese_percent', 'P/Filipinx_percent',
           'Latinx_percent', 'Hmong_percent', 'Indian_percent', 'Japanese_percent',
           'Korean_percent', 'Lao_percent', 'Pacific Islander_percent',
           'Taiwanese_percent', 'Thai_percent', 'Vietnamese_percent', 'White_percent',
           'Other East Asian_percent', 'Other South Asian_percent',
           'Other Southeast Asian_percent', 'Other non-AA/PI_percent',
           'Other or unknown_ethnicity_percent'], barmode = 'group', title = "Race of Victims in California, New York, and Texas")
    return wow,


@app.cell
def __():
    import marimo as mo
    return mo,


if __name__ == "__main__":
    app.run()
