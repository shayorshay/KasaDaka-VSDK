# KasaDaka-Voice Service Development Kit including mobile payment prototype

## modify Asterisk extensions.conf file - include
exten => sms,1,Verbose(Incoming SMS from ${CALLERID(num)} ${BASE64_DECODE(${SMS_BASE64})})
exten => sms,n,System(AGI(/shellscript.sh, ${CALLERID(num), ${BASE64_DECODE(${SMS_BASE64}))
exten => sms,n,Hangup()

## create shell script (shellscript.sh) - run
python /var/www/vsdk/populate.py $*

