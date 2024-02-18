import g4f
import constants

def generate_filter(query):
    # Automatic selection of provider
    # streamed completion
    response = g4f.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model=g4f.models.gpt_4,
        messages=[{
                "role": "user",
                "content": """You are an AI intepreter that will translate the user's queries into json format based on the following information:
                These are the features and data types of the dataframe, you can only filter based on these columns:
                """ + str(constants.FEATURES_DATATYPES) + """
                These are the values of the About column:
                ['Outdoor seating', 'Delivery', 'Takeaway', 'Dine-in', 'Wheelchair-accessible entrance', 'Alcohol', 'Beer', 'Coffee', 'Late-night food', 'Small plates', 'Lunch', 'Dinner', 'Catering', 'Dessert', 'Seating', 'Gender-neutral toilets', 'Toilets', 'Casual', 'Family friendly', 'Groups', 'LGBTQ+ friendly', 'Transgender safe space', 'Debit cards', 'NFC mobile payments', 'Good for kids', 'High chairs', 'Free parking lot', 'Somewhat difficult to find a space']
                These are the values in the Region column:
                ['Central Region', 'East Region', 'North Region', 'North-East Region', 'West Region']
                These are the valid operators, you can only use these operators to filter the dataframe:
                """ + str(constants.OPERATORS) + """
                1. The first key of the json is the dataframe column name.
                2. the value of the key will be the value of the column that the user wants to filter
                3. You can only reply in json format.
                Please filter out non LGBTQ friendly restaurants."""
            },
            {
                "role": "assistant",
                "content": """[
  {
    "column": "About",
    "value": "LGBTQ+ friendly",
    "operator": "=="
  }
]"""
            },
            {
                "role": "user",
                "content": """restaurants which open after 9am in Bishan planning area."""
            },
            {
                "role": "assistant",
                "content": """[
  {
    "column": "First Opening Time",
    "value": "09:00",
    "operator": ">"
  },
  {
    "column": "Planning Area",
    "value": "Bishan",
    "operator": "=="
  }
]"""
            },
            {
                "role": "user",
                "content": """show me only shops that have less than 3 average star rating and are in Bishan and jurong east planning areas."""
            },
            {
                "role": "assistant",
                "content": """[
  {
    "column": "Average Star Rating",
    "value": "3.0",
    "operator": "<"
  },
  {
    "column": "Planning Areas",
    "value": "Bishan",
    "operator": "=="
  },
  {
    "column": "Planning Areas",
    "value": "Jurong East",
    "operator": "=="
  }
]"""
            },
            {
                "role": "user",
                "content": """display the top 5 restaurants with the highest search engine rating."""
            },
            {
                "role": "assistant",
                "content": """[
  {
    "column": "Search Engine Rating",
    "value": "5",
    "operator": "largest"
  }
]"""
            },
            {
                "role": "user",
                "content": """show me the bottom 10 restaurants with the lowest star rating."""
            },
            {
                "role": "assistant",
                "content": """[
  {
    "column": "Star Rating",
    "value": "10",
    "operator": "smallest"
  }
]"""
            },
            {
                "role": "user",
                "content": """top 100 restaurants based on bayesian rating and the first 10 to open"""
            },
            {
                "role": "assistant",
                "content": """[
  {
    "column": "Bayesian Rating",
    "value": "100",
    "operator": "smallest"
  },
  {
    "column": "First Opening Time",
    "value": "10",
    "operator": "smallest"
  }
]"""
            },
            {
                "role": "user",
                "content": """top 10 restaurants based on star rating where price rating more or equals to $$$"""
            },
            {
                "role": "assistant",
                "content": """[
  {
    "column": "Price Rating",
    "value": "$$$",
    "operator": ">="
  },
  {
    "column": "Average Star Rating",
    "value": "10",
    "operator": "largest"
  }
]"""
            },
            {
                "role": "user",
                "content": "**Reply only the json.** " + query
            }],
        # stream=True,
    )
    print(response)
    # remove instances of #### Assistant: 
    response = response.replace("#### Assistant: ", "")
    # remove the code block ```json and ```
    response = response.replace("```json", "")
    response = response.replace("```", "")
    # remove **
    response = response.replace("**", "")
    return response

