# import bs4 as bs
import urllib.request
import sys
import getpass

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time
from datetime import date, datetime

import pandas as pd
import numpy as np

# ### Functions for visibility checks and clicking buttons
# 
# The below contains functions to check if the various LinkedIn logos and buttons are visible on the window and functions to click on such logos/button.

# In[3]:


# check if dp is displayed upon login
# waits for a maximum of 10 seconds for the dp to be displayed
def login_dp_visible(driver, time_limit=10):
    try:
        login_dp = WebDriverWait(driver, time_limit).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@data-control-name='identity_profile_photo']")
            )
        )
        return login_dp
    
    except:
        return False
    
# check if profile pic is visible on profile page
def profile_dp_visible(driver, time_limit=10):
    try:
        profile_dp = WebDriverWait(driver, time_limit).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='pv-top-card--photo text-align-left']")
            )
        )
        return profile_dp
    
    except TimeoutException as error:
        return False

# check if profile pic of company page is visible
def company_dp_visible(driver, time_limit=10):
    try:
        company_dp = WebDriverWait(driver, time_limit).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='org-top-card-primary-content__logo-container']")
            )
        )
        return company_dp
    
    except TimeoutException as error:
        return False
    
# check if messaging window is visible
def msg_window_visible(driver, time_limit=10):
    try:
        msg_window = WebDriverWait(driver, time_limit).until(
            EC.presence_of_element_located(
                (By.XPATH, "//header[@class='msg-overlay-bubble-header']")
            )
        )
        return msg_window
    
    except TimeoutException as error:
        return False
    
# check if next button is visible
def next_button_visible(driver, time_limit=10):
    try:
        next_button = WebDriverWait(driver, time_limit).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='Next']")
            )
        )
        
        if 'disabled' in next_button.get_attribute("class"):
            return False
        
        return next_button
    
    except TimeoutException as error:
        return False
    
def results_page_visible(driver, time_limit=2):
    try:
        results_page = WebDriverWait(driver, time_limit).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='search-results ember-view']")
            )
        )
        return True
    
    except TimeoutException:
        return False
    
def results_exists(driver, time_limit=10):
    try:
        WebDriverWait(driver, time_limit).until(
            EC.presence_of_element_located(
                (By.XPATH, 
                 "//div[@class='search-results ember-view']"
                 + "//li[@class='search-result search-result__occluded-item ember-view']")
            )
        )
        
        return True
    
    except NoSuchElementException:
        return False
    
# retract the messaging button
def retract_msg_window(driver):
    msg_window = msg_window_visible(driver)
    
    if msg_window:
        name = msg_window.get_attribute("data-control-name")
        if name == "overlay.minimize_connection_list_bar":
            msg_window.click()
        else:
            print("Messaging window is retracted")
    else:
        print("Messaging window is not visible")

def more_exp_exists(driver, time_limit=3):
    try:
        more_exp_button = WebDriverWait(driver, time_limit).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state'"
                 + " and @aria-expanded='false']")
            )
        )
        return more_exp_button
    
    except TimeoutException as error:
        return False
    
def more_skills_exists(driver, time_limit=3):
    try:
        more_skills_button = WebDriverWait(driver, time_limit).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@aria-controls='skill-categories-expanded'"
                 + " and @aria-expanded='false']"
                 + "/span[normalize-space()='Show more']")
            )
        )
        return more_skills_button
    
    except TimeoutException as error:
        return False
    
def click_more_skills(driver, time_limit=1):
    
    xpath = "//button[@aria-controls='skill-categories-expanded'" + " and @aria-expanded='false']" + "/span[normalize-space()='Show more']"
    
    scroll_page(driver)
    
    if more_skills_exists(driver):
        # scroll to the show more button
        driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            WebDriverWait(driver, time_limit).until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpath)
                )
            )
        )
        
        # click the show more button
        driver.execute_script(
            "arguments[0].click();", 
            WebDriverWait(driver, time_limit).until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpath)
                )
            )
        )
        
