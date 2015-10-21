#!/usr/bin/env python3
#########################################################################
#  Copyright 2015 Sebastian Kuhn                  sebastian@derseppel.net
#########################################################################
#  This file is part of SmartHome.py.    http://mknx.github.io/smarthome/
#
#  SmartHome.py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHome.py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHome.py. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import logging
from influxdb import InfluxDBClient


logger = logging.getLogger('')


class InfluxDB():
  def __init__(self, smarthome, influx_host='localhost', influx_port=8086, influx_user='root', influx_pass='root', influx_db='smarthome', influx_keyword='influxdb', influx_update_cyle=10 ):
    logger.warn('Init InfluxDB')
    self._sh = smarthome
    self.influx_host = influx_host
    self.influx_port = influx_port
    self.influx_user = influx_user
    self.influx_pass = influx_pass
    self.influx_db = influx_db
    self.influx_keyword = influx_keyword
    self.influx_update_cyle = influx_update_cyle
    self.client = None
    self._items = []

    # connect to DB
    self.client = InfluxDBClient(self.influx_host, self.influx_port, self.influx_user, self.influx_pass, self.influx_db)
    logger.debug("InfluxDBClient("+self.influx_host+", "+str(self.influx_port)+", "+self.influx_user+", "+self.influx_pass+", "+self.influx_db+")")
    # check if database already exists, if not - create it
    exists = False
    dbs = self.client.get_list_database()
    for db in dbs:
      if db['name'] == self.influx_db:
        exists = True

    if exists == False:
      logger.debug('Database' + self.influx_db + ' does not exist, creating it.')
      self.client.create_database( self.influx_db)
    else:
      logger.debug('Database' + self.influx_db + ' exists')

      
  def run(self):
    self.alive = True
    self._sh.scheduler.add('InfluxDB', self._update_values, prio=5, cycle=self.influx_update_cyle)

  def stop(self):
    self.alive = False

  def parse_item(self, item):
    if self.influx_keyword in item.conf:
      if item.type() not in ['num', 'bool']:
        logger.debug("InfluxDB: only supports 'num' and 'bool' as types. Item: {} ".format(item.id()))
        return
      self._items.append(item)
      return self.update_item


  def update_item(self, item, caller=None, source=None, dest=None):
    logger.debug('InfluxDB, update item called')
    json_body = [
    {
        "measurement": item.id(),
        "tags": {
            "caller": caller,
        },
        "fields": {
            "value": float(item())
        }
    }
    ]
    self.client.write_points(json_body)    
    return None

  def _update_values(self):
    return None
