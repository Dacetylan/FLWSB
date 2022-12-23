# Frontend

## Grafana

### Introduction

### InfluxDb as Data Source

https://grafana.com/docs/grafana/latest/datasources/influxdb/

Use Flux as Query language.
Gives the use of token's instead of username and password -> safer

URL: http://influxdb:8086

### Provisioning

https://grafana.com/docs/grafana/latest/administration/provisioning/

Provisioning in Grafana is a way to manage and configure settings, from Data Sources to Dashboards, with the use of YAML files.

#### Data Sources

https://grafana.com/docs/grafana/latest/administration/provisioning/#data-sources

```yaml
apiVersion: 1

datasources:
  - name: InfluxDB_v2_Flux
    type: influxdb
    access: proxy
    url: http://influxdb:8086
    jsonData:
      version: Flux
      organization: ap
      defaultBucket: flwsb
      tlsSkipVerify: true
    secureJsonData:
      token: <Grafana token>
```

#### Dashboards
