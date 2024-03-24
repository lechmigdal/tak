from os import listdir, mkdir
from os.path import isfile, join
import shutil

KEY_FOLDER = "../keys"

OUTPUT_FOLDER = "../output"
OUTPUT_FOLDER_IOS = "../output_ios"
TEMP_FOLDER = "../temp"
TEMP_FOLDER_IOS = "../temp_ios"
PACKAGE_SOURCE = "../package_raw"
PACKAGE_SOURCE_IOS = "../package_raw_ios"

# add mapping of your user name to team color
colors = {
"toc":"White"
}

# run as a script
onlyfiles = [f for f in listdir(KEY_FOLDER) if isfile(join(KEY_FOLDER, f))]
# for every .p12 file in KEY_FOLDER
for file in onlyfiles:
    ##### ANDROID ####
    # in TEMP_FOLDER create a subfolder with name equal to .p12 filename
    new_folder = TEMP_FOLDER + "/" + file.split(".")[0]
    # delete target folder if it exists
    shutil.rmtree(new_folder, ignore_errors=True)
    # copy PACKAGE_SOURCE to TEMP_FOLDER subfolder
    shutil.copytree(PACKAGE_SOURCE, new_folder)
    # copy .p12 file to TEMP_FOLDER subfolder and rename it to "clientCert.p12"
    shutil.copy(KEY_FOLDER + "/" + file, new_folder + "/certs/clientCert.p12")
    
    # Read in the preferences file
    with open(new_folder+"/certs/config.pref", 'r') as config_file:
        filedata = config_file.read()
        callsign = file.split(".")[0]

        # replace REPLACE_CALLSIGN in config.pref with filename without user and without .p12       
        filedata = filedata.replace('REPLACE_CALLSIGN',  callsign  )
        # replace REPLACE_TEAM in config.pref with filename without .p12 and without number    
        team_name = colors[callsign] 
        filedata = filedata.replace('REPLACE_TEAM', team_name)
    
    # Write the file out again
    with open(new_folder+"/certs/config.pref", 'w') as config_file:
        config_file.write(filedata)    

    # zip the TEMP_FOLDER subfolder into OUTPUT_FOLDER as .p12 filename + ".zip"
    shutil.make_archive(OUTPUT_FOLDER+"/"+file.split(".")[0], 'zip', new_folder)

    ### IOS

    # in TEMP_FOLDER_IOS create a subfolder with name equal to .p12 filename
    new_folder_ios = TEMP_FOLDER_IOS + "/" + file.split(".")[0]
    # delete target folder if it exists
    shutil.rmtree(new_folder_ios, ignore_errors=True)
    # copy PACKAGE_SOURCE_IOS to TEMP_FOLDER_IOS subfolder
    shutil.copytree(PACKAGE_SOURCE_IOS, new_folder_ios)
    # copy .p12 file to TEMP_FOLDER_IOS subfolder and rename it to "clientCert.p12"
    shutil.copy(KEY_FOLDER + "/" + file, new_folder_ios + "/clientCert.p12")
    # copy the config file from android to ios package
    shutil.copy(new_folder+"/certs/config.pref", new_folder_ios+"/config.pref")
    
    # zip the TEMP_FOLDER_IOS subfolder into OUTPUT_FOLDER_IOS as .p12 filename + ".zip"
    shutil.make_archive(OUTPUT_FOLDER_IOS+"/"+file.split(".")[0], 'zip', new_folder_ios)
    
