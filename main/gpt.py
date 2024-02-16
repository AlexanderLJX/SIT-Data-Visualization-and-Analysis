import g4f

def generate_filter(query):
    print(g4f.Provider.Ails.params)  # supported args

    # Automatic selection of provider

    # streamed completion
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.You,
        messages=[{
                "role": "user",
                "content": """You are an AI intepreter that will translate the user's queries into json format based on the following information:
                These are the features of the dataframe:
                Region,Planning Area,Subzone,Name,Search Engine Rating,Sponsored,Opening Hours,First Opening Time,Popular Times,Average Star Rating,Individual Star Rating,Reviews,Category,Price Rating,Metadata,Tags,About
                These are the values of the About column:
                ['Outdoor seating', 'Delivery', 'Takeaway', 'Dine-in', 'Wheelchair-accessible entrance', 'Alcohol', 'Beer', 'Coffee', 'Late-night food', 'Small plates', 'Lunch', 'Dinner', 'Catering', 'Dessert', 'Seating', 'Gender-neutral toilets', 'Toilets', 'Casual', 'Family friendly', 'Groups', 'LGBTQ+ friendly', 'Transgender safe space', 'Debit cards', 'NFC mobile payments', 'Good for kids', 'High chairs', 'Free parking lot', 'Somewhat difficult to find a space']
                1. The first key of the json is the dataframe column name.
                2. the value of the key will be the value of the column that the user wants to filter
                3. You can only reply in json format.
                Please filter out non LGBTQ friendly restaurants."""
            },
            {
                "role": "assistant",
                "content": """{"column": "About", "value": "LGBTQ+ friendly", "operator": "=="}"""
            },
            {
                "role": "user",
                "content": """restaurants which open after 9am."""
            },
            {
                "role": "assistant",
                "content": """{"column": "First Opening Time", "value": "09:00", "operator": ">"}"""
            },
            {
                "role": "user",
                "content": """show me only shops that have less than 3 average star rating."""
            },
            {
                "role": "assistant",
                "content": """{"column": "Average Star Rating", "value": "3.0", "operator": "<"}"""
            },
            {
                "role": "user",
                "content": "**Reply only in json format.** " + query
            }],
        # stream=True,
    )
    print(response)
    # remove instances of #### Assistant: 
    response = response.replace("#### Assistant: ", "")
    # remove the code block ```json and ```
    response = response.replace("```json", "")
    response = response.replace("```", "")
    # remove the newline character
    response = response.replace("\n", "")
    # remove **
    response = response.replace("**", "")
    return response