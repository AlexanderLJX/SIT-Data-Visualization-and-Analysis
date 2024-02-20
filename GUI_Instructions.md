# Instructions for Using the PySimpleGUI Application for Data Visualisation and Analysis

## DISCLAIMER: 
## THIS GUI APPLICATION WORKS BEST WITH A COMPUTER SYSTEM SCALE OF 125%. PLEASE ADJUST BASE ON YOUR COMPUTER SYSTEM'S SCALE THAT GIVES YOU THE BEST VIEW.

## <ins>1. View Foodplaces Tab</ins>

The View foodplaces tab is used to view the list of foodplaces in Singapore on the map where users can set up to 3 filters -- entering a Natural Language Query, 
Areas of Singapore and also the Categories of Foodplaces.

### <ins>Filtering based on Natural Language Query</ins>
Natural Language Query provides users the flexibility to enter any query they want on how the data can be filtered and then visualised.
1. To begin, enter a Natural language Query. Only 1 Natural Language Query can be entered at a time.

Examples of Natural Language Query:
- list all the restaurants in the east
- dinein and takeaway and region is central and top 10 on bayesian rating
- top 100 based on avg star ratign and the 10 least pricey
- top 3 lowest bayesian rating
- top 100 based on relevancy and the 10 earliest to open

### <ins>Filtering based on Areas of Singapore</ins>
1. To begin, select the Areas of Singapore that you will want to view the foodplaces from in the list. Multiple selections are allowed.
   
### <ins>Filtering based on Categories of Foodplaces</ins>
1. To begin, select the Categories of Foodplaces that you will want to view the foodplaces from in the list. Multiple selections are allowed.

### <ins>For all 3 Filtering Methods (after Step 1 is completed)</ins>
2. Click on the "Generate" button.
3. View and Display the data results on the map by clicking on one of the 2 map options (green buttons).
4. To save a copy of the map, click "Export Map". Save the map HTML file at the desired location of your file system.
5. To save a copy of the filtered dataet, click "Export Filtered Datasset". Save the filtered dataset CSV file at the desired location of your file system.

### <ins>Combining Filters</ins>
Users can filter the dataset up to 3 filters. **Do note that certain filters that are set when generating will not produce any results if there are none available, resulting in a clean map without any hotspots and drop pins symbols.**

### <ins>Editing JSON filter after Natural Language Query geenration </ins>
The JSON filter that is generated after the Natural Language Query can also be edited and combined with the other 2 filters - Areas of Singapore and Categories of Foodplaces. However, by doing so, users **DO NOT need to click on the "Generate" button** to display the result, and the result produced on the map is based on the **latest settings configured on the JSON Filter**. 
**EITHER THE OPTION OF NATURAL LANGUAGE QUERY GENERAATION FROM THE NLQ TEXTBOX OR EDITING THE JSON FILTER CAN BE USED TOGETHER WITH OR WITHOUT THE OTHER 2 FILTERING OPTIONS AT ANY ONE TIME.**

### <ins>Saving Raw Dataset CSV File</ins>
If you would like to view the entire raw dataset without any filtering, click "Export Entire Dataset". Save the raw dataset CSV file at the desired location of 
your file system.

### <ins>Using the Map for Analysis</ins>
1. To use the map, use the "+" sign button found at the top left of the map or scroll up using the mouse to enlarge the map. Similar for the opposite, use the "-" sign button found at the top left of the map or scroll down using the mouse to minimse the map.
2. Enlarging the map makes the location more precise. Therefore, there will be more hotspots found with it being disperesed into more precise areas. 
3. Clicking on the hostpots will further zoom in the map. The final result will be a drop pin where hovering to it will show the foodplace names located at the particular location. 

### <ins>Map Result Example seen in View Foodplaces Tab </ins>
<figure>
  <img src="View_Foodplaces_Tab_Example.png" alt="View_Foodplaces_Tab_Example">
   <figcaption>Map result showing the foodplaces found in the Eastern Region of Singapore.</figcaption>
</figure>

## <ins>2. Data Diagrams Tab</ins>

The Data Diagrams Tab allows users to create stories and view data insights and relationships from the raw datatset CSV file.

1. To begin, 
