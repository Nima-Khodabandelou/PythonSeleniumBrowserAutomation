from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


opts = Options()

opts.set_headless()

assert opts.headless  # Operating in headless mode

browser = Firefox(options=opts)

browser.get('http://www.tsetmc.com/Loader.aspx?ParTree=15')
search_form = browser.find_element_by_id('search_form_input')
search_form.send_keys('نماد')
search_form.submit
