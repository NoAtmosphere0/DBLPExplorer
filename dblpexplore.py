import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd
from datetime import datetime
import argparse
import os

def crawl(url):
    """Fetch content from the specified URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error: {http_err} - URL: {url}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Error: {err} - URL: {url}")
    return None
    

def get_papers(url, exclude_pcd=True):
    """Extract paper titles and authors from the given URL."""
    response = crawl(url)
    if not response:
        logging.info(f"FAILED: Unable to extract data from {url}")
        return None
    
    soup = bs(response.text, 'html.parser')
    papers = pd.DataFrame(columns=["title", "authors"])
    publ_list = soup.find_all("cite", {"class": "data tts-content", "itemprop": "headline"})
    logging.info(f"SUCCESS: Extracted {len(publ_list)} publications at {url}")
    for publ in publ_list:
        new_record = {
            "title": publ.find("span", {"class": "title", "itemprop": "name"}).string,
            "authors": ', '.join(
                a.find("span", {"itemprop": "name"}).string for a in publ.find_all("span", {"itemprop": "author"})
            )
        }
        papers = papers._append(new_record, ignore_index=True)
    
    if exclude_pcd:
        papers = papers.iloc[1:]  # Exclude the first row as it is the proceeding's name
    return papers


def search(papers_list, keywords, method='all'):
    """Filter papers based on given keywords."""
    if not keywords:
        return papers_list  # Return all if no keywords are provided

    result = pd.DataFrame(columns=["title", "authors", "conf_id"])
    check_method = all if method == 'all' else any
    lower_keywords = [keyword.lower() for keyword in keywords]
    
    for idx, pp in papers_list.iterrows():
        try:
            lower_title = pp["title"].lower()
            if check_method(keyword in lower_title for keyword in lower_keywords):
                result = result._append(pp, ignore_index=True)
        except Exception as e:
            #TODO:fix the problem @@
            # logging.warning(f"Error with title '{pp['title']}': {e}")
            continue

    return result


def get_procd(name):
    """Retrieve proceedings for the specified conference."""
    BASE = "https://dblp.org/db/conf/"
    conf_url = BASE + name + "/index.html"
    response = crawl(conf_url)
    
    if not response:
        logging.info(f"FAILED: Unable to extract data from {conf_url}")
        return []

    soup = bs(response.text, 'html.parser')
    proceedings = soup.find_all("cite", {"class": "data tts-content", "itemprop": "headline"})
    logging.info(f"SUCCESS: Extracted {len(proceedings)} proceedings at {conf_url}")
    proceedings_df = pd.DataFrame(columns=["title", "authors", "publisher", "date_published", "link", "conf_id"])

    for pcd in proceedings:
        new_record = {
            "date_published": int(pcd.find("span", {"itemprop": "datePublished"}).string),
            "link": pcd.find("a", {"class": "toc-link"}).get('href'),
            "conf_id": pcd.find("a", {"class": "toc-link"}).get('href').rsplit('/', 1)[-1].rsplit('.', 1)[0]
        }
        proceedings_df = proceedings_df._append(new_record, ignore_index=True)

    return proceedings_df


def get_conf(conf, start, end, dest, search_method='all', search_keywords=[]):
    """Fetch conference proceedings and search for papers within a date range."""
    logging.info(f"STARTED: Started to extract publications from '{conf}' during [{start}, {end}], using method '{search_method}' with keywords '{search_keywords}', to '{dest}'.")
    proceedings = get_procd(conf.lower())
    
    if proceedings is None:
        logging.info(f"Cannot find data for {conf}")
        return
    
    fproceedings = proceedings[(proceedings['date_published'] >= start) & (proceedings['date_published'] <= end)]
    
    with open(dest, 'w') as file: #clear the file if already existed
        pass
    for index, pcd in fproceedings.iterrows():
        papers_list= get_papers(pcd["link"])
        papers_list["conf_id"] = pcd["conf_id"]
        search_results = search(papers_list, search_keywords, search_method)
        try:
            search_results.to_csv(dest, sep='\t', mode='a', header=False, index=False)
            logging.info(f"SUCCESS: Saved {len(search_results)} relevant publication(s) from '{pcd["conf_id"]}' to '{dest}'.")
        except:
            logging.info(f"FAILED: Unable to save publications from '{conf}' to '{dest}'.")
    logging.info(f"COMPLETED: Completed extracting publications from '{conf}' during [{start}, {end}], using method '{search_method}' with keywords '{search_keywords}', to '{dest}'.")
    return


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s -  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    file_handler = logging.FileHandler('app.log', mode='a')
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    current_year = datetime.now().year  # Get the current year for default end value

    # Argument parser setup
    parser = argparse.ArgumentParser(description='Save publications from a conference.')
    parser.add_argument('-c', '--conf', required=True, help='Conference name')
    parser.add_argument('-s', '--start', type=int, default=0, help='Start year (default: 0)')
    parser.add_argument('-e', '--end', type=int, default=current_year, help=f'End year (default: {current_year})')
    parser.add_argument('-m', '--search_method', default='all', help='Search method (default: all)')
    parser.add_argument('-k', '--search_keywords', nargs='*', help='Search keywords (optional)')
    parser.add_argument('-d', '--dest', help='Output file path (optional)')
    
    args = parser.parse_args()

    # Set default values for optional arguments
    if not args.search_keywords:
        args.search_keywords = []
    if not args.dest:
        args.dest = f"extracted_data/{args.conf}{args.start}-{args.end}_{args.search_method}{args.search_keywords}.tsv"
    os.makedirs(os.path.dirname(args.dest), exist_ok=True)
    

    # Execute the main function
    get_conf(args.conf, args.start, args.end, args.dest, args.search_method, args.search_keywords)

if __name__ == '__main__':
    main()
