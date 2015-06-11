#!/bin/bash
# Unicode Prompts which change based on your time!
# Modify this to your style and call this while executing terminal

declare -A symbols=(["night"]="🌙" ["day"]="🌅" ["break"]="🍩🍵" ["food"]="🍔🍟" ["travel"]="🚗" ["drink"]="🍷🍸" ["24/7"]="💻")
declare -a night=['01','02','03','04','05'] food=['09',10,13,14,21,22] day=['06','07','08']
u_symbols() {
  hour=$`date +"%H"`
  if [[ ${night[*]} =~ hour ]]
  	then
  	c=${symbols["night"]}
  elif [[ ${food[*]} =~ hour ]]
  	then
  	c=${symbols["food"]}
  elif((hour==11))
  	then
  	c=${symbols["break"]}
  elif((hour==17))
  	then
  	c=${symbols["travel"]}
  elif((hour==18))
  	then
  	c=${symbols["drink"]}
  else
  	c=${symbols["24/7"]}
  fi
  PS1='[\@] \u@\h:\w${c} '
};
u_symbols
export PROMPT_COMMAND="u_symbols;"
