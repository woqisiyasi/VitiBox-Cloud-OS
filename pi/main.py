import sys
sys.path.append('./')



from PyQt5 import QtCore, QtGui, QtWidgets
from ui.main_dialog import MainDialog
from services.gps import GPS
from services.picture_upload import PictureUpload

def main():
    
    app = QtWidgets.QApplication(sys.argv)
    
   
    main_dialog = MainDialog()
    
    gps = GPS(main_dialog)
    gps.run()

    picture_upload = PictureUpload( main_dialog)
    picture_upload.run()

    main_dialog.show()
    
    app.exec_()
    



if __name__ == "__main__":
    
 


    
    main()

    
    sys.exit(0)



