#! /bin/bash
# resource group name and location
rg=rg-bmr-calculator
location=australiaeast

# create the destroy script
echo "#! /bin/bash" > destroy.sh
echo "az group delete -n $rg --no-wait -y" >> destroy.sh

# create the resource group
az group create -n $rg -l $location -o table

# build infrastructure from bicep files
az deployment group create \
  --name BMRCalculatorDeployment \
  --resource-group $rg \
  --template-file bicep/main.bicep\
  --parameters location=$location\
  -o table
