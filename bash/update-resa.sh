#!/bin/bash
set -e
BASE_IMAGE="resa"
REGISTRY="bdeinsalyon"
IMAGE="$REGISTRY/$BASE_IMAGE"
CID=$(docker ps | grep $IMAGE | awk '{print $1}')
docker pull $IMAGE

for im in $CID
do
    LATEST=`docker inspect --format "{{.Id}}" $IMAGE`
    RUNNING=`docker inspect --format "{{.Image}}" $im`
    NAME=`docker inspect --format '{{.Name}}' $im | sed "s/\///g"`
    echo "Latest:" $LATEST
    echo "Running:" $RUNNING
    if [ "$RUNNING" != "$LATEST" ];then
        echo "upgrading $NAME"
        docker stop $NAME
        docker rm -f $NAME
        docker run --name $NAME \
            --env-file /var/conf/environements/$NAME.env \
            -v /var/www/$NAME:/app/staticfiles \
            --restart always \
            --network web \
            -d $IMAGE
    else
        echo "$NAME up to date"
    fi
done
