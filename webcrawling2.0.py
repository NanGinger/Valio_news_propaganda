import requests
from bs4 import BeautifulSoup
import json

def get_all_links(url):
    # Make a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all hyperlinks on the page using the 'a' tag
        links = soup.find_all('a', href=True)

        # Extract and return the href attribute (URL) for each hyperlink
        return [link['href'] for link in links]
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []


import requests
from bs4 import BeautifulSoup
import json

def get_text_from_links(links):
    all_json_data = []  # Initialize a list to hold all JSON objects
    for link in links:
        try:
            response = requests.get(link)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                content = response.text
                soup = BeautifulSoup(content, "html.parser")
                all_normaltext = soup.findAll("div", attrs={"class": "vl-news-article__content"})
                for normaltext in all_normaltext:
                    my_text = normaltext.get_text(separator='\n')  # Using get_text to strip HTML tags
                    with open("valio21.txt", "a", encoding="utf-8") as file:
                        file.write(my_text + "\n")  # Append text and add newline for separation between articles

                    # Append JSON object to the list
                    all_json_data.append({"text": my_text})
            else:
                print(f"Failed to fetch {link}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {link}: {e}")

    # Write all JSON objects to the JSON file
    with open("valio21.json", "w", encoding="utf-8") as fout:
        json.dump(all_json_data, fout, ensure_ascii=False, indent=4)  # Dump the entire list into the JSON file


            

url = 'https://www.valio.com/news-archive/'
all_links = get_all_links(url)

all_linksnew=all_links[66:216]
if all_linksnew:
   get_text_from_links(all_linksnew)
