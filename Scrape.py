from bs4 import BeautifulSoup
import requests
import csv

def findCandidates():
	response = requests.get("https://www.basketball-reference.com/friv/mvp.html")
	soup = BeautifulSoup(response.content, "html.parser")

	table_body = soup.find("tbody")
	table_rows = table_body.find_all("tr")

	# Find identifiers of MVP Candidates, e.g. 'antetgi01'
	players = []
	for row in table_rows:
	    items = row.find("td", {"class": "left ", "csk": True})
	    player = items["data-append-csv"]
	    players.append(player)

	# Create list of URLs based on identifiers
	url_list = ['https://www.basketball-reference.com/players/' + player[0] + '/' + player + '.html' for player in players]

	return url_list

def writeStatsToCSV(csvfile, url_list):

	# Set up CSV file
	fieldnames = ['Player', 'Age', 'G', 'MP', 'PTS', 'TRB', 'AST', 'STL',
	              'BLK', 'FG%', '3P%', 'FT%', 'WS']

	writer = csv.writer(csvfile)
	writer.writerow(fieldnames)

	# Go through the tables, find stats, store in CSV file
	for url in url_list:

		# Set up BS4 with the URL
		response = requests.get(url)
		soup = BeautifulSoup(response.content, "html.parser")

		name = soup.find("h1", { "itemprop" : "name" }).text

		# Individual stats
		row = soup.find("tr", { "id" : "per_game.2019" })
		parsed = parseItem(row)

		# Win shares
		winshare_table = soup.find("div", { "class" : "p3" })
		winshare = winshare_table.findAll("p")[2].text
		
		# Write to CSV
		info = [name, *parsed, winshare]
		writer.writerow(info)

def getVotingData(csvfile):

	# Set up CSV file
	fieldnames = ['Player', 'Age', 'G', 'MP', 'PTS', 'TRB', 'AST', 'STL',
	              'BLK', 'FG%', '3P%', 'FT%', 'WS', 'Share']

	writer = csv.writer(csvfile)
	writer.writerow(fieldnames)

	url_list = ['http://www.basketball-reference.com/awards/awards_' +  str(x) + '.html' for x in range(2018, 1980, -1)]

	for url in url_list:

		# Set up BS4 with the URL
		response = requests.get(url)
		soup = BeautifulSoup(response.content, "html.parser")

		# MVP Table
		mvps = soup.find("div", { "id" : "div_mvp" })

		
		# Parse table
		name = mvps.find("td", { "class" : "left " }).text
		parsed = parseItem(mvps)

		winshare = mvps.find("td", { "data-stat" : "ws" }).text
		voteshare = mvps.find("td", { "data-stat" : "award_share" }).text

		info = [name, *parsed, winshare, voteshare]
		writer.writerow(info)

# Parses HTML table for specific elements
def parseItem(item):

	age = item.find("td", { "data-stat" : "age" }).text
	games = item.find("td", { "data-stat" : "g" }).text
	mins = item.find("td", { "data-stat" : "mp_per_g" }).text
	points = item.find("td", { "data-stat" : "pts_per_g" }).text
	rebs = item.find("td", { "data-stat" : "trb_per_g" }).text
	assists = item.find("td", { "data-stat" : "ast_per_g" }).text
	steals = item.find("td", { "data-stat" : "stl_per_g" }).text
	blocks = item.find("td", { "data-stat" : "blk_per_g" }).text
	fg_pct = item.find("td", { "data-stat" : "fg_pct" }).text
	fg3_pct = item.find("td", { "data-stat" : "fg3_pct" }).text
	ft_pct = item.find("td", { "data-stat" : "ft_pct" }).text

	info = [age, games, mins, points, rebs, assists, steals, blocks, fg_pct, fg3_pct, ft_pct]

	return info


def main():
	
	candidates = findCandidates()

	with open('players.csv', 'w') as csvfile:
		writeStatsToCSV(csvfile, candidates)

	with open('mvp.csv', 'w') as trainfile:
		getVotingData(trainfile)




if __name__ == "__main__":
	main()
