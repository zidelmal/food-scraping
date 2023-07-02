import pandas as pd
from scrapers.jumiafood_tn import JumiaFoodTn
from scrapers.jumiafood_ma import JumiaFoodMa


SCRAPERS = [(JumiaFoodMa(), "JumiaFoodMA"), (JumiaFoodTn(), "JumiaFoodTN")]


for scraper in SCRAPERS:
    with scraper[0] as bot:
        bot.land_first_page()
        bot.first_popup()
        informations = bot.get_restaurants_url()

        data = pd.DataFrame()
        for i, row in enumerate(informations):
            try:
                bot.close_popup()
                item = bot.get_restaurant(row, data)
                data = pd.concat([data, pd.DataFrame(item)], ignore_index=True)
                data.to_csv(f'extracted_data/{scraper[1]}.csv', index=False)
            except:
                pass

