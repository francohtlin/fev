"""Point the checkpoint's base-model reference at the local bundle.

The base model name lives inside head.pt metadata (not adapter_config.json),
and it is an absolute path -- so it must be re-patched on every machine the
bundle lands on. Run via the kev venv, which has torch.
"""
import json, sys, torch, os
bundle = os.path.abspath(sys.argv[1])
head = os.path.join(bundle, "checkpoint", "head.pt")
base = os.path.join(bundle, "base", "Qwen2.5-0.5B")
d = torch.load(head, map_location="cpu", weights_only=False)
d["base"] = base
torch.save(d, head)
cfg = os.path.join(bundle, "checkpoint", "adapter_config.json")
c = json.load(open(cfg)); c["base_model_name_or_path"] = base
json.dump(c, open(cfg, "w"), indent=1)
print("base ->", base)
