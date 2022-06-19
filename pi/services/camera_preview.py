import picamera
import threading
import time


class CameraPreview:
    def __init__(self, dialog):
        self.camera = picamera.PiCamera()
        self.dialog = dialog
        self.camera.resolution = (400, 300)
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
        while(self._running):
            self.take_preview()
            #time.sleep(1)

    def take_preview(self):
       
#         path = '/home/vitibox-cloud/Desktop/vitivisor_gbvs_pi-master/tmp/viticanopy_preview.jpg'
        path = '/tmp/viticanopy_preview.jpg'
        self.camera.capture(path)
       
        self.dialog.update_preview(path)


        
    

