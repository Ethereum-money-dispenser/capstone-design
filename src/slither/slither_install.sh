git clone https://github.com/crytic/slither.git
cp -r ./for_capstone ./slither/slither/detectors/
echo -e "# added\nfrom .for_capstone.meme_token_blacklist import MemeTokenBlacklist \nfrom .for_capstone.meme_token_mintable import MemeTokenMintable \nfrom .for_capstone.meme_token_burnable import MemeTokenBurnable \nfrom .for_capstone.meme_token_proxy import MemeTokenProxy\nfrom .for_capstone.meme_token_event import MemeTokenEvent" >> ./slither/slither/detectors/all_detectors.py
cd slither
python3 setup.py install