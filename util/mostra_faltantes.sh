#!/bin/bash
#############################################
# Criado em: 13/11/2011 01:11:34 AM
# Sergio Cioban Filho
#############################################


###
# Funcoes especiais BASH
# Sergio Cioban Filho
typeset -ir STATUS_COL=70
typeset -i WAIT_COL="$STATUS_COL - 4"
###
function info() {
    echo -n "   - $1"
}
function red() {
    echo -en "\\033[1;31m"
}
function green() {
    echo -en "\\033[0;32m"
}
function yellow() {
    echo -en "\\033[2;33m"
}
function blue() {
    echo -en "\\033[0;34m"
}
function orange() {
    echo -en "\\033[0;33m"
}
function bold() {
        echo -en "\\033[1;39m"
}
function default() {
    echo -en "\\033[0;39m"
}
function infoOk() {
    tab $STATUS_COL
    green
    echo "OK"
    default
}
function infoFail() {
    tab $STATUS_COL
    red
    echo "NOK"
    default
}
function infoWarn() {
    tab $STATUS_COL
    yellow
    echo "ATENCAO"
    default
}
function tab() {
        RES_COL=$1
        echo -en "\\033[${RES_COL}G"
}
function cmd_wait() {

    SLEEP="sleep 1"
    usleep 1 > /dev/null 2> /dev/null
    if [ $? -eq 0  ]; then
        SLEEP="usleep 50000"
    fi

    tab $STATUS_COL ; orange ; echo -n "AGUARDE"; default
    while [ `ps -ef | awk '{ print $2; }' | grep "\<$1\>" | wc -l | awk '{ print $1; }'` -eq 1 ]
    do
        for PROGRESS in / - \\ \|
        do
            tab $WAIT_COL
            echo -n "[$PROGRESS]"
            `$SLEEP`
        done
    done

    tab $WAIT_COL; echo -n "   "
    tab $STATUS_COL ; default; echo -n "        "
}

function lowerCase() {
    LOWER='abcdefghijklmnopqrstuvwxyz'
    UPPER='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    echo $1 | sed 'y/$UPPER/$LOWER/'
}
###########################


if [ -z $1 ]; then
	echo "Falta arquivo pagseguro"
	exit 1
fi

cat "$1" | grep -v 'Cancelada' | while read DATA
do
	T_ID=`echo $DATA | awk '{ print $1 }' | sed 's/\-//g'`
	#echo $T_ID
	#echo $DATA
	#break
	teste=`echo "select * from event_subscribe where TransacaoID=\"$T_ID\";"  | sqlite3 ../subscribe.db`
	if [ -z "$teste" ]; then
		reference=`echo $DATA | awk -F'/' '{ print $NF }' | awk '{print $3 }'`
		STATUS=`echo $DATA | awk -F'@' '{print $2}' | awk '{print $4}'`
		NOME=`echo "select first_name,last_name,email,person_city,person_state from person_userprofile INNER JOIN auth_user ON person_userprofile.user_id=auth_user.id WHERE person_userprofile.activation_key=\"$reference\";" | sqlite3 ../subscribe.db`
		if [ -n "$NOME" ]; then
			echo " => $NOME - $STATUS"
			echo $DATA
		fi
	fi
done
