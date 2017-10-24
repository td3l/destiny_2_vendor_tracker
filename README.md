Context: In the online video game 'Destiny 2,' players receive gear rewards for their characters from different 'vendors.' The quality of the gear is quantized by a power level, where 300 is the maximum. The exact power level of gear being rewarded varies over time. Players are most interested in obtaining these rewards when they are being distributed at the maximum level (i.e. 300), thus the website http://destiny-vendor-gear-tracker.com/ was born as a community-reporting tool for tracking when vendors are rewarding power level 300 gear. 

This project retrieves the historical data from http://destiny-vendor-gear-tracker.com/ logs (timestamped entries every 30 minutes) and aggregates the data into pandas Data Frames. The goal was to examine this data for patterns and potentially subject it to predictive analysis. Ultimately, this project served as a useful exercise in HTML scraping, as further knowledge of the game mechanics and some quick examinations of the retreived data strongly suggest that the vendor rewards are distributed randomly. 

The file 'D2_vendors_data_scraper.py' performs the scraping and Data Frame loading. It works as-is as of Oct. 20, 2017--possible changes in the webpage code may necessitate changes in the scraper code. 
