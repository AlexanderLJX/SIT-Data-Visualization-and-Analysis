import csv
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
from dateutil.relativedelta import relativedelta
from datetime import datetime

# Constants
import constants

file_write_lock = threading.Lock()
file_write_lock_reviews = threading.Lock()
href_list = []
href_list_lock = threading.Lock()

def convert_relative_time(relative_time):
    now = datetime.now()

    if 'day' in relative_time:
        days_ago = int(relative_time.split()[0].replace("a", "1"))
        return now - relativedelta(days=days_ago)
    
    elif 'week' in relative_time:
        weeks_ago = int(relative_time.split()[0].replace("a", "1"))
        return now - relativedelta(weeks=weeks_ago)

    elif 'month' in relative_time:
        months_ago = int(relative_time.split()[0].replace("a", "1"))
        return now - relativedelta(months=months_ago)

    elif 'year' in relative_time:
        years_ago = int(relative_time.split()[0].replace("a", "1"))
        return now - relativedelta(years=years_ago)
    else:
        return None

def get_next_day(day_of_week):
    if day_of_week == "Monday":
        return "Tuesday"
    elif day_of_week == "Tuesday":
        return "Wednesday"
    elif day_of_week == "Wednesday":
        return "Thursday"
    elif day_of_week == "Thursday":
        return "Friday"
    elif day_of_week == "Friday":
        return "Saturday"
    elif day_of_week == "Saturday":
        return "Sunday"
    elif day_of_week == "Sunday":
        return "Monday"
    
# def get_current_element(browser, elements, element_index):
#     # more elements are loaded after scrolling, add the new elements to the list, but only if they are not already in the list
    

#     return current_element


def wait_for_target_popup(element, browser):
    # find the aria-label of the element, which contains the location name
    location_name = element.get_attribute("aria-label")
    # how to figure out if the pop out is loaded? check class "DUwDvf lfPIob"
    while True: # while loop to make sure it the popout is newly loaded and not the previous one
        location_name2 = ""
        try:
            location_name2 = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.DUwDvf.lfPIob'))).text
            print("location_name:", location_name)
            print("location_name2:", location_name2)
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
            print("TimeoutException")
            print("Waiting for more elements to load")
        
        if location_name == location_name2:
            break
        else:
            # reclick the element
            element.click()
            # click the overview tab
            overview_button = get_tab_button(browser, "Overview")
            if overview_button is not None:
                try:
                    overview_button.click()
                except StaleElementReferenceException:
                    logging.info("StaleElementReferenceException")
            
            location_name = element.get_attribute("aria-label")

        print("location_name2:", location_name2)
    
    return location_name

def find_target_category(browser):
    while True:
        try:
            # Find the category name e.g. "Japanese reaurant" using the class in <button class="DkEaL " jsaction="pane.rating.category">Japanese restaurant</button> ...
            category_name = browser.find_element(By.CLASS_NAME, 'DkEaL').text
            # Print the category name
            print("Category:", category_name)
            break
        except NoSuchElementException:
            # click the first button
            # find buttons
            tab_list = browser.find_element(By.CLASS_NAME, 'RWPxGd')
            buttons = tab_list.find_elements(By.TAG_NAME, 'button')
            buttons[0].click()
            logging.exception("NoSuchElementException")
            if category_name == "":
                category_name = "NoSuchElementException"
        except StaleElementReferenceException:
            logging.exception("StaleElementReferenceException")
            if category_name == "":
                category_name = "StaleElementReferenceException"
        except TimeoutException:
            # click the first button
            # find buttons
            tab_list = browser.find_element(By.CLASS_NAME, 'RWPxGd')
            buttons = tab_list.find_elements(By.TAG_NAME, 'button')
            buttons[0].click()
            logging.exception("TimeoutException")
            if category_name == "":
                category_name = "TimeoutException"

    return category_name

