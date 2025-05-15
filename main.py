import streamlit as st 
import pandas as pd 
import altair as alt
import numpy as np 

def load_data():
    # import the dateset
    df = pd.read_csv("aircrahesFullDataUpdated_2024 (1).csv")
    # remove all null values
    df = df.dropna()
    # remove rows with "'-" and "10" as the Country/Region
    df = df[~df.isin(["'-"]).any(axis=1)]
    df = df[~df.isin(["10"]).any(axis=1)]
    df['Total_casualities'] = df['Fatalities (air)'] + df['Ground']
    return df

df = load_data()


# App Title
st.title("AirCrash Investigation Analysis")

# Create Filters
filters ={
    "Year": df["Year"].unique(),
    "Country/Region":df["Country/Region"].unique(),
    "Location":df["Location"].unique()
}

# store user selection
selected_filters ={}

# Generate multi-select widgets dynamically
for key, options in filters.items():
    selected_filters[key] = st.sidebar.multiselect(key,options)

# Apply the filter to the full data
filtered_df = df.copy()


# Supply filter selection to the data
for key, selected_values in selected_filters.items():
    if selected_values:
        filtered_df = filtered_df[filtered_df[key].isin(selected_values)]

# Display the data
st.dataframe(filtered_df.head())

# Calculations for each metric
total_aircrashes = len(filtered_df)
total_aboard = df["Aboard"].sum()
total_fatalities =df["Fatalities (air)"].sum()
total_ground = df["Ground"].sum()
total_survivors = total_aboard - (total_fatalities + total_ground)

# Streamlit column component
col1, col2, col3, col4,col5 = st.columns(5)
with col1:
    st.metric("Total Aircrashes",total_aircrashes)

with col2:
    st.metric("Total Aboard",total_aboard)

with col3:
    st.metric("Total Fatalities",total_fatalities)

with col4:
    st.metric("Total Ground",total_ground)
with col5:
    st.metric("Total Survivors",total_survivors)

# Display the subheader
st.subheader("Geographic Analysis")
st.subheader("Deadliest Location in terms of casualities")

# Group by location by casualities
Deadliest_location=filtered_df.groupby("Location")["Total_casualities"].sum().nlargest(8).reset_index()

st.write(Deadliest_location)

 # plotting  the chart
chart1 =alt.Chart(Deadliest_location).mark_bar().encode(
    x=alt.X('Total_casualities:Q'),
    y=alt.Y("Location:N"),
    color = alt.Color("Location:N", legend= None)
 ).properties(height = 300)
 # display the chart
st.altair_chart(chart1, use_container_width = True)

# calculate country with the most crash
st.subheader("Country with the most crashes")
most_crashes = filtered_df["Country/Region"].value_counts().nlargest(6).reset_index()
#display the result
st.write(most_crashes)


# Convert to DataFrame for Altair
crash_df = most_crashes.reset_index()
crash_df.columns = ['SN','Country', 'Crashes']

# Create pie chart
pie_chart = alt.Chart(crash_df).mark_arc().encode(
    theta=alt.Theta(field="Crashes", type="quantitative"),
    color=alt.Color(field="Country", type="nominal"),
    tooltip=["Country", "Crashes"]
).properties(
    width=400,
    height=400,
    title="Countries with Most Crashes"
)

# Display chart
st.altair_chart(pie_chart)

# display the subheader
st.subheader("Aircraft Analysis")
st.subheader("Aircraft with the most crashes")

# Calculate the number of crashes for each aircrafts and diplsy the results
aircraft_crashes = filtered_df["Aircraft"].value_counts().nlargest(8).reset_index()
st.write(aircraft_crashes)

# Plot the chart
chart3 =alt.Chart(aircraft_crashes).mark_bar().encode(
    x=alt.X('count:Q'),
    y=alt.Y("Aircraft:N"),
    color = alt.Color("Aircraft:N", legend= None)
 ).properties(height = 300)
 # display the chart
st.altair_chart(chart3, use_container_width = True)

#Display the subheader
st.subheader("Aircraft Manufacturer with the most crashes")

# Group Aircraft Manufacturer by casualities
Manufacturer_crashes=filtered_df.groupby("Aircraft Manufacturer")["Total_casualities"].sum().nlargest(8).reset_index()
#display
st.write(Manufacturer_crashes)

 # plotting  the chart
chart4 =alt.Chart(Manufacturer_crashes).mark_bar().encode(
    x=alt.X('Total_casualities:Q'),
    y=alt.Y("Aircraft Manufacturer:N"),
    color = alt.Color("Aircraft Manufacturer:N", legend= None)
 ).properties(height = 300, )

 # display the chart
st.altair_chart(chart4, use_container_width = True)

#Display the subheader
st.subheader("Time Series Analysis")

# Groupping the years using bins and labels
bins =[1908,1920,1932,1944,1956,1968,1980,1992,2004,2016,2024]
labels =["1908-1920","1921-1932","1933-1944","1945-1956","1957-1968","1969-1980","1981-1992","1993-2004","2005-2016","2017-2024"]
filtered_df["YearGrouped"] = pd.cut(df.Year,bins = bins,labels = labels)
# to view the dataset to see the added column
st.write(filtered_df.head(5))
#display
st.subheader("Trend in Air casualities over the years")
year_casualities = filtered_df.groupby("YearGrouped")["Total_casualities"].sum().nlargest(7).reset_index()
st.write(year_casualities)

 # plotting  the chart
chart5 =alt.Chart(year_casualities).mark_line(color='pink').encode(
    x=alt.X('YearGrouped'),
    y=alt.Y("Total_casualities"),
 )
 #display the chart
st.altair_chart(chart5, use_container_width = True)

# Display
st.subheader("Month with the most crashes")
month_crashes = df["Month"].value_counts().reset_index()
st.write(month_crashes)

# Plot the chart
chart6 =alt.Chart(month_crashes).mark_bar().encode(
    x=alt.X('Month'),
    y=alt.Y("count"),
    color = alt.Color("count")
 )
 
 # display the chart
st.altair_chart(chart6, use_container_width = True)

# display
st.subheader("Operator Analysis")
st.subheader("Operator with the most number of crashes")


# Calculate the number of crashes for each operator and diplsy the results
operator_crashes = filtered_df["Operator"].value_counts().nlargest(8).reset_index()
st.write(operator_crashes)

# Plot the chart
chart7 =alt.Chart(operator_crashes).mark_bar().encode(
    x=alt.X('Operator'),
    y=alt.Y("count"),
    color = alt.Color("count")
 )
 # display the chart
st.altair_chart(chart7, use_container_width = True)






