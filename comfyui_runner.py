def gorsel_uret(prompt, index, negative_prompt=""):
    prompt = temizle_prompt(prompt)
    negative_prompt = temizle_prompt(negative_prompt)

    if not prompt:
        raise ValueError("Prompt boş olamaz!")

    with open("workflow_api.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data["4"]["inputs"]["text"] = prompt
    data["5"]["inputs"]["text"] = negative_prompt

    # clip ayarları burada kesin olmalı
    data["4"]["inputs"]["clip"] = ["1", 0]
    data["5"]["inputs"]["clip"] = ["1", 0]

    response = requests.post("http://127.0.0.1:8188/prompt", json=data)

    if response.status_code != 200:
        raise Exception(f"ComfyUI hatası: {response.text}")

    print(f"✅ [{index}] Görsel üretildi.") 