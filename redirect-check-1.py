import requests
import pandas as pd
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

input_file = "urls.txt"
output_file = "redirect_results.xlsx"

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
            response = requests.get(
                url,
                headers=headers,
                allow_redirects=True,
                timeout=20,
                verify=False
            )
        except:
            url = url.replace("https://", "http://")
            response = requests.get(
                url,
                headers=headers,
                allow_redirects=True,
                timeout=20,
                verify=False
            )

        # ✅ Build redirect chain
        chain = []
        visited = set()

        for resp in response.history:
            step_url = resp.url
            step_code = resp.status_code

            if step_url in visited:
                chain.append(f"{step_url} [{step_code}] (LOOP)")
                break

            visited.add(step_url)
            chain.append(f"{step_url} [{step_code}]")

        # Final destination
        final_url = response.url
        final_code = response.status_code

        if final_url in visited:
            loop_flag = "YES"
        else:
            loop_flag = "NO"

        chain.append(f"{final_url} [{final_code}]")

        # Convert chain to string
        chain_str = " → ".join(chain)

        status = "PASS" if final_code == 200 else "FAIL"

        results.append({
            "Source URL": original_url,
            "Final URL": final_url,
            "Final Status Code": final_code,
            "Redirect Count": len(response.history),
            "Redirect Chain": chain_str,
            "Loop Detected": loop_flag,
            "Result": status
        })

        print(f"{original_url} -> {final_url} [{final_code}]")

    except Exception as e:
        results.append({
            "Source URL": original_url,
            "Final URL": "ERROR",
            "Final Status Code": "N/A",
            "Redirect Count": 0,
            "Redirect Chain": "ERROR",
            "Loop Detected": "UNKNOWN",
            "Result": "FAIL"
        })

        print(f"{original_url} -> ERROR: {e}")

# ✅ Export to Excel
df = pd.DataFrame(results)
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"\n✅ Report saved to {output_file}")
