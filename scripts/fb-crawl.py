# THIS IS A SCRIPT TO CRAWL COMMENTS FROM A FACEBOOK POST

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import randint

# PREDEFINED HERE
driver_path = r''       # path to browser driver
userName = ''           # username/email to login FB (optional)
passWord = ''           # password to login FB (optional)
links_file_path = ''    # path to the file contains links to FB posts you want to get data
output_file_path = ''   # path to save data

# Initialize webdriver
driver = webdriver.Firefox(executable_path=driver_path)
driver.get('https://www.facebook.com')
sleep(randint(4, 7))

'''
# Close login popup if needed
loginPopup = driver.find_element_by_xpath('//*[@id="expanding_cta_close_button"]')
loginPopup.click()
sleep(2)
'''

# Login to fb
logInButton = driver.find_element_by_id('loginbutton')
userName_field = driver.find_element_by_id('email')
userName_field.send_keys(userName)
passWord_field = driver.find_element_by_id('pass')
passWord_field.send_keys(passWord)
logInButton.click()
sleep(randint(5, 10))

# Import posts' links
links = []
with open(links_file_path) as links_file:
    for line in links_file:
        links.append(line[:-1])
links_file.close()

# Comments list
comments = []

link_number = 0
total = 0
for link in links:
    link_number += 1
    print('Link {}:'.format(link_number))
    driver.get(link)
    sleep(randint(3, 8))

    # Get number of comments of current post
    commentsNumberElement = driver.find_element_by_xpath('//a[@class="_3hg- _42ft"]')
    commentsNumberText = commentsNumberElement.text
    comments_count = int(commentsNumberText[:-10])

    # Change comments mode to all
    commentModeButton = driver.find_element_by_xpath('//a[@class="_2pm3 _21q1 _p"]')
    commentModeButtonLocation = commentModeButton.location
    commentModeButton.click()
    sleep(2)

    # Scroll down so that driver can see comment section
    scrollDownHeight = commentModeButtonLocation['y']
    driver.execute_script('window.scrollTo(0, {})'.format(scrollDownHeight - 300))

    # Find menu to select show all comments
    menu = driver.find_element_by_xpath('//ul[@class="_54nf"]')
    showAllCommentsButton = menu.find_element_by_xpath('//li[3]/a[@class="_54nc"]')
    acts = ActionChains(driver)
    acts.move_to_element(menu)
    acts.click(showAllCommentsButton)
    try:
        acts.perform()
    except:
        print('\tError!')
        #continue
    sleep(randint(2, 5))

    # Click show more comments buttons
    showMoreCommentsButtons = driver.find_elements_by_xpath('//a[@class="_4sxc _42ft"]')
    for button in showMoreCommentsButtons:
        button.click()
        sleep(randint(1, 3))
    sleep(2)

    # Find all comments
    comment_elements = driver.find_elements_by_xpath('//span[@class="_3l3x"]')
    count = 0
    for item in comment_elements:
        if count == comments_count:
            break
        text = item.text
        comments.append(text)
        count += 1
        total += 1
    print('\t{} comments found'.format(count))

# Close driver
driver.close()

# Write to file
with open(output_file_path, 'a', encoding='utf-8') as output_file: 
    for comment in comments:
        output_file.write(comment + '\n')
output_file.close()
print('Total: {} comments added!'.format(total))
