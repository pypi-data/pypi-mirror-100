# -*- coding: utf-8 -*-

import atexit
import inspect
import json
import logging
import random
import re
import socket
import time
import xml.etree.ElementTree as ElementTree
from threading import Lock
from threading import Thread
from threading import Timer
from urllib.parse import urlparse

import yqn_project_cli.rpc.eureka.eureka_request as urllib2

long = int

_logger = logging.getLogger("EurekaClient")

"""
Status of instances
"""
INSTANCE_STATUS_UP = "UP"
INSTANCE_STATUS_DOWN = "DOWN"
INSTANCE_STATUS_STARTING = "STARTING"
INSTANCE_STATUS_OUT_OF_SERVICE = "OUT_OF_SERVICE"
INSTANCE_STATUS_UNKNOWN = "UNKNOWN"

"""
Action type of instances
"""
ACTION_TYPE_ADDED = "ADDED"
ACTION_TYPE_MODIFIED = "MODIFIED"
ACTION_TYPE_DELETED = "DELETED"

""" 
This is for the DiscoveryClient, when this strategy is set, get_service_url will random choose one of the UP instance and return its url
This is the default strategy
"""
HA_STRATEGY_RANDOM = 1
"""
This is for the DiscoveryClient, when this strategy is set, get_service_url will always return one instance until it is down
"""
HA_STRATEGY_STICK = 2
"""
This is for the DiscoveryClient, when this strategy is set, get_service_url will always return a new instance if any other instances are up
"""
HA_STRATEGY_OTHER = 3

"""
The timeout seconds that all http request to the eureka server
"""
_DEFAULT_TIME_OUT = 5
"""
Default eureka server url.
"""
_DEFAULT_EUREKA_SERVER_URL = "http://127.0.0.1:8761/eureka/"
"""
Default instance field values
"""
_DEFAULT_INSTANCE_PORT = 9090
_DEFAULT_INSTANCE_SECURE_PORT = 9443
_RENEWAL_INTERVAL_IN_SECS = 30
_DURATION_IN_SECS = 90
_DEFAULT_DATA_CENTER_INFO = "MyOwn"
_DEFAULT_DATA_CENTER_INFO_CLASS = "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo"
"""
Default encoding
"""
_DEFAULT_ENCODING = "utf-8"


# =========================> Base Mehods <========================================
# Beans


class Applications:

    def __init__(self,
                 apps_hashcode="",
                 versions_delta="",
                 applications=None):
        self.apps_hashcode = apps_hashcode
        self.versions_delta = versions_delta
        self._applications = applications if applications is not None else []
        self._application_name_dic = {}
        self._app_lock = Lock()

    @property
    def hashcode(self):
        return self.apps_hashcode

    @property
    def applications(self):
        return self._applications

    @property
    def version(self):
        return self.versions_delta

    def add_application(self, application):
        with self._app_lock:
            self._applications.append(application)
            self._application_name_dic[application.name] = application

    def get_application(self, app_name):
        with self._app_lock:
            if app_name in self._application_name_dic:
                return self._application_name_dic[app_name]
            else:
                return Application(name=app_name)


class Application:

    def __init__(self,
                 name="",
                 instances=None):
        self.name = name
        self.__instances = instances if instances is not None else []
        self.__instances_dict = {}
        self.__inst_lock = Lock()

    @property
    def instances(self):
        with self.__inst_lock:
            return self.__instances

    @property
    def up_instances(self):
        with self.__inst_lock:
            up_inst = []
            for item in self.__instances:
                if item.status == INSTANCE_STATUS_UP:
                    up_inst.append(item)
            return up_inst

    def get_instance(self, instance_id):
        with self.__inst_lock:
            if instance_id in self.__instances_dict:
                return self.__instances_dict[instance_id]
            else:
                return None

    def add_instance(self, instance):
        with self.__inst_lock:
            self.__instances.append(instance)
            self.__instances_dict[instance.instance_id] = instance

    def update_instance(self, instance):
        with self.__inst_lock:
            _logger.debug("update instance %s" % instance.instance_id)
            updated = False
            for idx in range(len(self.__instances)):
                ele = self.__instances[idx]
                if ele.instance_id == instance.instance_id:
                    _logger.debug("updating index %d" % idx)
                    self.__instances[idx] = instance
                    updated = True
                    break

            if not updated:
                self.add_instance(instance)

    def remove_instance(self, instance):
        with self.__inst_lock:
            for idx in range(len(self.__instances)):
                ele = self.__instances[idx]
                if ele.instance_id == instance.instance_id:
                    del self.__instances[idx]
                    break
            if instance.instance_id in self.__instances_dict:
                del self.__instances_dict[instance.instance_id]


class LeaseInfo:

    def __init__(self,
                 renewal_interval_sec=_RENEWAL_INTERVAL_IN_SECS,
                 duration_sec=_DURATION_IN_SECS,
                 registration_timestamp=0,
                 last_renewal_timestamp=0,
                 renewal_timestamp=0,
                 eviction_timestamp=0,
                 service_up_timestamp=0):
        self.renewal_interval_sec = renewal_interval_sec
        self.duration_sec = duration_sec
        self.registration_timestamp = registration_timestamp
        self.last_renewal_timestamp = last_renewal_timestamp
        self.renewal_timestamp = renewal_timestamp
        self.eviction_timestamp = eviction_timestamp
        self.service_up_timestamp = service_up_timestamp


class DataCenterInfo:

    def __init__(self,
                 name=_DEFAULT_DATA_CENTER_INFO,  # Netflix, Amazon, MyOwn
                 class_name=_DEFAULT_DATA_CENTER_INFO_CLASS):
        self.name = name
        self.class_name = class_name


