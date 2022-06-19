from services.api_service import ApiService
from services.db import DB
import threading
import time
import pdb
import os
from datetime import datetime
import requests
import csv

class PictureUpload:
    def __init__(self, dialog):
        self.dialog = dialog
        self.total_uploaded = 0
        

    def run(self):
        thread = threading.Thread(target=self.thread_function)
        thread.start()
       
        #self.thread_function()

    def update_progress(self, pending_count, total_uploaded):
        progress = "Pending: {pending_count}, Saved: {total_uploaded}".format(pending_count = pending_count, total_uploaded = self.total_uploaded)
        self.dialog.setProgress(progress)
        
    def thread_function(self):
        self.api_service = ApiService.getInstance()
        self.db = DB()
        time_sync_counter = 0
        while(True):
            pending_count = self.db.pending_count()
            self.update_progress(pending_count, self.total_uploaded)
            
            if pending_count > 0:
                print('pending_count', pending_count)
                
                pending_upload = self.db.pending_upload()
                picture = {
                    'image_id': pending_upload['image_id'],
                    'latitude': pending_upload['latitude'],
                    'longitude': pending_upload['longitude'],
                    'time_point': pending_upload['time_point'],
                    'property_id': pending_upload['property_id'],
                    'patch_id': pending_upload['patch_id']
                }
                pic_file = {
                    'picture':   open( pending_upload['path'], 'rb')
                }
                success = False
                
                token = pending_upload['token']
                
                if token:
                    #print('db token=', token)
                    try:
                    
                        date_separator = datetime.strptime('20211001', '%Y%m%d')
                        time_point_id = ''
                        
                        if datetime.strptime(picture['time_point'], '%Y%m%d') > date_separator:
                        
                            res = self.api_service.upload_image(token, picture, pic_file)
                            print(res)
                            if res.get('message') == 'Server error!':
                                success = False
                                print('Upload api error')
                            else:
                                success = True
                            
                            
                        elif datetime.now() > date_separator:
                            time_point_id = datetime.now().strftime("%Y%m%d")
                            picture['time_point'] = time_point_id

                            res = self.api_service.upload_image(token, picture, pic_file)
                            print(res)
                            if res.get('message') == 'Server error!':
                                success = False
                                print('Upload api error')
                            else:
                                success = True
                            
                            
                        else:
                            success = False
                            print('Waiting syetem to sync datetime.')
                            if time_sync_counter % 30 == 0:
                                os.system('sudo /etc/init.d/ntp restart')
                            time_sync_counter += 1
                        
                            
                            
                    except requests.exceptions.SSLError as e:
                        print(e)
                        if time_sync_counter % 30 == 0:
                            os.system('sudo /etc/init.d/ntp restart')
                            time_sync_counter += 1
                    
                    except Exception as e:
                        
                        print(e)
                        
                        
                else:
                    
                    print('Saving local files')
                    csv_path = pending_upload['path'].replace('.jpg', '.csv')
                    csv_row = [
                        ['image_id', 'file_name', 'latitude', 'longitude', 'time_point', 'property_id', 'patch_id'] ,
                        [ picture['image_id'], pending_upload['path'], picture['latitude'], picture['longitude'], picture['time_point'], picture['property_id'], picture['patch_id']]   
                    ]
                   
                    with open(csv_path, 'w') as csvfile:
                        csvwriter = csv.writer(csvfile) 
                        csvwriter.writerows(csv_row)
                    success = True
                    
                if success:
                    self.db.upload_image(pending_upload['image_id'])
                    
                    #remove image
                    #os.remove( pending_upload['path'])
                    
                    self.total_uploaded += 1
                    
                
                
                if success == False:
                    time.sleep(1)
            else:
                time.sleep(1)

    
    

