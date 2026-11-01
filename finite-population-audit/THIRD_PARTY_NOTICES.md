# Third-party notices

## Base model and adapter

Qwen Team / Alibaba Cloud: Qwen2.5-1.5B-Instruct. The pinned upstream model revision is 989aa7980e4cf806f80c7fef2b1adb7bc71aa306. Upstream license: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/989aa7980e4cf806f80c7fef2b1adb7bc71aa306/LICENSE (Apache License 2.0).

The evidence includes an author-trained LoRA adapter; the base model weights are not included. The adapter changes are low-rank updates trained on the documented development set. Original adapter configuration, weights, README and hashes are preserved without modification. No upstream endorsement is implied.

## Teacher and software

The Teacher was openai/gpt-oss-20b served by Groq. Responses and metadata are archived as generated; no provider endorsement or cryptographic origin attestation is implied. Relevant model/service terms continue to apply. See https://console.groq.com/docs/legal/services-agreement and the model's applicable terms.

NumPy, SciPy, py-ecc, Matplotlib, Pandoc and LaTeX retain their respective licenses. They are dependencies, not re-licensed by this release. The package does not vendor these projects' implementations except the generic upstream Apache license text.