def click_more_exp(driver, time_limit=1):
    
    xpath = "//button[@class='pv-profile-section__see-more-inline pv-profile"         + "-section__text-truncate-toggle link link-without-hover-state'"         + " and @aria-expanded='false']"

    scroll_page(driver)
    
    if more_exp_exists(driver):
        # scroll to the show more button
        driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            WebDriverWait(driver, time_limit).until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpath)
                )
            )
        )
        
        # click the show more button
        driver.execute_script(
            "arguments[0].click();", 
            WebDriverWait(driver, time_limit).until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpath)
                )
            )
        )
        
def click_next_button(driver, time_limit=2):    
    if next_button_visible(driver):
        try:
            # click the Next button
            driver.execute_script(
                "arguments[0].click();", 
                WebDriverWait(driver, time_limit).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Next']")
                    )
                )
            )
        except:
            print("Next button not displayed/clickable.")


# ### Miscellaneous LinkedIn functions
# Any functions that aren't for scraping, clicking or checking for visibility.

# In[4]:


# transform linkedin date format in string to datetime objects:
def transform_date_range(date_str, degree=False):
    start_date = np.nan
    end_date = np.nan
    
    # no dates available
    if date_str == '':
        return start_date, end_date
    
    # date range is only within 1 month
    elif len(date_str.split('–')) == 1:
        start = date_str.split('–')[0].strip()
        end = start
        if len(start.split(" ")) == 1:
            start_date = datetime.strptime(start, '%Y')
            end_date = start_date
        elif len(start.split(" ")) == 2:
            start_date = datetime.strptime("1 " + start, '%d %b %Y')
            end_date = datetime.strptime("28 " + start, '%b %Y')
        
        return start_date, end_date
    
    # date range is more than 1 month
    start, end = date_str.split('–')
    start = start.strip()
    end = end.strip()
    
    if end.lower() == 'present':
        end_date = 'present'
    elif len(end.split(" ")) == 1 and degree:
        end_date = datetime.strptime("Jun " + end, '%b %Y')
    elif len(end.split(" ")) == 1 and not degree:
        end_date = datetime.strptime(end, '%Y')
    elif len(end.split(" ")) == 2:
        end_date = datetime.strptime(end, '%b %Y')
    else:
        print("End date is not in correct format")
        
    if len(start.split(" ")) == 1 and degree:
        start_date = datetime.strptime("Aug " + start, '%b %Y')
    elif len(start.split(" ")) == 1 and not degree:
        start_date = datetime.strptime(start, '%Y')
    elif len(start.split(" ")) == 2:
        start_date = datetime.strptime(start, '%b %Y')
    else:
        print("Start date is not in correct format")
        
    return start_date, end_date
        
# scroll through the whole page
def scroll_page(driver):
    for i in range(5):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight"
            + " * " + str(i+1) + "/5);")

# expand Experiences and Skills section for the current profile page
def expand_page(driver):
    try:
        # expand the experience section
        click_more_exp(driver)
        
        # expand the skills section
        click_more_skills(driver)
    except:
        pass

# get all profile links on a page
def get_page_links(links_dict):
    
    # scroll through the whole page
    scroll_page(driver)
    
    # get all profile links
    elements = driver.find_elements_by_xpath(
        "//a[@data-control-name='search_srp_result']"
    )
    
    # add all profile links to a dictionary
    for element in elements:
        link = element.get_attribute("href")
        
        # check if the link is a profile link
        if link[:28] != 'https://www.linkedin.com/in/':
            continue
            
        # check if the link is already in the dictionary
        if link not in links_dict:
            links_dict[link] = 1
    
    return links_dict

