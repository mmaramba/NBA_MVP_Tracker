from bs4 import BeautifulSoup
import requests

def findCandidates():
	response = requests.get("https://www.basketball-reference.com/friv/mvp.html")
	soup = BeautifulSoup(response.content, "html.parser")

	table_body = soup.find("tbody")
	table_rows = table_body.find_all("tr")

	links = []
	for row in table_rows:
	    items = row.find("td", {"class": "left ", "csk": True})
	    link = items["data-append-csv"]
	    links.append(link)

	return links

def main():
	candidates = findCandidates()

	print(candidates)

if __name__ == "__main__":
	main()