def is_sponsored(browser):
    sponsored_label = ""
    # check if element with the class "kpih0e uvopNe" exists
    try:
        # find element with class zvLtDc
        sponsored_parent = browser.find_element(By.CLASS_NAME, 'lMbq3e')
        # check if element with class "kpih0e uvopNe" exists
        sponsored_label_element = sponsored_parent.find_element(By.CLASS_NAME, 'kpih0e.uvopNe')
        sponsored_place = sponsored_parent.find_element(By.CLASS_NAME, 'DUwDvf').text
        print("sponsored_place:", sponsored_place)
        sponsored_label = "Yes"
    except NoSuchElementException:
        logging.info("NoSuchElementException - Target is not sponsored")
        if sponsored_label == "":
            sponsored_label = "No"
    except StaleElementReferenceException:
        logging.exception("StaleElementReferenceException")
        if sponsored_label == "":
            sponsored_label = "StaleElementReferenceException"
    return sponsored_label

def get_opening_times(browser):
    # Check if Opening Times is present
    opening_times = {}
    try:
        # Find the element with class "OqCZI fontBodyMedium WVXvdc"
        opening_times_parent = browser.find_element(By.CLASS_NAME, 'OqCZI.fontBodyMedium.WVXvdc')
        # find element with class "t39EBf GUrTXd" and extract the aria-label
        opening_times_string = opening_times_parent.find_element(By.CLASS_NAME, 't39EBf.GUrTXd').get_attribute('aria-label').replace('\u202f', ' ')
        # split the string into a list
        opening_times_list = opening_times_string.split("; ")
        # convert the list into a dictionary with the day of the week as the key
        opening_times = {}
        for opening_time in opening_times_list:
            opening_times[opening_time.split(",")[0]] = []
            opening_time = opening_time.replace("Closed", "Closed to Closed")
            opening_time = opening_time.replace("Open 24 hours", "12 am to 12 am")
            for opening_time_index in range(len(opening_time.split(", "))-1):
                # create a dictionary with opening and closing time as key
                open_and_close_timing = {}
                open_and_close_timing["open"] = opening_time.split(", ")[1].split(" to ")[0]
                open_and_close_timing["close"] = opening_time.split(", ")[1].split(" to ")[1]
                opening_times[opening_time.split(",")[0]].append(open_and_close_timing)
        # Print the opening times
        print("Opening Times:", opening_times)
    except NoSuchElementException:
        logging.info("NoSuchElementException - Target has no opening times")
    except StaleElementReferenceException:
        logging.exception("StaleElementReferenceException")
    
    return opening_times

def get_popular_times(browser):
    popular_times = {}
    # Check if popular times g2BVhd eoFzo  is present 
    try:
        # Find the element with class "g2BVhd eoFzo" using wait
        WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'C7xf8b')))
        all_popular_times = browser.find_elements(By.CLASS_NAME, 'g2BVhd')
        if len(all_popular_times) != 7 and len(all_popular_times) != 0:
            raise NoSuchElementException
        # get day of the week e.g. "Monday"
        day_of_week = datetime.today().strftime('%A')

        for day_popular_time in all_popular_times:
            busy_elements = day_popular_time.find_elements(By.CSS_SELECTOR, '.dpoVLd[aria-label]')

            day_popular_times = {}
            for busy_element in busy_elements:
                # Extract the aria-label value
                busy_time = busy_element.get_attribute('aria-label').replace('\u202f', ' ')
                if "Currently" in busy_time:
                    percentage_busy = busy_time.split("%")[-1].split(" ")[-1]
                    # find the current hour e.g. current time is 6:20 pm it becomes "6 pm"
                    current_hour = datetime.now().strftime('%I %p')
                    day_popular_times[current_hour] = percentage_busy+"%"
                else:
                    percentage_busy = busy_time.split("%")[0]
                    time_hour = busy_time.split("at ")[-1].replace(".", "")
                    # add to the dictionary with the time as the key
                    day_popular_times[time_hour] = percentage_busy+"%"
            # add to the dictionary with the day of the week as the key
            popular_times[day_of_week] = day_popular_times
            # get the next day of the week after the current day_of_week
            day_of_week = get_next_day(day_of_week)

        # Print the popular times
        print("Popular Times:", popular_times)
    except NoSuchElementException:
        logging.info("NoSuchElementException - Target has no popular times")
    except TimeoutException:
        logging.info("TimeoutException - Target has no popular times")
    
    return popular_times