def get_page_links_all(driver, url, pages='All'):
    links_dict = {}
    page = 0
    page_limit = 0
    
    if type(pages) == str and pages.lower() == 'all':
        page_limit = float('inf')
        
    elif type(pages) == int and pages > 0:
        page_limit = pages
    else:
        print("Enter a positive number for 'pages'")
        return []
    
    # visit url
    driver.get(url)
    
    scroll_page(driver)
    
    # retract the messaging chat if applicable
    retract_msg_window(driver)
    
    # get all the profile links on page 1
    if results_page_visible(driver) and results_exists(driver):
        links_dict = get_page_links(driver, links_dict)
        page = 1
        
        if page >= page_limit:
            print("Links scraped:", len(list(links_dict.keys())))
        else:
            print("Links scraped: " + str( len(list(links_dict.keys())) ) + " "*20, "\r", end="")
        
    while(next_button_visible(driver) and page < page_limit):
        print("Links scraped: " + str( len(list(links_dict.keys())) ) + " "*20, "\r", end="")
        click_next_button(driver)
        
        # try to avoid this, find a way to check if a page is loaded
        time.sleep(5)
        
        if results_page_visible(driver) and results_exists(driver):
            scroll_page(driver)
            time.sleep(1)
            
            # get all profile links on page
            links_dict = get_page_links(driver, links_dict)
            page += 1
        else:
            print("No more results found")
            print("Links scraped:", len(list(links_dict.keys())))
            return list(links_dict.keys())
    
    if (page_limit != float('inf')) and (page < page_limit):
        print("Only " + str(page) + " page(s) available and scraped.")
        print("Links scraped:", len(list(links_dict.keys())))
    else: 
        print("All profiles scraped")
        print("Links scraped:", len(list(links_dict.keys())))
        
    return list(links_dict.keys())

def login(driver):
    try:
        # scroll to the login field
        driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            WebDriverWait(driver, 0.5).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "login__form")
                )
            )
        )
    except TimeoutException:
        # Doing login on LinkedIn
        driver.get('https://www.linkedin.com/uas/login?');

    if login_dp_visible(driver, time_limit=0.5):
        print("You are already logged in")
        return 

    email = input("Please enter your Linkedin username: ")
    password = getpass.getpass("Please enter your Linkedin password: ")

    if type(email) == str and type(password) == str:
        # enter username
        email_box = driver.find_element_by_id('username')
        email_box.send_keys(email)

        # enter password
        pass_box = driver.find_element_by_id('password')
        pass_box.send_keys(password)

        # click submit button
        submit_button = driver.find_element_by_xpath("//button[@aria-label='Sign in']")
        submit_button.click()

        time.sleep(1)
                
        try:
            username_error_msg = driver.find_element_by_id("error-for-username").text
            password_error_msg = driver.find_element_by_id("error-for-password").text

            if username_error_msg != '':
                print(username_error_msg)
            if password_error_msg != '':
                print(password_error_msg)
        except NoSuchElementException:
            # check if the display pic is visible upon login
            if login_dp_visible(driver):
                # retract the messaging window
                retract_msg_window(driver)
        
def is_NUS_Bachelor(df):
    for i in range(df.shape[0]):
        if type(df.loc[i, "School"]) != str or type(df.loc[i, "Degree type"]) != str:
            continue
            
        school_name = df.loc[i, "School"].lower()
        if "national university of singapore" in school_name:
            deg_name = df.loc[i, "Degree type"].lower()
            if "bachelor" in deg_name or "hon" in deg_name:
                return df.loc[[i]].reset_index(drop=True)
        
    return pd.DataFrame(columns = df.columns)

# given a pandas dataframe with variables "Career start date", "Career end date",
# it returns the row of the dataframe corresponding to the first job
# assumptions: the dates are all in datetime format and the dataframe is in reverse chronological order
def get_first_job(df, degree_end_date):
    try:
        for i in range(df.shape[0]):
            if df.loc[i, "Career start date"] >= degree_end_date:
                if i == df.shape[0]-1:
                    return df.iloc[[i]]
                elif df.loc[i+1, "Career start date"] >= degree_end_date:
                    continue
                elif df.loc[i+1, "Career start date"] < degree_end_date:
                    return df.iloc[[i]]
    except:
        return pd.DataFrame(columns = df.columns)
    
    return pd.DataFrame(columns = df.columns)


# ### Scraping functions

# In[5]:


def scrape_name_indiv(driver, profile_url, reload=True):
    df = pd.DataFrame(columns = ["Name"])
    
    if reload:
        # visit the profile url
        driver.get(profile_url)
        profile_dp_visible()
        expand_page()
    
    try:
        df.loc[0, 'Name'] = driver.find_element_by_xpath(
            "//ul[@class='pv-top-card--list inline-flex align-items-center']//li"
        ).text
    except:
        pass

    return df

