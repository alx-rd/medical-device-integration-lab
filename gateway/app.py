from fastapi import FastAPI, Body

app = FastAPI()

KNOWN_DEVICES = {
    "MON-001": {
        "fhir_device_id": "mon-001",
        "display": "Fake Vital Signs Monitor 001"
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

    return {
        "status": "received",
        "message": "Device message passed basic required-field validation",
        "received_message": device_message
    }