class PortWrapper:
    def __init__(self, port=0, enabled=False):
        self.port = port
        self.enabled = enabled


class Instance:

    def __init__(self,
                 instance_id="",
                 sid="",  # @deprecated
                 app="",
                 app_group_name="",
                 ip_addr="",
                 port=PortWrapper(port=_DEFAULT_INSTANCE_PORT, enabled=True),
                 secure_port=PortWrapper(port=_DEFAULT_INSTANCE_SECURE_PORT, enabled=False),
                 home_page_url="",
                 status_page_url="",
                 health_check_url="",
                 secure_health_check_url="",
                 vip_address="",
                 secure_vip_address="",
                 country_id=1,
                 data_center_info=DataCenterInfo(),
                 host_name="",
                 status="",  # UP, DOWN, STARTING, OUT_OF_SERVICE, UNKNOWN
                 overridden_status="",  # UP, DOWN, STARTING, OUT_OF_SERVICE, UNKNOWN
                 lease_info=LeaseInfo(),
                 is_coordinating_discovery_server=False,
                 metadata=None,
                 last_updated_timestamp=0,
                 last_dirty_timestamp=0,
                 action_type=ACTION_TYPE_ADDED,  # ADDED, MODIFIED, DELETED
                 asg_name=""):
        self.instance_id = instance_id
        self.sid = sid
        self.app = app
        self.app_group_name = app_group_name
        self.ip_addr = ip_addr
        self.port = port
        self.secure_port = secure_port
        self.home_page_url = home_page_url
        self.status_page_url = status_page_url
        self.health_check_url = health_check_url
        self.secure_health_check_url = secure_health_check_url
        self.vip_address = vip_address
        self.secure_vip_address = secure_vip_address
        self.countryId = country_id
        self.data_center_info = data_center_info
        self.host_name = host_name
        self.status = status
        self.overridden_status = overridden_status
        self.lease_info = lease_info
        self.is_coordinating_discovery_server = is_coordinating_discovery_server
        self.metadata = metadata if metadata is not None else {}
        self.last_updated_timestamp = last_updated_timestamp
        self.last_dirty_timestamp = last_dirty_timestamp
        self.action_type = action_type
        self.asg_name = asg_name


# Basic functions #################################
# Registry functions
def register(eureka_server, instance):
    instance_dic = {
        'instanceId': instance.instance_id,
        'hostName': instance.host_name,
        'app': instance.app,
        'ipAddr': instance.ip_addr,
        'status': instance.status,
        'overriddenstatus': instance.overridden_status,
        'port': {
            '$': instance.port.port,
            '@enabled': str(instance.port.enabled).lower()
        },
        'securePort': {
            '$': instance.secure_port.port,
            '@enabled': str(instance.secure_port.enabled).lower()
        },
        'countryId': instance.countryId,
        'dataCenterInfo': {
            '@class': instance.data_center_info.class_name,
            'name': instance.data_center_info.name
        },
        'leaseInfo': {
            'renewalIntervalInSecs': instance.lease_info.renewal_interval_sec,
            'durationInSecs': instance.lease_info.duration_sec,
            'registrationTimestamp': instance.lease_info.registration_timestamp,
            'lastRenewalTimestamp': instance.lease_info.last_renewal_timestamp,
            'evictionTimestamp': instance.lease_info.eviction_timestamp,
            'serviceUpTimestamp': instance.lease_info.service_up_timestamp
        },
        'metadata': instance.metadata,
        'homePageUrl': instance.home_page_url,
        'statusPageUrl': instance.status_page_url,
        'healthCheckUrl': instance.health_check_url,
        'vipAddress': instance.vip_address,
        'secureVipAddress': instance.secure_vip_address,
        'lastUpdatedTimestamp': str(instance.last_updated_timestamp),
        'lastDirtyTimestamp': str(instance.last_dirty_timestamp),
        'isCoordinatingDiscoveryServer': str(instance.is_coordinating_discovery_server).lower()
    }
    _register(eureka_server, instance_dic)


def _register(eureka_server, instance_dic):
    req = urllib2.Request(_format_url(eureka_server) + "apps/%s" % instance_dic["app"])
    req.add_header('Content-Type', 'application/json')
    req.get_method = lambda: "POST"
    response = urllib2.urlopen(req,
                               json.dumps({"instance": instance_dic}).encode(_DEFAULT_ENCODING),
                               timeout=_DEFAULT_TIME_OUT)
    response.close()


def cancel(eureka_server, app_name, instance_id):
    req = urllib2.Request(_format_url(eureka_server) + "apps/%s/%s" % (app_name, instance_id))
    req.get_method = lambda: "DELETE"
    response = urllib2.urlopen(req, timeout=_DEFAULT_TIME_OUT)
    response.close()


def send_heart_beat(eureka_server,
                    app_name,
                    instance_id,
                    last_dirty_timestamp,
                    status=INSTANCE_STATUS_UP,
                    overridden_status=""):
    url = _format_url(eureka_server) + "apps/%s/%s?status=%s&lastDirtyTimestamp=%s" % \
          (app_name, instance_id, status, str(last_dirty_timestamp))
    _logger.debug("heartbeat url::" + url)
    if overridden_status != "":
        url += "&overriddenstatus=" + overridden_status

    req = urllib2.Request(url)
    req.get_method = lambda: "PUT"
    response = urllib2.urlopen(req, timeout=_DEFAULT_TIME_OUT)
    response.close()


def status_update(eureka_server, app_name, instance_id, last_dirty_timestamp, status):
    url = _format_url(eureka_server) + "apps/%s/%s?status=%s&lastDirtyTimestamp=%s" % \
          (app_name, instance_id, status, str(last_dirty_timestamp))

    req = urllib2.Request(url)
    req.get_method = lambda: "PUT"
    response = urllib2.urlopen(req, timeout=_DEFAULT_TIME_OUT)
    response.close()