# scrapes all the educational info of a profile specified by a profile url
# returns the info in a pandas dataframe
def scrape_edu_indiv(driver, profile_url, reload=True):
    # check if the link is a profile link
    if profile_url[:28] != 'https://www.linkedin.com/in/':
        print("The url is not from a Linkedin profile.")
        return pd.DataFrame()
    
    df = pd.DataFrame(columns = ['School', 'Degree type', 'Major', 'Degree start year', 'Degree end year',
                                 'Graduated', 'Activities and societies', 'Edu description'])
    education_x_path = "//section[@id='education-section']//ul/li"
    time_info = ''
    
    if reload:
        # visit the profile url
        driver.get(profile_url)
        profile_dp_visible()
        expand_page()
    
    # get education web elements
    schools = driver.find_elements_by_xpath(education_x_path + "//div[@class='pv-entity__degree-info']//h3")
    
    # store information of school
    for i in range(len(schools)):
        df.loc[i, 'School'] = driver.find_element_by_xpath(
            education_x_path 
            + "[" + str(i+1) + "]" 
            + "//div[@class='pv-entity__degree-info']"
            + "/h3"
        ).text
        
        try:
            df.loc[i, 'Degree type'] = driver.find_element_by_xpath(
                education_x_path 
                + "[" + str(i+1) + "]" 
                + "//div[@class='pv-entity__degree-info']"
                + "//p[@class='pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal']"
                + "/span[2]"
            ).text
        except:
            pass

        try:
            df.loc[i, 'Major'] = driver.find_element_by_xpath(
                education_x_path 
                + "[" + str(i+1) + "]" 
                + "//div[@class='pv-entity__degree-info']"
                + "//p[@class='pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal']"
                + "/span[2]"
            ).text

        except:
            pass

        try:
            time_info = driver.find_element_by_xpath(
                education_x_path 
                + "[" + str(i+1) + "]"
                + "//p[@class='pv-entity__dates t-14 t-black--light t-normal']"
                + "/span[2]"
            ).text
        except:
            time_info = ''

        df.loc[i, 'Degree start year'], df.loc[i, 'Degree end year'] = transform_date_range(time_info, degree=True)
        
        try:
            df.loc[i, 'Activities and societies'] = driver.find_element_by_xpath(
                education_x_path 
                + "[" + str(i+1) + "]"
                + "//p[@class='pv-entity__secondary-title t-14 t-black--light t-normal']"
                + "/span[2]"
            ).text
        except:
            pass
        
        try:
            df.loc[i, 'Edu description'] = driver.find_element_by_xpath(
                education_x_path 
                + "[" + str(i+1) + "]" 
                + "//div[@class='pv-entity__extra-details t-14 t-black--light ember-view']"
            ).text
        except:
            pass
        
        # check if this person has graduated from his/her educational institutes
        if type(df.loc[i, 'Degree end year']) == float and np.isnan(df.loc[i, 'Degree end year']):
            df.loc[i, 'Graduated'] = np.nan
        elif df.loc[i, 'Degree end year'] == 'present':
            if datetime.today() > datetime.strptime('2020', '%Y'):
                df.loc[i, 'Graduated'] = True
            else:
                df.loc[i, 'Graduated'] = False
        elif datetime.today() > df.loc[i, 'Degree end year']:
            df.loc[i, 'Graduated'] = True
        else:
            df.loc[i, 'Graduated'] = False
            
        if df.empty:
            print(
                driver.find_element_by_xpath("//ul[@class='pv-top-card--list inline-flex align-items-center']//li").text
                + " did not do Bachelor's in NUS"
            )
            return pd.DataFrame(columns = df.columns)
    
    return df

