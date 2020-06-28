from app import create_app
import os
import sys
from config import ProductionConfig, DevelopmentConfig

PORT = "5000"

def main(args=[]):
    app_port = PORT if len(args)<=1 else args[1]

    environment = os.getenv('TUTUBO_ENV')
    
    config = ProductionConfig() if environment == "PROD" else DevelopmentConfig()
    app = create_app(config)
    
    print("Raising AuthServer in port", app_port)
    app.run(host="0.0.0.0", port=app_port)

# -- Run

if __name__ == '__main__':
    main(sys.argv)
    