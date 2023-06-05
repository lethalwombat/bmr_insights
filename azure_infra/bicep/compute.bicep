param location string
param appName string
param networkInterfaceId string
param adminUsername string

resource sshKey 'Microsoft.Compute/sshPublicKeys@2022-11-01' = {
  name: '${appName}-vm-ssh-key'
  location: location
  properties: {
    publicKey: 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDKCn0MtqP3rGaDTcp2lMe3gMrjPqXnh5Q93l7Q9QjytZNNu/w3r2hXS0nYGQ9PAK0fd8ZntzVxlF+CLCTWhRFr22KXhzUZ/G3dv3JzONHJMVF99xP7g2wcwFhln0ffoYlzgoH+3SnqTZ0lgAbM4iP6g1wrtn/OdM5e+5zlfnzzIK/rV9iNub6EaFQcrVhh1YSiUc1jHvFGxstYJyiiFAkORWY5taClgMSeqTrd6YLjSBtYOFphArYLfHLHSgz6CyS2mtoECdfsFk7ALB9k7QcLTzzXJ5CBt60BLtSr4bn+IiIFtMj52ihGJzXk1+6R4tPAuZJzx6a1aaoGOxFAyIUio5VR/8JKoUHcddwCtSaUpogu49tCNf5OJSdnfcx2/s3IkVdvDFQ647rylcz0GuuLxas4C5MaEmU5h8fxhv06I+EiHdaQ8qIkanaafhSR7DMqhIPG1VDZvKm2EBphibr3aeIAIXlPdPGkT1wqTuigCNd1gMbkLG2S2pL1JFXTspU= lethwombie@Earth'
  }
}

resource virtualMachine 'Microsoft.Compute/virtualMachines@2022-03-01' = {
  name: '${appName}-vm'
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1ms'
    }
    storageProfile: {
      osDisk: {
        name: '${appName}-vm-disk'
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
        deleteOption: 'Delete'
      }
      imageReference: {
        publisher: 'canonical'
        offer: '0001-com-ubuntu-server-jammy'
        sku: '22_04-lts-gen2'
        version: 'latest'
      }
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: networkInterfaceId
          properties: {
            deleteOption: 'Detach'
          }
        }
      ]
    }
    osProfile: {
      computerName: appName
      adminUsername: adminUsername
      linuxConfiguration: {
        disablePasswordAuthentication: true
        ssh: {
          publicKeys: [
            {
              path: '/home/azureuser/.ssh/authorized_keys'
              keyData: sshKey.properties.publicKey
            }
          ]
        }
      }
    }
    securityProfile: {
      securityType: 'TrustedLaunch'
      uefiSettings: {
        secureBootEnabled: false
        vTpmEnabled: false
      }
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: false
      }
    }
  }
}
