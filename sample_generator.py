import pandas as pd
from datetime import timedelta, datetime
import random
import json

# Seed for reproducibility
random.seed(42)

# Sample data
data = {
    "service date": ["3/28/18 0:00"] * 4,
    "submitted procedure": ["D0180", "D0210", "D4346", "D4211"],
    "quadrant": ["", "", "", "UR"],
    "Plan/Group #": ["GRP-1000"] * 4,
    "Subscriber#": [3730189502] * 4,
    "Provider NPI": [1497775530] * 4,
    "provider fees": ["$100.00 ", "$108.00 ", "$130.00 ", "$178.00 "],
    "Allowed fees": ["$100.00 ", "$108.00 ", "$65.00 ", "$178.00 "],
    "member coinsurance": ["$0.00 ", "$0.00 ", "$16.25 ", "$35.60 "],
    "member copay": ["$0.00 "] * 4
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Generate additional 100 lines of data
additional_rows = 100
start_date = datetime.strptime("3/29/18", "%m/%d/%y")
procedures = ["D0180", "D0210", "D4346", "D4211", "D1110"]
quadrants = ["", "UR", "UL", "LR", "LL"]

for _ in range(additional_rows):
    row = {
        "service date": (start_date + timedelta(days=random.randint(0, 365))).strftime("%m/%d/%y 0:00"),
        "submitted procedure": random.choice(procedures),
        "quadrant": random.choice(quadrants),
        "Plan/Group #": "GRP-1000",
        "Subscriber#": random.randint(3730189500, 3730189600),
        "Provider NPI": random.choice([1497775530, 1497775531, 1497775532]),
        "provider fees": f"${random.randint(80, 200)}.00 ",
        "Allowed fees": f"${random.randint(50, 200)}.00 ",
        "member coinsurance": f"${random.randint(0, 40)}.00 ",
        "member copay": "$0.00 "
    }
    df = df.append(row, ignore_index=True)

# Convert a few rows to JSON as a sample
sample_json = df.head().to_json(orient="records", date_format="iso")
sample_json = json.loads(sample_json)

df.head(), sample_json