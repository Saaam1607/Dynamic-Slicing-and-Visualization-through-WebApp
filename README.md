# ProgettoNet2

## Access web application outside vagrant
1) Exit the vagrant machine
2) Add this line to the vagrant file 
   ```
   config.vm.network "private_network", tyoe: "dhcp"
   ```
3) Run `vagrant reload`
4) Run `vagrant ssh`
5) Now a new ip address is assigned to the vagrant machine, we will use it to access the web application from outside the vagrant machine