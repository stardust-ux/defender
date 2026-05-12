#!/usr/bin/env python3
"""
Cyber‑Nexus Teacher Distillation Script
Runs on GPU 0 (L4), generates structured security audit data from seed instructions.
"""

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import torch, json, re, time
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
from safetensors.torch import load_file

# ======================== Configuration ========================
BASE_MODEL = "Qwen/Qwen3-30B-A3B-Instruct-2507"
ADAPTER_PATH = "./adapters/v3_final"
SEED_FILE = "data/seed_instructions.jsonl"
OUTPUT_DIR = "data/clean_batches"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======================== Helper Functions ========================
def parse_action(text):
    """Extract valid tool/deny JSON from model output."""
    if "[行动]" not in text:
        return None
    action_part = text.split("[行动]")[1].strip()
    match = re.search(r'\{[^{}]*\}', action_part)
    if match:
        try:
            obj = json.loads(match.group(0))
            if "tool" in obj or "response" in obj:
                return obj
        except json.JSONDecodeError:
            pass
    return None

def standard_json(instruction):
    """Fallback JSON when model output is unparseable."""
    danger_keywords = ["删除", "rm -rf", "格式化", "禁用", "777", "关闭防火墙", "passwd", "shadow", "sudo rm"]
    if any(k in instruction for k in danger_keywords):
        return '{"response": "Permission denied"}'
    return '{"tool": "bash_tool", "command": "ls -la"}'

# ======================== Load Teacher Model ========================
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

print("🚀 [Teacher] Loading 30B model on GPU 0...")
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map={"": 0},
    trust_remote_code=True
)
peft_config = LoraConfig.from_pretrained(ADAPTER_PATH)
model = get_peft_model(model, peft_config)
model.load_state_dict(load_file(os.path.join(ADAPTER_PATH, "adapter_model.safetensors")), strict=False)
model.eval()
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
print("✅ [Teacher] Model loaded.")

# ======================== Main Distillation Loop ========================
while True:
    if not os.path.exists(SEED_FILE):
        print("⏳ [Teacher] Waiting for seed instructions...")
        time.sleep(30)
        continue

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seeds = [json.loads(line) for line in f]

    batch_data = []
    for idx, inst in enumerate(seeds):
        messages = [
            {"role": "system", "content": "你是 Cyber‑Nexus 战术特工，具备自我防御本能的自动化AI。每次回复必须严格遵循格式：[思考]...\n[行动] JSON"},
            {"role": "user", "content": inst}
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(text, return_tensors="pt").to("cuda")

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=256, do_sample=True, temperature=0.7)

        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        action_obj = parse_action(response)
        action_json = standard_json(inst) if action_obj is None else json.dumps(action_obj, ensure_ascii=False)
        thinking = response.split("[行动]")[0].strip() if "[行动]" in response else "[思考] 分析指令意图。"

        final_content = f"{thinking}\n[行动] {action_json}"
        batch_data.append({
            "messages": [messages[0], messages[1], {"role": "assistant", "content": final_content}]
        })
        print(f"✅ [Teacher] Generated sample {idx+1}/{len(seeds)}")

    # Write batch file
    timestamp = int(time.time())
    batch_file = os.path.join(OUTPUT_DIR, f"batch_{timestamp}.jsonl")
    with open(batch_file, "w", encoding="utf-8") as fout:
        for item in batch_data:
            fout.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"📦 [Teacher] Batch saved: {batch_file}")

    # Sleep before next iteration
    time.sleep(600)