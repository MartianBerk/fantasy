import requests

from argparse import ArgumentParser
from bs4 import BeautifulSoup


url_pattern = "https://www.fantasypros.com/nfl/projections/%s.php"
positions = ["qb", "rb", "te", "wr", "dst", "k"]


def main(position, location):
    if position not in positions:
        raise ValueError(f"invalid position, expected one of {', '.join(positions)}")

    # only some positions have ppr format
    if position in ("rb", "te", "wr"):
        url = (url_pattern % position) + "?scoring=PPR&week=draft"
    else:
        url = url_pattern % position + "?week=draft"

    header = ["name", "team", "pts"]

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    table_div = soup.find("div", {"class": "mobile-table"})
    table = table_div.find("table")

    row_count = len(table.findAll("tr")) - 1

    players = []

    for row in table.findAll("tr")[2:row_count]:
        col = row.findAll("td")
        player = []

        parts = col[0].getText().split(" ")
        player.append(" ".join([parts[0], parts[1]]))
        player.append("")
        player.append(col[-1].getText())

        players.append(player)

    with open(f"{location}/{position}.csv", "w") as fh:
        fh.write(f"{','.join(header)}\n")

        for pl in players:
            fh.write(f"{','.join(pl)}\n")

    print(f"{position}.csv generated at {location}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--position", type=str, help="position")
    parser.add_argument("-l", "--location", type=str, help="save location")

    args = vars(parser.parse_args())
    main(**args)
