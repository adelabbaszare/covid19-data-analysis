# CSV Schema Analysis

Historical COVID-19 daily reports changed column names over time.

| Historical column | Canonical column |
|---|---|
| Province/State | Province_State |
| Country/Region | Country_Region |
| Last Update | Last_Update |
| Latitude | Lat |
| Longitude | Long_ |
| Incidence_Rate | Incident_Rate |
| Case-Fatality_Ratio | Case_Fatality_Ratio |

Every CSV is normalized before concatenation. When both variants exist, values are coalesced into the canonical column. The loader also adds `Source_File` for traceability.
