# SBB cost parser

Parses an SBB ticket purchases overview HTML document (August 2025).  
To generate a cost overview:
1. Visit https://sbb.ch/de/kaufen/pages/bestellungen.xhtml
2. Define time range, init search
3. Save page as HTML
4. Run script against HTML file

```bash
$ pip install -r requirements.txt
$ python main.py file.html
```

## Output

The script will generate two tables (in the CLI), both showing all parsed journeys with their associated costs.  
Only unique journeys will be shown; Duplicates will be added together and their total cost displayed instead.  
- The first table shows all journeys in a detailed manner, displaying the specific bus/tram/train station.
- The second table shows all journeys without any specfic bus/tram/train station, thereofre being less cluttered.

```
                                 Line statistics                                 
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
┃ From                         ┃ To                      ┃ Amount ┃ Total cost  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
│ Interlaken West, Bahnhof     │ Beatenberg, Waldegg     │ 12     │ 36.00 CHF   │
│ Interlaken West, Bahnhof     │ Beatenberg, Station     │ 9      │ 37.80 CHF   │
│ Grindelwald, Firstbahn       │ First (Grindelwald)     │ 8      │ 136.00 CHF  │
│ ...                          │ ...                     │ ...    │ ...         │
│ Thun, Bahnhof                │ Beatenbucht             │ 2      │ 10.40 CHF   │
│ Interlaken West, Bahnhof     │ Grindelwald, Terminal   │ 1      │ 7.00 CHF    │
│ Interlaken West, Bahnhof     │ Grindelwald             │ 1      │ 7.40 CHF    │
│ Bern, Eigerplatz             │ Ostermundigen, Waldeck  │ 1      │ 3.00 CHF    │
└──────────────────────────────┴─────────────────────────┴────────┴─────────────┘
                     Line statistics (region only)                      
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
┃ From                   ┃ To                   ┃ Amount ┃ Total cost  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
│ Interlaken West        │ Beatenberg           │ 21     │ 63.00 CHF   │
│ Interlaken West        │ Grindelwald          │ 2      │ 14.70 CHF   │
│ Chrindi                │ Stockhorn            │ 1      │ 10.00 CHF   │
│ ...                    │ ...                  │ ...    │ ...         │
│ Interlaken Ost         │ Breitlauenen         │ 1      │ 13.40 CHF   │
└────────────────────────┴──────────────────────┴────────┴─────────────┘
Total amount spent: 1337.00 CHF
```