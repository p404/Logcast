#!/bin/bash
 ROLE_PATH=''$1'/etc/logstash/conf.d'
 OPS_TOOLS_FOLDER=$3
 FILTERS_FOLDER=$4
 HUB=$5

 FILTER_NUMBER=$(ls $OPS_TOOLS_FOLDER/$ROLE_PATH | grep 'filter' | tail -1 | grep -o -E '[0-9]+'| awk '{ SUM += $1} END { print SUM }')
 OUTPUT_NUMBER=$(ls $OPS_TOOLS_FOLDER/$ROLE_PATH | grep 'output' | tail -n 2 | head -n 1 | grep -o -E '[0-9]+'| awk '{ SUM += $1} END { print SUM }')
 NAME_UNDERSCORE="$(sed 's/-/_/g' <<< "$2")"

# GIT Tasks
 git -C $OPS_TOOLS_FOLDER checkout master
 git -C $OPS_TOOLS_FOLDER pull
 if git -C $OPS_TOOLS_FOLDER checkout -b "$1-$2-logs"; then
    cp $FILTERS_FOLDER/output_$2.conf $OPS_TOOLS_FOLDER/$ROLE_PATH/$(expr $OUTPUT_NUMBER + 1)_output_$NAME_UNDERSCORE.conf
    cp $FILTERS_FOLDER/filter_$2.conf $OPS_TOOLS_FOLDER/$ROLE_PATH/$(expr $FILTER_NUMBER + 1)_filter_$NAME_UNDERSCORE.conf
    cp $FILTERS_FOLDER/templates/$2.json $OPS_TOOLS_FOLDER/$ROLE_PATH/templates/$2.json

    case $1 in
        elk1-staging.east)
            sed -i ''  "s#elasticsearch:9200#http://localhost:9200#g" "$OPS_TOOLS_FOLDER/$ROLE_PATH/$(expr $OUTPUT_NUMBER + 1)_output_$NAME_UNDERSCORE.conf"
            ;;
        logstash1.east)
            sed -i ''  "s#elasticsearch:9200#http://elasticsearch-cluster.east:80#g" "$OPS_TOOLS_FOLDER/$ROLE_PATH/$(expr $OUTPUT_NUMBER + 1)_output_$NAME_UNDERSCORE.conf"
            ;;
        phi-logstash1.east)
            sed -i '' "s#elasticsearch:9200#http://phi-elasticsearch1.east:9200#g" "$OPS_TOOLS_FOLDER/$ROLE_PATH/$(expr $OUTPUT_NUMBER + 1)_output_$NAME_UNDERSCORE.conf"
            ;;
    esac

    git -C $OPS_TOOLS_FOLDER add .
    git -C $OPS_TOOLS_FOLDER commit -m "Added new $2 logs"
    git -C $OPS_TOOLS_FOLDER push
    $HUB -C $OPS_TOOLS_FOLDER pull-request -m "Added new $2 logs on $1"
    echo 'Done'
    exit 0
 else
    exit 1
 fi 
