from colors import TermColors


def program_header(version:str) -> None:
        print(f"\t\t\tVersion: {TermColors.BOLD}{version}{TermColors.ENDC}\t\t\t\tDev: {TermColors.BOLD}Dr. Xavier{TermColors.ENDC}\t\t\t\t\t Country: {TermColors.BOLD}Egypt{TermColors.ENDC}")
        print(f"\t\t\t\t\t+{'-'*80}+")
        print(f"\t\t\t\t\t|{' '*(40-int(len('+----- Welcome to noonPyMe Scraper -----+')/2))}{TermColors.OKBLUE}{TermColors.BOLD}+----- Welcome to noonPyMe Scraper -----+{TermColors.ENDC}{' '*(38-int(len('+----- Welcome to noonPyMe Scraper -----+')/2))} |")
        print(f"\t\t\t\t\t+{'-'*80}+")
        print(f"\n\t\t - This program is a web scraping build for data scraping noon.com \n")