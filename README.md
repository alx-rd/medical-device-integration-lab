# Medical Device Integration Lab

A homelab project for learning bedside medical device integration concepts using synthetic patients, simulated vital-sign devices, HL7/FHIR mapping, HAPI FHIR, PostgreSQL, and Grafana.

## Purpose

This project simulates a basic medical device integration pipeline:

```text
Synthetic patient data
    ↓
Simulated bedside monitor
    ↓
Device gateway / adapter
    ↓
FHIR or HL7 mapping
    ↓
FHIR server / dashboard
```

The goal is to learn the core concepts behind bedside medical device integration, including device data capture, patient-device association, observation mapping, interface validation, error handling, and monitoring.

## Planned Components

* Python vital signs simulator
* Device gateway service
* Patient-device association table
* HAPI FHIR server
* PostgreSQL database
* Grafana dashboard
* HL7 ORU message examples
* FHIR Observation examples
* Incident response runbooks
* Validation and testing documentation

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

## Target Architecture

```text
Fake bedside monitor
        ↓
Device gateway
        ↓
Validation and mapping layer
        ↓
FHIR server / HL7 output
        ↓
Dashboard, logs, and alerts
```

## Learning Goals

By building this lab, I want to practice:

* Medical device integration concepts
* HL7 v2 ORU message structure
* FHIR Patient, Encounter, Device, Location, and Observation resources
* Device-to-patient association workflows
* Data validation and rejection handling
* Interface monitoring and troubleshooting
* Synthetic clinical data generation
* Healthcare integration documentation
* Incident runbook creation

## Roadmap

### Phase 1 — Basic FHIR Setup

* Deploy HAPI FHIR
* Create a synthetic Patient
* Create a synthetic Device
* POST a basic vital-sign Observation

### Phase 2 — Device Simulator

* Build a Python vital signs simulator
* Generate heart rate, SpO2, respiratory rate, temperature, and blood pressure
* Send fake device messages to a gateway service

### Phase 3 — Gateway and Validation

* Receive fake device events
* Validate device ID, timestamp, values, and units
* Normalize device data
* Reject malformed or unsafe messages

### Phase 4 — Patient-Device Association

* Create an association table
* Associate a device to a patient and encounter
* Prevent charting when no valid association exists
* Log association and disassociation events

### Phase 5 — FHIR Observation Mapping

* Convert validated device data into FHIR Observations
* Link Observations to Patient, Encounter, Device, and Location
* Query Observations by patient and device

### Phase 6 — HL7 Practice

* Generate sample HL7 ORU^R01 messages
* Map OBX segments to FHIR Observations
* Practice basic interface-engine style troubleshooting

### Phase 7 — Monitoring and Alerts

* Add PostgreSQL logging
* Add Grafana dashboards
* Track message counts, failures, latency, and device status
* Simulate device outages and bad data

## Disclaimer

This project is not a medical product, clinical tool, or replacement for a real medical device integration platform. It is a learning lab using synthetic data only.
