import urllib.request
import csv
import io

# We will download the GCAT launch list (which is the gold standard for orbital launches)
# URL: https://planet4589.org/space/gcat/tsv/derive/launch.tsv
print("Downloading GCAT master launch list...")
url = "https://planet4589.org/space/gcat/tsv/derive/launch.tsv"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
    
    print("Download complete. Parsing TSV...")
    # The GCAT launch list is tab-separated
    reader = csv.DictReader(io.StringIO(content), delimiter='\t')
    
    soviet_count = 0
    us_count = 0
    
    # Let's count launches from 1960 to 1989
    for row in reader:
        # Launch_Date format: YYYY-MM-DD
        date = row.get('Launch_Date', '')
        if len(date) >= 4 and date[:4].isdigit():
            year = int(date[:4])
            if 1960 <= year <= 1989:
                # GCAT uses 'SU' for Soviet Union, 'US' for USA in the 'Agency' or 'State' column if it exists.
                # Actually, GCAT launch.tsv might not have a direct country code for the launch itself easily readable vs agency.
                # Let's look at the Launch_Site. 
                # Soviet sites: TT (Baikonur), PL (Plesetsk), KY (Kapustin Yar)
                site = row.get('Launch_Site', '')
                if site in ['TT', 'PL', 'KY']:
                    soviet_count += 1
                # US sites: CC (Cape Canaveral), KSC (Kennedy), VAFB, WI (Wallops)
                elif site in ['CC', 'KSC', 'VAFB', 'WI']:
                    us_count += 1
                    
    print(f"\n--- GCAT Master List Verification (1960-1989) ---")
    print(f"Total Soviet Launches (TT, PL, KY): {soviet_count}")
    print(f"Total US Launches (CC, KSC, VAFB, WI): {us_count}")
    
except Exception as e:
    print(f"Error: {e}")

