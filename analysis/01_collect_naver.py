#!/usr/bin/env python3
"""Phase 1: Collect Naver DataLab Search Trend API data.

180 API calls: 6 keywords × 10 age conditions × 3 gender conditions.
Rate-limited to ≥1.2s between calls. Retry up to 3 times on error.
Saves to data/raw/naver_rsv_all.csv
"""

import os
import sys
import time
import json
import requests
import pandas as pd
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────────────────
NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET", "")
API_URL = "https://openapi.naver.com/v1/datalab/search"

START_DATE = "2016-01-01"
END_DATE = "2025-12-31"
TIME_UNIT = "month"

KEYWORDS = [
    {"groupName": "실리프팅", "keywords": ["실리프팅", "실리프팅시술"]},
    {"groupName": "울쎄라", "keywords": ["울쎄라", "울쎄라피프라임"]},
    {"groupName": "슈링크", "keywords": ["슈링크", "슈링크유니버스"]},
    {"groupName": "써마지", "keywords": ["써마지", "써마지FLX"]},
    {"groupName": "인모드", "keywords": ["인모드", "인모드포마"]},
    {"groupName": "리프팅시술", "keywords": ["리프팅시술"]},
]

# None = all ages; '3'~'11' = age codes 19-24 through 60+
AGE_CODES = [None, "3", "4", "5", "6", "7", "8", "9", "10", "11"]

# None = all genders; 'f' = female; 'm' = male
GENDERS = [None, "f", "m"]

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "naver_rsv_all.csv")

MAX_RETRIES = 3
MIN_INTERVAL = 1.2  # seconds between API calls


def build_request_body(keyword_group, age_code=None, gender=None):
    """Build Naver DataLab API request body."""
    body = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "timeUnit": TIME_UNIT,
        "keywordGroups": [
            {
                "groupName": keyword_group["groupName"],
                "keywords": keyword_group["keywords"],
            }
        ],
    }
    if age_code is not None:
        body["ages"] = [age_code]
    if gender is not None:
        body["gender"] = gender
    return body


def call_api(body, retries=MAX_RETRIES):
    """Call Naver DataLab API with retry logic."""
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        "Content-Type": "application/json",
    }
    for attempt in range(retries):
        try:
            resp = requests.post(API_URL, headers=headers, json=body, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
                if attempt < retries - 1:
                    wait = 2 ** (attempt + 1)
                    print(f"  Retrying in {wait}s...", file=sys.stderr)
                    time.sleep(wait)
        except requests.RequestException as e:
            print(f"  Request error: {e}", file=sys.stderr)
            if attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  Retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
    return None


def parse_response(resp_json, keyword_name, age_code, gender):
    """Parse API response into list of row dicts."""
    rows = []
    if not resp_json or "results" not in resp_json:
        return rows
    for result in resp_json["results"]:
        for data_point in result.get("data", []):
            rows.append({
                "keyword": keyword_name,
                "age_code": age_code if age_code else "all",
                "gender": gender if gender else "all",
                "period": data_point["period"],
                "ratio": data_point["ratio"],
            })
    return rows


def main():
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        print("ERROR: NAVER_CLIENT_ID and NAVER_CLIENT_SECRET must be set.", file=sys.stderr)
        sys.exit(1)

    total_calls = len(KEYWORDS) * len(AGE_CODES) * len(GENDERS)
    print(f"Starting Naver DataLab collection: {total_calls} API calls")
    print(f"Period: {START_DATE} ~ {END_DATE}, timeUnit={TIME_UNIT}")

    all_rows = []
    call_count = 0
    failed_calls = []
    last_call_time = 0

    for kw in KEYWORDS:
        for age in AGE_CODES:
            for gender in GENDERS:
                call_count += 1

                # Rate limiting
                elapsed = time.time() - last_call_time
                if elapsed < MIN_INTERVAL:
                    time.sleep(MIN_INTERVAL - elapsed)

                age_label = age if age else "all"
                gender_label = gender if gender else "all"
                print(f"[{call_count}/{total_calls}] {kw['groupName']} | age={age_label} | gender={gender_label}")

                body = build_request_body(kw, age, gender)
                last_call_time = time.time()
                resp = call_api(body)

                if resp is None:
                    failed_calls.append((kw["groupName"], age_label, gender_label))
                    print(f"  FAILED — skipped", file=sys.stderr)
                    continue

                rows = parse_response(resp, kw["groupName"], age, gender)
                all_rows.extend(rows)

    # Save results
    df = pd.DataFrame(all_rows)
    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT_PATH)), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"\nSaved {len(df)} rows to {OUTPUT_PATH}")

    if failed_calls:
        print(f"\n{len(failed_calls)} failed calls:")
        for fc in failed_calls:
            print(f"  keyword={fc[0]}, age={fc[1]}, gender={fc[2]}")
    else:
        print("\nAll API calls succeeded.")

    print(f"\nDataset shape: {df.shape}")
    print(f"Keywords: {df['keyword'].unique().tolist()}")
    print(f"Age codes: {sorted(df['age_code'].unique().tolist())}")
    print(f"Genders: {sorted(df['gender'].unique().tolist())}")
    print(f"Period range: {df['period'].min()} ~ {df['period'].max()}")


if __name__ == "__main__":
    main()