def delete_status_override(eureka_server, app_name, instance_id, last_dirty_timestamp):
    url = _format_url(eureka_server) + "apps/%s/%s/status?lastDirtyTimestamp=%s" % \
          (app_name, instance_id, str(last_dirty_timestamp))

    req = urllib2.Request(url)
    req.get_method = lambda: "DELETE"
    response = urllib2.urlopen(req, timeout=_DEFAULT_TIME_OUT)
    response.close()


# Discovory functions ########
def get_applications(eureka_server, regions=[]):
    return _get_applications_(_format_url(eureka_server) + "apps/", regions)


def _format_url(url):
    if url.endswith('/'):
        return url
    else:
        return url + "/"


def _get_applications_(url, regions=[]):
    _url = url
    if len(regions) > 0:
        _url = _url + ("&" if "?" in _url else "?") + "regions=" + (",".join(regions))

    f = urllib2.urlopen(_url, timeout=_DEFAULT_TIME_OUT)
    txt = f.read().decode(_DEFAULT_ENCODING)
    f.close()
    return _build_applications(ElementTree.fromstring(txt))


def _build_applications(xml_node):
    if xml_node.tag != "applications":
        return None
    applications = Applications()
    for child_node in xml_node.getchildren():
        if child_node.tag == "versions_delta" and child_node.text is not None:
            applications.versions_delta = child_node.text
        elif child_node.tag == "apps_hashcode" and child_node.text is not None:
            applications.apps_hashcode = child_node.text
        elif child_node.tag == "application":
            applications.add_application(_build_application(child_node))

    return applications


def _build_application(xml_node):
    if xml_node.tag != "application":
        return None
    application = Application()
    for child_node in xml_node:
        if child_node.tag == "name":
            application.name = child_node.text
        elif child_node.tag == "instance":
            application.add_instance(_build_instance(child_node))
    return application


def _build_instance(xml_node):
    if xml_node.tag != "instance":
        return None
    instance = Instance()
    for child_node in xml_node:
        if child_node.tag == "instanceId":
            instance.instance_id = child_node.text
        elif child_node.tag == "sid":
            instance.sid = child_node.text
        elif child_node.tag == "app":
            instance.app = child_node.text
        elif child_node.tag == "appGroupName":
            instance.app_group_name = child_node.text
        elif child_node.tag == "ipAddr":
            instance.ip_addr = child_node.text
        elif child_node.tag == "port":
            instance.port = _build_port(child_node)
        elif child_node.tag == "securePort":
            instance.secure_port = _build_port(child_node)
        elif child_node.tag == "homePageUrl":
            instance.home_page_url = child_node.text
        elif child_node.tag == "statusPageUrl":
            instance.status_page_url = child_node.text
        elif child_node.tag == "healthCheckUrl":
            instance.health_check_url = child_node.text
        elif child_node.tag == "secureHealthCheckUrl":
            instance.secure_health_check_url = child_node.text
        elif child_node.tag == "vipAddress":
            instance.vip_address = child_node.text
        elif child_node.tag == "secureVipAddress":
            instance.secure_vip_address = child_node.text
        elif child_node.tag == "countryId":
            instance.countryId = int(child_node.text)
        elif child_node.tag == "dataCenterInfo":
            instance.data_center_info = DataCenterInfo(name=child_node.text, class_name=child_node.attrib["class"])
        elif child_node.tag == "hostName":
            instance.host_name = child_node.text
        elif child_node.tag == "status":
            instance.status = child_node.text
        elif child_node.tag == "overriddenstatus":
            instance.overridden_status = child_node.text
        elif child_node.tag == "leaseInfo":
            instance.lease_info = _build_lease_info(child_node)
        elif child_node.tag == "isCoordinatingDiscoveryServer":
            instance.is_coordinating_discovery_server = (child_node.text == "true")
        elif child_node.tag == "metadata":
            instance.metadata = _build_metadata(child_node)
        elif child_node.tag == "lastUpdatedTimestamp":
            instance.last_updated_timestamp = long(child_node.text)
        elif child_node.tag == "lastDirtyTimestamp":
            instance.last_dirty_timestamp = long(child_node.text)
        elif child_node.tag == "actionType":
            instance.action_type = child_node.text
        elif child_node.tag == "asgName":
            instance.asg_name = child_node.text

    return instance


def _build_metadata(xml_node):
    metadata = {}
    for child_node in xml_node.getchildren():
        metadata[child_node.tag] = child_node.text
    return metadata


def _build_lease_info(xml_node):
    leaseInfo = LeaseInfo()
    for child_node in xml_node.getchildren():
        if child_node.tag == "renewalIntervalInSecs":
            leaseInfo.renewal_interval_sec = int(child_node.text)
        elif child_node.tag == "durationInSecs":
            leaseInfo.duration_sec = int(child_node.text)
        elif child_node.tag == "registrationTimestamp":
            leaseInfo.registration_timestamp = long(child_node.text)
        elif child_node.tag == "lastRenewalTimestamp":
            leaseInfo.last_renewal_timestamp = long(child_node.text)
        elif child_node.tag == "renewalTimestamp":
            leaseInfo.renewal_timestamp = long(child_node.text)
        elif child_node.tag == "evictionTimestamp":
            leaseInfo.eviction_timestamp = long(child_node.text)
        elif child_node.tag == "serviceUpTimestamp":
            leaseInfo.service_up_timestamp = long(child_node.text)

    return leaseInfo


def _build_port(xml_node):
    port = PortWrapper()
    port.port = int(xml_node.text)
    port.enabled = (xml_node.attrib["enabled"] == "true")
    return port


