import json
import logging
import os
import threading
import time
from telnetlib import Telnet
from typing import Any, Dict, Optional

import requests

from yqn_project_cli.utils.core.exceptions import BasicException, NameSpaceNotFoundException, ServerNotResponseException


class ApolloClient:

    def __new__(cls, *args, **kwargs):
        """
        singleton model
        """
        tmp = {_: kwargs[_] for _ in sorted(kwargs)}
        key = f"{args},{tmp}"
        if hasattr(cls, "_instance"):
            if key not in cls._instance:
                cls._instance[key] = super().__new__(cls)
        else:
            cls._instance = {key: super().__new__(cls)}
        return cls._instance[key]

    def __init__(
            self,
            app_id: str,
            cluster: str = "default",
            config_server_url: str = "http://192.168.10.223:8080",
            env: str = "FAT",
            ip: str = None,
            timeout: int = 10,
            cycle_time: int = 30,
            cache_file_path: str = None,
            authorization: str = None,
    ):
        """
        init method
        :param app_id: application id
        :param cluster: cluster name, default value is 'default'
        :param config_server_url: with the format 'http://localhost:80080'
        :param env: environment, default value is 'DEV'
        :param timeout: http request timeout seconds, default value is 60 seconds
        :param ip: the deploy ip for grey release, default value is the local ip
        :param cycle_time: the cycle time to update configuration content from server
        :param cache_file_path: local cache file store path
        """
        self.config_server_url = config_server_url
        self.app_id = app_id
        self.cluster = cluster
        self.timeout = timeout
        self.stopped = False
        self._env = env
        self.ip = self.init_ip(ip)
        remote = self.config_server_url.split(":")
        self.host = f"{remote[0]}:{remote[1]}"
        if len(remote) == 1:
            self.port = 8090
        else:
            self.port = int(remote[2])
        self._authorization = authorization

        self._request_model = None
        self._cache: Dict = {}
        self._notification_map = {'application': -1}
        # if namespaces is None:
        #     namespaces = ["application"]
        # self._notification_map = {namespace: -1 for namespace in namespaces}
        self._cycle_time = cycle_time
        self._hash: Dict = {}
        if cache_file_path is None:
            self._cache_file_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "config"
            )
        else:
            self._cache_file_path = cache_file_path
        self._path_checker()
        self._stopping = False
        # for http request extension
        # self.start()

    def _get_clusters(self) -> dict:
        """
        get clusters by app id
        :return :
        """
        url = f"{self.host}:{self.port}/apps/{self.app_id}/clusters"
        r = self._http_get(url)
        if r.status_code == 200:
            return r.json()
        else:
            return {}

    def _get_namespaces(self) -> dict:
        """
        get namespaces by app id and cluster
        :return :
        """
        # url = f"{self.host}:{self.port}/apps/{self.app_id}/clusters/{self.cluster}/namespaces"
        # r = self._http_get(url)
        url = '{}/notifications/v2'.format(self.config_server_url)
        notifications = []
        temp = {'application': -1}
        for key in temp:
            notification_id = temp[key]
            notifications.append({
                'namespaceName': key,
                'notificationId': notification_id
            })

        r = requests.get(url=url, params={
            'appId': self.app_id,
            'cluster': self.cluster,
            'notifications': json.dumps(notifications, ensure_ascii=False)
        }, timeout=self.timeout)
        if r.status_code == 200:
            namespaces = r.json()
            return {_.get("namespaceName"): _.get("notificationId") for _ in namespaces}
        else:
            return {"application": -2}

    @staticmethod
    def init_ip(ip: Optional[str]) -> str:
        """
        for grey release
        :param ip:
        :return:
        """
        if ip is None:
            try:
                import socket

                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("114.114.114.114", 53))
                ip = s.getsockname()[0]
                s.close()
            except BaseException:
                return "127.0.0.1"
        return ip

    def get_value(
            self, key: str, default_val: str = None, namespace: str = "application"
    ) -> Any:
        """
        get the configuration value
        :param key:
        :param default_val:
        :param namespace:
        :return:
        """
        try:
            # check the namespace is existed or not
            if namespace in self._cache:
                return self._cache[namespace].get(key, default_val)
            return default_val
        except BasicException:
            return default_val

    def stop(self, ) -> None:
        self._stopping = True

    def start(self, call_back_func) -> None:
        """
        Start the long polling loop.
        :return:
        """
        # check the cache is empty or not
        # if len(self._cache) == 0:
        #     self._long_poll()
        #     call_back_func()
        # start the thread to get config server with schedule
        self._first_request(call_back_func)
        t = threading.Thread(target=self._listener, args=(call_back_func,))
        t.setDaemon(True)
        t.start()

    def _http_get(self, url: str, params: Dict = None) -> requests.Response:
        """
        handle http request with get method
        :param url:
        :return:
        """
        if self._request_model is None:
            return self._request_get(url, params=params)
        else:
            return self._request_model(url)

    def _request_get(self, url: str, params: Dict = None) -> requests.Response:
        """
        :param url:
        :param params:
        :return:
        """
        try:
            if self._authorization:
                return requests.get(
                    url=url,
                    params=params,
                    timeout=self.timeout // 2,
                    headers={"Authorization": self._authorization},
                )
            else:
                return requests.get(url=url, params=params, timeout=self.timeout // 2)

        except requests.exceptions.ReadTimeout:
            # if read timeout, check the server is alive or not
            try:
                tn = Telnet(host=self.host, port=self.port, timeout=self.timeout // 2)
                tn.close()
                # if connect server succeed, raise the exception that namespace not found
                raise NameSpaceNotFoundException("namespace not found")
            except ConnectionRefusedError:
                # if connection refused, raise server not response error
                raise ServerNotResponseException(
                    "server: %s not response" % self.config_server_url
                )

    def _path_checker(self) -> None:
        """
        create configuration cache file directory if not exits
        :return:
        """
        if not os.path.isdir(self._cache_file_path):
            os.mkdir(self._cache_file_path)

    def _update_local_cache(
            self, release_key: str, data: str, namespace: str = "application"
    ) -> None:
        """
        if local cache file exits, update the content
        if local cache file not exits, create a version
        :param release_key:
        :param data: new configuration content
        :param namespace::s
        :return:
        """
        # trans the config map to md5 string, and check it's been updated or not
        if self._hash.get(namespace) != release_key:
            # if it's updated, update the local cache file
            with open(
                    os.path.join(
                        self._cache_file_path,
                        "%s_configuration_%s.txt" % (self.app_id, namespace),
                    ),
                    "w",
            ) as f:
                new_string = json.dumps(data)
                f.write(new_string)
            self._hash[namespace] = release_key

    def _get_local_cache(self, namespace: str = "application") -> Dict:
        """
        get configuration from local cache file
        if local cache file not exits than return empty dict
        :param namespace:
        :return:
        """
        cache_file_path = os.path.join(
            self._cache_file_path, "%s_configuration_%s.txt" % (self.app_id, namespace)
        )
        if os.path.isfile(cache_file_path):
            with open(cache_file_path, "r") as f:
                result = json.loads(f.readline())
            return result
        return {}

    def _get_config_by_namespace(self, namespace: str = "application") -> None:
        """
        :param namespace:
        :return:
        """
        url = '{}/configs/{}/{}/{}?ip={}'.format(self.config_server_url, self.app_id, self.cluster, namespace, self.ip)
        # url = f"{self.host}:{self.port}/apps/{self.app_id}/clusters/{self.cluster}/namespaces/{namespace}/releases/latest"
        try:
            r = self._http_get(url)
            if r.status_code == 200:
                data = r.json()
                self._cache[namespace] = data.get("configurations", "{}")
                self._update_local_cache(
                    data.get("releaseKey", str(time.time())),
                    data.get("configurations", {}),
                    namespace,
                )
            else:
                data = self._get_local_cache(namespace)
                self._cache[namespace] = data
        except BaseException as e:
            logging.getLogger(__name__).warning(str(e))
            data = self._get_local_cache(namespace)
            self._cache[namespace] = data

    def _long_poll(self) -> None:
        try:
            # url = '{}/notifications/v2'.format(self.config_server_url)
            # notifications = []
            # for key in self._notification_map:
            #     notification_id = self._notification_map[key]
            #     notifications.append({
            #         'namespaceName': key,
            #         'notificationId': notification_id
            #     })
            #
            # r = requests.get(url=url, params={
            #     'appId': self.app_id,
            #     'cluster': self.cluster,
            #     'notifications': json.dumps(notifications, ensure_ascii=False)
            # }, timeout=self.timeout)
            new_notification_map = self._get_namespaces()
            if new_notification_map == self._notification_map:
                pass
            else:
                self._notification_map = new_notification_map
                for namespace in self._notification_map.keys():
                    self._get_config_by_namespace(namespace)
        except requests.exceptions.ReadTimeout as e:
            logging.getLogger(__name__).warning(str(e))
        except requests.exceptions.ConnectionError as e:
            logging.getLogger(__name__).warning(str(e))
            self._load_local_cache_file()

    def _load_local_cache_file(self) -> bool:
        """
        load all cached files from local path
        is only used while apollo server is unreachable
        :return:
        """
        for file_name in os.listdir(self._cache_file_path):
            file_path = os.path.join(self._cache_file_path, file_name)
            if os.path.isfile(file_path):
                file_simple_name, file_ext_name = os.path.splitext(file_name)
                if file_ext_name == ".swp":
                    continue
                namespace = file_simple_name.split("_")[-1]
                with open(file_path) as f:
                    self._cache[namespace] = json.loads(f.read())["configurations"]
        return True

    def _first_request(self, call_back_func) -> None:
        self._long_poll()
        call_back_func()

    def _listener(self, call_back_func) -> None:
        """
        :return:
        """
        logging.getLogger(__name__).info("Entering listener loop...")
        while not self._stopping:
            self._long_poll()
            call_back_func()
            time.sleep(self._cycle_time)
