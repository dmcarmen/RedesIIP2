import os
token = ""

def config_ini():
    global token
    if os.stat("token.txt").st_size == 0:
        print("Error: no hay token")
        return -1
    file = open("token.txt", "r")
    #TODO cuidado con \n
    token = file.read()[:-1]


def error(request):
    json = request.json()
    if "error_code" in json:
        print("Error {}: {} -> {}".format(json.get("http_error_code"), json.get("error_code"), json.get("description")))
    else:
        print("Error {}".format(r.status_code))
