#!/bin/bash

### Populate db with python script
## Mark python script as executable
chmod +x /influxdb-testdata/testdata-populate.py
## Running it
python /influxdb-testdata/testdata-populate.py

### Restore data from backup (not working)
## Make backup with: docker exec -it baavend-db bash
## influx backup /data-backups/testdata -t <root-token>
## influx backup /data-backups/$(date '+%Y-%m-%d_%H-%M') -t <root-token>
# influx restore /data-backups/testdata --bucket flwsb