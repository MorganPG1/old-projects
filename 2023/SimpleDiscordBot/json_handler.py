import json
class main():
    def open_file(file):
        try:
            file_contents = open(file, 'r')
            json_content = json.loads(file_contents.read())
            return json_content
        except Exception as error:
            print("Error during decoding: "+str(error.with_traceback(None)))
            return {'error': str(error.with_traceback(None))}
    def write_file(json_data, file):
        try:
            file_contents = open(file, 'w')
            file_contents.write(json.dumps(json_data))
            file_contents.close()
        except Exception as error:
            return False
class other():
    def get_token():
        token = main.open_file('token.json')
        return token