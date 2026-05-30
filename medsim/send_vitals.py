import random
import time
from datetime import datetime, timezone

import requests


FHIR_BASE_URL = "http://localhost:8080/fhir"
PATIENT_ID = "patient-001"
DEVICE_ID = "mon-001"


VITAL_MAPPINGS = {
    "heart_rate": {
        "display": "Heart rate",
        "loinc": "8867-4",
        "unit": "beats/min",
        "unit_code": "/min",
        "min": 65,
        "max": 105,
    },
    "spo2": {
        "display": "Oxygen saturation",
        "loinc": "59408-5",
        "unit": "%",
        "unit_code": "%",
        "min": 94,
        "max": 100,
    },
    "respiratory_rate": {
        "display": "Respiratory rate",
        "loinc": "9279-1",
        "unit": "breaths/min",
        "unit_code": "/min",
        "min": 12,
        "max": 22,
    },
    "temperature": {
        "display": "Body temperature",
        "loinc": "8310-5",
        "unit": "Cel",
        "unit_code": "Cel",
        "min": 36.4,
        "max": 37.8,
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def make_observation(vital_name: str, value: float) -> dict:
    vital = VITAL_MAPPINGS[vital_name]

    return {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs",
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": vital["loinc"],
                    "display": vital["display"],
                }
            ],
            "text": vital["display"],
        },
        "subject": {
            "reference": f"Patient/{PATIENT_ID}"
        },
        "device": {
            "reference": f"Device/{DEVICE_ID}"
        },
        "effectiveDateTime": utc_now(),
        "valueQuantity": {
            "value": value,
            "unit": vital["unit"],
            "system": "http://unitsofmeasure.org",
            "code": vital["unit_code"],
        },
    }


def generate_value(vital_name: str) -> float:
    vital = VITAL_MAPPINGS[vital_name]

    if vital_name == "temperature":
        return round(random.uniform(vital["min"], vital["max"]), 1)

    return random.randint(vital["min"], vital["max"])


def post_observation(observation: dict) -> None:
    response = requests.post(
        f"{FHIR_BASE_URL}/Observation",
        json=observation,
        headers={"Content-Type": "application/fhir+json"},
        timeout=10,
    )

    if response.status_code not in [200, 201]:
        print(f"Failed to post Observation: {response.status_code}")
        print(response.text)
        return

    created = response.json()
    print(
        f"Posted {observation['code']['text']}: "
        f"{observation['valueQuantity']['value']} "
        f"{observation['valueQuantity']['unit']} "
        f"as Observation/{created.get('id')}"
    )


def main() -> None:
    print("Starting fake vital signs monitor...")
    print(f"Patient: Patient/{PATIENT_ID}")
    print(f"Device: Device/{DEVICE_ID}")
    print()

    for cycle in range(1, 6):
        print(f"Cycle {cycle}")

        for vital_name in VITAL_MAPPINGS:
            value = generate_value(vital_name)
            observation = make_observation(vital_name, value)
            post_observation(observation)

        print()
        time.sleep(5)

    print("Simulation complete.")


if __name__ == "__main__":
    main()