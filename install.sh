cd $HOME
git clone git@github.com:EwanValentine/k8ie.git

cd k8ie
virtualenv venv
. venv/bin/activate
pip3 install --editable .

k8ie --help

rm -rf ~/k8ie
