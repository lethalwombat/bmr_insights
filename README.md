### Application deployment steps using Microsoft Azure infrastructure

#### 1. Clone the repo into your local machine
#### 2. Clone the Provision Azure infrastrucure 
```
cd azure_infra && ./build.sh
```
#### 3. Verify the infrastructure in the Azure portal
#### 4. Upload application assets into the newly provisioned virtual machine
Make note of the provisioned public ip address, for example `20.213.89.69` and upload the application assets
```
cd post_deployment && ./upload_assets.sh 20.213.89.69
```
#### 5. Install docker
The above step will ssh you into the provisioned virtual machine. Once in the virtual machine, assume the sudo role and run the `docker_install.sh` to install Docker
```
sudo -i
```
```
cd /home/azureuser && ./docker_install.sh
```
Once done, exit the sudo role
```
exit
```
#### 6. Clone the repo into the Azure virtual machine 
```
cd ~ && ./repo_clone.sh
```
#### 7. Navigate into the app directory and start the application
```
cd ~/bmr_insights && ./start_app.sh
```
#### 8. Application is available at the address below
http://bmr-calculator.australiaeast.cloudapp.azure.com/
#### 9. Shut down and destroy (optional)
In your local machine run
```
cd azure_infra && ./destroy.sh
```
