Group Members - Group No. 5 :

    * Faseem Shanavas	    B190515CS
    * Abhinav Ajithkumar	B180461CS
    * Amal Firosh Thayyil	B190848CS
    * Aravind I M	        B180461CS

CODE EXECUTION DETAILS :

    Domain Name of VM which is already running : server
    Domain Name of VM which will be started by the autoscale : server-clone

    * Run the autoscaler on the host via the following commannd
        -> python3 myautoscaler.py

    * Run the  client program in the host via the following command
        1) For lowload mode
            -> python3 myclient.py 1 1
        2) For highload mode
            -> python3 myclient.py 10 5

    * Run the myserver.py file on both VMs as a background process using the myserver.service file


