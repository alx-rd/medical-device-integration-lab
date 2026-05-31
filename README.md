# Medical Device Integration Lab

A homelab project for learning bedside medical device integration concepts using synthetic patients, simulated vital-sign devices, a custom device gateway, Open Integration Engine, FHIR mapping, HAPI FHIR, and future monitoring/logging components.

## Purpose

This project simulates a basic medical device integration pipeline:

```text
Synthetic patient data
    ↓
Simulated bedside monitor
    ↓
Custom device gateway
    ↓
Validation and FHIR mapping
    ↓
Open Integration Engine
    ↓
HAPI FHIR server
    ↓
Future dashboard, logs, and alerts
```

The goal is to learn the core concepts behind bedside medical device integration, including device data capture, device identity validation, measurement validation, patient-device association, FHIR Observation mapping, interface-engine routing, dependency checking, error handling, and monitoring.

This project is inspired by real bedside medical device integration patterns, but it is not a replacement for a real medical device integration platform.

## Current Architecture

The current lab architecture is:

```text
Raw device event
    ↓
FastAPI gateway
    ↓
Required-field validation
    ↓
Known-device validation
    ↓
Measurement validation
    ↓
FHIR Observation mapping
    ↓
HAPI FHIR
```

The gateway currently receives raw simulated device messages like:

```json
{
  "device_id": "MON-001",
  "timestamp": "2026-05-30T12:00:00Z",
  "measurements": {
    "hr": 84,
    "spo2": 97
  }
}
```

It validates the message, maps each measurement into a FHIR Observation, and posts the Observation resources to HAPI FHIR.

The next architecture change is to place **Open Integration Engine** between the custom gateway and HAPI FHIR.

## Planned Architecture

Short-term target:

```text
Simulated bedside monitor
        ↓
Custom gateway
        ↓
Validation, mapping, and dependency checking
        ↓
HAPI FHIR server
        ↓
Logs and troubleshooting output
```

Interface-engine target:

```text
Simulated bedside monitor
        ↓
Custom gateway / mini device integration layer
        ↓
Open Integration Engine
        ↓
HAPI FHIR server
        ↓
Dashboard, logs, alerts, and incident runbooks
```

In this model:

* The **simulated bedside monitor** generates fake raw device data.
* The **custom gateway** validates device identity, measurements, and FHIR dependencies.
* The **custom gateway** maps raw measurements into FHIR Observation JSON.
* **Open Integration Engine** acts as the interface engine layer.
* **HAPI FHIR** acts as the FHIR server / fake EHR backend.
* Future logging and dashboards will help monitor accepted, rejected, and failed events.

## Planned Components

* Python vital signs simulator
* FastAPI device gateway service
* Device inventory / known-device validation
* Measurement validation and range checking
* FHIR Observation mapping
* Open Integration Engine
* HAPI FHIR server
* Patient-device association table
* Dependency checking for required FHIR resources
* Logging for accepted, rejected, and failed events
* PostgreSQL database
* Grafana dashboard
* HL7 ORU message examples
* Incident response runbooks
* Validation and testing documentation
* Future openEHR exploration as a separate learning path

## Safety and Privacy Rules

This project is for learning only.

Do not use:

* Real patient data
* Production healthcare data
* Real medical device output
* Proprietary Oracle/Cerner documentation
* Internal work screenshots
* Credentials, tokens, passwords, or `.env` files

All patients, encounters, devices, vitals, and clinical data in this project should be synthetic or fictional.

## Learning Goals

By building this lab, I want to practice:

* Medical device integration concepts
* FHIR Patient, Device, Encounter, Location, and Observation resources
* FHIR Observation mapping
* LOINC coding for vital signs
* UCUM units for clinical measurements
* Raw device event validation
* Known-device validation
* Measurement range validation
* Dependency checking before posting clinical observations
* Device-to-patient association workflows
* Data validation and rejection handling
* API development with FastAPI
* Healthcare interface-engine concepts
* Open Integration Engine routing and channel configuration
* Healthcare integration troubleshooting
* Synthetic clinical data generation
* Healthcare integration documentation
* Incident runbook creation