def get_star_rating_and_number_of_reviews(browser):
    star_rating = "NAN"
    number_of_reviews = 0
    try:
        # Find the star rating element within the main content div
        review_main_content_div = browser.find_element(By.CSS_SELECTOR, '.F7nice')

        # Extract the text content of the span containing the star rating
        star_rating = review_main_content_div.find_element(By.TAG_NAME, 'span').text

        # Print the star rating
        print("star_rating:", star_rating)

        try:

            # Extract the text content of the span containing the reviews count
            number_of_reviews = review_main_content_div.find_element(By.CSS_SELECTOR, 'span[aria-label*="reviews"]').text

            # remove the brackets
            number_of_reviews = number_of_reviews.replace("(", "").replace(")", "").replace(",", "")
            
            # Print the reviews count
            print("Number of Reviews:", number_of_reviews)
        except NoSuchElementException:
            # Extract the text content of the span containing the reviews count
            number_of_reviews = review_main_content_div.find_element(By.CSS_SELECTOR, 'span[aria-label*="1 review"]').text

            # remove the brackets
            number_of_reviews = number_of_reviews.replace("(", "").replace(")", "").replace(",", "")
            
            # Print the reviews count
            print("Number of Reviews:", number_of_reviews)
    except NoSuchElementException:
        logging.info("NoSuchElementException - Target has no star rating")
    except StaleElementReferenceException:
        logging.exception("StaleElementReferenceException")

    return star_rating, number_of_reviews

def get_price_rating(browser):
    price_rating = ""
    try:
        # Find the element with class "mgr77e" - pricing
        price_element = browser.find_element(By.CLASS_NAME, 'mgr77e')

        # Find the nested span element containing the aria-label
        nested_span_element = price_element.find_element(By.XPATH, './/span[@aria-label]')

        # Extract the aria-label value
        price_rating = nested_span_element.get_attribute('aria-label').split(":")[-1]

        # Print the price label
        print("Price Label:", price_rating)

    except NoSuchElementException:
        print("Target has no price label")
        if price_rating == "":
            price_rating = "NAN"
    except StaleElementReferenceException:
        logging.exception("StaleElementReferenceException")
        if price_rating == "":
            price_rating = "StaleElementReferenceException"
    except TimeoutException:
        logging.exception("TimeoutException")
        if price_rating == "":
            price_rating = "TimeoutException"

    return price_rating

def get_address_and_metadata_list(browser):
    metadata_list = []
    address = ""
    try:
        # find the text of all the divs with class "Io6YTe fontBodyMedium kR99db "
        list_of_divs = browser.find_elements(By.CSS_SELECTOR, '.Io6YTe.fontBodyMedium.kR99db')
        for i, div in enumerate(list_of_divs):
            if i == 0:
                # write to address
                address = div.text
                print("address:", address)
            else:
                print("metadata " + str(i + 1), ": " + str(div.text))
                metadata_list.append(div.text)
    except NoSuchElementException:
        print("NoSuchElementException")
        print("Target has no metadata")
        metadata_list = ["NoSuchElementException"]
    except StaleElementReferenceException:
        print("StaleElementReferenceException")
        print("Target has no metadata")
        metadata_list = ["StaleElementReferenceException"]
       
    return address, metadata_list

def select_review_tab(browser):
    # make sure there is a Review tab
    initial_time = datetime.now()
    while True:
        found_reviews_tab = False
        # Locate the tab list
        tab_list = browser.find_element(By.CLASS_NAME, 'RWPxGd')
        buttons = tab_list.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            if button.find_element(By.CLASS_NAME, 'Gpq6kf.fontTitleSmall').text == "Reviews":
                found_reviews_tab = True
                review_button = button
                break
        # if more than 5 seconds have passed, refresh the page
        if (datetime.now() - initial_time).seconds > 5:
            browser.refresh()
            initial_time = datetime.now()
        if found_reviews_tab:
            break
    while True:
        # Click on the Second tab which is the "Reviews" tab
        review_button.click()
        # Locate the button element
        button = browser.find_element(By.CLASS_NAME, 'hh2c6.G7m0Af')
        # Check if the button is selected
        data_tab_index= button.get_attribute('data-tab-index')
        if data_tab_index == "1":
            print("Reviews tab is selected")
            break

