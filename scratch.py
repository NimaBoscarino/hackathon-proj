from huggingface_hub import get_repo_discussions, get_discussion_details

# from huggingface_hub import DatasetFilter, HfApi
from huggingface_hub import hf_hub_download
#
# claim = get_discussion_details(
#     repo_id="Team8/dataset",
#     repo_type="dataset",
#     discussion_num=int(1)
# )
#
# print(claim.events[0].content)

from Crypto.PublicKey import RSA
key = RSA.generate(2048)
pub = key.public_key()

f = open('mykey.pem','wb')
f.write(key.export_key('PEM'))
f.close()

f = open('public_key.pem','wb')
f.write(pub.export_key('PEM'))
f.close()


# api = HfApi()
# filt = DatasetFilter(
#     author="Team8",
#     dataset_name="dataset"
# )
#
# dsets = api.list_datasets(filter=filt)[0]

# print(dsets)

from huggingface_hub import hf_hub_download

loc = hf_hub_download(repo_id="Team8/dataset", repo_type="dataset", filename="README.md")

import yaml

with open(loc) as f:
    front_matter = next(yaml.load_all(f, Loader=yaml.FullLoader))
    print(front_matter["public_key"])


RSA