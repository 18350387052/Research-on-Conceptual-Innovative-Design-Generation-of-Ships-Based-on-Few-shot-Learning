# Research on Conceptual Innovative Design Generation of Ships Based on Few-shot Learning

A ComfyUI-based workflow project for few-shot learning-driven ship conceptual design, leveraging SDXL and specialized LoRA models to enable efficient, innovative ship design generation with limited reference samples.

## Project Overview

This project focuses on **conceptual innovative ship design generation** using few-shot learning techniques. By integrating ComfyUI’s modular node-based workflow with the SDXL base model and a ship-design-specific LoRA, we achieve:

- Rapid generation of ship conceptual designs with minimal reference data (few-shot learning paradigm).
- Customizable design parameters (e.g., hull shape, material texture, functional modules) via visual workflow adjustments.
- Reproducibility of experimental results from the associated research paper (via pre-configured workflows).

## Core Dependencies

All tools and models required for this project are open-source and easily accessible. Below are the key resources and their roles:

| Resource Type    | Name & Description                                           | Hosted Address                                               |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Workflow Engine  | **ComfyUI** - Modular node-based interface for stable diffusion pipelines (required for running workflows). | https://github.com/comfyanonymous/ComfyUI.git                |
| Base Model       | **SDXL** - Stable Diffusion XL, the foundational model for high-quality image generation. | Included in the linked LoRA repository (or use official SDXL checkpoints). |
| Specialized LoRA | **Industrial-Design-Extreme-Material-SDXL_v1.0** - LoRA fine-tuned for industrial/ship design, optimizing material texture and structural details. | https://huggingface.co/Awsteam7052/Industrial-Design-Extreme-Material-SDXL_v1.0/tree/main |

## Installation Guide

Follow these steps to set up the project environment (supports Windows, Linux, and macOS; NVIDIA GPUs recommended for optimal performance).

### Step 1: Install ComfyUI

ComfyUI is the core engine for running our ship design workflows. Choose one of the following installation methods:

#### Option A: Windows Portable (Simplest)

