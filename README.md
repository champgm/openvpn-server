## Prerequisites:
* Create a keypair in EC2 at https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#KeyPairs:
* Remember the name of that keypair OR create it in `us-west-2` with the name `vpn-west-2` (the default for the deployment script)
* Set up your AWS account on the machine where you'll do your deployment.

## Deploy
You should just be able to run `python .\deploy.py` but I guess the python script has some dependencies... I didn't think of that. Someone should probably add a `requirements.txt` file and update the doc.

*NOTE*: deployment will take some time, especially the Cloudformation bootstrap thing. Give it some time, or SSH in and check its status with the troubleshooting commands.

## Troubleshooting
Once logged into the server, these commands can help you figure out what's going wrong.

### Cloudformation Bootstrap:
```
sudo cat /var/log/cfn-init.log
sudo cat /var/log/cfn-init-cmd.log
```

### Openvpn service startup:
```
systemctl status openvpn-server@server.service
journalctl -xeu openvpn-server@server.service
```

### Openvpn configuration
```
/etc/openvpn/server/server.conf
```
