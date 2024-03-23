# cbm-email-ziplog-to-file
cbm-email-ziplog-to-file
# install python env
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
ln -s ~/github/cbm-email-ziplog-to-file/.procmailrc ~/.procmailrc
eval "$(/home/ceds_log/miniforge3/bin/conda shell.bash hook)"
conda init
conda create -n procmail python=3.12
conda activate procmail
pip install eml-parser
