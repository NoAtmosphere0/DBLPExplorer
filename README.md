# DBLPExplore

DBLPExplore is a Python-based tool designed to crawl and scrape publication data from the DBLP website. This project enables users to extract information about papers and conferences, making it easier to analyze academic publications over a specified time period.

## Features

- Crawl data from DBLP.
- Scrape paper titles, authors, and publication dates.
- Filter results based on specified keywords and search methods.
- Save extracted data in a tab-separated values (TSV) format.

## Installation

### Prerequisites

Make sure you have Python 3.12 installed. You can download it from [python.org](https://www.python.org/).

### Required Packages

# DBLPExplore

DBLPExplore is a Python-based tool designed to crawl and scrape publication data from the DBLP website. This project enables users to extract information about papers and conferences, making it easier to analyze academic publications over a specified time period.

## Features

- Crawl data from DBLP.
- Scrape paper titles, authors, and publication dates.
- Filter results based on specified keywords and search methods.
- Save extracted data in a tab-separated values (TSV) format.

## Installation

### Prerequisites

Make sure you have Python 3.12 installed. 

### Required Packages

You can install the required packages using pip. My project uses the versions specified in requirements.txt. To install the requirements, run:
```bash
pip install -r requirements.txt
```
Feel free to adjust further if needed!

## Usange
To use DBLPExplore, run the following command in your terminal:
| Argument | Description | Required/Optional |
|---|---|---|
| -c, --conf | The acronym of the conference you want to explore. | Required |
| -s, --start | The start year for publication (default: 0). | Optional |
| -e, --end | The end year for publication (default: current year). | Optional |
| -m, --search_method | The search method to use (default: "all"). Options: "all", "any". | Optional |
| -k, --search_keywords | Keywords to search for publications. Enter multiple keywords separated by spaces. | Optional |
| -d, --dest | Destination file path for saving the results (default: <conference_name><start_year>-<end_year>_<search_method><search_keywords>.tsv). | Optional |

*Note: The acronyms for these conferences follow the naming conventions of DBLP, which means some conference acronyms may not align with the standard formats. See more in the Conferences section below.*

### Example
Here’s an example command to extract publications from a conference:
```bash
python dblpexplore.py -c ACL -s 2020 -e 2022 -m all -k "neural network" -d "data/acl_nn.tsv"
```

This command will extract data from the ACL conference on DBLP.com for the years 2020 to 2022, including publications that have the phrase "neural network" in the title. The results will be saved to data/acl_nn.tsv.

## Logging

The tool logs the extracting process to app.log and terminal, helping you track its operations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

Thanks to the developers of DBLP for providing a comprehensive database of computer science publications.

## Conferences

@@ I'll fill later



