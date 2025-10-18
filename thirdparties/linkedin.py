import requests
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()
api_key = os.environ.get("BRIGHT_DATA")

# External URLs configurable via environment for portability and security
MOCK_GIST_URL = os.environ.get(
    "MOCK_GIST_URL",
    "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json",
)
BRIGHTDATA_TRIGGER_URL = os.environ.get(
    "BRIGHTDATA_TRIGGER_URL",
    "https://api.brightdata.com/datasets/v3/trigger?dataset_id=gd_l1viktl72bvl7bjuj0&include_errors=true",
)
BRIGHTDATA_SNAPSHOT_BASE = os.environ.get(
    "BRIGHTDATA_SNAPSHOT_BASE",
    "https://api.brightdata.com/datasets/v3/snapshot",
)

def get_linkedin_data(linkedin_url: str, mock: bool = False):
    """
    Fetch structured information from a LinkedIn profile.
    When mock=True, returns a static sample for local development.
    """

    if mock:
        res = requests.get(MOCK_GIST_URL, timeout=30).json()

    else:
        if not api_key:
            raise ValueError(
                "BRIGHT_DATA environment variable is required when mock=False"
            )

        res = requests.post(
            url=BRIGHTDATA_TRIGGER_URL,
            json=[{"url": linkedin_url}],
            headers={"Authorization": f"Bearer {api_key}"},
        ).json()

        snapshot_id = res.get("snapshot_id")
        if not snapshot_id:
            raise ValueError("No snapshot_id returned!")

        print("Snapshot triggered:", snapshot_id)

        # Step 2: poll for results
        results_url = f"{BRIGHTDATA_SNAPSHOT_BASE}/{snapshot_id}?format=json"

        while True:
            result_res = requests.get(
                results_url, headers={"Authorization": f"Bearer {api_key}"}
            )

            if result_res.status_code == 200:
                data = result_res.json()
                if data:  # snapshot is ready
                    return data[0]

            print("Waiting for snapshot to be ready...")
            time.sleep(2)  # wait 2 seconds before trying again

if __name__ == "__main__":
    pass
