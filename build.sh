rm -rf ./docker/context/dockerdist/*
touch ./docker/context/dockerdist/README.md
cp -Rf ./housthon.iml ./docker/context/dockerdist/
cp -Rf ./launch.py ./docker/context/dockerdist/
cp -Rf ./setup.py ./docker/context/dockerdist/
cp -Rf ./entrypoint.sh ./docker/context/dockerdist/
cp -Rf ./requirements.txt ./docker/context/dockerdist/

docker-compose -f ./docker/housthon.yml build
