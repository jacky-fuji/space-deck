import urllib.request
import re

url = "https://en.wikipedia.org/wiki/Timeline_of_spaceflight"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    print("Checking for references to Soviet launch volume...")
    # Find tables that contain "Soviet Union" or "Russia"
    tables = re.findall(r'<table.*?class="wikitable".*?>(.*?)</table>', html, re.DOTALL | re.IGNORECASE)
    
    for table in tables:
        if "Soviet" in table:
            # Extract headers
            headers = re.findall(r'<th[^>]*>(.*?)</th>', table, re.DOTALL | re.IGNORECASE)
            headers = [re.sub(r'<[^>]*>', '', h).strip() for h in headers]
            
            # If it looks like a comparison table
            if any("Soviet" in h for h in headers) or any("US" in h or "United States" in h for h in headers):
                print(f"Header: {', '.join(headers[:10])}...")
                
                rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL | re.IGNORECASE)
                print("First 15 years:")
                for r in rows[1:16]:
                    cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.DOTALL | re.IGNORECASE)
                    clean_cells = [re.sub(r'<[^>]*>', '', c).strip() for c in cells]
                    clean_cells = [re.sub(r'&#\d+;', '', c) for c in clean_cells]
                    print(" | ".join(clean_cells[:10]))
                break
                
except Exception as e:
    print(f"Error fetching data: {e}")

