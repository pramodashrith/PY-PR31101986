import os

def find_config_files(root_folder):
    config_files = []
    for folder, -, files in os.walk(root_folder):
        for file in files:
            if file in files:
                if file == "config.xml":
                    config_files.append(os.path.join(folder, file))
        return config_files

if __name__ == "__main__":
    root_folder = ""
    config_files = find_config_files(root_folder)
    
    for file in config_files:
        print(file)