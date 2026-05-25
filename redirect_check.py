import requests
import csv

input_file = "urls.txt"
output_file = "redirect_results.csv"

headers = {
    "User-Agent": "Mozilla/5.0"
}

results = []

with open(input_file, "r") as f:
    urls = f.read().splitlines()

for original_url in urls:
    try:
        url = original_url.strip()

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

       
        try:
            response = requests.get(url, headers=headers, allow_redirects=True, timeout=10, verify=False)
        except:
            # fallback to HTTP
            url = url.replace("https://", "http://")
     

        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)

        final_url = response.url
        status_code = response.status_code
        redirect_count = len(response.history)

        status = "PASS" if status_code == 200 else "FAIL"

        results.append([original_url, final_url, status_code, redirect_count, status])

        print(f"{original_url} -> {final_url} [{status_code}]")

    except Exception as e:
        results.append([original_url, "ERROR", "N/A", 0, "FAIL"])
        print(f"{original_url} -> ERROR: {e}")

# Save report
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Source URL", "Final URL", "Status Code", "Redirect Count", "Result"])
    writer.writerows(results)

print(f"\nReport saved to {output_file}")
