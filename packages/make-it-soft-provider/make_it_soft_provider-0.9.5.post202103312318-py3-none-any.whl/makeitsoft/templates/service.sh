#!/bin/bash
#
# Copyright (c) 2017 EFAB Corporate
#

set -o errexit
set -o pipefail

silentMode=false

usage () {
   echo "Argument incorrect !"
   echo "Usage: service.sh start|stop|status|status-simple|reset [appname] [-s]"
   exit 1
}

log () {
   if [[ $silentMode = false ]]; then
      echo -e $1
   fi
}

while getopts ":s:" option; do
    case "${option}" in
        s)
            silentMode=true
            shift
            ;;
        *)
            usage
            ;;
    esac
done

action=$1
appname=$2

# service
log "Service - Start time: $(date)"

case "$action" in
   "start") 
        actionLabel="Demarrage"
        operation="up -d"
   ;;
   "stop") 
        actionLabel="Arret" 
        operation="stop"
   ;;
   "status") 
        actionLabel="Statut" 
        operation="ps"
   ;;
   "status-simple")
        actionLabel="Statut Simple"
   ;;
   "reset")
        actionLabel="Reset"
        operation="down -v"
   ;;
   *)
        usage
esac

if [ -z "$appname" ]
    then actionLabel="$actionLabel des applications"
    else actionLabel="$actionLabel de l'application $appname"
fi

#cd {{ variables['output_dir'] }}
log ""

log "$actionLabel"
for dir in */
do
    if [[ -d $dir ]]; then
        app=$(basename "$dir")
        if [ -z "$appname" ]
            then 
                log "Application : $app"
                docker-compose -f "$dir/docker-compose.yml" $operation
                log ""
            else
                if [ "$app" = "$appname" ]
                    then
                        log "Application : $appname"
                        case "$action" in
                           "start")
                                docker-compose -f "$dir/docker-compose.yml" $operation
                           ;;
                           "stop")
                                docker-compose -f "$dir/docker-compose.yml" $operation
                           ;;
                           "status")
                                docker-compose -f "$dir/docker-compose.yml" $operation
                           ;;
                           "status-simple")
                                cd "$dir/" >/dev/null 2>&1
                                docker inspect -f '{{ '{{.State.Status}}' }}' $(docker-compose ps -q $appname)
                                cd - >/dev/null 2>&1
                           ;;
                           "reset")
                                docker-compose -f "$dir/docker-compose.yml" $operation
                           ;;
                           *)
                                usage
                        esac
                        log ""
                fi
        fi		
    fi
done

# service
log "Service - End time: $(date)"