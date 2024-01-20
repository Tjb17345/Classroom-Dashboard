
---Excel Sheet
	-Most of the data within the data Excel file is randomly generated using the RAND and RANDBETWEEN Excel formulas.
	-Some exceptions include:
		--The 'Semester' column which was updated manually.
		--The 'Grade' column, which was modified based on how much the student studied to show more of a correlation between the two.
		--The 'Grade(Percentage)' column, which was randomly generated based on what letter grade the student had.
		--And the 'Avg Time Spent Per Slide (Mins)' column, which was created by calculating the averages of the different individual slide columns.

---Running the dashboard stand-alone
	-To open the dashboard, go to the same directory as the Python script within the command prompt and type "streamlit run dashboard.py".
	-Once open, you can adjust what data is shown using the sidebar filters on the left.
	-Hovering over the graphs will show a more exact number.
	-Clicking and dragging on the bar graph or scatterplot will zoom in at that location (Double-click the graph to revert back).  
