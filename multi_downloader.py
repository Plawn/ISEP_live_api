import threading
import time
import queue
import sys

def console_write(string):
    sys.stdout.write(string)
    sys.stdout.flush()

class Download_worker(threading.Thread):
    def __init__(self, queue, folder, pool):
        threading.Thread.__init__(self)
        self.queue = queue
        self.stopped = False
        self.download_folder = folder
        self.pool = pool

    def run(self):
        while not self.stopped:
            d = None
            try:
                d = self.queue.get(block=False)
                d.set_download_folder(self.download_folder)
            except:
                return
            try:
                d.download()
                self.pool.notify()
            except:
                print('download error -> re schedule download')
                self.re_schedule(d)

    def re_schedule(self, download):
        self.pool.add(download)
        self.pool.notify()

    def stop(self):
        self.stopped = True


class Download_pool(threading.Thread):
    def __init__(self, nb_workers, folder):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.workers = []
        self.nb_workers = nb_workers
        self.folder = folder
        self.done = 0
        self.remaining = 0
        self.to_do = 0
        self.lock = threading.Lock()

        for _ in range(self.nb_workers):
            self.add_workder()

    def add_workder(self):
        self.workers.append(Download_worker(self.queue, self.folder, self))

    def add(self, url):
        with self.lock:
            self.to_do += 1
            self.remaining += 1
            self.queue.put(url)

    def notify(self):
        with self.lock:
            self.done += 1
            self.remaining -= 1

    def run(self):
        for worker in self.workers:
            worker.start()

    def stop_finished(self):
        while self.remaining > 0:
            console_write('\r{}/{}'.format(self.done, self.to_do))
            time.sleep(0.2)
        for worker in self.workers:
            worker.stop()