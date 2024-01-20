import pandas as pd 
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Classroom Dashboard", page_icon=":bar_chart:", layout="wide")

# Enhances preformance by using a cache to prevent constant reloading of data
@st.cache_data
def get_data_from_file():

# Reads data from excel sheet 
    df = pd.read_excel( 'data.xlsx',
        engine='openpyxl',
        skiprows=0,
        usecols='A:U',
        nrows=100
    )

    return df
df = get_data_from_file()



#----Sidebar

# Adds image
st.sidebar.image("./CMU_Logo.png", use_column_width=True)

# Adds decorative line
st.sidebar.markdown("""---""")

# Adds sidebar header
st.sidebar.header("**Filter**")

# Adds filter functionality to the dashboard
semester = st.sidebar.multiselect(
    '**Sort by Academic Term**', 
    ['Fall', 'Spring','Summer'], 
    ['Fall', 'Spring','Summer']
)

major = st.sidebar.multiselect(
    '**Sort by Major:**',
    ['CPS','IT','Other'], 
    ['CPS','IT','Other']
)

grade = st.sidebar.multiselect(
    '**Sort by Grade**', 
    ['A', 'B','C','D','F'], 
    ['A', 'B','C','D','F']
)

df_selection = df.query(
    "Semester == @semester & Major == @major & Grade ==@grade"
)

st.sidebar.markdown("""---""")




# ---Mainpage
st.title(":bar_chart: Classroom Dashboard")
st.markdown("##")

average_Grade = round(df_selection["Grade (Percentage)"].mean())
average_Study = round(df_selection["Study Time Avg (Hrs)"].mean(), 1)
average_Slide_Time = round(df_selection["Avg Time Spent Per Slide (Mins)"].mean(), 1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average Grade Percentage:")
    st.subheader(f":clipboard: {average_Grade} %")
with middle_column:
    st.subheader("Average Study Time:")
    st.subheader(f":books: {average_Study} hours")
with right_column:
    st.subheader("Average Time Spent on Each Slide:")
    st.subheader(f":computer: {average_Slide_Time} mins")

st.markdown("""---""")
st.markdown("""---""")



#---Bar charts

# Groups the data by letter grade and finds the avg study times for those grades
study_by_grade =(
round(df_selection.groupby(by=["Grade"]).mean(numeric_only=True)[["Avg Time Spent Per Slide (Mins)"]],2) # Sorts chart so it goes from highest slide time to lowest
)

# Set up a the bar chart for avg time spent studying by Grade
fig_Study_Grade = px.bar(
    study_by_grade,
    x="Avg Time Spent Per Slide (Mins)",
    y=study_by_grade.index,
    orientation="h",
    title="<b>Avg Time Spent Per Slide By Grade</b>",
    color_discrete_sequence=["#ff2b2a"] * len(study_by_grade),
    template="plotly_white",
)

# Shows the grid for the x axis, sorts the y axis, and increase font
fig_Study_Grade.update_layout(
    xaxis=(dict(showgrid=True)),
    yaxis=dict(categoryorder="array",
        categoryarray=list(reversed(sorted(df_selection['Grade'].unique())))),
    title_font_size=25,
    xaxis_title_font_size= 20,
    yaxis_title_font_size= 20,
    xaxis_tickfont_size= 15,
    yaxis_tickfont_size= 15,
    hoverlabel_font_size= 15

)


# Create an empty list to store the slide averages
slide_avgs =  []

# Loop through each column in the dataframe and calculate its average if it contains "Slide #" in the title
for col in df_selection.columns:
    if 'Slide #' in col:
        slide_avg = round(df_selection[col].mean(),1)
        slide_avgs.append(slide_avg)


# Set up a the bar chart for avg time spent on each slide
fig_Slide_Time = px.bar(
    x=[col for col in df_selection.columns if 'Slide #' in col],
    y=slide_avgs,
    labels={'x': 'Slide Number', 'y': 'Minutes'},
    orientation="v",
    title="<b>Avg Time Spent on Each Individual Slide</b>",
)

# Displays all labels on the y axis and increase font
fig_Slide_Time.update_layout(
    yaxis=dict(tickmode="linear"),
    title_font_size=25,
    xaxis_title_font_size= 20,
    yaxis_title_font_size= 20,
    xaxis_tickfont_size= 15,
    yaxis_tickfont_size= 15,
    hoverlabel_font_size= 15
)

# Display the bar charts
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_Study_Grade, use_container_width=True)
right_column.plotly_chart(fig_Slide_Time, use_container_width=True)

st.markdown("""---""")



#---Pie Charts

grouped_data = df_selection.groupby('Major').size(numeric_only=True)

# Create pie chart for precentages of majors
major_Pie = px.pie(
    values=grouped_data, names=grouped_data.index, 
    labels={'value': 'Percentage'}, 
    title='Major Precentages',
    hole=0.4,
)

# Increase font of charts
major_Pie.update_layout(
    title_font_size=25,
    legend_font_size=20,
    hoverlabel_font_size= 15
)

# Display labels with the percentages
major_Pie.update_traces(
    textinfo='percent+label'
)

# Create pie chart for precentages of letter grades
grouped_data = df_selection.groupby('Grade').size(numeric_only=True)

grade_Pie = px.pie(
    values=grouped_data, names=grouped_data.index, 
    labels={'value': 'Percentage'}, 
    title='Letter Grade Percentages'
)

# Increase font of charts
grade_Pie.update_layout(
    title_font_size=25,
    legend_font_size=20,
    hoverlabel_font_size= 15
)

# Sort the chart by alphabetical order
grade_Pie.update_traces(
    sort=False,
    textinfo='percent+label'
)

# Display the pie charts 

left_column, right_column = st.columns(2)
left_column.plotly_chart(major_Pie, use_container_width=True)
right_column.plotly_chart(grade_Pie, use_container_width=True)

st.markdown("""---""")

#---Scatterplot

# Create the scatter plot
fig=px.scatter(
    df_selection,
    x='Grade (Percentage)',
    y='Study Time Avg (Hrs)', 
    title='Relationship Between Grade and Study Time')

# Increase the font
fig.update_layout(
    plot_bgcolor="rgba(175, 175, 175, 1)",
    title_font_size=25,
    xaxis_title_font_size= 20,
    yaxis_title_font_size= 20,
    xaxis_tickfont_size= 20,
    yaxis_tickfont_size= 20,
    hoverlabel_font_size= 15,
)

# Display the plot in Streamlit
st.plotly_chart(fig,use_container_width=True)

st.markdown("""---""")
st.markdown("""---""")

# Clean up dashboard look
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
