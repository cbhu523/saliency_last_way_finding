# A Saliency-Guided Street View Image Inpainting Framework for Efficient Last-Meters Wayfinding [<a href="https://arxiv.org/pdf/2205.06934.pdf?ref=https://githubhelp.com">Paper</a>]

We propose a saliency-guided street view image inpainting method, which can remove distracting objects to redirect human visual attention to static landmarks.

### Step1 - Context-aware salient object detection

Hierarchical salient object selection based on Image Segemmentation (<a href="https://github.com/open-mmlab/mmsegmentation/tree/master/configs/deeplabv3plus">DeepLabv3+</a>, <a href="https://github.com/open-mmlab/mmsegmentation/blob/master/configs/deeplabv3plus/deeplabv3plus_r101-d8_769x769_80k_cityscapes.py">Model</a>) and Salient Object Detection (<a href="https://github.com/xuebinqin/U-2-Net">U^2Net</a>).

![Figure1](Fig.jpg)

## Citation
For more details please refer to the original papers:
```
@inproceedings{chen2018encoder,
  title={Encoder-decoder with atrous separable convolution for semantic image segmentation},
  author={Chen, Liang-Chieh and Zhu, Yukun and Papandreou, George and Schroff, Florian and Adam, Hartwig},
  booktitle={Proceedings of the European conference on computer vision (ECCV)},
  pages={801--818},
  year={2018}
}
