How to deploy to akash network

1. download docker at https://docs.docker.com/get-docker/
2. Install it. (Could be possible, that you have to enable Hardware assisted virtualization in your bios settings first)
3. Create a user at https://hub.docker.com/
4. Create a repository called wizardapi on docker hub. https://hub.docker.com/repository/create
5. start docker desktop
6. open a terminal window and navigate to the folder containing the dockerfile
7. run 'docker build --pull --rm -f "Dockerfile" -t yourdockerusername/wizardapi:version "."' example value for -t: zjuuu/wizardapi:1.0
8. run docker push yourdockerusername/wizardapi:version
9. open a akash deploytool of your choice ex. cloudmos
10. create a new deployment with the supplied sdl in akash-sdl.yml
11. replace the name of the docker image in line 5 to your name and version you find on hub.docker.com. Please note that your docker image has to be public to be visible by hosting providers on akash.
12. set your domain in line 10
13. set the environment variables in line 14 and 15
14. Click deploy and wait to receive a link to your deployment

Please note that you have to direct the CNAME Record of your domain to the supplied url from akash network to use your own domain.