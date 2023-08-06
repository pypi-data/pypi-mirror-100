# hyperkv
## Get Hyper-V Key Value Pairs on Linux Guest

Simple parser of the files made by `hv_kvp_daemon` on a Linux guest. This allows a guest to determine its name, the host's name, etc. [Learn more about Hyper-V Data Exchange here](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-R2-and-2012/dn798287(v=ws.11)#linux-guests).

## Install
```sh
pip install hyperkv
```

## Usage
```sh
hyperkv
```
will write the contents as a JSON to standard out like this:
```json
{
  "HostName": "thehost.example.com",
  "HostingSystemEditionId": "8",
  "HostingSystemNestedLevel": "0",
  "HostingSystemOsMajor": "10",
  "HostingSystemOsMinor": "0",
  "HostingSystemProcessorArchitecture": "9",
  "HostingSystemProcessorIdleStateMax": "0",
  "HostingSystemProcessorThrottleMax": "100",
  "HostingSystemProcessorThrottleMin": "5",
  "HostingSystemSpMajor": "0",
  "HostingSystemSpMinor": "0",
  "PhysicalHostName": "THEHOST",
  "PhysicalHostNameFullyQualified": "thehost.example.com",
  "VirtualMachineDynamicMemoryBalancingEnabled": "0",
  "VirtualMachineId": "461B2364-3901-4349-B3C2-FA4821CBEEFE",
  "VirtualMachineName": "my-guest-vm"
}
```
By default, this script reads from `/var/lib/hyperv/.kvp_pool_3`, but you can specify a different path with `-f`
```sh
hyperkv -f /var/lib/hyperv/.kvp_pool_2
```

## Requirements
`hv_kvp_daemon` must be installed and working. If it is working, you will find files in `/var/lib/hyperv`.

### Ubuntu
```sh
apt-get install linux-azure linux-azure-tools
grub-update
```
At boot time, you need to pick advanced startup and make sure it boots with the newly installed Azure kernel. To make that more permanent, you can open `/etc/default/grub`, add the line `GRUB_SAVEDEFAULT=true`, and change `GRUB_DEFAULT=0` to `GRUB_DEFAULT=saved`. The next time you boot, choose the Azure kernel and that will become the default until you pick a different one at the GRUB menu.