# scrapes all the experience info of a profile specified by a profile url
# returns the info in a pandas dataframe
def scrape_exp_indiv(driver, profile_url, reload=True, industries=True):
    '''
    parameters: 
        df, a one row dataframe containing details of a person
        profile_url: weblink to the person of interest
    returns:
        a dataframe with more information about the experiences of the person
    '''
    
    # check if the link is a profile link
    if profile_url[:28] != 'https://www.linkedin.com/in/':
        print("The url is not from a Linkedin profile.")
        return pd.DataFrame()
    
    experience_x_path = "//section[@id='experience-section']/ul/li"
    exp_df = pd.DataFrame(columns = ["Company", "Company url", "Industry", "Job position", 
                                     "Career start date", "Career end date", "Career description"])
    job_duration = []
    
    if reload:
        # visit the profile url
        driver.get(profile_url)
        profile_dp_visible()
        expand_page()
    
    experiences = driver.find_elements_by_xpath(experience_x_path)
    
    for i in range(len(experiences)):
        try:
            row = exp_df.shape[0]
            
            exp_df.loc[row, "Career start date"], exp_df.loc[row, "Career end date"] = transform_date_range(
                driver.find_element_by_xpath(
                    experience_x_path + "[" + str(i+1) + "]" 
                    + "//h4[@class='pv-entity__date-range t-14 t-black--light t-normal']/span[2]"
                ).text
            )
            
            # to get the Linkedin url of the company
            exp_df.loc[row, "Company url"] = driver.find_element_by_xpath(
                experience_x_path + "[" + str(i+1) + "]" 
                + "//a[@data-control-name='background_details_company']"
            ).get_attribute("href")

            # check if there are another jobs done under the same company
            sub_exp = driver.find_elements_by_xpath(
                experience_x_path + "[" + str(i+1) + "]" 
                + "//li[@class='pv-entity__position-group-role-item']"
            )
                        
            # if there is only 1 job position in the company
            if len(sub_exp) == 0:
                exp_df.loc[row, "Job position"] = driver.find_element_by_xpath(
                    experience_x_path + "[" + str(i+1) + "]"
                    + "//h3[@class='t-16 t-black t-bold']"
                ).text
                
                exp_df.loc[row, "Company"] = driver.find_element_by_xpath(
                    experience_x_path + "[" + str(i+1) + "]"
                    + "//p[@class='pv-entity__secondary-title t-14 t-black t-normal']"
                ).text
                
                exp_df.loc[row, "Career description"] = driver.find_element_by_xpath(
                    experience_x_path + "[" + str(i+1) + "]"
                    + "//div[@class='pv-entity__extra-details t-14 t-black--light ember-view']"
                ).text
                
            # if there is more than 1 job position in the company
            else:
                exp_df.loc[row, "Company"] = driver.find_element_by_xpath(
                    experience_x_path + "[" + str(i+1) + "]" 
                    + "//div[@class='pv-entity__company-details']"
                    + "//h3[@class='t-16 t-black t-bold']/span[2]"
                ).text
                
                exp_df.loc[row, "Job position"] = driver.find_element_by_xpath(
                    experience_x_path + "[" + str(i+1) + "]" 
                    + "//li" + "[" + str(1) + "]" 
                    + "[@class='pv-entity__position-group-role-item']"
                    + "//h3[@class='t-14 t-black t-bold']"
                    + "/span[2]"
                ).text
            
            for j in range(1, len(sub_exp)):
                try:
                    exp_df.loc[row+j, "Company"] = exp_df.loc[row, "Company"]
                    exp_df.loc[row+j, "Industry"] = exp_df.loc[row, "Industry"]
                    exp_df.loc[row+j, "Company url"] = exp_df.loc[row, "Company url"]
                    exp_df.loc[row+j, "Career start date"], exp_df.loc[row+j, "Career end date"] = transform_date_range(
                        driver.find_element_by_xpath(
                            experience_x_path + "[" + str(i+1) + "]" 
                            + "//li" + "[" + str(j+1) + "]" 
                            + "[@class='pv-entity__position-group-role-item']"
                            + "//h4[@class='pv-entity__date-range t-14 t-black--light t-normal']"
                            + "/span[2]"
                        ).text)
                    
                    exp_df.loc[row+j, "Job position"] = driver.find_element_by_xpath(
                        experience_x_path + "[" + str(i+1) + "]" 
                        + "//li" + "[" + str(j+1) + "]" 
                        + "[@class='pv-entity__position-group-role-item']"
                        + "//h3[@class='t-14 t-black t-bold']"
                        + "/span[2]"
                    ).text
                    
                    exp_df.loc[row+j, "Career description"] = driver.find_element_by_xpath(
                        experience_x_path + "[" + str(i+1) + "]"
                        + "//li" + "[" + str(j+1) + "]"
                        + "//div[@class='pv-entity__extra-details t-14 t-black--light ember-view']"
                    ).text
                except:
                    pass
        except:
            pass
    if industries:
        exp_df["Industry"] = scrape_industries(driver, exp_df["Company url"])["Industry"]
    
    return exp_df

