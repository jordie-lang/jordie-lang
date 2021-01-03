# create jordie-lang directory in /usr/lib
mkdir /usr/lib/jordie-lang

# mv jordie-lang files to /usr/lib/jordie-lang
mv * /usr/lib/jordie-lang

# create alias to run jordie-lang when keyword 'jordie' is used
alias jordie="python3 /usr/lib/jordie-lang/jordie.py"

# enable for all useres
echo 'alias jordie="python3 /usr/lib/jordie-lang/jordie.py"' >> /etc/bash.bashrc
