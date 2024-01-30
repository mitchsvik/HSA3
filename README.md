# Example of using TIG stack for monitoring web application

This an example project to show the TIG (Telegraf, InfluxDB and Grafana) stack.

## Start the stack with docker compose

```bash
$ docker-compose up
```

## Possible solutions of docker permissions for telegraf

https://github.com/influxdata/telegraf/blob/master/plugins/inputs/docker/README.md#docker-daemon-permissions

## Services and Ports

### Grafana
- URL: http://localhost:8081 
- User: admin
- Default pass: admin

### Telegraf
- Monitoring NGINX, ElasticSearch and MongoDB

### InfluxDB
- Port: 8086 (HTTP API)
- User: admin
- Database: influx

## Examples

Examples of monitoring during loading produced by Siege

#### NGINX
![Example NGINX](./NGINX_check.png?raw=true "Example NGINX")

#### ElasticSearch
![Example ElasticSearch](./Elastic_check.png?raw=true "Example ElasticSearch")

#### MongoDB
![Example MongoDB](./Mongo_check.png?raw=true "Example MongoDB")

#### CPU
![Example CPU](./CPU_check.png?raw=true "Example CPU")

#### IOPS
![Example IOPS](./IOPS_check.png?raw=true "Example IOPS")
