from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# If hours change, just update this mapping (24h format, HH:MM~HH:MM).
RECITATION_HOURS = {
    "a": "09:00~09:50",
    "b": "10:00~10:50",
    "c": "11:00~11:50",
    "d": "12:00~12:50",
}

MICROSERVICE_LINK = "http://17313-teachers2.s3d.cmu.edu:8080/section_info/"


@app.get("/section_info/{section_id}")
def get_section_info(section_id: str):
    if not section_id:
        raise HTTPException(status_code=404, detail="Missing section id")

    section_id = section_id.lower()

    # Validate the section id against our configured recitation hours
    if section_id not in RECITATION_HOURS:
        raise HTTPException(status_code=404, detail="Invalid section id")

    # Call upstream microservice to get TA info
    try:
        response = requests.get(f"{MICROSERVICE_LINK}{section_id}", timeout=5)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Upstream microservice error: {e}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Upstream microservice returned {response.status_code}"
        )

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="Invalid JSON from microservice")

    ta_list = data.get("ta", [])
    if not isinstance(ta_list, list):
        ta_list = []

    # Parse configured times
    try:
        start_time, end_time = RECITATION_HOURS[section_id].split("~", 1)
    except Exception:
        raise HTTPException(status_code=500, detail="Server time configuration error")

    return {
        "section": section_id,
        "start_time": start_time,
        "end_time": end_time,
        "ta": ta_list,  # e.g., ["Juan", "---"] for section 'a'
    }
