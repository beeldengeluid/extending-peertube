# INTRODUCTION #

In this document you will find the necessary steps to install LaMachine with Kaldi and Kaldi_nl on Ubuntu 20.04.2 LTS, as well as how to use it. The installation will provide you with a Docker image on which the user will be able to perform ASR.

# PREREQUISITES #

- 60GB of disk space is required
- Docker and Ansible
- sudo rights

# INSTALLATION #

1. LaMachine provides an installation script which can be invoked by the following command:

`bash <(curl -s https://raw.githubusercontent.com/proycon/LaMachine/master/bootstrap.sh)`

2. You are shown the question "Where do you want to install LaMachine?". Check that option 3) shows "supported on your machine" and select that option.

3. In order to select the required packages for Kaldi, select the option "1) Build a new image" in the following step.

4. Press enter in the following step.

5. Select option "1) a stable version" in the following step.

6. Enter "y" in the following step.

7. You are now prompted to enter a name for your LaMachine, for the benefits of this guide we assume you choose "lamachine_1".

8. You are prompted to enter a FQDN or leave the field blank. For the benefits of this we assume you do the latter.

9. In the next step you are asked if you want to share your home folder or a custom folder. In our example we use /home/user/docker_share/.

10. Enter "y" to the following question.

11. Press enter to use the default port 8080.

12. You are shown the Ansible configuration, enter "n" unless you wish to make changes.

13. Now you should see the preselected software packages staged for installation. Enter "y" to edit these. Make sure that the packages included are:
- lamachine-core
- kaldi
- kaldi_nl
- oralhistory
- labirinto

Packages are added and removed by commenting them out using the '#' character. It is advisable to to comment out all other packages unless you are certain that you need them.

# USAGE #

Now that you have a working Kaldi installation on a Docker image. You can start a new image using the following command:

`docker run -it --mount type=bind,source=/home/ubuntu/docker_share,target=/docker_share proycon/lamachine:lamachine_1`

In our example the files we intend to process are shared with the image via the shared directory `docker_share` in our home folder. In this folder the input files are stored in the directory `input` and the output files in `output`. 

While in the docker image, change your working directory to /usr/local/opt/kaldi_nl
