import pandas as pd
import io
import requests

# point at 'main' not 'master'
base_url = "https://raw.githubusercontent.com/travisdesell/exact/main/datasets/2018_coal/burner_{i}.csv"

dfs = []
for i in range(21):  # trying 0..20
    burner_name = f"burner_{i}"
    url = base_url.format(i=i)
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"⚠️ {burner_name}.csv not found — skipping")
        continue

    df = pd.read_csv(io.StringIO(r.text))
    df["burner_name"] = burner_name
    dfs.append(df)

if dfs:
    all_burners = pd.concat(dfs, ignore_index=True)
    all_burners.to_csv("all_burners_0_to_20.csv", index=False)
    print(f"✅ Done! {len(dfs)} burners merged into all_burners_0_to_20.csv")
else:
    print("No burner files were found.")

