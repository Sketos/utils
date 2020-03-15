

def directory_update_with_folder_names(directory, folder_names):
    directory_temp = directory
    for name in folder_names:
        directory_temp += "/" + name

    return directory_temp
