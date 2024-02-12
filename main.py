import subprocess
import logging

def main():
    logging.basicConfig(filename='errors.log', level=logging.DEBUG)
    try:
        # Use full path to the virtual environment activation script
        venv_activate_script = r'virt\Scripts\activate'

        choice = int(input("Which Spider you want to run? Enter 1 for Facebook or 2 for Kijiji: "))
        year = input("Enter Year: ")
        make = input("Enter Make: ")
        model = input("Enter Model: ")
        city = input("Enter the name of the city to target: ")
        keyword_1 = input("Enter First Keyword if any(eg. 'Front','Automatic','Headlight') else press Enter: ")
        keyword_2 = input("Enter 2nd Keyword if any(eg. 'Bumper','Automatic','Engine') else press Enter: ")
        
        #Select Spider
        if choice == 1:
            spider = 'fb_market'
        elif choice == 2:
            spider = 'kiji_market'
        
        # construct filename
        filename = f"{year}_{make}_{model}_{city}_{keyword_1}_{keyword_2}_{spider}.csv"

        # Combine all commands into a single string
        command = f'{venv_activate_script} && cd marketplace_scraper && scrapy crawl {spider} -O ../output/{filename} -a year={year} -a make={make} -a model={model} -a keyword_1={keyword_1} -a keyword_2={keyword_2} -a city={city}'

        # Execute the command in a single subprocess call
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
        print(result.stdout)
        
        logging.info("Script executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")

    # Wait for user input before exiting
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
