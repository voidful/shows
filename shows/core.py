import psutil
from gpustat import GPUStatCollection
from cpuinfo import get_cpu_info
import threading
import time
import socket
from collections import deque


def bytes2MB(bytes):
    return int(bytes / 1024 / 1024)


class machine:
    def __init__(self, name=None):
        self.name = name if name is not None else socket.gethostname()
        self.cpu_info = get_cpu_info()
        self.status = deque(maxlen=10000)
        self.__end = False
        try:
            GPUStatCollection.new_query().jsonify()
            self.__type = 'gpu'
        except:
            self.__type = 'cpu'

        self.__my_hardware_state(interval=0.1)
        self.__t = threading.Thread(target=self.__get_cpu_percent_loop)
        self.__t.start()

    def __my_hardware_state(self, interval=1):
        stat = {
            "host_name": self.name,
            "is_alive": True,
            'type': self.__type
        }
        # basic info
        try:
            stat['cpus'] = [{"name": self.cpu_info.get('brand_raw', "CPU"), "usage": cpu} for cpu in
                            psutil.cpu_percent(interval=interval, percpu=True)]
            stat['mem'] = {"total": bytes2MB(psutil.virtual_memory().total),
                           "used": bytes2MB(psutil.virtual_memory().used)}
            stat['disk'] = [{"total": bytes2MB(psutil.disk_usage('/').total),
                             "used": bytes2MB(psutil.disk_usage('/').used)}]
            stat['net'] = {"in": bytes2MB(psutil.net_io_counters().bytes_recv),
                           "out": bytes2MB(psutil.net_io_counters().bytes_sent)}
        except Exception as e:
            print({'error': '%s!' % getattr(e, 'message', str(e))})
            stat['is_alive'] = False

        # gpu info
        stat['gpus'] = []
        try:
            gpu_stat = GPUStatCollection.new_query().jsonify()
            stat['gpus'] = [{"name": gpu.get('name', "CPU"),
                             "usage": gpu.get('utilization.gpu'),
                             "men_used": gpu.get('memory.used'),
                             "men_total": gpu.get('memory.total'),
                             "temp": gpu.get('temperature.gpu')} for gpu in gpu_stat['gpus']]
        except:
            pass
        self.status.append(stat)

    def __get_cpu_percent_loop(self):
        while not self.__end:
            self.__my_hardware_state()
            time.sleep(0.5)

    def get_state(self):
        return self.status[-1]

    def close(self):
        self.__end = True
