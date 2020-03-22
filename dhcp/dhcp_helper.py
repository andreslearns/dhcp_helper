import click
from colorama import *
from netaddr import *

while True:
#start vlan input and error handling
    try:
        office_name = input("OFFICE NAME\t\t: ")
        if not office_name:
            raise ValueError("Empty Input")
        
    except ValueError:
        click.clear()
        RED = '\033[31m'
        print(RED+"INVALID! kindly enter correct office name!")
        print(Style.RESET_ALL)
        continue
           
    try:
        start_vlan = int(input("VLAN START RANGE\t: "))
        
    except ValueError:
        click.clear()
        RED = '\033[31m'
        print(RED + "INVALID! not a valid vlan number!")
        print(Style.RESET_ALL)
        continue
        
#end vlan input and error handling 
    try:
        end_vlan = int(input("VLAN END RANGE\t\t: "))
    
    except ValueError:
        click.clear()
        RED = '\033[31m'
        print(RED+"INVALID! not a valid vlan number!")
        print(Style.RESET_ALL)
        continue
        
#public ip and subnetmask error handling
    try:
        public_ip = input("PUBLIC IP CIDR FORMAT\t: ")
        net = IPNetwork(public_ip)  ### will use ip address formatting
        break


    except AddrFormatError:
        click.clear()
        RED = '\033[31m'
        print(RED+"INVALID! CIDR ipv4 network format!")
        print(Style.RESET_ALL)
        
        
    except:
        click.clear()
        RED = '\033[31m'
        print(RED+"INVALID! not a valid ip address!")
        print(Style.RESET_ALL)
        
    
#variables and conversions
vlanx  = int(start_vlan - 1)
my_dhcp_file = open("dhcp.conf", 'w') #open and write a file
office_name = office_name.upper() #convert the office name to upper case

#loops for dhcp and nat configuration
#main config output
for vlans in range (vlanx, end_vlan):
    vlans = vlans + 1
    my_dhcp_file.write(f"\nint g0/0/2.{vlans}")
    my_dhcp_file.write(f"encapsulation dot1q {vlans}\n")
    my_dhcp_file.write(f"ip address 192.168.{vlans}.254 255.255.255.0\n")
    my_dhcp_file.write(f"ip nat inside\n!\n")
    
    my_dhcp_file.write(f"ip dhcp pool {office_name}_{vlans}\n")
    my_dhcp_file.write(f"network 192.168.{vlans}.0 255.255.255.0\n")
    my_dhcp_file.write(f"default-router 192.168.{vlans}.254\n")
    my_dhcp_file.write(f"dns-server 8.8.8.8 208.67.222.222 208.67.220.220\n!")
    
    my_dhcp_file.write(f"\nip dhcp excluded-address 192.168.{vlans}.254\n!")
    
    my_dhcp_file.write(f"\nip access-list extended O{office_name}_{vlans}\n")
    my_dhcp_file.write(f"permit udp 192.168.{vlans}.0 0.0.0.255 any\n")
    my_dhcp_file.write(f"permit tcp 192.168.{vlans}.0 0.0.0.255 any\n")
    my_dhcp_file.write(f"permit icmp 192.168.{vlans}.0 0.0.0.255 any\n!")
    
    my_dhcp_file.write(f"\nip nat pool net{vlans} {net[vlans]} {net[vlans]} netmask {net.netmask}\n")
    my_dhcp_file.write(f"ip nat inside source list O{office_name}_{vlans} pool net{vlans} overload\n!!!!\n")
    
my_dhcp_file.close()

file_name = "dhcp.conf"

with open(file_name, 'r') as config_file:
    dhcp_content = config_file.read()
    
while True:
    print(f"Do you want to load and display the generated config in terminal?")
    options = input("yes/no: ")
    
    if options == "yes":
        print(dhcp_content)
        break
    else:
        print(f"Thank you for using config generator! you can manually view the config in {file_name}")
        break
    


    
    
    
    

    


    
    

        