1. Download the latest Windows Portable Package from the [ComfyUI Releases Page](https://github.com/comfyanonymous/ComfyUI/releases).
2. Extract the package with 7-Zip (right-click → "Extract Here").
3. Skip to **Step 2** (portable version includes pre-configured dependencies).

#### Option B: Manual Install (All OS)

1. Clone the ComfyUI repository:

   ```bash
   git clone https://github.com/comfyanonymous/ComfyUI.git
   cd ComfyUI
   ```

2. Install Python 3.12 or 3.13 (recommended for compatibility with custom nodes).

3. Install PyTorch (match your GPU type):

   - NVIDIA:

     ```bash
     pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu129
     ```

   - AMD (Linux):

     ```bash
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.4
     ```

     

   - Apple Silicon:

     Follow Apple’s Accelerated PyTorch Guide to install nightly PyTorch.

4. Install ComfyUI dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   

### Step 2: Add SDXL & LoRA Models

Place the base SDXL model and specialized LoRA in ComfyUI’s model directories to ensure the workflow can load them:

1. **SDXL Base Model**:
   - Download the official SDXL checkpoint (e.g., `sdxl-base-1.0.safetensors`) from [Hugging Face](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0).
   - Move it to: `ComfyUI/models/checkpoints/`.
2. **Ship Design LoRA**:
   - Download `Industrial-Design-Extreme-Material-SDXL_v1.0` (LoRA file) from the [Hugging Face Repository](https://huggingface.co/Awsteam7052/Industrial-Design-Extreme-Material-SDXL_v1.0/tree/main).
   - Move it to: `ComfyUI/models/loras/` (create the `loras` folder if missing).

### Step 3: Install Required Custom Nodes

Custom nodes extend ComfyUI’s functionality (e.g., ControlNet, IPAdapter, layer management) and are critical for our ship design workflow.

#### Method 1: Install via ComfyUI-Manager (Recommended)

1. Launch ComfyUI (run `python main.py` in the ComfyUI folder).

2. In the ComfyUI interface, open the **Manager** (via the top menu or `ComfyUI-manager` node).

3. Search for each node name below and click "Install" (restart ComfyUI after installation):

   | Required Custom Nodes       |
   | --------------------------- |
   | comfyui_controlnet_aux      |
   | comfyui_essentials          |
   | comfyui_ipadapter_plus      |
   | comfyUI_LayerStyle          |
   | ComfyUI_LayerStyle_Advance  |
   | comfyui-advanced-controlnet |
   | comfyui-animatediff-evolved |
   | comfyui-crystools           |
   | comfyui-custom-scripts      |
   | ComfyUI-DiffusersLoader     |
   | ComfyUI-Easy-Use            |
   | Comfyui-ergouzi-Nodes       |
   | comfyui-Impact-Pack         |
   | ComfyUI-Impact-Subpack      |
   | comfyui-inspire-pack        |
   | comfyui-layerdiffuse        |
   | comfyui-manager             |
   | ComfyUI-MultiGPU            |
   | ComfyUI-Styles_CSV_Loader   |
   | comfyui-WD14-Tagger         |

#### Method 2: Manual Installation (If Manager Fails)

For each node, clone its GitHub repository into `ComfyUI/custom_nodes/`:

```bash
# Example: Install comfyui_controlnet_aux
cd ComfyUI/custom_nodes
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git
```

Repeat this for all nodes in the list above, then restart ComfyUI.

## Using the Ship Design Workflow

The project includes pre-configured workflows that replicate the research paper’s experiments. Here’s how to use them:

1. **Load the Workflow**:
   - Download the workflow files from the project’s `/my_workflows/` directory (included in your local project folder).
   - In ComfyUI:
     1. Click `File` → `Load Workflow` (or use the shortcut `Ctrl+O`).
     2. Select the desired workflow file (e.g., `ship_design_few_shot_v1.json`).
2. **Configure Few-Shot Reference Data**:
   - In the workflow, locate the **Image Load** node (labeled "Few-Shot References").
   - Upload 1–5 ship design reference images (consistent with the few-shot learning paradigm).
3. **Adjust Design Parameters**:
   - Modify nodes like `CLIP Text Encode` (to tweak prompts, e.g., "futuristic cargo ship with lightweight alloy hull") or `KSampler` (to adjust steps/CFG scale).
   - Use the `LoRA Loader` node to adjust the ship LoRA strength (recommended: 0.7–1.0 for optimal design alignment).
4. **Generate Designs**:
   - Click `Queue` (or use `Ctrl+Enter`) to start generation.
   - Results are saved to `ComfyUI/output/` (with metadata to reproduce the workflow later).

## Workflow Structure Explanation

The pre-configured workflow follows a modular design to ensure flexibility and reproducibility. Key components:

| Node Module               | Purpose                                                      |
| ------------------------- | ------------------------------------------------------------ |
| Few-Shot Reference Loader | Loads 1–5 reference images to guide the few-shot learning process. |
| ControlNet Aux Nodes      | Refines ship structural details (e.g., hull symmetry, proportion). |
| IPAdapter Plus            | Aligns generated designs with the style/content of reference images. |
| SDXL + LoRA Loader        | Combines the base SDXL model with the ship-design LoRA for specialization. |
| LayerStyle Nodes          | Adjusts material textures (e.g., metal, composite) and color schemes. |
| WD14 Tagger               | Auto-labels reference images to enhance prompt consistency.  |

## Reproducing Paper Results

To replicate the experimental results from the associated research paper:

1. Use the exact workflow file: `/my_workflows/ship_design_paper_experiment.json`.
2. Use the reference images provided in `/my_workflows/references/` (consistent with the paper’s few-shot setup).
3. Set LoRA strength to `0.8`, sampler steps to `25`, and CFG scale to `7.0` (as used in the paper).
4. Run 5 independent generations per reference set and compare results to the paper’s quantitative/qualitative analysis.

## Troubleshooting

- **Torch CUDA Error**: Uninstall and reinstall PyTorch with the NVIDIA command (see Step 1B3).
- **Missing Custom Nodes**: Ensure all nodes are installed via ComfyUI-Manager and ComfyUI is restarted.
- **LoRA Not Loading**: Verify the LoRA file is in `ComfyUI/models/loras/` and the filename matches the `LoRA Loader` node’s configuration.
- **Slow Generation**: Use an NVIDIA GPU with ≥8GB VRAM (or enable CPU offloading via ComfyUI’s memory settings).

## License

- ComfyUI: [MIT License](https://github.com/comfyanonymous/ComfyUI/blob/master/LICENSE)
- SDXL Model: [Stability AI Non-Commercial License](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/LICENSE.md)
- Ship Design LoRA: Refer to the [Hugging Face Repository](https://huggingface.co/Awsteam7052/Industrial-Design-Extreme-Material-SDXL_v1.0/tree/main) for licensing details.

## Contact

For questions about the project, workflow, or research, please contact:

- Project Maintainer: [Your Name/Team Name]
- Email: [your.email@example.com]
- Paper Reference: [Citation of the associated research paper, if published]