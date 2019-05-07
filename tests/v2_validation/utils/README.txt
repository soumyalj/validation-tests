In the directory where this repo will be downloaded, make sure rancher cli is configured.
./rancher config

1. Generate the envfile which contains all the envs of the setup.
python3 getenvfile.py
The scripts launchcontainers.py and upgrade.py will use this env file 
2. To launch containers in a env
python3 launchcontainers.py 10
For a 3 node env - "python3 launchcontainers.py 1" [120 containers are launched]
3. To upgrade infra stacks in each inv
python3 upgrade.py 


Note: The scripts can be manually edited to provide any specific env if required
