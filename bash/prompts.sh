#!/bin/bash
# Unicode prompts which change based on your time!
# Modify this to your style and put this in your `.bashrc`

declare -A symbols=(["night"]="🌙" ["day"]="🌅" ["break"]="🍩 🍵" ["food"]="🍔 🍟" ["travel"]="🚗" ["drink"]="🍷 🍸" ["24/7"]="💻")
declare -a night=('00' '01' '02' '03' '04' '05') food=('09' 10 13 14 21 22) day=('06' '07' '08')
hour=`date +"%H"`
if [[ "${night[@]}" =~ "$hour" ]]
    then
    c=${symbols["night"]}
elif [[ "${food[@]}" =~ "$hour" ]]
    then
    c=${symbols["food"]}
elif [[ "${day[@]}" =~ "$hour" ]]
    then
    c=${symbols["day"]}
elif [[ $hour == 11 ]]
    then
    c=${symbols["break"]}
elif [[ $hour == 17 ]]
    then
    c=${symbols["travel"]}
elif [[ $hour == 18 ]]
    then
    c=${symbols["drink"]}
else
    c=${symbols["24/7"]}
fi
export PS1='$(date +(%A)\ %B\ %d,\ %Y) [\@] \u@\h (${c} ) (\[\033[96m\]\w\[\033[0m\])\n$ '
