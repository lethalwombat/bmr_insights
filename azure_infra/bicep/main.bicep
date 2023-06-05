param location string
var appName = 'bmr-calculator'

module networkModule 'network.bicep' = {
  name: 'networkDeploy'
  params: {
    location: location  
    appName: appName
  }
}

module computeModule 'compute.bicep' = {
  name: 'computeDeploy'
  params: {
    location: location
    appName: appName
    adminUsername: 'azureuser'
    networkInterfaceId: networkModule.outputs.networkInterfaceId
  }
}
