from fastapi import  Response 

def GetResponse(response= Response, *, message='', error=False,data=None,  status=200):
    response.status_code = status
    return {
        "error": error,
        "message": message,
        "data": data
    }