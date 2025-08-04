from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from collections import defaultdict
import sys
import re

lines = []          # List of {"from": <string>, "to": <string>, "price": <float>}
lines_region = []   # List of {"from": <string>, "to": <string>, "price": <float>}
                    # Only contains regions without subregion (i.e. "Bern, Hauptbahnhof" -> "Bern")

prices = []
orders_div_classname = "mod_bestellungen_dossierzeilen_list"

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    soup = BeautifulSoup(content, 'html.parser')
    
    ul = soup.find("ul", class_=orders_div_classname)
    if not ul:
        print(f"No <ul> with classname {orders_div_classname} found.")
        sys.exit(1)
    else:
        for li in ul.find_all("li"):
            inner_wrapper = li.find("div", class_="mod_bestellungen_dossierzeilen_item_inner_wrapper")
            if inner_wrapper:
                preis_div = inner_wrapper.find("div", class_="mod_bestellungen_dossierzeilen_item_container var_wide var_align_right var_order_preis")
                bestelldatum_div = inner_wrapper.find("div", class_="mod_bestellungen_dossierzeilen_item_container var_order_bestelldatum")
                preis = preis_div.get_text(strip=True) if preis_div else "?"
                bestelldatum = bestelldatum_div.find("span", class_="visuallyhidden").get_text(strip=True) if bestelldatum_div else "?"

                preis_float = float(preis.replace("CHF", "").strip() if preis != "?" else None)

                line_name = "Unknown line"
                line_name_div = inner_wrapper.find("div", class_="mod_bestellungen_dossierzeilen_item_container var_wide")
                line_name_h4 = line_name_div.find("h4")
                if line_name_h4:
                    line_name = " ".join(line_name_h4.stripped_strings)

                    # Extract text between "von" and "nach"
                    match = re.search(r"von\s+(.*?)\s+nach\s+(.*)", line_name)
                    if match:
                        line_from = match.group(1).strip()
                        #                                                 Omit last word
                        line_to = " ".join(match.group(2).strip().split()[:-1])
                    else:
                        line_from = "Unknown"
                        line_to = "Unknown"

                    lines.append({"from": line_from, "to": line_to, "price": preis_float})

                    # Remove everything after (including) the comma in the string
                    region_from = line_from.split(",")[0].strip()
                    region_to = line_to.split(",")[0].strip()
                    lines_region.append({"from": region_from, "to": region_to, "price": preis_float})

                print(line_name)
                print(f"> Date: {bestelldatum}\n> Price: {preis}")
                prices.append(preis_float)

if __name__ == "__main__":
    main()

    # Line Statistics
    line_counter = defaultdict(lambda: {"count": 0, "price": 0.0})
    if len(lines) > 0:
        for line in lines:
            key = (line['from'], line['to'])
            line_counter[key]["count"] += 1
            line_counter[key]["price"] = line['price']  # Assumes price is the same for same route

        line_stats = [
            {"from": k[0], "to": k[1], "count": v["count"], "price": v["price"]}
            for k, v in line_counter.items()
        ]
        line_stats.sort(key=lambda x: x["count"], reverse=True)

    line_counter_region = defaultdict(lambda: {"count": 0, "price": 0.0})
    if len(lines_region) > 0:
        for line in lines_region:
            key = (line['from'], line['to'])
            line_counter_region[key]["count"] += 1
            line_counter_region[key]["price"] = line['price']

        line_stats_region = [
            {"from": k[0], "to": k[1], "count": v["count"], "price": v["price"]}
            for k, v in line_counter_region.items()
        ]
        line_stats_region.sort(key=lambda x: x["count"], reverse=True)
    
    table_main = Table(title="Line statistics")
    table_secondary = Table(title="Line statistics (region only)")
    for column in ["From", "To", "Amount", "Total cost"]:
        table_main.add_column(column)
        table_secondary.add_column(column)
    
    # Main table
    for stat in line_stats:
        table_main.add_row(
            stat['from'],
            stat['to'],
            str(stat['count']),
            f"{stat['count'] * stat['price']:.2f} CHF"
        )

    # Secondary table
    for stat in line_stats_region:
        table_secondary.add_row(
            stat['from'],
            stat['to'],
            str(stat['count']),
            f"{stat['count'] * stat['price']:.2f} CHF"
        )

    console = Console()
    console.print(table_main)
    console.print(table_secondary)
    
    # Prices
    if len(prices) > 0:
        finalPrice = 0
        for price in prices:
            finalPrice += price

        print(f"\033[1mTotal amount spent: {finalPrice:.2f} CHF\033[0m")

    else:
        print("No prices found.")
        sys.exit(1)