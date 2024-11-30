

def load_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            print("File loaded successfully!")
            return file_content
    except FileNotFoundError:
        print(f"The file located at {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None