import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='HMS')
st.header('Hospital Management System')
st.subheader('was the detail helpful for you?')

### --- LOAD DATAFRAME
#excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_csv("hospitalData.csv")

data = pd.read_csv("hospitalData.csv")
data.dropna(inplace=True)

# --- STREAMLIT SELECTION
hos = df['Hospital_Name'].unique().tolist()
ages = df['no_of_patient'].unique().tolist()

age_selection = st.slider('no_of_patient:',
                        min_value= min(ages),
                        max_value= max(ages),
                        value=(min(ages),max(ages)))

hos_selection = st.multiselect('Hospital_Name:',
                                    hos,
                                    default=hos)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['no_of_patient'].between(*age_selection)) & (df['Hospital_Name'].isin(hos_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['no_of_beds']).count()[['no_of_patient']]
df_grouped = df_grouped.rename(columns={'no_of_patient': 'no_of_staff'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='no_of_beds',
                   y='no_of_staff',
                   text='no_of_staff',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
image = Image.open('hmsd.png')
col1.image(image,
        caption='Designed by slidesgo / Freepik',
        use_column_width=True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(data)
#                 title='Total No.',
#                 values='Participants',
#                 names='Hospital_Name')

st.plotly_chart(pie_chart)