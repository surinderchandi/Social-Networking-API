
    # runserver_https.py
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("runserver")
    # Adding arguments to specify the port and certificate files
    # Example command: python runserver_https.py 8000
    sys.argv.append("--cert-file=localhost.pem")
    sys.argv.append("--key-file=localhost-key.pem")
    execute_from_command_line(sys.argv)