def generate_plot_json(query):
    # Automatic selection of provider
    # streamed completion
    response = g4f.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model=g4f.models.gpt_4,
        messages=[{
                "role": "user",
                "content": """You are an AI intepreter that will translate the user's queries into json format in order to plot a graph:
                These are the features of the dataframe:
                """ + str(constants.PLOT_FEATURES_DATATYPES) + """
                These are the values of the About column:
                ['Outdoor seating', 'Delivery', 'Takeaway', 'Dine-in', 'Wheelchair-accessible entrance', 'Alcohol', 'Beer', 'Coffee', 'Late-night food', 'Small plates', 'Lunch', 'Dinner', 'Catering', 'Dessert', 'Seating', 'Gender-neutral toilets', 'Toilets', 'Casual', 'Family friendly', 'Groups', 'LGBTQ+ friendly', 'Transgender safe space', 'Debit cards', 'NFC mobile payments', 'Good for kids', 'High chairs', 'Free parking lot', 'Somewhat difficult to find a space']
                These are the plot types:
                """ + str(constants.PLOT_TYPES) + """
                1. The key "feature1" refers to the the x-axis. the value of the key is the column name of the dataframe.
                2. The key "feature2" refers to the the y-axis. 
                3. The key "plot" refers to the type of plot to be plotted.
                **You can only reply in json format.**
                This is the first query:
                plot the distribution of the average star rating."""
            },
            {
                "role": "assistant",
                "content": """{
  "feature1": "About",
  "plot": "distribution"
}"""
            },
            {
                "role": "user",
                "content": """Plot the relevancy ranking and star rating in a hexbin plot."""
            },
            {
                "role": "assistant",
                "content": """{
  "feature1": "Search Engine Rating",
  "feature2": "Average Star Rating",
  "plot": "hexbin"
}"""
            },
            {
                "role": "user",
                "content": """Plot planning area against star rating!"""
            },
            {
                "role": "assistant",
                "content": """{
  "feature1": "Planning Area",
  "feature2": "Average Star Rating",
  "plot": "bar chart"
}"""
            },
            {
                "role": "user",
                "content": "**Reply only in json format.** \n" + query
            }],
        # stream=True,
    )
    print(response)
    # remove instances of #### Assistant: 
    response = response.replace("#### Assistant: ", "")
    # remove the code block ```json and ```
    response = response.replace("```json", "")
    response = response.replace("```", "")
    # remove **
    response = response.replace("**", "")
    return response

def generate_ml_train_json(query):
    # Automatic selection of provider
    # streamed completion
    response = g4f.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model=g4f.models.gpt_4,
        messages=[{
                "role": "user",
                "content": """You are an AI intepreter that will translate the user's queries into json format in order to train a ML model based on the following information:
                These are the features of the dataframe:
                Region,Planning Area,Subzone,Name,Search Engine Rating,Sponsored,Opening Hours,First Opening Time,Popular Times,Average Star Rating,Individual Star Rating,Reviews,Category,Price Rating,Metadata,Tags,About
                These are the values of the About column:
                ['Outdoor seating', 'Delivery', 'Takeaway', 'Dine-in', 'Wheelchair-accessible entrance', 'Alcohol', 'Beer', 'Coffee', 'Late-night food', 'Small plates', 'Lunch', 'Dinner', 'Catering', 'Dessert', 'Seating', 'Gender-neutral toilets', 'Toilets', 'Casual', 'Family friendly', 'Groups', 'LGBTQ+ friendly', 'Transgender safe space', 'Debit cards', 'NFC mobile payments', 'Good for kids', 'High chairs', 'Free parking lot', 'Somewhat difficult to find a space']
                1. The key "feature1" refers to the the x-axis. the value of the key is the column name of the dataframe.
                2. The key "feature2" refers to the the y-axis. 
                3. The key "plot" refers to the type of plot to be plotted.
                **You can only reply in json format.**
                You are to determine the appropriate ML model to use based on the user's query.
                This is the first query:
                a linear regression model between number of reviews and star rating."""
            },
            {
                "role": "assistant",
                "content": """{
  "feature1": "Reviews",
  "feature2": "Average Star Rating",
  "ML model": "linear regression"
}"""
            },
            {
                "role": "user",
                "content": """train a model to see the relationship of relavancy and star rating"""
            },
            {
                "role": "assistant",
                "content": """{
  "feature1": "Search Engine Rating",
  "feature2": "Average Star Rating",
  "ML model": "linear regression"
}"""
            },
            {
                "role": "user",
                "content": """see if there are any anomalies in number of reviews"""
            },
            {
                "role": "assistant",
                "content": """{
  "feature1": "Reviews",
  "ML model": "anomaly detection"
}"""
            },
            {
                "role": "user",
                "content": "**Reply only in json format.** \n" + query
            }],
        # stream=True,
    )
    print(response)
    # remove instances of #### Assistant: 
    response = response.replace("#### Assistant: ", "")
    # remove the code block ```json and ```
    response = response.replace("```json", "")
    response = response.replace("```", "")
    # remove **
    response = response.replace("**", "")
    return response