# Marketplace Scraper

Marketplace Scraper is a web scraping tool designed to extract listings from online marketplaces such as Facebook Marketplace and Kijiji. It allows users to specify search parameters such as year, make, model, city, and keywords to filter the search results and save them to a CSV file.

## Features

- Scrapes listings from Facebook Marketplace and Kijiji.
- Filters search results by year, make, model, city, and keywords.
- Saves filtered listings to a CSV file.
- Error logging for encountered issues during scraping.
- Easy setup and installation using a virtual environment.

## Installation

1. **Download Python 3.10.9**: You need to download Python 3.10.9 from the [official Python website](https://www.python.org/downloads/release/python-3109/).

2. **Install Python**: After downloading the installer, follow the instructions provided to install Python on your system. Make sure to select the option to add Python to your PATH during the installation process.

3. **Configure PATH** (if necessary): If Python is not automatically added to your PATH during installation, you can manually configure it. Follow the appropriate instructions for your operating system:
   - **Windows**: Follow [these instructions](https://geek-university.com/python/add-python-to-the-windows-path/).
   - **macOS/Linux**: Edit the `.bashrc` or `.bash_profile` file in your home directory and add the following line:
     ```bash
     export PATH="$PATH:/path/to/python3.10.9/bin"
     ```
     Replace `/path/to/python3.10.9` with the actual path where Python is installed.

4. **Check Python Installation**: Open a terminal or command prompt and run the following command to verify that Python 3.10.9 is installed correctly:
   ```bash
   python3 --version

5. **Double Click Install.py**
Double click install.py file to complete the installation process. once finished you will see a folder created by the name virt. that means installation is complete. This may take 10-15 mins.

## Usage

1. Once the installation is complete, you can run the `main.py` script to start scraping listings from the desired marketplace.

2. Follow the prompts to select the spider, enter the required information (year, make, model, city, keywords), and start the scraping process.

3. The output CSV file will be saved in the `output` directory with the specified filename.

## Spider Selection

- When prompted, enter `1` to select the Facebook spider or `2` to select the Kijiji spider.

## Input Parameters

- You will be asked to enter the year, make, model, city, and optional keywords (if any) to filter the search results.
- For example, if you want to search for a 2010 Toyota Corolla in Toronto, you would enter `2010`, `Toyota`, `Corolla`, and `Toronto` as input.

## Output

- After the spider finishes scraping, the results will be saved in a CSV file named based on the provided input parameters. 
- You can find the output CSV file in the `output` directory.

## Error Logging

- Any errors encountered during the scraping process will be logged in the `errors.log` file located in the project directory.

## Exiting the Program

- Press `Enter` to exit the program after the scraping process is complete.