def get_indv_star_rating(browser):
    indv_star_rating = {}
    while True:
        try:
            # Extract the number of reviews for each star level
            reviews_elements = browser.find_elements(By.CLASS_NAME, 'BHOKXe')

            for review_element in reviews_elements:
                star_level = review_element.find_element(By.CLASS_NAME, 'yxmtmf').text
                reviews_count = review_element.get_attribute('aria-label').split(",")[1].split()[0]
                print(f"{star_level} - {reviews_count}")
                indv_star_rating[int(star_level)] = int(reviews_count)
            break
        except StaleElementReferenceException:
            logging.exception("StaleElementReferenceException")
    
    return indv_star_rating

def get_list_of_tags(browser):
    all_tags = {}
    # Wait for the element with class "m6QErb tLjsW" to be present
    tags_elements_parent = WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.CLASS_NAME, 'm6QErb.tLjsW')))

    # Find all tags and review counts under the element
    tags_elements = browser.find_elements(By.XPATH, '//div[@class="m6QErb tLjsW "]//div[@class="KNfEk "]')

    # Extract and print the tag and review count for each element
    for tag_element in tags_elements:
        tag = tag_element.find_element(By.CLASS_NAME, 'fontBodyMedium').text
        tag_count = tag_element.find_element(By.CLASS_NAME, 'bC3Nkc').text
        all_tags[tag] = int(tag_count)
    print(all_tags)
    return all_tags

def get_reviewer_info(current_review):
    # Get local guide status class RfnDt
    try:
        reviewer_status = current_review.find_element(By.CLASS_NAME, 'RfnDt').text
        reviewer_status_list = reviewer_status.split(" · ")
        if len(reviewer_status_list) == 3:
            reviewer_local_guide_status = True
            reviewer_total_reviews = reviewer_status_list[1]
            reviewer_total_photos = reviewer_status_list[2]
        elif len(reviewer_status_list) == 2:
            reviewer_local_guide_status = False
            reviewer_total_reviews = reviewer_status_list[0]
            reviewer_total_photos = reviewer_status_list[1]
        elif len(reviewer_status_list) == 1:
            reviewer_local_guide_status = False
            reviewer_total_reviews = reviewer_status_list[0]
            reviewer_total_photos = "NAN"
        else:
            raise NoSuchElementException
        reviewer_total_reviews = reviewer_total_reviews.split(" ")[0].replace(",", "")
        reviewer_total_photos = reviewer_total_photos.split(" ")[0].replace(",", "")
    except NoSuchElementException:
        logging.info("NoSuchElementException - No reviewer status")
        reviewer_local_guide_status = False
        reviewer_total_reviews = "NAN"
        reviewer_total_photos = "NAN"
    return reviewer_local_guide_status, reviewer_total_reviews, reviewer_total_photos

def get_reviewer_star_rating(current_review):
    # Get star rating in aria-label of kvMYJc class in current review
    reviewer_star_rating = current_review.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute('aria-label')
    reviewer_star_rating = reviewer_star_rating.split(" star")[0]
    print("reviewer_star_rating:", reviewer_star_rating)

    return reviewer_star_rating

def get_review_date(current_review):
    relative_time = current_review.find_element(By.CLASS_NAME, 'rsqaWe').text
    # find today's date and subtract the relative_time
    review_date = convert_relative_time(relative_time)
    print("review_date:", review_date)

    return review_date

def expand_review(current_review):
    while True:
        # Click the "more" button w8nwRe kyuRq to expand the review text if present
        try:
            more_button = current_review.find_element(By.CLASS_NAME, 'w8nwRe.kyuRq')
            more_button.click()
        except NoSuchElementException:
            logging.info("NoSuchElementException - No more button")
            break
        except StaleElementReferenceException:
            logging.info("StaleElementReferenceException - No more button")
            break

def get_review_text(current_review):
    # Get review text in class wiI7pd
    try:
        review_text = current_review.find_element(By.CLASS_NAME, 'wiI7pd').text
        print("review_text:", review_text)
    except NoSuchElementException:
        logging.info("NoSuchElementException - No review text")
        review_text = "NAN"

    return review_text

