# Steel_Degradation
We present a framework for degradation estimation of low-carbon steel by the comparison of different approaches.


**Abstract**

The progressive degradation of microstructural low-carbon steel after long-term service is determined by spheroidization observed by scanning electron microscopy (SEM). While traditional computer vision techniques struggle to accurately quantify these complex morphological evolutions, deep learning offers robust alternatives. In this Study we present a comprehensive comparative evaluation of three computational approaches to assess progressive damage induced by accelerated artificial degradation via ultraviolet (UV) light exposure across four exposure intervals ($0\text{ h}$, $500\text{ h}$, $1,000\text{ h}$, and $1,500\text{ h}$) captured via Scanning Electron Microscopy (SEM). The methods under study are: classical deterministic 2D Fractal Dimension ($D$) analysis via Box-Counting, a U-Net semantic segmentation model coupled with phase fraction ($\%F$) quantification, and a ResNet-50 deep convolutional neural network leveraging macro-level soft-voting probability inference.

Evaluated on an independent blind test dataset (N=15), the classical Fractal Dimension approach demonstrated severe topological limitations, yielding a random-level accuracy of $20.00\%$ ($F1\text{-score} = 19.84\%$) and failing to distinguish intermediate spheroidization stages due to overlapping edge-density signatures. The U-Net segmentation framework achieved a moderate accuracy of $66.67\%$ ($F1\text{-score} = 65.00\%$), successfully isolating pearlite regions but showing sensitivity to local morphological non-linearities. In contrast, the ResNet-50 architecture achieved flawless performance with $100.00\%$ classification accuracy and macro $F1\text{-score}$, demonstrating its ability to extract rich, multi-scale hierarchical texture patterns that transcend local boundary noise. These results quantitatively demonstrate the inadequacy of first-order geometric metrics for thermal degradation assessment and highlight deep holistic feature extraction as a superior paradigm for automated metallographical inspection.


The present work presents a Deep Learning framework for the analysis and degradation-age estimation of microstructural low-carbon steel after long-term service.
A novel Feature-wise Linear Modulator-Demodulator (FiLM+D) network is proposed and trained for the spheroidization estimation and degradation exposure time determination.

**The Data**

To simulate the natural degradation experienced by ferrite-perlite steels during service, selected low-carbon steel was subjected to an artificial aging treatment via isothermal heating in a laboratory furnace, followed by air cooling. From this process, a set of optical microscopy images was scanned to observe the microstructural evolution across different thermal aging intervals: $T = 0$, $500$, $1000$, and $1500$ hours (Based on the thesis by Nayte Guadalupe López Sánchez). Every image was visually observed for quality assurance; images at a magnification within the range 2500X-5000X were selected; magnifications of 1000X and above 10,000X are discarded, as well as images out of focus and images with no significant information. Finally, every image was split into patches of size 256x256 to generate the ground truth dataset for model training and evaluation. 
From this dataset, an independent subset of 15 full micrographs was strictly isolated prior to any data processing to serve as a blind evaluation dataset. These 15 blind micrographs were never exposed to the training or validation pipelines, ensuring an unbiased macro-level benchmark for testing the generalization capability of the trained U-Net and ResNet-50 models.

**Ground Truth Dataset Construction**
A ground truth set set was prepared for the classification task  by separating the source images into four group of images according to each thermal aging class: class 1 for T=0, class2 for T=500, class 3 for T=1000 and class 4 for T=1500. Formed by the image patches of size 256x256 wich passed the quality verification. Besides this dataset ground truth a secondary reference dataset was prepared to train the segmentation UNET model, which was specifically trained to detect the main image structures: Complete lamella, fragmented lamella and spheroidized. This specific dataset was manually prepared by image processing methods by a binarization and morphological analysis of the binary objects to extract main object features and a corresponding class was assigned according to the criteria summarized in Table 1. 

<img width="866" height="268" alt="image" src="https://github.com/user-attachments/assets/3ef31803-b14f-47a1-a7f9-0262c3ee80b5" />

The statistical distribution for each class was studied, the percentage of each class is presented in the  box plots according to the time degradation; as can be seen, there is a relationship between the percentage of each class and the degradation time. This representation was observed for both types of steel: 1020 and 1045


Distribution for steel 1020

<img width="1289" height="392" alt="Figure_1" src="https://github.com/user-attachments/assets/ccb24958-8108-49f6-a02e-80319f6098cb" />

Distribution for steel 1045


<img width="1289" height="392" alt="Figure_1_b" src="https://github.com/user-attachments/assets/841ec6f3-b90b-4388-8080-4b7d2577e9ec" />


An example of a reference image for file "Acero T0B-12_e.jpg"

<img width="1768" height="619" alt="image" src="https://github.com/user-attachments/assets/4e2af2c1-7c0f-4426-9950-8c4bc7dadb71" />


**Methodology**

