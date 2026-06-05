import requests

from fastapi import FastAPI, Body

app = FastAPI()

FHIR_BASE_URL = "http://localhost:8080/fhir"
DEFAULT_PATIENT_ID = "patient-001"


KNOWN_DEVICES = {
    "MON-001": {
        "fhir_device_id": "mon-001",
        "display": "Fake Vital Signs Monitor 001"
    }
}


ALLOWED_MEASUREMENTS = {
    "hr": {
        "meaning": "Heart Rate",
        "loinc": "8867-4",
        "unit": "beats/min",
        "unit_code": "/min",
        "min": 20,
        "max": 250
    },
    "spo2": {
        "meaning": "Oxygen Saturation",
        "loinc": "59408-5",
        "unit": "%",
        "unit_code": "%",
        "min": 50,
        "max": 100
    },
    "rr": {
        "meaning": "Respiratory Rate",
        "loinc": "9279-1",
        "unit": "breaths/min",
        "unit_code": "/min",
        "min": 2,
        "max": 80
    },
    "temp_c": {
        "meaning": "Temperature Celsius",
        "loinc": "8310-5",
        "unit": "Cel",
        "unit_code": "Cel",
        "min": 30,
        "max": 45
    }
}


def fhir_resource_exists(resource_type: str, resource_id: str) -> bool:
    response = requests.get(
        f"{FHIR_BASE_URL}/{resource_type}/{resource_id}",
        headers={"Accept": "application/fhir+json"},
        timeout=10
    )

    return response.status_code == 200


def make_fhir_observation(
    measurement_name: str,
    value: float,
    device_message: dict
) -> dict:
    device_id = device_message["device_id"]
    measurement = ALLOWED_MEASUREMENTS[measurement_name]
    fhir_device_id = KNOWN_DEVICES[device_id]["fhir_device_id"]

    return {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": measurement["loinc"],
                    "display": measurement["meaning"]
                }
            ],
            "text": measurement["meaning"]
        },
        "subject": {
            "reference": f"Patient/{DEFAULT_PATIENT_ID}"
        },
        "device": {
            "reference": f"Device/{fhir_device_id}"
        },
        "effectiveDateTime": device_message["timestamp"],
        "valueQuantity": {
            "value": value,
            "unit": measurement["unit"],
            "system": "http://unitsofmeasure.org",
            "code": measurement["unit_code"]
        }
    }


def post_observation_to_fhir(observation: dict) -> dict:
    response = requests.post(
        f"{FHIR_BASE_URL}/Observation",
        json=observation,
        headers={"Content-Type": "application/fhir+json"},
        timeout=10
    )

    if response.status_code not in [200, 201]:
        return {
            "status": "failed",
            "status_code": response.status_code,
            "error": response.text
        }

    created_observation = response.json()

    return {
        "status": "created",
        "observation_id": created_observation.get("id")
    }


@app.post("/device-event")
async def receive_device_event(device_message: dict = Body(...)):
    required_fields = ["device_id", "timestamp", "measurements"]
    missing_fields = []

    for field in required_fields:
        if field not in device_message:
            missing_fields.append(field)

    if missing_fields:
        return {
            "status": "rejected",
            "reason": "missing_required_fields",
            "missing_fields": missing_fields
        }

    device_id = device_message["device_id"]

    if device_id not in KNOWN_DEVICES:
        print(f"Rejected unknown device_id: {device_id}")
        return {
            "status": "rejected",
            "reason": "unknown_device_id",
            "device_id": device_id
        }

    print("Received valid-looking device message:")
    print(device_message)

    measurements = device_message["measurements"]

    if not isinstance(measurements, dict):
        return {
            "status": "rejected",
            "reason": "measurements_not_object"
        }

    for measurement_name, value in measurements.items():
        if measurement_name not in ALLOWED_MEASUREMENTS:
            return {
                "status": "rejected",
                "reason": "unknown_measurement",
                "measurement": measurement_name
            }

        if not isinstance(value, (int, float)):
            return {
                "status": "rejected",
                "reason": "measurement_value_not_number",
                "measurement": measurement_name,
                "value": value
            }

        allowed = ALLOWED_MEASUREMENTS[measurement_name]

        if value < allowed["min"] or value > allowed["max"]:
            return {
                "status": "rejected",
                "reason": "measurement_out_of_range",
                "measurement": measurement_name,
                "value": value,
                "min": allowed["min"],
                "max": allowed["max"]
            }

    print("Received valid measurements:")
    print(measurements)

    fhir_device_id = KNOWN_DEVICES[device_id]["fhir_device_id"]

    missing_dependencies = []

    if not fhir_resource_exists("Patient", DEFAULT_PATIENT_ID):
        missing_dependencies.append(f"Patient/{DEFAULT_PATIENT_ID}")

    if not fhir_resource_exists("Device", fhir_device_id):
        missing_dependencies.append(f"Device/{fhir_device_id}")

    if missing_dependencies:
        return {
            "status": "rejected",
            "reason": "missing_fhir_dependencies",
            "missing_dependencies": missing_dependencies
        }

    fhir_observations = []
    fhir_post_results = []

    for measurement_name, value in measurements.items():
        observation = make_fhir_observation(
            measurement_name,
            value,
            device_message
        )

        fhir_observations.append(observation)

        post_result = post_observation_to_fhir(observation)
        fhir_post_results.append(post_result)

    return {
        "status": "received",
        "message": "Device message passed validation, dependencies were found, was mapped to FHIR, and was sent to HAPI FHIR",
        "received_message": device_message,
        "fhir_post_results": fhir_post_results,
        "fhir_observations": fhir_observations
    }