def scrape_skills_indiv(driver, profile_url, reload=True):
    df = pd.DataFrame(columns = ["Skills"])
    
    if reload:
        # visit the profile url
        driver.get(profile_url)
        profile_dp_visible(driver)
        expand_page(driver)
    
    skills_list = []
    skills = driver.find_elements_by_xpath(
        "//span[@class='pv-skill-category-entity__name-text t-16 t-black t-bold']"
    )

    for skill in skills:
        if len(skill.text.strip()) != 0:
            skills_list.append(skill.text.strip())

    df.loc[0, 'Skills'] = ';'.join(skills_list)
    
    return df

# only scrapes the top 6 interests displayed without clicking the 'See all' button
def scrape_interests_indiv(driver, profile_url, reload=True):
    df = pd.DataFrame(columns = ["Interests"])
    
    if reload:
        # visit the profile url
        driver.get(profile_url)
        profile_dp_visible(driver)
        expand_page(driver)
        
    interests_list = []
    
    interests = driver.find_elements_by_xpath(
        "//section[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']"
        + "//li"
        + "//h3"
    )

    for interest in interests:
        if len(interest.text.strip()) != 0:
            interests_list.append(interest.text.strip())

    df.loc[0, 'Interests'] = ';'.join(interests_list)
    return df

def scrape_industry(driver, company_url):
    if type(company_url) != str:
        return np.nan
    
    if company_url[:32]  == 'https://www.linkedin.com/school/':
        return "Academia/Education"
    elif company_url[:33]  == 'https://www.linkedin.com/company/':
        driver.get(company_url + "about/")
        if company_dp_visible:
            org_info = driver.find_elements_by_xpath(
                "//dt[@class='org-page-details__definition-term t-14 t-black t-bold']"
            )
            for i in range(len(org_info)):
                if org_info[i].text.lower() == 'industry':
                    return driver.find_element_by_xpath(
                        "//dd" + "[" + str(i+1) + "]"
                        + "[@class='org-page-details__definition-text t-14 t-black--light t-normal']"
                    ).text
            
    return np.nan

def scrape_industries(driver, company_urls):
    df = pd.DataFrame(columns = ["url", "Industry"])
    df["url"] = company_urls
    
    industries = [scrape_industry(driver, url) for url in company_urls]
    df["Industry"] = industries
    
    return df

# selects the first job after the NUS Bachelor's for career data and selects NUS Bachelor's for edu data
def scrape_profile(driver, profile_url):
    name_df = scrape_name_indiv(driver, profile_url, reload=True)
    edu_df = scrape_edu_indiv(driver, profile_url, reload=False)
    exp_df = scrape_exp_indiv(driver, profile_url, reload=False, industries=False)
    skills_df = scrape_skills_indiv(driver, profile_url, reload=False)
    interests_df = scrape_interests_indiv(driver, profile_url, reload=False)
    
    first_job_df = pd.DataFrame(columns=exp_df.columns)
    
    time.sleep(0.1)
    
    nus_df = is_NUS_Bachelor(edu_df)
    if not nus_df.empty:
        first_job_df = get_first_job(exp_df, nus_df.loc[0,"Degree end year"])
    if not first_job_df.empty:
        exp_df["Industry"] = scrape_industries(driver, first_job_df.loc[0, "Company url"])["Industry"]
    
    df_list = [name_df.reset_index(), nus_df.reset_index(), first_job_df.reset_index(),
               skills_df.reset_index(), interests_df.reset_index()]
    
    profile_df = pd.concat(df_list, axis=1)
    
    return profile_df.drop(columns = "index")

def scrape_all_profiles(driver, profile_url):
    counter = 1
    profiles_df = pd.DataFrame()
    for url in profile_url:
        print("Scraping profile #" + str(counter) + ": " + url + " " * 20, "\r", end="")
        counter += 1

        profile_df = scrape_profile(driver, url)
        profile_df['url'] = url
        profiles_df = pd.concat([profiles_df, profile_df], axis=0)
        
    return profiles_df.reset_index().drop(columns = "index")