def get_delta(eureka_server, regions=[]):
    return _get_applications_(_format_url(eureka_server) + "apps/delta", regions)


def get_vip(eureka_server, vip, regions=[]):
    return _get_applications_(_format_url(eureka_server) + "vips/" + vip, regions)


def get_secure_vip(eureka_server, svip, regions=[]):
    return _get_applications_(_format_url(eureka_server) + "svips/" + svip, regions)


def get_application(eureka_server, app_name):
    url = _format_url(eureka_server) + "apps/" + app_name
    f = urllib2.urlopen(url, timeout=_DEFAULT_TIME_OUT)
    txt = f.read().decode(_DEFAULT_ENCODING)
    f.close()
    return _build_application(ElementTree.fromstring(txt))


def get_app_instance(eureka_server, app_name, instance_id):
    return _get_instance_(_format_url(eureka_server) + "apps/%s/%s" % (app_name, instance_id))


def get_instance(eureka_server, instance_id):
    return _get_instance_(_format_url(eureka_server) + "instances/" + instance_id)


def _get_instance_(url):
    f = urllib2.urlopen(url, timeout=_DEFAULT_TIME_OUT)
    txt = f.read().decode(_DEFAULT_ENCODING)
    f.close()
    return _build_instance(ElementTree.fromstring(txt))


def _current_time_millis():
    return int(time.time() * 1000)


"""====================== Registry Client ======================================="""


class RegistryClient:
    """Eureka client for spring cloud"""

    def __init__(self,
                 eureka_server=_DEFAULT_EUREKA_SERVER_URL,
                 app_name="",
                 instance_id="",
                 instance_host="",
                 instance_ip="",
                 instance_port=_DEFAULT_INSTANCE_PORT,
                 instance_unsecure_port_enabled=True,
                 instance_secure_port=_DEFAULT_INSTANCE_SECURE_PORT,
                 instance_secure_port_enabled=False,
                 countryId=1,  # @deprecaded
                 data_center_name=_DEFAULT_DATA_CENTER_INFO,  # Netflix, Amazon, MyOwn
                 renewal_interval_in_secs=_RENEWAL_INTERVAL_IN_SECS,
                 duration_in_secs=_DURATION_IN_SECS,
                 home_page_url="",
                 status_page_url="",
                 health_check_url="",
                 vip_adr="",
                 secure_vip_addr="",
                 is_coordinating_discovery_server=False):
        assert eureka_server is not None and eureka_server != "", "eureka server must be specified."
        assert app_name is not None and app_name != "", "application name must be specified."
        assert instance_port > 0, "port is invalid"

        self.__net_lock = Lock()
        self.__eureka_servers = eureka_server.split(",")

        def try_to_get_client_ip(url):
            url_addr = urllib2.get_url_and_basic_auth(url)[0]
            if instance_host == "" and instance_ip == "":
                self.__instance_host = self.__instance_ip = RegistryClient.__get_instance_ip(url_addr)
            elif instance_host != "" and instance_ip == "":
                self.__instance_host = instance_host
                if RegistryClient.__is_ip(instance_host):
                    self.__instance_ip = instance_host
                else:
                    self.__instance_ip = RegistryClient.__get_instance_ip(url_addr)
            else:
                self.__instance_host = instance_ip
                self.__instance_ip = instance_ip

        self.__try_all_eureka_server(try_to_get_client_ip)

        self.__instance = {
            'instanceId': instance_id if instance_id != "" else "%s:%s:%d" % (
                self.__instance_host, app_name.lower(), instance_port),
            'hostName': self.__instance_host,
            'app': app_name.upper(),
            'ipAddr': self.__instance_ip,
            'port': {
                '$': instance_port,
                '@enabled': str(instance_unsecure_port_enabled).lower()
            },
            'securePort': {
                '$': instance_secure_port,
                '@enabled': str(instance_secure_port_enabled).lower()
            },
            'countryId': countryId,
            'dataCenterInfo': {
                '@class': _DEFAULT_DATA_CENTER_INFO_CLASS,
                'name': data_center_name
            },
            'leaseInfo': {
                'renewalIntervalInSecs': renewal_interval_in_secs,
                'durationInSecs': duration_in_secs,
                'registrationTimestamp': 0,
                'lastRenewalTimestamp': 0,
                'evictionTimestamp': 0,
                'serviceUpTimestamp': 0
            },
            'metadata': {
                'management.port': str(instance_port)
            },
            'homePageUrl': RegistryClient.__format_url(home_page_url,
                                                         self.__instance_host,
                                                         instance_port),
            'statusPageUrl': RegistryClient.__format_url(status_page_url,
                                                           self.__instance_host,
                                                           instance_port,
                                                           "info"),
            'healthCheckUrl': RegistryClient.__format_url(health_check_url,
                                                            self.__instance_host,
                                                            instance_port,
                                                            "health"),
            'vipAddress': vip_adr if vip_adr != "" else app_name.lower(),
            'secureVipAddress': secure_vip_addr if secure_vip_addr != "" else app_name.lower(),
            'isCoordinatingDiscoveryServer': str(is_coordinating_discovery_server).lower()
        }

        self.__alive = False
        self.__heart_beat_timer = Timer(renewal_interval_in_secs, self.__heart_beat)
        self.__heart_beat_timer.daemon = True

    def __try_all_eureka_server(self, fun):
        with self.__net_lock:
            untry_servers = self.__eureka_servers
            tried_servers = []
            ok = False
            while len(untry_servers) > 0:
                url = untry_servers[0].strip()
                try:
                    fun(url)
                except (urllib2.HTTPError, urllib2.URLError):
                    _logger.warn("Eureka server [%s] is down, use next url to try." % url)
                    tried_servers.append(url)
                    untry_servers = untry_servers[1:]
                else:
                    ok = True
                    break
            if len(tried_servers) > 0:
                untry_servers.extend(tried_servers)
                self.__eureka_servers = untry_servers
            if not ok:
                raise urllib2.URLError("All eureka servers are down!")

    @staticmethod
    def __format_url(url, host, port, defalut_ctx=""):
        if url != "":
            if url.startswith('http'):
                _url = url
            elif url.startswith('/'):
                _url = 'http://%s:%d%s' % (host, port, url)
            else:
                _url = 'http://%s:%d/%s' % (host, port, url)
        else:
            _url = 'http://%s:%d/%s' % (host, port, defalut_ctx)
        return _url

    @staticmethod
    def __is_ip(ip_str):
        return re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_str)

    @staticmethod
    def __get_instance_ip(eureka_server):
        _target_ = eureka_server
        if not _target_.endswith('/'):
            _target_ += '/'
        url_obj = urlparse(_target_)
        _target_ = url_obj.netloc
        _logger.debug("target eureka host::: %s" % _target_)
        if _target_.find(':') > 0:
            arr = _target_.split(':')
            target_ip = arr[0]
            target_port = int(arr[1])
        else:
            target_ip = _target_
            if url_obj.scheme == "http":
                target_port = 80
            elif url_obj.scheme == "https":
                target_port = 443
            else:
                raise Exception("Cannot parse your eureka url! ")

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target_ip, target_port))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def register(self, status=INSTANCE_STATUS_UP, overridden_status=INSTANCE_STATUS_UNKNOWN):
        self.__instance["status"] = status
        self.__instance["overriddenstatus"] = overridden_status
        self.__instance["lastUpdatedTimestamp"] = str(_current_time_millis())
        self.__instance["lastDirtyTimestamp"] = str(_current_time_millis())
        try:
            self.__try_all_eureka_server(lambda url: _register(url, self.__instance))
        except:
            _logger.exception("error!")
        else:
            self.__alive = True

    def cancel(self):
        try:
            self.__try_all_eureka_server(
                lambda url: cancel(url, self.__instance["app"], self.__instance["instanceId"]))
        except:
            _logger.exception("error!")
        else:
            self.__alive = False

    def send_heart_beat(self, overridden_status=""):
        try:
            self.__try_all_eureka_server(lambda url: send_heart_beat(url, self.__instance["app"],
                                                                     self.__instance["instanceId"],
                                                                     self.__instance["lastDirtyTimestamp"],
                                                                     status=self.__instance["status"],
                                                                     overridden_status=overridden_status))
        except:
            _logger.exception("error!")

    def status_update(self, new_status):
        self.__instance["status"] = new_status
        try:
            self.__try_all_eureka_server(
                lambda url: status_update(url, self.__instance["app"], self.__instance["instanceId"],
                                          self.__instance["lastDirtyTimestamp"], new_status))
        except:
            _logger.exception("error!")

    def delete_status_override(self):
        self.__try_all_eureka_server(lambda url: delete_status_override(
            url, self.__instance["app"], self.__instance["instanceId"], self.__instance["lastDirtyTimestamp"]))

    def start(self):
        _logger.debug("start to registry client...")
        self.register()
        self.__heart_beat_timer.daemon = True
        self.__heart_beat_timer.start()

    def stop(self):
        if self.__alive:
            _logger.debug("stopping client...")
            if self.__heart_beat_timer.isAlive():
                self.__heart_beat_timer.cancel()
            self.register(status=INSTANCE_STATUS_DOWN)
            self.cancel()

    def __heart_beat(self):
        _logger.debug("sending heart beat to spring cloud server ")
        self.send_heart_beat()
        self.__heart_beat_timer = Timer(self.__instance["leaseInfo"]["renewalIntervalInSecs"], self.__heart_beat)
        self.__heart_beat_timer.daemon = True
        self.__heart_beat_timer.start()


