def app(amb, start_response):
    with open("index.html", "rb") as file:
        body = file.read()
    status = "200 OK"
    response_headers = [("Content-type", "text/html")]
    start_response(status, response_headers)
    return [body]