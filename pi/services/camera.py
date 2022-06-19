import picamera
import threading
import time
import uuid
from services.db import DB

class Camera:
    def __init__(self, dialog, interval = 5):
        self.camera = picamera.PiCamera()
        self.interval = interval
        self.camera.resolution = (1920, 1080)
        self.dialog = dialog
        #self.camera.brightness = 100
        #self.camera.shutter_speed = 10
        self._running = False
        
    def __del__(self):
        self.camera.close()

    def start(self):
        #start
        self._running = True
        self.thread = threading.Thread(target=self.thread_function)
        self.thread.start()
        
        #self.thread_function()

    def stop(self):
        self._running = False

    def thread_function(self):
        self.db = DB()
        while(self._running):
            
            self.take_photo()
            time.sleep(self.interval)

    def take_photo(self):
        
        image_id = str(uuid.uuid4())
        
        file_name = image_id + '_' + time.strftime("%Y%m%d-%H%M%S")
        path = '/home/vitibox-cloud/Desktop/vitivisor_gbvs_pi-master/images/' + file_name + '.jpg'
        self.camera.capture(path)
        
        self.db.add_image(image_id, path, self.dialog.token, self.dialog.latitude, self.dialog.longitude, time.strftime("%Y%m%d"), self.dialog.property_id, self.dialog.patch_id )
        

        
    
# c = Camera()
# c.start()
