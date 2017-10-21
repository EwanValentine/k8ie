cd $HOME
git clone git@github.com:EwanValentine/k8ie.git

cd k8ie
virtualenv venv
. venv/bin/activate
pip install --editable .

k8ie --help