def get_detail_list(current_review):
    detail_list = []
    try:
        # Find the review element using Selenium with jslog="127691" attribute
        review_text_element = current_review.find_element(By.XPATH, './/div[@jslog="127691"]')
        # Find all the metadata elements PBK6be
        metadata_elements = review_text_element.find_elements(By.CLASS_NAME, 'PBK6be')
        # Extract and print metadata details
        for metadata_element in metadata_elements:
            # Extract detail title
            detail_title_element = metadata_element.find_element(By.CLASS_NAME, 'RfDO5c')
            detail_title = detail_title_element.text.strip()

            try:
                # Extract detail content
                detail_content_elements = metadata_element.find_elements(By.XPATH, './/div')
                detail_content = detail_content_elements[1].text.strip()
            except IndexError:
                detail_content = ""
            if detail_content == "":
                detail_list.append(detail_title)
            else:
                detail_list.append(f"{detail_title}: {detail_content}")
            print(f"{detail_title}: {detail_content}")
    except NoSuchElementException:
        logging.info("NoSuchElementException - No Review Metadata")

    return detail_list


def scrape_all_reviews(browser, csv_writer_reviews, number_of_reviews, href):
    # Scrape all reviews
    review_index = 0
    
    # Locate the div element
    div_element = browser.find_element(By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf')

    # Scroll down within the div using JavaScript
    # find element m6QErb tLjsW 
    tags_element_scroll = browser.find_element(By.CLASS_NAME, 'm6QErb.tLjsW')
    browser.execute_script("arguments[0].scrollIntoView();", tags_element_scroll)

    # wait for the element with class "jftiEf fontBodyMedium", the review element class, to be present
    try:
        review_present = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'jftiEf.fontBodyMedium')))
    except TimeoutException:
        # TO FIX 
        logging.exception("TimeoutException")

    
    visible_reviews = browser.find_elements(By.CLASS_NAME, 'jftiEf.fontBodyMedium')
    while True:
        current_review = visible_reviews[review_index]
        # # if less than 5 elements left, scroll and load more elements
        # if len(reviews) - review_index < 5:
        # Get href of current place
        href_of_place = href

        # Get review ID
        review_id = current_review.get_attribute('data-review-id')

        # Get relavancy ranking
        relavancy_ranking = review_index + 1

        # Get reviewer href which is the data-review-id of WEBjve class in the current review
        reviewer_href = current_review.find_element(By.CLASS_NAME, 'WEBjve').get_attribute('data-href')

        # Get reviewer name which is in the aria-label of the current review
        reviewer_name = current_review.get_attribute('aria-label')
        print("reviewer_name:", reviewer_name)

        # Get reviewer local guide status, total reviews and total photos
        reviewer_local_guide_status, reviewer_total_reviews, reviewer_total_photos = get_reviewer_info(current_review)

        # Get reviewer star rating
        reviewer_star_rating = get_reviewer_star_rating(current_review)

        # Get date of review in class rsqaWe
        review_date = get_review_date(current_review)

        # Expand review text, click the "More" button
        expand_review(current_review)
        
        # Get review text
        review_text = get_review_text(current_review)

        # Get detail list
        detail_list = get_detail_list(current_review)

        # Write to reviews CSV file
        with file_write_lock_reviews:
            csv_writer_reviews.writerow([href_of_place, review_id, relavancy_ranking, reviewer_href, reviewer_name, reviewer_local_guide_status, reviewer_total_reviews, reviewer_total_photos, reviewer_star_rating, review_date, review_text, detail_list])

        # scroll until there's more reviews below the current review
        # set max timing to wait for the next review to load to 5 seconds
        # start timing
        start_time = datetime.now()
        time_out_error = False
        while True:
            if (datetime.now() - start_time).seconds > 5:
                time_out_error = True
                break
            # scroll to last element
            presentation_elements = browser.find_elements(By.CLASS_NAME, 'qCHGyb')
            try:
                browser.execute_script("arguments[0].scrollIntoView();", presentation_elements[-1])
            except StaleElementReferenceException:
                logging.info("StaleElementReferenceException - Cannot scroll to last element")

            # more elements are loaded after scrolling, add the new elements to the list, but only if they are not already in the list
            new_reviews = browser.find_elements(By.CLASS_NAME, 'jftiEf.fontBodyMedium')
            for new_review in new_reviews:
                if new_review not in visible_reviews:
                    visible_reviews.append(new_review)
            if len(visible_reviews) > review_index + 1 or review_index == int(number_of_reviews)-1:
                break
        
        if review_index == int(number_of_reviews)-1: # if reached the last review
            break
        if review_index == constants.MAX_REVIEWS_PER_PLACE-1:
            break
        if time_out_error:
            break

        # increment review index
        review_index += 1

