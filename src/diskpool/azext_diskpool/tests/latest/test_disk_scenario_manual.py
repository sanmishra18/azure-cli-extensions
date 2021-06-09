# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------
import mock
from azure.cli.testsdk import ScenarioTest
from azure.cli.testsdk import ResourceGroupPreparer


class DiskpoolScenarioTest(ScenarioTest):
    @ResourceGroupPreparer(name_prefix='clitest', location='eastus', random_name_length=16)
    def test_diskpool_scenario_manual(self, resource_group):
        self.kwargs.update({
            'rg': resource_group,
            'diskName': self.create_random_name(prefix='disk', length=10),
            'diskName2': self.create_random_name(prefix='disk', length=10),
            'vnet': self.create_random_name(prefix='vnet', length=10),
            'subnet': self.create_random_name(prefix='subnet', length=10),
            'subnetPrefix': '10.0.0.0/24',
            'zone': "3",
            'diskPoolName': self.create_random_name(prefix='diskpool', length=16),
            'location': 'eastus',
            'targetName': self.create_random_name(prefix='iscsi', length=10),
            'storagePoolObjectId': '09f10f07-08cf-4ab7-be0f-e9ae3d72b9ad'
        })
        result = self.cmd('disk create --name {diskName} --resource-group {rg} --zone {zone} --location {location} '
                          '--sku Premium_LRS --max-shares 2 --size-gb 256').get_output_in_json()
        self.kwargs['diskId'] = result['id']
        result = self.cmd('disk create --name {diskName2} --resource-group {rg} --zone {zone} --location {location} '
                          '--sku Premium_LRS --max-shares 2 --size-gb 256').get_output_in_json()
        self.kwargs['diskId2'] = result['id']
        with mock.patch('azure.cli.command_modules.role.custom._gen_guid', side_effect=self.create_guid):
            self.cmd('role assignment create --assignee-object-id {storagePoolObjectId} --role "Virtual Machine Contributor" --scope {diskId}')
        with mock.patch('azure.cli.command_modules.role.custom._gen_guid', side_effect=self.create_guid):
            self.cmd('role assignment create --assignee-object-id {storagePoolObjectId} --role "Virtual Machine Contributor" --scope {diskId2}')

        self.cmd('network vnet create --name {vnet} --resource-group {rg} --location {location}')
        result = self.cmd('network vnet subnet create --name {subnet} --vnet-name {vnet} --resource-group {rg} '
                          '--address-prefixes {subnetPrefix} --delegations Microsoft.StoragePool/diskPools').get_output_in_json()
        self.kwargs['subnetId'] = result['id']

        # Create a Disk Pool
        self.cmd('disk-pool create --name {diskPoolName} --resource-group {rg} --location {location} '
                 '--availability-zones {zone} --subnet-id {subnetId} --sku name="Standard" tier="Standard" '
                 '--disks {diskId}', checks=[self.check('name', '{diskPoolName}'),
                                             self.check('availabilityZones[0]', '{zone}'),
                                             self.check('disks[0].id', '{diskId}'),
                                             self.check('subnetId', '{subnetId}'),
                                             self.check('tier', 'Standard')])
        self.cmd('disk-pool show --name {diskPoolName} --resource-group {rg}',
                 checks=[self.check('name', '{diskPoolName}'),
                         self.check('availabilityZones[0]', '{zone}'),
                         self.check('disks[0].id', '{diskId}'),
                         self.check('subnetId', '{subnetId}'),
                         self.check('tier', 'Standard')])
        self.cmd('disk-pool list --resource-group {rg}',
                 checks=[self.check('length(@)', 1)])

        # TODO: Add back when fixed in server
        # self.cmd('disk-pool list-outbound-network-dependency-endpoint --name {diskPoolName} --resource-group {rg}',
        #          checks=[self.check('length(@)', 1)])

        # Create an ISCSI target
        self.cmd('disk-pool iscsi-target create --name {targetName} --disk-pool-name {diskPoolName} '
                 '--resource-group {rg} --acl-mode Dynamic --luns name="lun0" managed-disk-azure-resource-id={diskId}',
                 checks=[self.check('aclMode', 'Dynamic'),
                         self.check('luns[0].managedDiskAzureResourceId', '{diskId}'),
                         self.check('luns[0].name', 'lun0')])
        self.cmd('disk-pool iscsi-target show --name {targetName} --disk-pool-name {diskPoolName} --resource-group {rg}',
                 checks=[self.check('aclMode', 'Dynamic'),
                         self.check('luns[0].managedDiskAzureResourceId', '{diskId}'),
                         self.check('luns[0].name', 'lun0')])
        self.cmd('disk-pool iscsi-target list --disk-pool-name {diskPoolName} --resource-group {rg}',
                 checks=[self.check('length(@)', 1)])

        # Update Disk Pool
        self.cmd('disk-pool update --name {diskPoolName} --resource-group {rg} --disks {diskId} {diskId2}',
                 checks=[self.check('name', '{diskPoolName}'),
                         self.check('disks[0].id', '{diskId}'),
                         self.check('disks[1].id', '{diskId2}')])

        # Update iSCSI target -- add a LUN
        self.cmd('disk-pool iscsi-target update --name {targetName} --disk-pool-name {diskPoolName} '
                 '--resource-group {rg} --luns name="lun0" managed-disk-azure-resource-id={diskId} '
                 '--luns name="lun1" managed-disk-azure-resource-id={diskId2}',
                 checks=[self.check('aclMode', 'Dynamic'),
                         self.check('luns[0].managedDiskAzureResourceId', '{diskId}'),
                         self.check('luns[0].name', 'lun0'),
                         self.check('luns[1].managedDiskAzureResourceId', '{diskId2}'),
                         self.check('luns[1].name', 'lun1')])

        self.cmd('disk-pool stop --name {diskPoolName} --resource-group {rg}')
        self.cmd('disk-pool show --name {diskPoolName} --resource-group {rg}',
                 checks=[self.check('status', 'Stopped (deallocated)')])

        self.cmd('disk-pool start --name {diskPoolName} --resource-group {rg}')
        self.cmd('disk-pool show --name {diskPoolName} --resource-group {rg}',
                 checks=[self.check('status', 'Running')])

        self.cmd('disk-pool iscsi-target delete --name {targetName} --disk-pool-name {diskPoolName} '
                 '--resource-group {rg} -y')
        self.cmd('disk-pool iscsi-target list --disk-pool-name {diskPoolName} --resource-group {rg}',
                 checks=[self.check('length(@)', 0)])

        self.cmd('disk-pool delete --name {diskPoolName} --resource-group {rg} -y')
        self.cmd('disk-pool list --resource-group {rg}',
                 checks=[self.check('length(@)', 0)])

    def test_diskpool_list_sku_scenario_manual(self):
        result = self.cmd('disk-pool list-skus -l eastus ').get_output_in_json()
        self.assertIsNotNone(result)