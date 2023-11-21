# Capstone Design
## Object
* Make framework for automatically collecting smart contract and reporting vulnerability

## Structure
* This framework consists of serveral components: 
    * server for reporting vulnerability by web service
    * master server for collecting smart contract and managing fuzzing dockers
    * docker for fuzzing 
### Web server
* Receive data from managing server and post it to the web page
### Master server
* Crawl smart contract and send it to serveral dockers
* Receive vulnerability datas from serveral dockers
### Docker
* Receive smart contract address from managing server
* Get source code from ethereum address and fuzz it
* Send data about vulnerability to the managing server
