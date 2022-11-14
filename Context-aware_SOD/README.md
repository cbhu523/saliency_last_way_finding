# A Saliency-Guided Street View Image Inpainting Framework for Efficient Last-Meters Wayfinding [<a href="https://arxiv.org/pdf/2205.06934.pdf?ref=https://githubhelp.com">Paper</a>]

We propose a saliency-guided street view image inpainting method, which can remove distracting objects to redirect human visual attention to static landmarks.

### Step 1 - Context-aware salient object detection (SOD)

1) Image Segmmentation using <a href="https://github.com/open-mmlab/mmsegmentation/tree/master/configs/deeplabv3plus">DeepLabv3+</a> (<a href="https://github.com/open-mmlab/mmsegmentation/blob/master/configs/deeplabv3plus/deeplabv3plus_r101-d8_769x769_80k_cityscapes.py">Model</a>);
2) Salient Object Detection using <a href="https://github.com/xuebinqin/U-2-Net">U^2Net</a>;
3) Inpainting Mask Generation using "mask_selection.ipynb": input the segmenation result and SOD result to the mask generation module and get the inpainting mask.

## Citation
For more details please refer to the DeepLabv3+ paper:
```
@inproceedings{chen2018encoder,
  title={Encoder-decoder with atrous separable convolution for semantic image segmentation},
  author={Chen, Liang-Chieh and Zhu, Yukun and Papandreou, George and Schroff, Florian and Adam, Hartwig},
  booktitle={Proceedings of the European conference on computer vision (ECCV)},
  pages={801--818},
  year={2018}
}


U^2Net paper:
```
@article{qin2020u2,
  title={U2-Net: Going deeper with nested U-structure for salient object detection},
  author={Qin, Xuebin and Zhang, Zichen and Huang, Chenyang and Dehghan, Masood and Zaiane, Osmar R and Jagersand, Martin},
  journal={Pattern recognition},
  volume={106},
  pages={107404},
  year={2020},
  publisher={Elsevier}
}


and our paper:
```
@article{hu2022saliency,
  title={A Saliency-Guided Street View Image Inpainting Framework for Efficient Last-Meters Wayfinding},
  author={Hu, Chuanbo and Jia, Shan and Zhang, Fan and Li, Xin},
  journal={arXiv preprint arXiv:2205.06934},
  year={2022}
}
