from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#https://www.youtube.com/watch?v=EELySnTPeyw&ab_channel=PyPros
def get_results(search_term):
    url = "https://www.allrecipes.com/search/results/?IngIncl="
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    # press Filters button
    browser.find_element_by_id('faceted-search-filters-prompt').click()

    search_box = browser.find_element_by_xpath("//input[@class='faceted-search-filters-available-item-filter-choices option include-option']")
    search_box.send_keys(search_term)
    search_box.submit()
    try:
        links = browser.find_elements_by_xpath("//div[@class='search-results-content-results-wrapper//div[@class='component card card__recipe card__facetedSearchResult']//a[@class='card__titleLink manual-link-behavior']")
    except:
        links = browser.find_elements_by_xpath("//a[@class='card__titleLink manual-link-behavior']")
    results = []
    for link in links:
        href = link.get_attribute("href")
        print(href)
        results.append(href)
    browser.close()
    return results

get_results("egg")

