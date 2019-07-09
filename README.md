# misp2elastic
Dockerized method to pull threat intel from MISP and use it to enrich Elasticsearch data via Logstash and Memcached 

NOTE: This has only been tested in a standalone configuration with Security Onion

`wget https://raw.githubusercontent.com/weslambert/misp2elastic/master/install_misp2elastic && sudo chmod +x install_misp2elastic && sudo ./install_misp2elastic`

Modify `/etc/misp2elastic/misp2elastic.conf` with appropriate connection details (URL/APIKEY).`

Bring up services with `sudo docker-compose -f /opt/misp2elastic/docker-compose.yaml up -d`

Restart Logstash with `so-logstash-restart`

Once Logstash has restarted and pulled in the new config, check to see if entries are populated in Memcached:

`echo "stats cachedump 1 0" | nc localhost 11211`

If entries are present, then if there are matches in the Logstash pipeline according to the lookups defined in `/etc/logstash/custom/8300_postprocess_misp_tagging.conf`, you should see a tag appended to events with matches, as well as a field called `misp_match`.  You will also need to refresh the field list for the index pattern in Kibana (Management -> Index Patterns) in order to search on the `misp_match` field and use it for visualizations, etc.

