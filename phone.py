#-------------------------------------------| PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION|--------------------------------------------------------------------------------#

#-------------------------------------------| IMPORT LIBRARIES |---------------------------------------------------------------------------------------------------------------#

import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import requests
import pandas as pd
import numpy as np
import os
import json
import geopandas as gpd
import mysql.connector as sql
import PIL
from PIL import Image




#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
mydb = sql.connect(host="localhost",
                   user="root",
                   password="",
                   database= "phonepe_data"
                  )
mycursor = mydb.cursor(buffered=True)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#CREATE NAVBAR FOR EACH PROCESS
st.set_page_config(layout='wide')
def streamlit_menu(example=2):
    if example == 2:
        st.title(":violet[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]")
        selected = option_menu(
            menu_title=None,  # required
            options=["ABOUT","DASHBOARD","ANALYSIS", "INSIGHTS","REPORTS"],  # required
            icons=["file-person","speedometer","pie-chart-fill", "award","flag"],  # optional
            menu_icon=None,  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={"container": {"padding": "0!important", "background-color": "#A16FE8","size":"cover", "width": "100%"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#B692EA"},
        "nav-link-selected": {"background-color": "#B692EA"}}
        )
        return selected

#Page Contents
selected = streamlit_menu(example=2)

if selected == "ABOUT":
    col1,col2 =st.columns(2)
        
    with col1:
        st.write(":violet[ABOUT THE PHONEPE-PULSE:]")
        st.write("**1)The Indian digital payments story has truly captured the world's imagination.**")
        st.write("**2)From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.**")
        st.write("**3)When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India.**")
        st.write("**4)Some of the questions we were seeking answers to were - How are consumers truly using digital payments?**")
        st.write("**5)What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?**")
        st.write("**6)This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.**")
        st.write("**7)This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as India's largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money. So it was time to demystify and share the what, why and how of digital payments in India.**")
        st.write("**8)PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.**")
    with col2:
        video_file = open('pulse-video.mp4', 'rb')
        video_bytes = video_file.read()

        st.video(video_bytes)
#---------------------------------------------------| INSIGHTS TAB |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

if selected == "INSIGHTS":
    st.title("INSIGHTS")
    st.write("----")
    st.subheader("HERE WE CAN GET SOME BASIC INSIGHTS")
    options = ["--select--",
               "1.TOP 10 STATES BASED ON YEAR AND AMOUNT OF TRANSACTION",
               "2.2.LIST 10 STATES BASED ON TYPE AND AMOUNT OF TRANSACTION",
               "3.TOP 10 BRANDS BASED ON PERCENTAGE",
               "4.TOP 10 REGISTERED-USERS BASED ON STATES AND PINCODE",
               "5.TOP 10 DISTRICTS BASED ON STATES AND COUNT OF TRANSACTION",
               "6.LIST 10 DISTRICTS BASED ON STATES AND AMOUNT OF TRANSACTION",
               "7.LIST 10 TRANSACTION_COUNT BASED ON DISTRICTS AND STATES",
               "8.TOP 10 REGISTEREDUSERS BASED ON STATES AND DISTRICT",
               "9.TOP 10 TRANSACTION_TYPE BASED ON TRANSACTION_COUNT AND TRANSACTION_AMOUNT",
               "10.TOP 10 TRANSACTION_AMOUNT BASED ON YEAR AND STATES"]
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------#              
#QUERY:1        
    
    select = st.selectbox("Select the option",options)
    if select=="1.TOP 10 STATES BASED ON YEAR AND AMOUNT OF TRANSACTION":
        mycursor.execute("SELECT DISTINCT State,Transaction_amount,Year,Quarter FROM top_trans GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10");
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','Transaction_amount', 'Year','Quarter'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df1)
        with col2:
            
            fig_vc = px.bar(df1, y='State', x='Transaction_amount', text_auto='.2s', title="TOP 10 STATES AMOUNT OF TRANSACTION IN CR", )
            fig_vc.update_traces(textfont_size=16,marker_color='violet')
            fig_vc.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
            st.plotly_chart(fig_vc,use_container_width=True) 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#            
#QUERY:2       
    elif select=="2.LIST 10 STATES BASED ON TYPE AND AMOUNT OF TRANSACTION":
        mycursor.execute("SELECT DISTINCT State, SUM(Transaction_Count) as Total FROM top_trans GROUP BY State ORDER BY Transaction_amount LIMIT 10");
        df2 = pd.DataFrame(mycursor.fetchall(),columns=['State','Transaction_count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df2)
        with col2:
            fig_vc = px.bar(df2, y='Transaction_count', x='State', text_auto='.2s', title="LIST 10 STATES BASED ON TYPE AND AMOUNT OF TRANSACTION", )
            fig_vc.update_traces(textfont_size=16,marker_color='violet')
            fig_vc.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
            st.plotly_chart(fig_vc,use_container_width=True) 
#------------------------------------------------------------------------------------------------------------------------------------------------------------#            
#QUERY:3
    elif select == "3.TOP 10 BRANDS BASED ON PERCENTAGE":
        mycursor.execute("SELECT DISTINCT Brands, SUM(Percentage) AS Amount FROM agg_user GROUP BY Percentage ORDER BY Count DESC LIMIT 10")
        df3 = pd.DataFrame(mycursor.fetchall(), columns=['Brands', 'Percentage'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df3)
        with col2:
            st.write("**TOP 10 BRANDS BASED ON PERCENTAGE**")
            st.bar_chart(data=df3, y="Percentage", x="Brands")
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------#            
#QUERY:4
    elif select=="4.TOP 10 REGISTERED-USERS BASED ON STATES AND PINCODE":
        mycursor.execute("SELECT DISTINCT State, Pincode, SUM(Registered_users) AS Users FROM top_user GROUP BY State, Pincode ORDER BY Users DESC LIMIT 10");
        df4 = pd.DataFrame(mycursor.fetchall(),columns=['State','Pincode','Registered_users'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df4)
        with col2:
            fig_vc = px.bar(df4, y='Registered_users', x='State', text_auto='.2s', title="TOP 10 REGISTERED-USERS BASED ON STATES AND PINCODE", )
            fig_vc.update_traces(textfont_size=16,marker_color='GREEN')
            fig_vc.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
            st.plotly_chart(fig_vc,use_container_width=True)
            
           
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#            
#QUERY:5
    elif select=="5.TOP 10 DISTRICTS BASED ON STATES AND COUNT OF TRANSACTION":
        mycursor.execute("SELECT DISTINCT State,District,SUM(Count) AS Counts FROM map_trans GROUP BY State,District ORDER BY Counts DESC LIMIT 10");
        df5 = pd.DataFrame(mycursor.fetchall(),columns=['State','District','Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df5)
        with col2:
            #st.title("TOP 10 DISTRICTS BASED ON STATES AND COUNT OF TRANSACTION")
            #st.bar_chart(data=df,y="State",x="Count")
            fig_vc = px.bar(df5, y='Count', x='District', text_auto='.2s', title="TOP 10 DISTRICTS BASED ON STATES AND COUNT OF TRANSACTION", )
            fig_vc.update_traces(textfont_size=16,marker_color='grey')
            fig_vc.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
            st.plotly_chart(fig_vc,use_container_width=True)
       
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#        
#QUERY:6
    elif select=="6.LIST 10 DISTRICTS BASED ON STATES AND AMOUNT OF TRANSACTION":
        mycursor.execute("SELECT DISTINCT State,Year,SUM(Transaction_amount) AS Amount FROM agg_trans GROUP BY State, Year ORDER BY Amount ASC LIMIT 10");
        df6 = pd.DataFrame(mycursor.fetchall(),columns=['State','Year','Transaction_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df6)
        with col2:
            fig_vc = px.bar(df6, y='Transaction_amount', x='State', text_auto='.2s', title="LIST 10 DISTRICTS BASED ON STATES AND AMOUNT OF TRANSACTION", )
            fig_vc.update_traces(textfont_size=16,marker_color='violet')
            fig_vc.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
            st.plotly_chart(fig_vc,use_container_width=True)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#            
#QUERY:7
    elif select=="7.LIST 10 TRANSACTION_COUNT BASED ON DISTRICTS AND STATES":
        mycursor.execute("SELECT DISTINCT State, District, SUM(Count) AS Counts FROM map_trans GROUP BY State,District ORDER BY Counts ASC LIMIT 10");
        df7 = pd.DataFrame(mycursor.fetchall(),columns=['State','District','Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df7)
        with col2:
            #st.title("LIST 10 TRANSACTION_COUNT BASED ON DISTRICTS AND STATES")
            #st.bar_chart(data=df7,y="State",x="Transaction_Count")
            fig_vc = px.bar(df7, y='Count', x='State', text_auto='.2s', title="LIST 10 TRANSACTION_COUNT BASED ON DISTRICTS AND STATES", )
            fig_vc.update_traces(textfont_size=16,marker_color='orange')
            fig_vc.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
            st.plotly_chart(fig_vc,use_container_width=True)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#            
#QUERY:8
    elif select=="8.TOP 10 REGISTEREDUSERS BASED ON STATES AND DISTRICT":
        mycursor.execute("SELECT DISTINCT State,District, SUM(Registered_user) AS Users FROM map_user GROUP BY State,District ORDER BY Users DESC LIMIT 10");
        df8 = pd.DataFrame(mycursor.fetchall(),columns = ['State','District','Registered_user'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df8)
        with col2:
            
            fig_vc = px.bar(df8, y='Registered_user', x='State', text_auto='.2s', title="LIST 10 TRANSACTION_COUNT BASED ON DISTRICTS AND STATES", )
            fig_vc.update_traces(textfont_size=16,marker_color='red')
            fig_vc.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
            st.plotly_chart(fig_vc,use_container_width=True)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# 
#QUERY:9           
    elif select == "9.TOP 10 TRANSACTION_TYPE BASED ON TRANSACTION_COUNT AND TRANSACTION_AMOUNT":
        mycursor.execute("SELECT State, Transaction_type, SUM(Transaction_count) AS Transaction_count, SUM(Transaction_amount) AS Transaction_amount FROM agg_trans GROUP BY State, Transaction_type ORDER BY Transaction_count DESC, Transaction_amount DESC LIMIT 20")
        df9 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_type', 'Transaction_count', 'Transaction_amount'])
    
        col1, col2 = st.columns(2)
    
        with col1:
         st.write(df9)
    
         with col2:
             fig_vc = px.bar(df9, y='Transaction_amount', x='Transaction_type', text='Transaction_amount', title="TOP 10 TRANSACTION_TYPE BASED ON TRANSACTION_COUNT AND TRANSACTION_AMOUNT")
             fig_vc.update_traces(textfont_size=16, marker_color='brown')
             fig_vc.update_layout(title_font_color='#1308C2', title_font=dict(size=25))
             st.plotly_chart(fig_vc, use_container_width=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# QUERY:10
    elif select=="10.TOP 10 TRANSACTION_AMOUNT BASED ON YEAR AND STATES":
        mycursor.execute("SELECT State,Year, SUM(Transaction_amount) AS Transaction_amount FROM agg_trans GROUP BY State,Year ORDER BY Transaction_amount DESC LIMIT 10");
        df10 = pd.DataFrame(mycursor.fetchall(),columns = ['State','Year','Transaction_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df10)
        with col2:
            #st.write("TOP 10 REGISTEREDUSERS BASED ON STATES AND DISTRICT")
            #st.bar_chart(data=df8,y="Registered_user",x="State")
            fig_vc = px.bar(df10, y='Transaction_amount', x='Year', text_auto='.2s', title="TOP 10 TRANSACTION_AMOUNT BASED ON YEAR AND STATES", )
            fig_vc.update_traces(textfont_size=16,marker_color='red')
            fig_vc.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
            st.plotly_chart(fig_vc,use_container_width=True)        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#DASHBOARD  
if selected == "DASHBOARD":
    col1,col2, = st.columns(2)
    col1.image(Image.open("D:\DS PROJECTS\PHONEPEPULSE\PhonePe_Logo.jpg"),width = 500)
    with col1:
        st.write(":violet[1)PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India.]")
        st.write(":violet[2)PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer.]")
        st.write(":violet[3)The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.]")
        st.write(":violet[4)It is owned by Flipkart, a subsidiary of Walmart.]")
        st.download_button("DOWNLOAD THE APP ", "https://play.google.com/store/search?q=phonepe&c=apps/")
    with col2:
        st.video("D:\DS PROJECTS\PHONEPEPULSE\original-ee7ad1ff21fad3b8a69928e5d907ddf8.mp4")
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#  

from streamlit_extras.add_vertical_space import add_vertical_space

if selected == "ANALYSIS":
    Data_Aggregated_Transaction_df= pd.read_csv(r'D:\DS PROJECTS\PHONEPEPULSE\Data_Aggregated_Transaction_Table.csv')
    Data_Aggregated_User_Summary_df= pd.read_csv(r'D:\DS PROJECTS\PHONEPEPULSE\Data_Aggregated_User_Summary_Table.csv')
    Data_Aggregated_User_df= pd.read_csv(r'D:\DS PROJECTS\PHONEPEPULSE\Data_Aggregated_User_Table.csv')
    Scatter_Geo_Dataset =  pd.read_csv(r'D:\DS PROJECTS\PHONEPEPULSE\Data_Map_Districts_Longitude_Latitude.csv')
    Coropleth_Dataset =  pd.read_csv(r'D:\DS PROJECTS\PHONEPEPULSE\Data_Map_IndiaStates_TU.csv')
    Data_Map_Transaction_df = pd.read_csv(r'D:\DS PROJECTS\PHONEPEPULSE\Data_Map_Transaction_Table.csv')
    Data_Map_User_Table= pd.read_csv(r'D:\DS PROJECTS\PHONEPEPULSE\Data_Map_User_Table.csv')
    Indian_States= pd.read_csv(r'D:\DS PROJECTS\PHONEPEPULSE\Longitude_Latitude_State_Table.csv')

    c1,c2=st.columns(2)
    with c1:
        Year = st.radio(
                'SELECT THE YEAR',
                ('2018', '2019', '2020','2021','2022'))
    with c2:
        Quarter = st.radio(
                'SELECT THE QUARTER',
                ('1', '2', '3','4'))
    year=int(Year)
    quarter=int(Quarter)
    
    Transaction_scatter_districts=Data_Map_Transaction_df.loc[(Data_Map_Transaction_df['Year'] == year ) & (Data_Map_Transaction_df['Quarter']==quarter) ].copy()
    Transaction_Coropleth_States=Transaction_scatter_districts[Transaction_scatter_districts["State"] == "india"]
    Transaction_scatter_districts.drop(Transaction_scatter_districts.index[(Transaction_scatter_districts["State"] == "india")],axis=0,inplace=True)
    # Dynamic Scattergeo Data Generation
    
    Transaction_scatter_districts = Transaction_scatter_districts.sort_values(by=['Place_Name'], ascending=False)
    Scatter_Geo_Dataset = Scatter_Geo_Dataset.sort_values(by=['District'], ascending=False) 
    Total_Amount=[]
    for i in Transaction_scatter_districts['Total_Amount']:
        Total_Amount.append(i)
    Scatter_Geo_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_scatter_districts['Total_Transactions_count']:
        Total_Transaction.append(i)
    Scatter_Geo_Dataset['Total_Transactions']=Total_Transaction
    Scatter_Geo_Dataset['Year_Quarter']=str(year)+'-Q'+str(quarter)
    # Dynamic Coropleth
    
    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['state'], ascending=False)
    Transaction_Coropleth_States = Transaction_Coropleth_States.sort_values(by=['Place_Name'], ascending=False)
    Total_Amount=[]
    for i in Transaction_Coropleth_States['Total_Amount']:
        Total_Amount.append(i)
    Coropleth_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_Coropleth_States['Total_Transactions_count']:
        Total_Transaction.append(i)
    Coropleth_Dataset['Total_Transactions']=Total_Transaction 
    
    
    
    
    #scatter plotting the states codes 
    Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
    Indian_States['Registered_Users']=Coropleth_Dataset['Registered_Users']
    Indian_States['Total_Amount']=Coropleth_Dataset['Total_Amount']
    Indian_States['Total_Transactions']=Coropleth_Dataset['Total_Transactions']
    Indian_States['Year_Quarter']=str(year)+'-Q'+str(quarter)
    fig=px.scatter_geo(Indian_States,
                        lon=Indian_States['Longitude'],
                        lat=Indian_States['Latitude'],                                
                        text = Indian_States['code'], #It will display district names on map
                        hover_name="state", 
                        hover_data=['Total_Amount',"Total_Transactions","Year_Quarter"],
                        )
    fig.update_traces(marker=dict(color="white" ,size=0.3))
    fig.update_geos(fitbounds="locations", visible=False,)
    # scatter plotting districts
    Scatter_Geo_Dataset['col']=Scatter_Geo_Dataset['Total_Transactions']
    fig1=px.scatter_geo(Scatter_Geo_Dataset,
                        lon=Scatter_Geo_Dataset['Longitude'],
                        lat=Scatter_Geo_Dataset['Latitude'],
                        color=Scatter_Geo_Dataset['col'],
                        size=Scatter_Geo_Dataset['Total_Transactions'],     
                    #text = Scatter_Geo_Dataset['District'], #It will display district names on map
                        hover_name="District", 
                        hover_data=["State", "Total_Amount","Total_Transactions","Year_Quarter"],
                        title='District',
                        size_max=22)
    
    fig1.update_traces(marker=dict(color="rebeccapurple" ,line_width=1))    #rebeccapurple
#coropleth mapping india
    fig_ch = px.choropleth(
                        Coropleth_Dataset,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',                
                        locations='state',
                        color="Total_Transactions",                                       
                        )
    fig_ch.update_geos(fitbounds="locations", visible=False,)
#combining districts states and coropleth
    fig_ch.add_trace( fig.data[0])
    fig_ch.add_trace(fig1.data[0])
    st.write("### **:violet[PHONEPE INDIA MAP]**")
    colT1,colT2 = st.columns([6,4])
    with colT1:
        st.plotly_chart(fig_ch, use_container_width=True)
    with colT2:
        st.info(
        """
        Details of Map:
        - The darkness of the state color represents the total transactions
        - The Size of the Circles represents the total transactions dictrict wise
        - The bigger the Circle the higher the transactions
        - Hover data will show the details like Total transactions, Total amount
        """
        )
        st.info(
        """
        Important Observations:
        - User can observe Transactions of PhonePe in both statewide and Districtwide.
        - We can clearly see the states with highest transactions in the given year and quarter
        - We get basic idea about transactions district wide
        """
        )


    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['Total_Transactions'])
    fig = px.bar(Coropleth_Dataset, x='state', y='Total_Transactions',title=str(year)+" Quarter-"+str(quarter))
    with st.expander("THE BAR GRAPH IS PROVIDED BELOW"):
        st.info('**:violet[The bar graph showing the increasing order of PhonePe Transactions according to the states of India, Here we can observe the top states with highest Transaction by looking at graph]**')
        st.plotly_chart(fig, use_container_width=True)
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
if selected =="REPORTS":
    col1,col2 = st.columns(2)
    with col1:
     st.write("PROJECT DONE BY: MUTHUSWAMI")
     st.write("BATCH : DW52")
     st.write("GITHUB : https://github.com/muthu173cyber")
     st.write("LINKED IN :https://www.linkedin.com/in/muthuswami-pandian-199185260/")
     st.write("PROJECT TITLE : PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")
     st.write("DOMAIN : FINTECH")
     st.write("TECHNOLOGIES :")
     st.write("1)GITHUB CLONING")
     st.write("2)PYTHON")
     st.write("3)PANDAS")
     st.write("4)MYSQL")
     st.write("5)STREAMLIT")
     st.write("6)PLOTLY")
    
    with col2:
     st.write("**SCRIPT TO CLONE DATA FROM GITHUB**")
     st.image("script.png")

    