def get_tab_button(browser, tab_name):
    about_button = None
    while True:
        try:
            tab_list = browser.find_element(By.CLASS_NAME, 'RWPxGd')
            buttons = tab_list.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                if button.find_element(By.CLASS_NAME, 'Gpq6kf.fontTitleSmall').text == tab_name:
                    about_button = button
            break
        except NoSuchElementException:
            logging.info("NoSuchElementException - No " + tab_name + " tab")
            break
        except StaleElementReferenceException:
            logging.info("StaleElementReferenceException - No " + tab_name + " tab")
    return about_button

def get_about_combined(browser, about_button):
    about_combined = []
    start_time = datetime.now()
    while True:
        try:
            if (datetime.now() - start_time).seconds > 5:
                break
            about_button.click()
            # wait till element present
            # WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.CLASS_NAME, 'iP2t7d.fontBodyMedium')))
            element = browser.find_element(By.CLASS_NAME, 'iP2t7d.fontBodyMedium')
            break
        except NoSuchElementException:
            logging.info("NoSuchElementException - No About tab elements")
            return about_combined
        except ElementClickInterceptedException:
            logging.exception("ElementClickInterceptedException - No About tab elements")
            return about_combined
        except TimeoutException:
            logging.exception("TimeoutException - No About tab elements")
            return about_combined

    while True:
        try:
            about_elements = browser.find_elements(By.XPATH, '//ul[@class="ZQ6we"]/li/span')
            about_options = [option.text for option in about_elements]
            about_combined = about_options
            break
        except StaleElementReferenceException:
            logging.exception("StaleElementReferenceException")
            continue
    
    return about_combined


def find_targets_in_area(url, area, subzone, browser, csv_writer, csv_writer_reviews):
    url = url  + "+in+" + subzone + ",+" + area + ",+Singapore"
    browser.get(url)
    print(url)
    # get all elements with class "hfpxzc"
    elements = browser.find_elements(By.CLASS_NAME, "hfpxzc")
    print(elements[0].get_attribute("href"))

    noMoreResults = False
    element_index = 0


    # Loop through list of restaurants
    while True:
        # reset the timer to 10 mins everytime a new element is clicked
        # timer.reset(600)
        # if lesser than 5 elements left, scroll and load more elements
        # if len(elements) - element_index < 10:
        #     browser.execute_script("arguments[0].scrollIntoView();", elements[-1])

        # current_element = get_current_element(browser, elements, element_index)
        new_elements = browser.find_elements(By.CLASS_NAME, "hfpxzc")
        for new_element in new_elements:
            if new_element not in elements:
                elements.append(new_element)
        
        # get the current element
        current_element = new_elements[element_index]

        # href of current element
        href = current_element.get_attribute("href")

        # Check if the "You've reached the end of the list." message is present
        end_of_list_element = browser.find_elements(By.CLASS_NAME, 'HlvSq')
        if end_of_list_element:
            print("You've scrolled to the end of the list.")
            noMoreResults = True
        
        element_index += 1
        
        if noMoreResults and element_index == len(elements):
            print("Finished scraping all elements")
            break

        # get the seo rating of the current element
        seo_rating = element_index

        
        # print(new_elements[0].get_attribute("href"))

        

        # if href is already present in csv
        if href in href_list:
            print("href already present in csv")
            continue
        else:
            with href_list_lock:
                href_list.append(href)
        print("current element:", element_index)
        browser.execute_script("arguments[0].scrollIntoView();", current_element)
        current_element.click()

        # wait for the restaurant clicked to popup and load
        location_name = wait_for_target_popup(current_element, browser)
        
        category_name = find_target_category(browser)

        for blacklisted_word in constants.CATEGORY_BLACKLISTED_WORDS:
            if blacklisted_word in category_name.lower():
                print("Blacklisted word found in category name:", blacklisted_word)
                print("Skipping this element")
                continue

        sponsored_label = is_sponsored(browser)

        opening_times = get_opening_times(browser)

        popular_times = get_popular_times(browser)

        star_rating, number_of_reviews = get_star_rating_and_number_of_reviews(browser)
        
        price_rating = get_price_rating(browser)
            
        address, metadata_list = get_address_and_metadata_list(browser)

        # Initialize indv_star_rating, all_tags, about_combined
        indv_star_rating = {}
        all_tags = {}
        about_combined = []

        # if there is at least 1 review there is a review tab
        if number_of_reviews != 0:
            select_review_tab(browser)

            # Get individual star rating
            indv_star_rating = get_indv_star_rating(browser)
            
            # List of dishes
            all_tags = get_list_of_tags(browser)
                
            # Long function
            scrape_all_reviews(browser, csv_writer_reviews, number_of_reviews, href)


        # Find the about tab
        about_button = get_tab_button(browser, "About")
        if about_button is not None:
            about_combined = get_about_combined(browser, about_button)
            
        # Write to main CSV file
        with file_write_lock:
            csv_writer.writerow([href, area, subzone, location_name, seo_rating, sponsored_label, opening_times, popular_times, star_rating, indv_star_rating, number_of_reviews, category_name, price_rating, address, metadata_list, all_tags, about_combined])

