# Import necessary libraries for web app creation, data manipulation, and visualization
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

# Disable warnings that can clutter the output
warnings.filterwarnings("ignore")

# Streamlit page configuration with title, icon, and layout settings
st.set_page_config(page_title="Super Dashboard", page_icon=":bar_chart:", layout="wide")

# Set the title of the Streamlit web page
st.title(" :bar_chart: Super Dashboard Exploratory Data Analysis!")
# Use Markdown to apply custom styles to the Streamlit page, here to adjust the padding at the top of the block container
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

# Create a file uploader widget that accepts CSV files
file_upload = st.file_uploader("Upload a file :file_folder::", type=("csv"))

# If a file is uploaded, read it into a DataFrame, otherwise load a default CSV file
if file_upload is not None:
    df = pd.read_csv(file_upload, encoding="ISO-8859-1")
else:
    df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")

# Rename a column in the DataFrame for better clarity
df = df.rename(columns={"State/Province": "State"})

# Create two columns in the Streamlit interface for layout purposes
col1, col2 = st.columns((2))

# Add a header to the sidebar for filter options
st.sidebar.header("Choose your filter: ")

# Convert the 'OrderDate' column to datetime objects for filtering purposes
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# Get the minimum and maximum dates from the 'OrderDate' column to set the bounds for a date input widget
startDate = df["OrderDate"].min()
endDate = df["OrderDate"].max()

# Create two date input widgets for selecting a date range, and filter the DataFrame based on this range
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))
df = df[(df["OrderDate"] >= date1) & (df["OrderDate"] <= date2)]

# Add another header for additional filters in the sidebar
st.sidebar.header("Choose your filter: ")

# Create a multi-select sidebar widget for filtering by Region, and filter the DataFrame accordingly
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
df2 = df[df["Region"].isin(region)] if region else df

# Create a multi-select sidebar widget for filtering by State, and filter the DataFrame accordingly
state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
df3 = df2[df2["State"].isin(state)] if state else df2

# Create a multi-select sidebar widget for filtering by City, and filter the DataFrame accordingly
city = st.sidebar.multiselect("Pick the City", df3["City"].unique())
filtered_df = df3[df3["City"].isin(city)] if city else df3

# Group the filtered DataFrame by 'Category' and sum the 'Sales' for each category
category_df = filtered_df.groupby("Category")["Sales"].sum().reset_index()

# Use Plotly to create and display a bar chart of sales by category
with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x="Category", y="Sales")
    st.plotly_chart(fig, use_container_width=True)

# Use Plotly to create and display a pie chart of sales by region
with col2:
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Region")
    st.plotly_chart(fig, use_container_width=True)
# Define two columns for the Streamlit layout to display data view and download options side by side
cl1, cl2 = st.columns((2))

# Column 1: Create an expandable section named 'Category_ViewData' for category-wise sales
with cl1:
    with st.expander("Category_ViewData"):
        # Apply a blue gradient background to the category dataframe display
        st.write(category_df.style.background_gradient(cmap="Blues"))
        # Convert the category dataframe to a CSV format for download
        csv = category_df.to_csv(index=False).encode('utf-8')
        # Create a download button for the category data CSV
        st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

# Column 2: Create an expandable section named 'Region_ViewData' for region-wise sales
with cl2:
    with st.expander("Region_ViewData"):
        # Group the filtered dataframe by region and sum the sales
        region_sales = filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()
        # Apply an orange gradient background to the region dataframe display
        st.write(region_sales.style.background_gradient(cmap="Oranges"))
        # Convert the region dataframe to a CSV format for download
        csv = region_sales.to_csv(index=False).encode('utf-8')
        # Create a download button for the region data CSV
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

# Add a new column to the filtered dataframe that represents the month and year of the 'OrderDate'
filtered_df["month_year"] = filtered_df["OrderDate"].dt.to_period("M")

# Create a subheader for the time series analysis section
st.subheader('Time Series Analysis')

# Create a line chart dataframe by grouping sales data by month_year and summing up the sales
linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
# Use Plotly to create a line chart for the time series data
fig2 = px.line(linechart, x="month_year", y="Sales", labels={"Sales": "Amount"}, height=500, width=1000, template="gridon")
# Display the line chart in the Streamlit app
st.plotly_chart(fig2, use_container_width=True)

# Create an expandable section for viewing and downloading the time series data
with st.expander("View Data of TimeSeries:"):
    # Apply a blue gradient background to the time series data display
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    # Convert the linechart data to a CSV format for download
    csv = linechart.to_csv(index=False).encode("utf-8")
    # Create a download button for the time series data CSV
    st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')

# Create a subheader for the TreeMap section, which provides a hierarchical view of sales
st.subheader("Hierarchical view of Sales using TreeMap")
# Use Plotly to create a TreeMap based on Region, Category, and Sub-Category
fig3 = px.treemap(filtered_df, path=["Region", "Category", "Sub-Category"], values="Sales", hover_data=["Sales"],
                  color="Sub-Category")
# Update the layout dimensions of the TreeMap
fig3.update_layout(width=800, height=650)
# Display the TreeMap in the Streamlit app
st.plotly_chart(fig3, use_container_width=True)

# Create two columns for additional pie chart visualizations
chart1, chart2 = st.columns((2))

# Column 1: Segment-wise sales pie chart
with chart1:
    st.subheader('Segment wise Sales')
    # Create a pie chart for segment-wise sales
    fig = px.pie(filtered_df, values="Sales", names="Segment", template="plotly_dark")
    # Update the chart to display segment names inside the pie chart
    fig.update_traces(text=filtered_df["Segment"], textposition="inside")
    # Display the pie chart in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

# Column 2: Category-wise sales pie chart
with chart2:
    st.subheader('Category wise Sales')
    # Create a pie chart for category-wise sales
    fig = px.pie(filtered_df, values="Sales", names="Category", template="gridon")
    # Update the chart to display category names inside the pie chart
    fig.update_traces(text=filtered_df["Category"], textposition="inside")
    # Display the pie chart in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

# Import Plotly's figure factory for advanced visualization options
import plotly.figure_factory as ff

# Create a subheader for the month-wise sub-category sales summary
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
# Create an expandable section for the summary table
with st.expander("Summary_Table"):
    # Take a sample of the dataframe for the summary table
    df_sample = df.head()[["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]
    # Use Plotly's figure factory to create a table figure
    fig = ff.create_table(df_sample, colorscale="Cividis")
    # Display the table in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

    # Markdown text for sub-category table
    st.markdown("Month wise sub-Category Table")
    # Create a pivot table for month-wise sub-category sales
    sub_category_Year = pd.pivot_table(data=filtered_df, values="Sales", index=["Sub-Category"], columns="month")
    # Apply a blue gradient background to the pivot table display
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

# Create a scatter plot to analyze the relationship between Sales, Profit, and Quantity
data1 = px.scatter(filtered_df, x="Sales", y="Profit", size="Quantity")
# Update the layout of the scatter plot with titles and font settings
data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot",
                       titlefont=dict(size=20), xaxis=dict(title="Sales", titlefont=dict(size=19)),
                       yaxis=dict(title="Profit", titlefont=dict(size=19)))
# Display the scatter plot in the Streamlit app
st.plotly_chart(data1, use_container_width=True)

# Reminder comment: the script is to be run with 'streamlit run filename.py' in the terminal
