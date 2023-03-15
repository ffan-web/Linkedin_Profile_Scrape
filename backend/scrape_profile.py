from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import constants as c
import json

def scrape_profile(scrape_username):
    # get a chromedriver
    PATH = c.driver_path
    #print(PATH)
    driver = webdriver.Chrome(PATH)

    # let chromedriver visit login page
    driver.get("https://www.linkedin.com/uas/login")
    time.sleep(3)

    #  linkedin account login
    email=driver.find_element("id", "username")
    #print(email)
    USERNAME = c.linkedin_username
    email.send_keys(USERNAME)
    PASSWORD = c.linkedin_password
    password=driver.find_element("id", "password")
    password.send_keys(PASSWORD)
    time.sleep(3)
    password.send_keys(Keys.RETURN)

    # check need security check
    #print(driver.current_url)
    if driver.current_url != "https://www.linkedin.com/feed/":
        time.sleep(15)
    else :
        time.sleep(3)

    URL = 'https://www.linkedin.com/in/' + scrape_username + '/'
    driver.get(URL)
    time.sleep(3)

    soup = bs(driver.page_source, 'html.parser')
    profile_name = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text.strip()
    print('profile name : ', profile_name)
    title_description = soup.find('div', {'class' : 'text-body-medium break-words'}).text.strip()
    print('title_description : ', title_description)
    location = soup.find('span', {'class' : 'text-body-small inline t-black--light break-words'}).text.strip()
    print('location : ', location)
    # Extract About section
    about_div = soup.find('div', {'class' : 'inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp full-width'})
    about_content = about_div.find('span', {'class' : 'visually-hidden'}).text.strip()

    print('About : ', about_content)


    # Extract work experience
    experience_url = URL + "details/experience/"
    driver.get(experience_url)
    time.sleep(3)

    soup = bs(driver.page_source, 'html.parser')
    experience_section = soup.find('div', {'class' : 'scaffold-finite-scroll__content'})
    #print(experience_section)
    experience_lst = experience_section.find_all('li', {'class' : 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
    #print(len(experience_lst))
    experiences = []

    for experience in experience_lst:
        pos_title = experience.find('span', {'class' : 'mr1 t-bold'}).find('span').text.strip()
        #print(pos_title)
        pos_company = experience.find('span', {'class' : 't-14 t-normal'}).find('span').text.strip()
        #print(pos_company)
        pos_daterange = experience.find('span', {'class' : 't-14 t-normal t-black--light'}).find('span').text.strip()
        #print(pos_daterange)
        try:
            pos_location = experience.find_all('span', {'class': 't-14 t-normal t-black--light'})[1].find('span').text.strip()
            #print(pos_location)
        except:
            pos_location = 'null'
        pos_content_section = experience.find('div', {'class' : 'pvs-list__outer-container'})
        if pos_content_section:
            pos_content = pos_content_section.find('span').text.strip()
        experiences.append({
            'Title' : pos_title,
            'Company' :  pos_company,
            'DateRange' : pos_daterange,
            'Location' : pos_location,
            'JobContent' : pos_content
        })

    print('Experience : ', experiences)

    # Extract education
    education_url = URL + "details/education/"
    driver.get(education_url)
    time.sleep(3)

    soup = bs(driver.page_source, 'html.parser')
    education_section = soup.find('section', {'class' : 'artdeco-card ember-view pb3'})
    education_section = education_section.find('div', {'class' : 'pvs-list__container'})
    education_section = education_section.find('div', {'class' : 'scaffold-finite-scroll__content'})
    #print(education_section)
    education_lst = education_section.find_all('li', {'class' : 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
    #print(education_lst)
    educations = []


    for education in education_lst:
        edu_school = education.find('span', {'class' : 'mr1 hoverable-link-text t-bold'}).find('span').text.strip()
        try:
            edu_degree = education.find('span', {'class' : 't-14 t-normal'}).find('span').text.strip()
        except:
            edu_degree = 'null'
        try :
            edu_daterange = education.find('span', {'class' : 't-14 t-normal t-black--light'}).find('span').text.strip()
        except:
            edu_daterange = 'null'
        educations.append({
            'School' : edu_school,
            'Degree' :  edu_degree,
            'DateRange' : edu_daterange
        })

    print('Education : ', educations)


    # Extract recommendation
    recommendation_url = URL + "details/recommendations/"
    driver.get(recommendation_url)
    time.sleep(3)

    soup = bs(driver.page_source, 'html.parser')
    recommendation_section = soup.find('section', {'class' : 'artdeco-card ember-view pb3'})
    recommendations = []

    try:
        recommendation_section = recommendation_section.find('div', {'class' : 'artdeco-tabs artdeco-tabs--size-t-48 ember-view'})
        recommendation_section = recommendation_section.find('div', {'class' : 'artdeco-tabpanel active ember-view'})
        recommendation_section = recommendation_section.find('div', {'class' : 'scaffold-finite-scroll__content'})
        recommendation_lst = recommendation_section.find_all('li', {'class' : 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
        recommendations = []

        for recommendation in recommendation_lst:
            recomm_name = recommendation.find('span', {'class' : 'mr1 hoverable-link-text t-bold'}).find('span').text.strip()
            #print('-----------------------------')
            #print(recomm_name)
            recomm_profile_link = recommendation.find('a', {'class' : 'optional-action-target-wrapper display-flex flex-column full-width'})["href"]
            #print(recomm_profile_link)
            recomm_secion = recommendation.find('span', {'class' : 't-14 t-normal t-black--light'}).find('span')
            temp_str = recomm_secion.text.strip()
            #print(temp_str)
            recomm_arr = temp_str.split(", ")
            #print(recomm_arr)
            if len(recomm_arr) > 2 :
                recomm_date = recomm_arr[0] + ", " + recomm_arr[1]
                recomm_relation = recomm_arr[2]
            else:
                recomm_date = recomm_arr[0] + ", " + recomm_arr[1]
                recomm_relation = 'null'
            #print(recomm_date)
            #print(recomm_relation)
            recomm_content = recommendation.find('div', {'class' : 'display-flex align-items-center t-14 t-normal t-black'}).text.strip()
            #print(recomm_content)
            recommendations.append({
                'Name' : recomm_name,
                'Link' : recomm_profile_link,
                'Date' : recomm_date,
                'Relation' : recomm_relation,
                'Content' : recomm_content
            })

    except:
        print("No recommend information")

    print('Recommendation : ', recommendations)

    return json.dumps({
        'Name' : profile_name,
        'Title' : title_description,
        'Location' : location,
        'About' : about_content,
        'Experience' : experiences,
        'Education' : educations,
        'Recommendation' : recommendations})
