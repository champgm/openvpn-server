## Prerequisites:
* Create a keypair in EC2 at https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#KeyPairs:
* Remember the name of that keypair OR create it in `us-west-2` with the name `vpn-west-2` (the default for the deployment script)
* Set up your AWS account on the machine where you'll do your deployment.

## Deploy
You should just be able to run `python .\deploy.py` but I guess the python script has some dependencies... I didn't think of that. Someone should probably add a `requirements.txt` file and update the doc. Oh damn, the script doesn't take input for the keypair name either... that should be fixed too.

## TODOs:
Oops.
* Add a `requirements.txt` file to the repo and document how to install them
* Enhance `deploy.py` so it takes keypair name as a parameter and feeds it to the CFN template
