# Capstone Design
## Object
## Structure
## Dependencies
### IR-Fuzz
* CMake: >=3.5.1
* Python: >=3.5（ideally 3.6）
* Go: >=1.15
* leveldb 1.20
* Geth & Tools: geth, evm, etc
* solc: 0.4.26
* numpy
## Dependency commands
```shell
sudo apt install cmake
sudo apt install python3
sudo apt install python-is-python3
python -m pip install numpy
sudo wget https://golang.org/dl/go1.21.4.linux-amd64.tar.gz
rm -rf /usr/local/go
tar -C /usr/local -xzf go1.21.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
sudo apt-get install libsnappy-dev
git clone https://github.com/google/leveldb.git
cd leveldb/
make
sudo scp out-static/lib* out-shared/lib* /usr/local/lib/
cd include/
sudo scp -r leveldb /usr/local/include/
sudo ldconfig
cd ../../
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum
sudo apt-get install solc
```