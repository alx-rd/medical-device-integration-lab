from fastapi import FastAPI, Body

app = FastAPI()

KNOWN_DEVICES = {
    "MON-001": {
        "fhir_device_id": "mon-001",
        "display": "Fake Vital Signs Monitor 001"
    }
}

ALLOWED_MEASUREMENTS = {
    "hr": {

        "meaning": "Heart Rate",
        "min": 20,
        "max":250
    },

    "spo2": {

        "meaning": "Oxygen Saturation",
        "min": 50,
        "max":100
    },

    "rr": {

        "meaning": "Respiratory Rate",
        "min": 2,
        "max":80
    },

    "temp_c": {

        "meaning": "Temperature Celsius",
        "min": 30,
        "max": 45
    }
    
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

    return {
        "status": "received",
        "message": "Device message passed device and measurement validation",
        "received_message": device_message
    }