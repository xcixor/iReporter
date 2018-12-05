"""App entry point."""

import os

from app import create_app

APP = create_app('default')

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=PORT)
