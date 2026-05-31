# Gateway Design

1. What should the simulator send to the gateway?
2. What should the gateway validate?
3. What should the gateway create before sending to HAPI FHIR?
4. What should happen if the device ID is unknown?
5. What should happen if a vital value is outside a safe range?

1. The simulator sends raw device messages with device_id, timestamp, and measurements.
2. The gateway validates structure, known device ID, timestamp, measurement names, values, and patient-device association.
3. The gateway converts accepted measurements into FHIR Observation JSON.
4. Unknown devices are rejected and not forwarded to HAPI FHIR.
5. Impossible values are rejected; abnormal-but-possible values may be forwarded and flagged.

Input:
  raw device message

Gateway logic:
  receive message
  check device_id
  check measurements
  map measurements to FHIR
  send Observations to HAPI FHIR

Output:
  FHIR Observations in HAPI FHIR