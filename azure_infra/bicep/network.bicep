param location string
param appName string

resource networkSecurityGroup 'Microsoft.Network/networkSecurityGroups@2019-11-01' = {
  name: '${appName}-nsg'
  location: location
  properties: {
    securityRules: [
      {
        name: 'AllowSshAndHttp'
        properties: {
          description: 'Allow SSH and HTTP access'
          protocol: 'Tcp'
          sourcePortRange: '*'
          destinationPortRanges: ['22', '80']
          sourceAddressPrefix: '*'
          destinationAddressPrefix: '*'
          access: 'Allow'
          priority: 100
          direction: 'Inbound'
        }
      }
    ]
  }
}

resource virtualNetwork 'Microsoft.Network/virtualNetworks@2022-11-01' = {
  name: '${appName}-network'
  location: location
  extendedLocation: null
  tags: {}
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/29'
      ]
    }
    subnets: [
      {
        name: 'default'
        properties: {
          addressPrefix: '10.0.0.0/29'
          networkSecurityGroup: {
            id: networkSecurityGroup.id
          }
        }
      }
    ]
    enableDdosProtection: false
  }
  dependsOn: []
}

resource publicIP 'Microsoft.Network/publicIPAddresses@2022-11-01' = {
  name: '${appName}-public-ip'
  location: location
  properties: {
    publicIPAllocationMethod: 'Static'
    dnsSettings: {
      domainNameLabel: appName
      fqdn: '${appName}.${location}.cloudapp.azure.com'
    }
  }
  sku: {
    name: 'Basic'
  }
  dependsOn:[
    virtualNetwork
  ]
}

resource networkInterface 'Microsoft.Network/networkInterfaces@2022-11-01' = {
  name: '${appName}-network-interface'
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'Ipv4config'
        properties: {
          privateIPAddressVersion: 'IPv4'
          privateIPAllocationMethod: 'Dynamic'
          subnet: {
            id: resourceId('Microsoft.Network/VirtualNetworks/subnets', '${appName}-network', 'default')
          }
          publicIPAddress: {
            id: publicIP.id
          }
        }
      }
    ]
  }
  tags: {}
  dependsOn: [virtualNetwork]
}

output networkInterfaceId string = networkInterface.id
