cd app
# go to https://fastforex.readme.io/ create an account to get your own FAST_FOREX_API_KEY
export FAST_FOREX_API_KEY='4c8c86ff34-711826bf4b-rfbs99'
export JWT_SECRET='SdyGEj0GJs6NDOYuYhDS1CF2abc'
# SECRET_KEY used by the hashing fuction to hash passwords
export SECRET_KEY='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
# The kind of hashing algorithm to use
export ALGORITHM="HS256"
# You can set the to what ever time you want `Note` the time given is calcuated in minutes
export ACCESS_TOKEN_EXPIRE_MINUTES=30
sudo DOCKER_BUILDKIT=1 docker build -t currecyconverterapi -f Dockerfile .
sudo docker container run -e FAST_FOREX_API_KEY=$FAST_FOREX_API_KEY -e JWT_SECRET=$JWT_SECRET -e SECRET_KEY=$SECRET_KEY -e ALGORITHM=$ALGORITHM -e ACCESS_TOKEN_EXPIRE_MINUTES=$ACCESS_TOKEN_EXPIRE_MINUTES -p 8000:8000 --name shakeapitest currecyconverterapi


docker rm $(docker stop $(docker ps -a -q))