A U-Net model (Ronneberger) was selected initially to perform the segmentation of a microscope image, and performance was measured by means of accuracy, Jaccard, and IoU. This model has been extensively used in the medical field, and the results have been satisfactory.


As the main purpose of the research is to correlate the degradation process against time, the T variable in the dataset indicates the time exposed directly to UV light to accelerate degratatión; however, it can be asociated to the aging time and is considered a valuable parameter that can be used to give extra information to the DL model. Initially, a Physics-Informed Network (PINN) was evaluated by incorporating the Avrami-Kolmogorov (JMAK) phase transformation kinetic model into the loss function. A Physics-Informed Neural Network (PINN) is a neural network that embeds physical laws, expressed as differential equations, directly into its loss function to constrain model learning. However, incorporating this temporal kinetic penalty into a standard U-Net architecture yielded no statistically significant improvement over an unconstrained baseline model.

To have a stronger influence of the model from the time parameter, a conditioned network was next explored, followed by the modulated FiLM architecture (E. Perez). This network was originally presented as a successful framework to process images with data coming from different questions about the image. In our approach, this multimodal system only involves the image alongside a time variable that determines the age degradation, thus demonstrating the relevance of modulating the network with this parameter. This model was successfully trained, with faster convergence and improved training accuracy. Moreover, accuracy was also improved in the overall results.


To address the problem of determining time degradation, a modification of the original FiLM is proposed, which we name FiLM+D, in which a demodulation branch is integrated into the previous FiLM model, removing the conditional input. Thus, this framework addresses both the forward conditioning (modulation) and the inverse inference (demodulation) of a continuous physical parameter associated with microstructural degradation in spheroidal geometries. Transfer learning was used to train the model by using the previous coefficients obtained from the FiLM model. Because this model is almost equal to the FiLM model, the training time was much faster, as can be seen in the accuracy and loss curves. Blue is the standard U-Net, green is the FiLM model, and red is the FiLM+D (our contribution). As can be seen in the training, the model completed the training in less than half the epochs (mainly due to transfer learning, and also because both are indeed almost the same architecture).

<img width="1363" height="412" alt="image" src="https://github.com/user-attachments/assets/16c1df0c-4d8c-45b0-b225-d37826686ce6" />


 **Results**

 A subset of 10 images of higher resolution were tested and segmented by this framework, and segmentation performance was obtained. For the +D proposal, time degradation was also estimated.
 
 <img width="4041" height="791" alt="segmentation_Comparison" src="https://github.com/user-attachments/assets/ee070f78-c3cd-4835-bb36-a861e1b58efe" />

Performance was measured against the ground truth over the 10 selected images and mean IoU was computed. The results are presented in the next table


<img width="866" height="329" alt="image" src="https://github.com/user-attachments/assets/9c70754f-f01b-4dca-8810-9e4d7886e8a1" />


Incorporating the +D auxiliary task yielded substantial gains across all evaluated microstructural classes. This approach aligns with the principles of Multi-Task Learning (MTL), first introduced by Caruana (1997). By training the network to predict the auxiliary variable alongside segmenting the images, the architecture exploits shared latent representations—benefiting from the core MTL principle where 'learning tasks in parallel while using a shared representation [allows] what is learned for each task [to] help other tasks be learned better.'

**Research Contributions**

* Enhanced segmentation based on Feature Conditioning (FiLM Integration): Incorporating Feature-wise Linear Modulation (FiLM) into the standard U-Net architecture yields a measurable performance  over the baseline model by effectively modulating intermediate feature maps with temporal heat-treatment metadata.

* Superior Accuracy via Auxiliary Multi-Task Learning (+D): Introducing an auxiliary time-demodulation regression branch (+D) creates a powerful inductive bias that dramatically increases overall segmentation accuracy—reaching 95.69% mIoU (excluding outliers)—with substantial gains in visually ambiguous transitional phases like segmented (+8.93%) and spheroidized (+5.96%) lamellae.

* Computational Efficiency and Optimized Training Dynamics: The multi-task framework optimizes shared latent representations, accelerating training convergence and reducing overall computational training time compared to training standalone single-task models.

* Direct Microstructural Degradation Time Estimation: The auxiliary branch enables the model to solve an inverse problem: accurately estimating heat-treatment / degradation time directly from raw micrographs during blind inference, eliminating reliance on explicit input metadata.

* Localized Degradation Heatmapping: Beyond scalar time estimation, the architecture allows for spatial mapping of degradation levels across a single image, generating visual heatmaps that identify micro-scale structural variations and heterogeneous phase evolution within the same specimen.

**Work to do**

To prepare an inference test for the segmentation and Time estimation and elaborate a heatmap.

Retrain the same model and perform an experiment for a multiclass estimation-added task, instead of the regression task. The proposed experiment is to estimate: low, moderate, and severe degradation. 

The current experiment was performed on Steel 1020, there still remains the analysis of Steel 1045. Maybe present the results for each type of steel and overall results.