## Roadmap

### Phase 1 — Basic FHIR Setup

* Deploy HAPI FHIR with Docker
* Create a synthetic Patient resource
* Create a synthetic Device resource
* POST a basic vital-sign Observation
* Confirm Patient, Device, and Observation resources can be queried

### Phase 2 — Static FHIR Examples

* Create example FHIR JSON resources
* Add Patient, Device, and Observation examples
* Use PowerShell to send example resources to HAPI FHIR
* Document how each FHIR resource relates to the others

### Phase 3 — Basic Device Simulator

* Build a Python vital signs simulator
* Generate heart rate, SpO2, respiratory rate, and temperature
* Initially send FHIR Observations directly to HAPI FHIR
* Use this phase to understand FHIR Observation structure

### Phase 4 — Gateway Receiver

* Build a FastAPI gateway service
* Create a `POST /device-event` endpoint
* Receive raw simulated device messages
* Return accepted or rejected responses
* Test the gateway using FastAPI docs and PowerShell

### Phase 5 — Gateway Validation

* Validate required fields:

  * `device_id`
  * `timestamp`
  * `measurements`
* Validate known device IDs
* Validate measurement names
* Validate numeric measurement values
* Validate measurement ranges
* Reject malformed, unknown, or unsafe messages

### Phase 6 — FHIR Observation Mapping

* Convert validated raw measurements into FHIR Observations
* Map raw fields such as `hr`, `spo2`, `rr`, and `temp_c` to LOINC-coded FHIR Observations
* Link Observations to Patient and Device references
* Return generated FHIR Observations in the gateway response

### Phase 7 — Send Gateway Output to HAPI FHIR

* POST generated FHIR Observations from the gateway to HAPI FHIR
* Return created Observation IDs
* Handle failed FHIR posts
* Confirm Observations appear in HAPI FHIR

### Phase 8 — Dependency Checking

* Check whether required downstream FHIR resources exist before posting Observations
* Verify that the referenced Patient exists
* Verify that the referenced Device exists
* Reject messages with a clear dependency error if required resources are missing
* Prevent avoidable FHIR post failures

### Phase 9 — Patient-Device Association

* Create a simple association table
* Associate a device to a patient and encounter
* Prevent charting when no valid association exists
* Log association and disassociation events
* Replace hard-coded patient references with association-based lookup

### Phase 10 — Logging and Error Handling

* Log accepted events
* Log rejected events
* Log failed FHIR posts
* Track created Observation IDs
* Add basic troubleshooting output
* Create incident runbooks for common failures

### Phase 11 — Open Integration Engine

* Add Open Integration Engine to the Docker environment
* Create an HTTP listener channel
* Configure the gateway to send mapped FHIR Observations to Open Integration Engine
* Configure Open Integration Engine to forward FHIR Observations to HAPI FHIR
* Practice channel routing, error queues, retry behavior, and interface monitoring

Target architecture for this phase:

```text
Simulated device
    ↓
Custom gateway
    ↓
Open Integration Engine
    ↓
HAPI FHIR
```

### Phase 12 — HL7 Practice

* Generate sample HL7 ORU^R01 messages
* Map OBX segments to FHIR Observations
* Practice interface-engine style troubleshooting
* Compare HL7-style workflows with FHIR API workflows

### Phase 13 — Monitoring and Alerts

* Add PostgreSQL logging
* Add Grafana dashboards
* Track message counts, failures, latency, and device status
* Simulate device outages and bad data
* Monitor rejected events and downstream FHIR failures

### Phase 14 — openEHR Exploration

openEHR may be explored later as a separate clinical data modeling topic.

Possible future comparison:

```text
FHIR Observation storage in HAPI FHIR
vs
openEHR composition storage in an openEHR-compatible platform
```

## Disclaimer

This project is not a medical product, clinical tool, or replacement for a real medical device integration platform. It is a learning lab using synthetic data only.