__cache_key = "default"
__cache_registry_clients = {}
__cache_registry_clients_lock = Lock()


def init_registry_client(eureka_server=_DEFAULT_EUREKA_SERVER_URL,
                         app_name="",
                         instance_id="",
                         instance_host="",
                         instance_ip="",
                         instance_port=_DEFAULT_INSTANCE_PORT,
                         instance_unsecure_port_enabled=True,
                         instance_secure_port=_DEFAULT_INSTANCE_SECURE_PORT,
                         instance_secure_port_enabled=False,
                         countryId=1,  # @deprecaded
                         data_center_name=_DEFAULT_DATA_CENTER_INFO,  # Netflix, Amazon, MyOwn
                         renewal_interval_in_secs=_RENEWAL_INTERVAL_IN_SECS,
                         duration_in_secs=_DURATION_IN_SECS,
                         home_page_url="",
                         status_page_url="",
                         health_check_url="",
                         vip_adr="",
                         secure_vip_addr="",
                         is_coordinating_discovery_server=False):
    with __cache_registry_clients_lock:
        client = RegistryClient(eureka_server=eureka_server,
                                app_name=app_name,
                                instance_id=instance_id,
                                instance_host=instance_host,
                                instance_ip=instance_ip,
                                instance_port=instance_port,
                                instance_unsecure_port_enabled=instance_unsecure_port_enabled,
                                instance_secure_port=instance_secure_port,
                                instance_secure_port_enabled=instance_secure_port_enabled,
                                countryId=countryId,
                                data_center_name=data_center_name,
                                renewal_interval_in_secs=renewal_interval_in_secs,
                                duration_in_secs=duration_in_secs,
                                home_page_url=home_page_url,
                                status_page_url=status_page_url,
                                health_check_url=health_check_url,
                                vip_adr=vip_adr,
                                secure_vip_addr=secure_vip_addr,
                                is_coordinating_discovery_server=is_coordinating_discovery_server)
        __cache_registry_clients[__cache_key] = client
        client.start()
        return client


