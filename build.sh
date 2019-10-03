rm -rf ./docker/context/dockerdist/*
touch ./docker/context/dockerdist/README.md
mkdir -p ./docker/context/dockerdist/src/ && cp -Rf ./src/* ./docker/context/dockerdist/src/
mkdir -p ./docker/context/dockerdist/samples/ && cp -Rf ./samples/* ./docker/context/dockerdist/samples/
mkdir -p ./docker/context/dockerdist/img_94A/
cp -Rf ./housthon.iml ./docker/context/dockerdist/
cp -Rf ./launch.py ./docker/context/dockerdist/
cp -Rf ./setup.py ./docker/context/dockerdist/
cp -Rf ./entrypoint.sh ./docker/context/dockerdist/
cp -Rf ./requirements.txt ./docker/context/dockerdist/

docker-compose -f ./docker/housthon.yml build
