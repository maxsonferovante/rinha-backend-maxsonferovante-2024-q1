from http import HTTPStatus
import re
import orjson

from api.service.client import ClientService

class Handler:
    def __init__(self, environ, start_response,
                  routes: tuple = None) -> None:
        self.request_method = environ["REQUEST_METHOD"]

        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            request_body_size = 0

        self.request_body = environ["wsgi.input"].read(request_body_size)
        
        self.path = environ["PATH_INFO"]
        self.start_response = start_response

        # Add routes to the handler if they are passed. Is dict
        self.routes = routes if isinstance(routes, tuple) else None
        self.routes_validation = self._compile_validation_routes() if isinstance(routes, tuple) else None

        self.clientService = ClientService()

    def _compile_validation_routes(self):
        validation_routes = {}
        for route in self.routes:
            regex = re.compile(route['path'])
            validation_routes[route["name"]] = regex
        return validation_routes
    
    def _make_response(self,http_status, response_body):
        
        response_headers = [
            ("Content-type", "application/json"),
            ("Content-Length", str(len(response_body)))
        ]
        response_status = f"{http_status.value} {http_status.phrase}"

        self.start_response(response_status, response_headers)
        
        #self._log_response(http_status)
        if isinstance (response_body, str):    
            return [response_body.encode("utf-8")]
        return [response_body]
    
    def _make_router_options(self, http_status, response_body):
        allowed_methods = []
        for route in self.routes:
                allowed_methods.append({
                    "path": route["path"].replace(r"\d+", "<id:int>"),
                    "methods": route["methods"]
                })
        #self._log_response(http_status)
        return self._make_response(HTTPStatus.OK, orjson.dumps(allowed_methods))
       
    def _log_request(self):
        print(f"Request: {self.request_method} {self.path}")
    
    def _log_response(self, http_status):
        print(f"Response: {http_status.value} {http_status.phrase}")
    
    def run(self):
        #self._log_request()
        if isinstance(self.routes, tuple):
            if self.request_method == "OPTIONS":
                return self._make_router_options(HTTPStatus.OK, "Options")            
            
            elif self.request_method == "POST" and self.routes_validation["clientes-transacoes"].match(self.path):                
                
                params_query = int(self.path.split("/")[2])

                
                response = self.clientService.add_transaction(params_query, self.request_body)
                
                return self._make_response(response["status"], response["body"]) 
            
            elif self.request_method == "GET" and self.routes_validation["clientes-extrato"].match(self.path):                

                params_query = int(self.path.split("/")[2])

                response = self.clientService.get_client(params_query)

                return self._make_response(response["status"], response["body"]) 
            
            elif self.request_method == "GET":                
                return self._make_response(HTTPStatus.OK, "Richa Backend - Maxson Almeida!")    
            
            return self._make_response(HTTPStatus.METHOD_NOT_ALLOWED, "Method Not Allowed")
        
        elif self.request_method == "GET":                
                return self._make_response(HTTPStatus.OK, "Hello, world!")

        return self._make_response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal Server Error")