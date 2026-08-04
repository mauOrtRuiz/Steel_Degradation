# Steel_Degradation
End-to-end FiLM architecture for spheroidal feature enhancement, dual parameter ($T$) modulation-demodulation, and localized 256x256 degradation heatmaps.

The present work shows a Deep Lerarning framework for the analysis and degradation age estimation of microstructural low-carbon steel after long-term service.
A novel Feature-wise Linear MOdulator-Demodulator (FiLM+D) network is proposed and trained for the spheroidization estimation and degradation exposure time determination.

The Data
To simulate the natural degradation experienced by ferrite-perlite steels during service, the material was subjected to an artificial aging treatment via isothermal heating in a laboratory furnace, followed by air cooling. From this process, a dataset of optical microscopy images was generated to observe the microstructural evolution across different thermal aging intervals: $T = 0$, $500$, $1000$, and $1500$ hours (basado en DESARROLLO DE UN ALGORITMO DE PROCESAMIENTO 
DE IMÁGENES PARA LA CUANTIFICACIÓN DEL ENVEJECIMIENTO ARTIFICIAL EN ACEROS AL CARBONO Nayte Guadalue López Sánchez)

Ground Truth Dataset Construction
The microstructural images were processed using computer vision techniques and analyzed morphologically to categorize the pearlite lamellae into three distinct structural degradation stages. The classification criteria applied for automatic feature extraction are summarized in Table 1. The labeled images generated through this process served as the ground truth dataset for model training and evaluation.

<img width="866" height="268" alt="image" src="https://github.com/user-attachments/assets/3ef31803-b14f-47a1-a7f9-0262c3ee80b5" />


Methodology

Data is cleaned, and images at a magnification within the range 2500X-5000X is only used, magnifications of 1000X and above 10,000X are discarded. Also, images out of focus and images with no information at all. Then, different computer vision methods were applied to perform segmentation under a supervised way. The clases Every image was segmented and selected for quality assurance, and next the image was split into patches of size 256x256 to prapare a dataset 
 
