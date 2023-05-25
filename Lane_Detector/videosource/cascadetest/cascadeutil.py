import os
def generate_negative_description_file():

    with open(r'C:\Users\Niles Alexis\Documents\PWP Lane Detection\PWP-Lane-Detection\Lane_Detector\videosource\cascadetest\neg.txt','w') as f:

        for filename in os.listdir(r'C:\Users\Niles Alexis\Documents\PWP Lane Detection\PWP-Lane-Detection\Lane_Detector\videosource\cascadetest\negative'):
            print("test")
            f.write('negative/' + filename + "\n")
    
generate_negative_description_file()