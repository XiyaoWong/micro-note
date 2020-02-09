curPath=$(readlink -f "$(dirname "$0")")
source "$curPath/../env/bin/activate"
gunicorn -w 3 -b 0.0.0.0:5000 app:app