######################### Base Install ##########################
apt update
apt upgrade -y
apt install curl wget make gcc cmake git -y
apt install libssl-dev libz3-dev pkg-config build-essential clang -y

# install openssl
wget https://www.openssl.org/source/openssl-1.1.1w.tar.gz
tar xf ./openssl-1.1.1w.tar.gz
cd openssl-1.1.1w
./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared
make
make install_sw
cd ../

# install dotnet
wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh
chmod +x ./dotnet-install.sh
./dotnet-install.sh --channel 5.0
echo "export PATH=$PATH:/root/.dotnet" >> /root/.bashrc

# install rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# install go
wget https://go.dev/dl/go1.21.4.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.21.4.linux-amd64.tar.gz
echo "export PATH=$PATH:/usr/local/go/bin" >> /root/.bashrc

source /root/.bashrc

# install solc
apt-get install software-properties-common
add-apt-repository ppa:ethereum/ethereum
add-apt-repository ppa:ethereum/ethereum-dev
apt-get update
apt-get install solc -y

######################### IR-Fuzz ###############################
git clone https://github.com/Messi-Q/IR-Fuzz.git
cd ./IR-Fuzz
./initial_.sh
cd ../
#################################################################

######################### Smartian ##############################
git clone https://github.com/SoftSec-KAIST/Smartian.git
cd ./Smartian
git submodule update --init --recursive
cd ../
#################################################################

######################### ityfuzz ###############################
curl -L https://ity.fuzz.land/ | bash
source /root/.bashrc
# ityfuzzup

#################################################################