def get_registry_client():
    # type (str) -> RegistryClient
    with __cache_registry_clients_lock:
        if __cache_key in __cache_registry_clients:
            return __cache_registry_clients[__cache_key]
        else:
            return None


"""======================== Cached Discovery Client ============================"""


class DiscoveryClient:
    """Discover the apps registered in spring cloud server, this class will do some cached, if you want to get the apps immediatly, use the global functions"""

    def __init__(self, eureka_server, regions=None, renewal_interval_in_secs=_RENEWAL_INTERVAL_IN_SECS,
                 ha_strategy=HA_STRATEGY_RANDOM):
        assert ha_strategy in [HA_STRATEGY_RANDOM, HA_STRATEGY_STICK,
                               HA_STRATEGY_OTHER], "do not support strategy %d " % ha_strategy
        self.__eureka_servers = eureka_server.split(",")
        self.__regions = regions if regions is not None else []
        self.__cache_time_in_secs = renewal_interval_in_secs
        self.__applications = None
        self.__delta = None
        self.__ha_strategy = ha_strategy
        self.__ha_cache = {}
        self.__timer = Timer(self.__cache_time_in_secs, self.__heartbeat)
        self.__timer.daemon = True
        self.__application_mth_lock = Lock()
        self.__net_lock = Lock()

    def __heartbeat(self):
        self.__fetch_delta()
        self.__timer = Timer(self.__cache_time_in_secs, self.__heartbeat)
        self.__timer.daemon = True
        self.__timer.start()

    @property
    def applications(self):
        with self.__application_mth_lock:
            if self.__applications is None:
                self.__pull_full_registry()
            return self.__applications

    def __try_all_eureka_server(self, fun):
        with self.__net_lock:
            untry_servers = self.__eureka_servers
            tried_servers = []
            ok = False
            while len(untry_servers) > 0:
                url = untry_servers[0].strip()
                try:
                    fun(url)
                except (urllib2.HTTPError, urllib2.URLError):
                    _logger.warn("Eureka server [%s] is down, use next url to try." % url)
                    tried_servers.append(url)
                    untry_servers = untry_servers[1:]
                else:
                    ok = True
                    break
            if len(tried_servers) > 0:
                untry_servers.extend(tried_servers)
                self.__eureka_servers = untry_servers
            if not ok:
                raise urllib2.URLError("All eureka servers are down!")

    def __pull_full_registry(self):
        def do_pull(url):  # the actual function body
            self.__applications = get_applications(url, self.__regions)
            self.__delta = self.__applications

        self.__try_all_eureka_server(do_pull)

    def __fetch_delta(self):
        def do_fetch(url):
            if self.__applications is None or len(self.__applications.applications) == 0:
                self.__pull_full_registry()
                return
            delta = get_delta(url, self.__regions)
            _logger.debug("delta got: v.%s::%s" % (delta.version, delta.hashcode))
            if self.__delta is not None \
                    and delta.version == self.__delta.version \
                    and delta.hashcode == self.__delta.hashcode:
                return
            self.__merge_delta(delta)
            self.__delta = delta
            if not self.__is_hash_match():
                self.__pull_full_registry()

        self.__try_all_eureka_server(do_fetch)

    def __is_hash_match(self):
        app_hash = self.__get_applications_hash()
        _logger.debug("check hash, local[%s], remote[%s]" % (app_hash, self.__delta.hashcode))
        return app_hash == self.__delta.hashcode

    def __merge_delta(self, delta):
        _logger.debug("merge delta...length of application got from delta::%d" % len(delta.applications))
        for application in delta.applications:
            for instance in application.instances:
                _logger.debug("instance [%s] has %s" % (instance.instance_id, instance.action_type))
                if instance.action_type in (ACTION_TYPE_ADDED, ACTION_TYPE_MODIFIED):
                    existingApp = self.applications.get_application(application.name)
                    if existingApp is None:
                        self.applications.add_application(application)
                    else:
                        existingApp.update_instance(instance)
                elif instance.action_type == ACTION_TYPE_DELETED:
                    existingApp = self.applications.get_application(application.name)
                    if existingApp is None:
                        self.applications.add_application(application)
                    existingApp.remove_instance(instance)

    def __get_applications_hash(self):
        app_hash = ""
        app_status_count = {}
        for application in self.__applications.applications:
            for instance in application.instances:
                if instance.status not in app_status_count:
                    app_status_count[instance.status.upper()] = 0
                app_status_count[instance.status.upper()] = app_status_count[instance.status.upper()] + 1

        sorted_app_status_count = sorted(app_status_count.items(), __cache_key=lambda item: item[0])
        for item in sorted_app_status_count:
            app_hash = app_hash + "%s_%d_" % (item[0], item[1])
        return app_hash

    def walk_nodes_async(self, app_name="", service="", prefer_ip=False, prefer_https=False, walker=None,
                         on_success=None, on_error=None):
        def async_thread_target():
            try:
                res = self.walk_nodes(app_name=app_name, service=service, prefer_ip=prefer_ip,
                                      prefer_https=prefer_https, walker=walker)
                if on_success is not None and (inspect.isfunction(on_success) or inspect.ismethod(on_success)):
                    on_success(res)
            except urllib2.HTTPError as e:
                if on_error is not None and (inspect.isfunction(on_error) or inspect.ismethod(on_error)):
                    on_error(e)

        async_thread = Thread(target=async_thread_target)
        async_thread.daemon = True
        async_thread.start()

    def walk_nodes(self, app_name="", service="", prefer_ip=False, prefer_https=False, walker=None):
        assert app_name is not None and app_name != "", "application_name should not be null"
        assert inspect.isfunction(walker) or inspect.ismethod(walker), "walker must be a method or function"
        error_nodes = []
        app_name = app_name.upper()
        node = self.__get_availabe_service(app_name)

        while node is not None:
            try:
                url = self.__generate_service_url(node, prefer_ip, prefer_https)
                if service.startswith("/"):
                    url = url + service[1:]
                else:
                    url = url + service
                _logger.debug("service url::" + url)
                return walker(url)
            except (urllib2.HTTPError, urllib2.URLError):
                _logger.warn("do service %s in node [%s] error, use next node." % (service, node.instanceId))
                error_nodes.append(node.instanceId)
                node = self.__get_availabe_service(app_name, error_nodes)

        raise urllib2.HTTPError("Try all up instances in registry, but all fail")

    def do_service_async(self, app_name="", service="", return_type="string",
                         prefer_ip=False, prefer_https=False,
                         on_success=None, on_error=None,
                         method="GET", headers=None,
                         data=None, timeout=_DEFAULT_TIME_OUT,
                         cafile=None, capath=None, cadefault=False, context=None):
        def async_thread_target():
            try:
                res = self.do_service(app_name=app_name,
                                      service=service, return_type=return_type,
                                      prefer_ip=prefer_ip, prefer_https=prefer_https,
                                      method=method, headers=headers,
                                      data=data, timeout=timeout,
                                      cafile=cafile, capath=capath,
                                      cadefault=cadefault, context=context)
                if on_success is not None and (inspect.isfunction(on_success) or inspect.ismethod(on_success)):
                    on_success(res)
            except urllib2.HTTPError as e:
                if on_error is not None and (inspect.isfunction(on_error) or inspect.ismethod(on_error)):
                    on_error(e)

        async_thread = Thread(target=async_thread_target)
        async_thread.daemon = True
        async_thread.start()

    def do_service(self, app_name="", service="", return_type="string",
                   prefer_ip=False, prefer_https=False,
                   method="GET", headers=None,
                   data=None, timeout=_DEFAULT_TIME_OUT,
                   cafile=None, capath=None, cadefault=False, context=None):
        def walk_using_urllib(url):
            req = urllib2.Request(url)
            req.get_method = lambda: method
            heads = headers if headers is not None else {}
            for k, v in heads.items():
                req.add_header(k, v)

            response = urllib2.urlopen(req, data=data, timeout=timeout, ca_file=cafile, capath=capath,
                                       ca_default=cadefault, context=context)
            res_txt = response.read().decode(_DEFAULT_ENCODING)
            response.close()
            if return_type.lower() in ("json", "dict", "dictionary"):
                return json.loads(res_txt)
            else:
                return res_txt

        return self.walk_nodes(app_name, service, prefer_ip, prefer_https, walk_using_urllib)

    def __get_availabe_service(self, application_name, ignore_instance_ids=None):
        app = self.applications.get_application(application_name)
        if app is None:
            return None
        up_instances = []
        if ignore_instance_ids is None or len(ignore_instance_ids) == 0:
            up_instances.extend(app.up_instances)
        else:
            for ins in app.up_instances:
                if ins.instance_id not in ignore_instance_ids:
                    up_instances.append(ins)

        if len(up_instances) == 0:
            # no up instances
            return None
        elif len(up_instances) == 1:
            # only one available instance, then doesn't matter which strategy is.
            instance = up_instances[0]
            self.__ha_cache[application_name] = instance.instance_id
            return instance

        def random_one(instances):
            if len(instances) == 1:
                idx = 0
            else:
                idx = random.randint(0, len(instances) - 1)
            selected_instance = instances[idx]
            self.__ha_cache[application_name] = selected_instance.instance_id
            return selected_instance

        if self.__ha_strategy == HA_STRATEGY_RANDOM:
            return random_one(up_instances)
        elif self.__ha_strategy == HA_STRATEGY_STICK:
            if application_name in self.__ha_cache:
                cache_id = self.__ha_cache[application_name]
                cahce_instance = app.get_instance(cache_id)
                if cahce_instance is not None and cahce_instance.status == INSTANCE_STATUS_UP:
                    return cahce_instance
                else:
                    return random_one(up_instances)
            else:
                return random_one(up_instances)
        elif self.__ha_strategy == HA_STRATEGY_OTHER:
            if application_name in self.__ha_cache:
                cache_id = self.__ha_cache[application_name]
                other_instances = []
                for up_instance in up_instances:
                    if up_instance.instance_id != cache_id:
                        other_instances.append(up_instance)
                return random_one(other_instances)
            else:
                return random_one(up_instances)
        else:
            return None

    def __generate_service_url(self, instance, prefer_ip, prefer_https):
        if instance is None:
            return None
        schema = "http"
        port = 0
        if instance.port.port and not instance.securePort.enabled:
            schema = "http"
            port = instance.port.port
        elif not instance.port.port and instance.securePort.enabled:
            schema = "https"
            port = instance.securePort.port
        elif instance.port.port and instance.securePort.enabled:
            if prefer_https:
                schema = "https"
                port = instance.securePort.port
            else:
                schema = "http"
                port = instance.port.port
        else:
            assert False, "generate_service_url error: No port is available"

        host = instance.ipAddr if prefer_ip else instance.hostName

        return "%s://%s:%d/" % (schema, host, port)

    def start(self):
        self.__pull_full_registry()
        self.__timer.start()

    def stop(self):
        if self.__timer.isAlive():
            self.__timer.cancel()


