# Downloading Docker on EC2

## Update EC2

```bash
sudo apt update
```

## Download Docker

```bash
sudo apt-get install docker.io
```

Additionally, add docker as a user:

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

## Download Docker Compose

Download the version of docker compose that you require and save it as docker-compose in the root directory:

```bash
cd
wget https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-linux-x86_64 -O docker-compose
```

Where the version of docker-compose can be found on the [Docker Compose GitHub](https://github.com/docker/compose#linux).

After downloading the file, it has to be made an executable which can be done as follows:

```bash
chmod +x docker-compose
```

To run docker-compose from any directory, it must be saved to the bashrc file which can be done as follows:

1. Open up bashrc using the command `nano ~/.bashrc`
2. Paste the following path into the bashrc ` export PATH="${HOME}:${PATH}"`
3. To save the bashrc, run `source ~/.bashrc`

To check if docker-compose has been downloaded successfully, run `docker-compose version`. If the version is shown, hten the downlaod is successful.

