
# CREATE TABLE images (
# 	id INTEGER PRIMARY KEY,
#     uuid TEXT NOT NULL,
# 	path TEXT NOT NULL,
#     status TEXT NOT NULL,
# 	uploaded_at NUMERIC,
# 	token TEXT,
#     latitude TEXT NOT NULL,
#     longitude TEXT NOT NULL,
#     time_point_id TEXT NOT NULL,
#     property_id INTEGER,
#     patch_id INTEGER
# );
# 
# CREATE TABLE user (
#   id INTEGER PRIMARY KEY,
#   first_name  TEXT NOT NULL,
#   token TEXT NOT NULL,
#   properties TEXT
# );

import sqlite3
import json
import pdb

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('/home/vitibox-cloud/Desktop/vitivisor_gbvs_pi-master/pi/db/pi.db')
     

    def remove_user(self):
        c = self.conn.cursor()
        c.execute('delete from user')
        self.conn.commit()

    def save_user(self, first_name, token, properties):
        self.remove_user()
        c = self.conn.cursor()
        c.execute('Insert into user (first_name, token, properties) values (?, ?, ?)', (first_name, token, properties))
        self.conn.commit()
    def update_properties(self, properties):
        c = self.conn.cursor()
        c.execute('Update user set properties = ?', [properties])
        self.conn.commit()

    def get_user(self):
        c = self.conn.cursor()
        c.execute('select * from user order by id limit 1')
        one = c.fetchone()
        if one == None:
            return None
        res = {
            'first_name': one[1],
            'token': one[2],
            'properties': one[3]
            }
        return res

    def add_image(self, uuid, path, token, latitude, longitude, time_point_id, property_id, patch_id):
        c = self.conn.cursor()
        c.execute('Insert into images (uuid, path, status, token, latitude, longitude, time_point_id, property_id, patch_id) values (?, ?, "not_uploaded", ?, ?, ?, ?, ?, ? )', (uuid, path, token, latitude, longitude, time_point_id, property_id, patch_id))
        self.conn.commit()

    def upload_image(self, uuid):
        c = self.conn.cursor()
        c.execute('update images set status="uploaded", uploaded_at=CURRENT_TIMESTAMP where uuid=?', [uuid])
        self.conn.commit()
        
    def pending_count(self):
        c = self.conn.cursor()
        c.execute('select count(*) from images where status="not_uploaded" ')
        return c.fetchone()[0]


    def pending_upload(self):
        c = self.conn.cursor()
        c.execute('select * from images where status="not_uploaded" order by id asc limit 1 ')
        one = c.fetchone()
        if one == None:
            return None
        
        res = {
            'token': one[5],
            'image_id': one[1],
            'latitude': one[6],
            'longitude': one[7],
            'time_point': one[8],
            'property_id': one[9],
            'patch_id': one[10],
            'path': one[2]
            }
        
        return res



#db = DB()
#token = 'test'
#properties = '[{"id": 1, "organisation_id": 1, "name": "Loxton Research Centre", "state": "SA", "region": "Riverland", "address": "Loxton Research Centre", "created_at": "2020-11-15T05:41:25.277Z", "updated_at": "2020-11-15T10:28:28.578Z", "patches": [{"id": 1, "property_id": 1, "name": "Block 47", "size": 0.943317, "plant_spacing": 3.0, "row_width": 1.0, "soil_type": null, "rootstock": null, "variety": "Shiraz", "coordinates": "[[[140.59834735706667,-34.437859959969465],[140.5993180984611,-34.43780916168233],[140.5993008054955,-34.43684859320308],[140.59834338035722,-34.436900786968835],[140.59834735706667,-34.437859959969465]]]", "created_at": "2020-11-15T05:45:13.430Z", "updated_at": "2021-06-04T04:17:30.571Z", "year_planted": 1977, "contract_type": "Short Term (1-5 years)", "production_status": "Bearing", "irrigation_method": "Drip", "picking_method": "Both (hand & mechanical)"}, {"id": 2, "property_id": 1, "name": "Block 50", "size": 0.643136, "plant_spacing": 3.0, "row_width": 1.0, "soil_type": null, "rootstock": null, "variety": "Chardonnay", "coordinates": "[[[140.59725258133068,-34.437317713236126],[140.59718815120442,-34.43794731820334],[140.5981700075026,-34.43792449499925],[140.59823680648176,-34.437846809908436],[140.5982119761978,-34.43729083144725],[140.59725258133068,-34.437317713236126]]]", "created_at": "2020-11-15T05:45:13.442Z", "updated_at": "2021-06-04T04:17:30.608Z", "year_planted": 1980, "contract_type": "Short Term (1-5 years)", "production_status": "Bearing", "irrigation_method": "Drip", "picking_method": "Both (hand & mechanical)"}], "farm_grape_area": 1.5864530205726624}]'
#db.add_image('dd2709f4-aac6-4cf4-9a33-1c4f9797fb50', 'images/1.jpg', token, '-34.884017', '138.645432', '20200922', 1, 1)
#print( db.pending_upload() )
#print(db.pending_count())

#db.remove_user()
#db.save_user('Loxton', token, properties)
#print(db.get_user() )
#db.upload_image('dd2709f4-aac6-4cf4-9a33-1c4f9797fb50')



