import requests
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import time

BASE_URL = "https://www.pokemon.co.jp/ex/shirts/en/pattern_all/"
BASE_IMG = "https://www.pokemon.co.jp/ex/shirts/en/img/pattern_all/"

def scrape_images(record_artists_work=True, download_images=False):
    designers = {}

    for i in range(1, 152):
        design_url = "{}{}.html".format(BASE_URL, i)
        r = requests.get(design_url)
        soup = BeautifulSoup(r.text, "html.parser")

        designer = soup.find("p", class_="credit").text.split("：")[1].strip()
        pokemon = soup.find("h1").text

        print(i, pokemon, designer)

        if record_artists_work:
            designers[designer] = designers.get(designer, [])
            designers[designer].append({"num": i,
                                        "pokemon": pokemon,
                                        "url": design_url})

        if download_images:
            # clean dir name
            designer = re.sub("é", "e", designer)
            designer = re.sub("[^a-zA-Z0-9]", "_", designer).strip("_")

            # make a folder for the lovely designer if it does not exist already
            if not os.path.exists(designer):
                os.mkdir(designer)

            # download image into that path
            img_path = "{}/{}_{}.jpg".format(designer, i, pokemon)

            if not os.path.exists(img_path):
                urllib.request.urlretrieve("{}{}.jpg".format(BASE_IMG, i), img_path)

        time.sleep(1.5)
    return designers


def write_readme(designers):
    with open("README.md", "w") as f:
        f.write("""# Pokémon Shirt Scraper
A web scraper that sorts and downloads all 151 Pokémon shirt designs by their designers.

All credit goes to the awesome artists and companies that made this all possible.

https://www.pokemon.co.jp/ex/shirts/en/
""")
        for designer, designs_list in designers.items():
            f.write("#### {}\n".format(designer))
            
            for pokemon_info in designs_list:
                f.write("* [{}]({})\n".format(pokemon_info["pokemon"],
                                              pokemon_info["url"]))


def main():
    designers = scrape_images()
    write_readme(designers)

if __name__ == "__main__":
    main()
