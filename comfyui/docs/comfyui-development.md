# ComfyUI developer notes

User setup: [README](../README.md). This folder is the standalone `kandinsky6`
package; the repository's Python pipeline is not a runtime dependency.

## Packaging and publishing

Run from `comfyui/`:

```bash
comfy --skip-prompt --no-enable-telemetry node pack
```

This builds `node.zip` without publishing. The package must be Git-tracked;
`.comfyignore` excludes tests, developer notes and generated files.
To publish an explicitly approved release, set a new semantic version in
`pyproject.toml` and run `comfy node publish` from this folder. Use the Comfy
Registry publishing key for publisher `kandinskylab`, not a GitHub PAT.
No merge or push automatically publishes this package.

## Model downloads

Use **Download models** in the template's setup note or the **Kandinsky 6** menu.
It downloads only after confirmation and reuses existing files. Exact public
URLs and destinations are recorded in each template's `properties.models` and
`properties.kandinsky6_required_files`; companion JSON files must stay beside
their weights. Models are placed under ComfyUI's configured model directories:

- `diffusion_models/`: Pro transformer and the SR Diffusers components.
- `text_encoders/`: Qwen3.5 beautifier, Qwen2.5-VL and CLIP-L.
- `vae/`: Hunyuan Video VAE.
- `audio_vae/`: audio VAE and `bigvgan_vocoder/`.

Distilled Pro defaults to 10 PiFlow steps, CFG 1 and automatic MagCache bypass.
Non-distilled Pro uses the normal Comfy sampler; set 50 steps and matching
MagCache steps. Gated HF checkpoints require access approval and authentication.

## Native Qwen with an older NVIDIA driver

The beautifier uses native Qwen3.5 and `CLIP.generate`, including the input image
for I2VA. No Comfy core edits or external LLM runtime are required.

Some compiled `comfy-kitchen` wheels require a newer NVIDIA driver. With ComfyUI
0.38.0 and driver 570, the official Python-only wheel of the same pinned
comfy-kitchen 0.2.36 was tested on H100 with Torch 2.10.0+cu128:

```bash
python -m pip install --force-reinstall --no-deps \
  https://files.pythonhosted.org/packages/38/23/a6787aac01d7c28ae3cb07579ba839297a35e6fad66baac096916246cc7f/comfy_kitchen-0.2.36-py3-none-any.whl
```

Use ComfyUI's Python, then restart. This replaces kitchen's compiled CUDA/HIP
kernels with its supported Triton/eager paths; inference remains on GPU.
Sage/Flash Attention are separate installations. For another ComfyUI version,
match its own kitchen requirement rather than forcing this pin.
[Upstream compatibility report](https://github.com/Comfy-Org/ComfyUI/issues/16455).

## Validation

Before releasing, run both shipped templates on GPU, including beautifier,
audio, SR and model reuse. Development tests are maintained separately and are
not shipped with this package.
