### Application deployment steps using Microsoft Azure infrastructure

#### 1. Provision Azure infrastrucure 
```
cd azure_infra && ./build.sh
```
#### 2. Verify the infrastructure in the Azure portal
#### 3. Upload application assets into the newly provisioned virtual machine
Make note of the provisioned public ip address, for example `20.213.89.69` and upload the application assets
```
cd post_deployment && ./upload_assets.sh 20.213.89.69
```
