import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from alive_progress import alive_bar

def get_episodes():
    driver = webdriver.Chrome()

    url = "https://onepace.net/watch"
    driver.get(url)

    total_json = {}

    arcs = driver.find_elements(By.CSS_SELECTOR, ".Carousel_root__t7h0u")[1:]

    total_episodes = sum(len(arc.find_elements(By.CSS_SELECTOR, ".CarouselSliderItem_item__fbsws")) for arc in arcs)

    sleep(3)

    with alive_bar(total_episodes) as bar:
        for arc_num, arc in enumerate(arcs):
            arc_name = arc.find_element(By.CSS_SELECTOR, "div").text
            arc_json = {'name': arc_name}
            episodes_json = {}
            episodes = arc.find_elements(By.CSS_SELECTOR, ".CarouselSliderItem_item__fbsws")
            next = None
            
            next_list = arc.find_elements(By.CSS_SELECTOR, '.CarouselSlider_scroller__IUunZ')
            if len(next_list) >= 1:
                next = next_list[0]
            
            for episode_num, episode in enumerate(episodes):
                ep_json = {}
                try:
                    episode.click()
                    sleep(1)
                
                except:
                    try:
                        next.click()
                        sleep(1)
                        episode.click()
                        sleep(1)
                    except:
                        raise ValueError(f'problem with arc {arc_num} cant click')
                expander = arc.find_element(By.CSS_SELECTOR, '.Carousel_expander__FQ9Fs')
                episode_name = expander.find_element(By.CSS_SELECTOR, 'h3').text
                episode_numbers = expander.find_elements(By.CSS_SELECTOR, 'p')[2].find_element(By.CSS_SELECTOR, 'strong').text
                released_date = expander.find_elements(By.CSS_SELECTOR, 'p')[5].find_element(By.CSS_SELECTOR, 'strong').text
                
                ep_json['name'] = episode_name
                ep_json['episode_number'] = episode_numbers
                ep_json['released_date'] = released_date


                buttons = expander.find_elements(By.CSS_SELECTOR, ".Carousel_buttons__GB2gF a")
                if len(buttons) >= 1:
                    magnet_link = buttons[0].get_attribute('href')
                    ep_json['magnet'] = magnet_link

                episodes_json[episode_num] = ep_json

                bar()

            arc_json['episodes'] = episodes_json
            total_json[arc_num] = arc_json
    
    return total_json

def save_json(d: dict, path: str):
    with open(path, "w") as json_file:
        json.dump(d, json_file, indent=4)

def download_onepace_json(*args, **kwargs):
    args = kwargs['args']
    path = args.path

    print("TODOOOOOOOT\n\n")
    d = get_episodes()
    save_json(d, path)
    print("\nRAAABOOOOOT\n\n")