__cache_discovery_clients = {}
__cache_discovery_clients_lock = Lock()


def init_discovery_client(eureka_server=_DEFAULT_EUREKA_SERVER_URL, regions=[],
                          renewal_interval_in_secs=_RENEWAL_INTERVAL_IN_SECS, ha_strategy=HA_STRATEGY_RANDOM):
    with __cache_discovery_clients_lock:
        assert __cache_key not in __cache_discovery_clients, "Client has already been initialized."
        cli = DiscoveryClient(eureka_server, regions=regions, renewal_interval_in_secs=renewal_interval_in_secs,
                              ha_strategy=ha_strategy)
        cli.start()
        __cache_discovery_clients[__cache_key] = cli
        return cli


def get_discovery_client():
    # type: (str) -> DiscoveryClient
    with __cache_discovery_clients_lock:
        if __cache_key in __cache_discovery_clients:
            return __cache_discovery_clients[__cache_key]
        else:
            return None


def init(eureka_server=_DEFAULT_EUREKA_SERVER_URL,
         regions=[],
         app_name="",
         instance_id="",
         instance_host="",
         instance_ip="",
         instance_port=_DEFAULT_INSTANCE_PORT,
         instance_unsecure_port_enabled=True,
         instance_secure_port=_DEFAULT_INSTANCE_SECURE_PORT,
         instance_secure_port_enabled=False,
         countryId=1,  # @deprecaded
         data_center_name=_DEFAULT_DATA_CENTER_INFO,  # Netflix, Amazon, MyOwn
         renewal_interval_in_secs=_RENEWAL_INTERVAL_IN_SECS,
         duration_in_secs=_DURATION_IN_SECS,
         home_page_url="",
         status_page_url="",
         health_check_url="",
         vip_adr="",
         secure_vip_addr="",
         is_coordinating_discovery_server=False,
         ha_strategy=HA_STRATEGY_RANDOM):
    registry_client = init_registry_client(eureka_server=eureka_server,
                                           app_name=app_name,
                                           instance_id=instance_id,
                                           instance_host=instance_host,
                                           instance_ip=instance_ip,
                                           instance_port=instance_port,
                                           instance_unsecure_port_enabled=instance_unsecure_port_enabled,
                                           instance_secure_port=instance_secure_port,
                                           instance_secure_port_enabled=instance_secure_port_enabled,
                                           countryId=countryId,
                                           data_center_name=data_center_name,
                                           renewal_interval_in_secs=renewal_interval_in_secs,
                                           duration_in_secs=duration_in_secs,
                                           home_page_url=home_page_url,
                                           status_page_url=status_page_url,
                                           health_check_url=health_check_url,
                                           vip_adr=vip_adr,
                                           secure_vip_addr=secure_vip_addr,
                                           is_coordinating_discovery_server=is_coordinating_discovery_server)
    discovery_client = init_discovery_client(eureka_server,
                                             regions=regions,
                                             renewal_interval_in_secs=renewal_interval_in_secs,
                                             ha_strategy=ha_strategy)
    return registry_client, discovery_client


