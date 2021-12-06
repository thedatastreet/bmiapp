#Build a docker image named bmiapp by using the docker build command

docker build -t bmiapp .

#Run the docker image by using the following command

docker run -p 80:5000 bmiapp
