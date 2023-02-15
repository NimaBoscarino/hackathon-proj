import gradio as gr
from huggingface_hub import get_repo_discussions, get_discussion_details
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import base64


def decrypt_claim(encrypted_claim_encoded, private_key_file):
    base64_encoded = encrypted_claim_encoded.split("\n")[1]
    encrypted_claim_encoded = encrypted_claim_encoded.split('\n')[1]
    b64_fixed = bytes(base64_encoded[2:-1], 'utf-8')
    encrypted_claim = base64.b64decode(b64_fixed)

    private_key = RSA.import_key(open(private_key_file.name).read())

    enc_session_key, nonce, tag, ciphertext = \
        [encrypted_claim for x in (private_key.size_in_bytes(), 16, 16, -1)]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    decrypted_claim = data.decode("utf-8")

    return decrypted_claim


def get_claim(claim_id, private_key):
    claims = []

    # TODO: Currently fetching ALL discussions, in case we want to build a view to see list of discussions in the claim-review space
    # for discussion in get_repo_discussions(repo_id="Team8/dataset", repo_type="dataset"):
    #     claims = claims + [discussion]
    #     # print(f"{discussion.num} - {discussion.title}, pr: {discussion.is_pull_request}")
    #
    # claim = [c for c in claims if c.num == claim_id][0]

    claim = get_discussion_details(
        repo_id="Team8/dataset",
        repo_type="dataset",
        discussion_num=int(claim_id)
    )

    return gr.Textbox.update(value=claim.title), gr.Textbox.update(value=decrypt_claim(claim.events[0].content, private_key))


demo = gr.Blocks()

with demo:
    gr.Markdown(
        """
    # Flip Text!
    Start typing below to see the output.
    """
    )
    button = gr.Button(value="Fetch Claim")
    private_key = gr.File(label="Private Key")

    claim_id = gr.Number()
    claim_title = gr.Textbox(label="Claim Title", value="")
    claim_text = gr.Textbox(label="Claim Text", value="")

    button.click(
        fn=get_claim,
        inputs=[claim_id, private_key],
        outputs=[claim_title, claim_text]
    )

demo.launch()
