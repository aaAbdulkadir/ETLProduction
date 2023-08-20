# Setting up AWS CLI

## Downloading the CLI

Check if AWS CLI is installed by the following command

```bash
aws --version
```

If not installed then follow as shown below:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

To ensure install run `aws --version` again.

## Configuring CLI 

Check if you have configured a profile

```bash
aws configure list
```

If there is nothing set then follow as shown below:

1. Go to IAM
2. Click on Users
3. Click on Security Credentials tab
4. Create an Access Key
5. Select CLI use case
6. Go to your CLI and type:

    ```bash
    aws configure
    ```
7. Copy and paste in your Access Key ID
8. Copy and paste in your Secret Access Key
8. Put in your default region name (can be found in aws nav bar)