def refresh_browser(browser):
    browser.refresh()
            
def scrape_area(area, subzone, csv_writer, csv_writer_reviews):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    if constants.RUN_HEADLESS:
        chrome_options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=chrome_options)

    # Navigate to the Chrome settings page
    browser.get('chrome://settings/')
    # Execute JavaScript code to set the default zoom level to 60%
    browser.execute_script('chrome.settingsPrivate.setDefaultZoom(0.6);')

    # set 10 mins timer to refresh browser
    # timer = ResettableTimer(600, refresh_browser, args=(browser,))
    # timer.start()

    find_targets_in_area(constants.URL + constants.TARGET, area, subzone, browser, csv_writer, csv_writer_reviews)

    # delete the timer
    # timer.cancel()

    browser.quit()

def main():
    # Create a CSV file and write the header
    csv_file = open('scraped_data_' + constants.TARGET.replace("+", "_") + '.csv', 'w', encoding='utf-8-sig', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['href', 'Planning Area', 'Subzone', 'Name', 'Search Engine Rating', 'Sponsored', 'Opening Hours', 'Popular Times', 'Average Star Rating', 'Individual Star Rating', 'Reviews', 'Category', 'Price Rating', 'Address', 'Metadata', 'Tags', 'About'])

    csv_file_reviews = open('scraped_data_reviews_' + constants.TARGET.replace("+", "_") + '.csv', 'w', encoding='utf-8-sig', newline='')
    csv_writer_reviews = csv.writer(csv_file_reviews)
    csv_writer_reviews.writerow(['href of Place', 'Review ID', 'Relavancy Ranking', 'Reviewer href', 'Reviewer Name', 'Local Guide', 'Total Reviews', 'Total Photos', 'Star Rating', 'Date', 'Review', 'Metadata', ])

    list_of_subzones = []
    list_of_areas = []
    list_of_places = constants.LIST_OF_PLACES
    # list_of_places is a dict, key is the region, value is another dict with key as the planning area and value as the list of sub zones
    # loop through each region key
    for region in list_of_places:
        # loop through each planning area
        for planning_area in list_of_places[region]:
            # loop through each sub zone
            for sub_zone in list_of_places[region][planning_area]:
                # append the sub zone to the planning area
                list_of_areas.append(planning_area)
                list_of_subzones.append(sub_zone)


    # zip
    for area, subzone in zip(list_of_areas, list_of_subzones):
        # convert / to %2F
        area = area.replace("/", "%2F")
        area = area.replace(" ", "+")
        subzone = subzone.replace("/", "%2F")
        subzone = subzone.replace(" ", "+")

    if constants.RUN_MULTITHREADED:
        # run Multi Threaded
        with ThreadPoolExecutor(max_workers=constants.NUM_THREADS) as executor:
            for area, subzone in zip(list_of_areas, list_of_subzones):
                executor.submit(scrape_area, area, subzone, csv_writer, csv_writer_reviews)
    else:
        # run Single Threaded
        for area, subzone in zip(list_of_areas, list_of_subzones):
            scrape_area(area, subzone, csv_writer, csv_writer_reviews)

    # # Close the CSV file
    # csv_file.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()