def walk_nodes_async(app_name="", service="", prefer_ip=False, prefer_https=False, walker=None, on_success=None,
                     on_error=None):
    cli = get_discovery_client()
    if cli is None:
        raise Exception("Discovery Client has not initialized. ")
    cli.walk_nodes_async(app_name=app_name, service=service,
                         prefer_ip=prefer_ip, prefer_https=prefer_https,
                         walker=walker, on_success=on_success, on_error=on_error)


def walk_nodes(app_name="", service="", prefer_ip=False, prefer_https=False, walker=None):
    cli = get_discovery_client()
    if cli is None:
        raise Exception("Discovery Client has not initialized. ")
    return cli.walk_nodes(app_name=app_name, service=service,
                          prefer_ip=prefer_ip, prefer_https=prefer_https, walker=walker)


def do_service_async(app_name="", service="", return_type="string",
                     prefer_ip=False, prefer_https=False,
                     on_success=None, on_error=None,
                     method="GET", headers=None,
                     data=None, timeout=_DEFAULT_TIME_OUT,
                     cafile=None, capath=None, cadefault=False, context=None):
    cli = get_discovery_client()
    if cli is None:
        raise Exception("Discovery Client has not initialized. ")
    cli.do_service_async(app_name=app_name, service=service, return_type=return_type,
                         prefer_ip=prefer_ip, prefer_https=prefer_https,
                         on_success=on_success, on_error=on_error,
                         method=method, headers=headers,
                         data=data, timeout=timeout,
                         cafile=cafile, capath=capath,
                         cadefault=cadefault, context=context)


def do_service(app_name="", service="", return_type="string",
               prefer_ip=False, prefer_https=False,
               method="GET", headers=None,
               data=None, timeout=_DEFAULT_TIME_OUT,
               cafile=None, capath=None, cadefault=False, context=None):
    cli = get_discovery_client()
    if cli is None:
        raise Exception("Discovery Client has not initialized. ")
    return cli.do_service(app_name=app_name, service=service, return_type=return_type,
                          prefer_ip=prefer_ip, prefer_https=prefer_https,
                          method=method, headers=headers,
                          data=data, timeout=timeout,
                          cafile=cafile, capath=capath,
                          cadefault=cadefault, context=context)


def stop():
    register_cli = get_registry_client()
    if register_cli is not None:
        register_cli.stop()
    discovery_client = get_discovery_client()
    if discovery_client is not None:
        discovery_client.stop()


@atexit.register
def _cleanup_before_exist():
    if len(__cache_registry_clients) > 0:
        _logger.debug("cleaning up registry clients")
        for k, cli in __cache_registry_clients.items():
            _logger.debug(
                "try to stop cache registry client [%s] this will also unregister this client from the eureka server" % k)
            cli.stop()
    if len(__cache_discovery_clients) > 0:
        _logger.debug("cleaning up discovery clients")
        for k, cli in __cache_discovery_clients.items():
            _logger.debug(
                "try to stop cache discovery client [%s] this will also unregister this client from the eureka server" % k)
            cli.stop()
