html_content = """<table class="wikitable sortable jquery-tablesorter"></table>"""

# import beautifulsoup
from bs4 import BeautifulSoup

# Assuming `html_content` contains the HTML source you provided
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table
table = soup.select_one('.wikitable')

# Initialize an empty dictionary to store the planning area and its subzones
area_dict = {}
key = ""
counter = 0
next_counter = 0
NUM_COLUMNS = 3
# Loop through each row in the tbody of the table
for i, cell in enumerate(table.find_all('td')):  # [1:] to skip header row
    # if cell contains a <a> tag
    # if cell.find('a'):
    # if cell has rowspan attribute, it is a key
    if i == 0:
        key = cell.text.strip()
        area_dict[key] = []
        try:
            # try get rowspan
            next_counter = int(cell['rowspan'])*NUM_COLUMNS
        except:
            # if error, means no rowspan
            next_counter = 1*NUM_COLUMNS
    elif next_counter == 0:
        # is a key
        key = cell.text.strip()
        area_dict[key] = []
        try:
            # try get rowspan
            next_counter = int(cell['rowspan'])*NUM_COLUMNS
        except:
            # if error, means no rowspan
            next_counter = 1*NUM_COLUMNS
        counter = 0
    else:
        if counter % NUM_COLUMNS == 0:
            # else it is a value, append
            value = cell.text.strip()
            # append to the last key
            area_dict[key].append(value)
        counter += 1
        next_counter -= 1

print(area_dict)
