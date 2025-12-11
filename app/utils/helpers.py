def some_helper_function(param1, param2):
    # This is an example of a helper function that performs a specific task.
    return param1 + param2

def another_helper_function(data):
    # This function processes data in a specific way.
    processed_data = [item for item in data if item is not None]
    return processed_data

def format_response(data, status_code=200):
    # This function formats the response to be returned from the API.
    return {
        "status": "success",
        "data": data,
        "status_code": status_code
    }

def handle_error(message, status_code=400):
    # This function formats error responses.
    return {
        "status": "error",
        "message": message,
        "status_code": status_code
    }