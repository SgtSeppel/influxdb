# smarthome-influxdb
Plugin to store data from smarthome.py in a InfluxDB i.e. for graphing with Grafana.


## Dependencies
At the moment I did not want to write the influxDB handling from scratch. Therefore the plugin uses the influxDB python client.
You can install it with
<pre>
pip install influxdb
</pre>

six is a known troublemaker in connection with smarthome.py. During my tests this lib did not lead to any problems.

If you get error messages referring to six, dateutils and tz, then try installing them via <pre>apt-get install python-dateutil python3-tz</pre>

## Configuration
### plugin.conf
<pre>
[influxdb]
    class_name = InfluxDB
    class_path = plugins.influx
#   influx_host = localhost
#   influx_port = 8083
#   influx_user = root
#   influx_pass = root
#   influx_db   = smarthome
    influx_keyword = influx
</pre>

### plugin.conf
The configuration flag influx_keyword has a special relevance. Here you can choose which keyword the plugin should look for.
If you do not specify anything, the default keyword "influx" will be use i.e.:

<pre>
[['aussentemperatur']]
    name = Außentemperatur
    type = num
    knx_dpt = 9
    influx = true
    visu_acl = true
    knx_send = 7/0/0
    knx_reply = 7/0/0
    cache = on
</pre>

However, you can change this. Many people use the sqlite keyword to store data in a sqlite database.
If you set 
<pre>
influx_keyword = sqlite
</pre>
you do not have to update anything in your item configuration files. All data thats pushed to sqlite (i.e. for smartVISU) will automatically be copied to InfluxDB also.
