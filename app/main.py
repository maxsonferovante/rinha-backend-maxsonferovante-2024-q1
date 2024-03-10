import fastwsgi
from api.handler import Handler
from api.settings import settings


def app(environ, start_response):

    handler = Handler(environ = environ,
                   start_response = start_response,
                   routes= (
                       {
                           "name": 'clientes-extrato', # 'name' is optional, but it's a good practice to name the routes
                           "path": r"/clientes/\d+/extrato",
                           "methods": ["GET"]
                       },
                        {   
                            "name": 'clientes-transacoes',
                            "path": r"/clientes/\d+/transacoes",
                            "methods": ["POST"]
                        }
                     ))
    
    return handler.run()


if __name__ == "__main__":
    fastwsgi.run(
        wsgi_app=app,
        host=settings.server_host, 
        port=settings.server_port
    )