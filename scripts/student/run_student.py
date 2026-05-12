#!/usr/bin/env python3
"""
Cyber‑Nexus Student Fine‑tuning Script
Runs on GPU 1 (L4), monitors clean data batches and incrementally fine‑tunes the 8B model.
"""

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

import torch, glob, time, shutil
from datasets import load_dataset
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, TrainingArguments,
    Trainer, DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, PeftModel

# ======================== Configuration ========================
STUDENT_MODEL = "Qwen/Qwen3-8B"
DATA_DIR = "data/clean_batches"
OUTPUT_DIR = "./cyber_nexus_8b_lora"
ARCHIVE_DIR = "data/archive"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# ======================== Training Function ========================
def train():
    files = glob.glob(f"{DATA_DIR}/*.jsonl")
    if not files:
        return

    print(f"🔥 [Student] Found {len(files)} new batch(es). Starting incremental fine‑tuning...")

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(STUDENT_MODEL, trust_remote_code=True, use_fast=False)

    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        STUDENT_MODEL,
        torch_dtype=torch.bfloat16,
        device_map={"": 0},
        trust_remote_code=True
    )
    model.gradient_checkpointing_enable()

    # If a previous adapter exists, merge it before training
    if os.path.exists(f"{OUTPUT_DIR}/final/adapter_model.safetensors"):
        print("🧬 [Student] Loading previous adapter for incremental training...")
        model = PeftModel.from_pretrained(model, f"{OUTPUT_DIR}/final")
        model = model.merge_and_unload()

    # Configure new LoRA
    peft_config = LoraConfig(
        r=64,
        lora_alpha=128,
        lora_dropout=0.0,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, peft_config)

    # Load and tokenize dataset
    dataset = load_dataset("json", data_files=files, split="train")
    dataset = dataset.map(
        lambda x: {"text": tokenizer.apply_chat_template(x["messages"], tokenize=False, add_generation_prompt=False)},
        batched=False
    )
    tokenized = dataset.map(
        lambda x: tokenizer(x["text"], truncation=True, max_length=2048),
        batched=True
    )

    # Training arguments
    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        num_train_epochs=1,
        learning_rate=2e-4,
        bf16=True,
        save_strategy="no",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    )

    # Train and save
    trainer.train()
    model.save_pretrained(f"{OUTPUT_DIR}/final")

    # Archive processed batches to prevent re‑training
    for f in files:
        shutil.move(f, os.path.join(ARCHIVE_DIR, os.path.basename(f)))

    print("✅ [Student] Fine‑tuning complete. Adapter saved.")

# ======================== Main Loop ========================
while True:
    train()
    time.sleep(300)