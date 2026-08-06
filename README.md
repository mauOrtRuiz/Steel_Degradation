# Steel_Degradation
End-to-end FiLM architecture for spheroidal feature enhancement, dual parameter ($T$) modulation-demodulation, and localized 256x256 degradation heatmaps.


**Abstract**
The progressive degradation of microstructural low-carbon steel after long-term service is determined by spheroidization observed by scanning electron microscopy (SEM). While traditional computer vision techniques struggle to accurately quantify these complex morphological evolutions, deep learning offers robust alternatives. In this study, we propose a Feature-wise Linear Modulation/Demodulation (FiLM) based Multimodal U-Net architecture designed specifically for the precise segmentation and analysis of microstructural phase degradation. By integrating FiLM layers into the U-Net, our architecture dynamically conditions the main backbone of U-Net feature maps on complementary data modalities—such as thermal history parameters, temperature etc. This multimodal fusion allows the network to learn highly complex, context-aware representations of phase boundaries and morphological anomalies that traditional unimodal networks overlook.
Our results demonstrate a significant leap in segmentation performance, achieving an overall Mean Intersection over Union (mIoU) improvement of over 12% compared to standard U-Net baselines, with accuracy gains reaching up to 18% in highly degraded and spheroidized microstructural phases. Building upon this modulated backbone, we extend the architecture into a unified modulator-demodulator framework (UNet-FiLM+D). While the forward path uses thermal history parameters to condition feature maps for precise segmentation, an integrated inverse regression head demodulates the latent space representation directly from the microstructural patterns. This allows the network to function as a non-destructive "microstructural clock," accurately predicting the equivalent degradation exposure time (T) and mapping spatial damage heterogeneity through patch-wise heatmaps. Ultimately, this dual framework bridges the gap between context-aware image segmentation and quantitative materials prognosis.



The present work presents a Deep Learning framework for the analysis and degradation-age estimation of microstructural low-carbon steel after long-term service.
A novel Feature-wise Linear Modulator-Demodulator (FiLM+D) network is proposed and trained for the spheroidization estimation and degradation exposure time determination.

**The Data**

To simulate the natural degradation experienced by ferrite-perlite steels during service, selected low-carbon steel was subjected to an artificial aging treatment via isothermal heating in a laboratory furnace, followed by air cooling. From this process, a set of optical microscopy images was scanned to observe the microstructural evolution across different thermal aging intervals: $T = 0$, $500$, $1000$, and $1500$ hours (Based on Thesis by Nayte Guadalupe López Sánchez)

**Ground Truth Dataset Construction**

The microstructural images were processed using computer vision techniques and analyzed morphologically to categorize the pearlite lamellae into three distinct structural degradation stages, which are the corresponding classes for the segmentation models: Complete lamella, fragmented lamella and spheroidized. The classification criteria applied for automatic feature extraction are summarized in Table 1. 

<img width="866" height="268" alt="image" src="https://github.com/user-attachments/assets/3ef31803-b14f-47a1-a7f9-0262c3ee80b5" />

Every image was processed and visually observed for quality assurance; images at a magnification within the range 2500X-5000X are used; magnifications of 1000X and above 10,000X are discarded, as well as images out of focus and images with no significant information. Finally, every image was split into patches of size 256x256 to generate the ground truth dataset for model training and evaluation. 

The percentage of each class is presented in the next box plots according to the time degradation; as can be seen the relation between the percentage of each class and the degradation time

<img width="1359" height="415" alt="image" src="https://github.com/user-attachments/assets/128f73f5-993b-457e-88dc-c87859733176" />

An example of a reference image for file "Acero T0B-12_e.jpg"

<img width="1768" height="619" alt="image" src="https://github.com/user-attachments/assets/4e2af2c1-7c0f-4426-9950-8c4bc7dadb71" />


**Methodology**

A U-Net model was selected initially to perform the segmentation of a microscope image, and performance was measured by means of accuracy, Jaccard, and IoU. This model has been extensively used in the medical field, and results showed satisfactory results.


As the main purpose of the research is to correlate the degradation process against time, the T variable in the dataset indicates the time exposed directly to UV light to accelerate degratatión; however, it can be asociated to the aging time and is considered a valuable parameter that can be used to give extra information to the DL model. Initially, a Physics-Informed Network (PINN) was evaluated by incorporating the Avrami-Kolmogorov (JMAK) phase transformation kinetic model into the loss function. A Physics-Informed Neural Network (PINN) is a neural network that embeds physical laws, expressed as differential equations, directly into its loss function to constrain model learning. However, incorporating this temporal kinetic penalty into a standard U-Net architecture yielded no statistically significant improvement over an unconstrained baseline model.

To have a stronger influence of the model from the time parameter, a conditioned network was next explored, followed by the modulated FiLM architecture. This network was originally presented as a successful framework to process images with data coming from different questions about the image. In our approach, this multimodal system only involves the image alongside a time variable that determines the age degradation, thus demonstrating the relevance of modulating the network with this parameter. This model was successfully trained, with faster convergence and improved training accuracy. Moreover, accuracy was also improved in the overall results.


To address the problem of determining time degradation, a modification of the original FiLM is proposed, which we name FiLM+D, in which a demodulation branch is integrated into the previous FiLM model, removing the conditional input. Thus, this framework addresses both the forward conditioning (modulation) and the inverse inference (demodulation) of a continuous physical parameter associated with microstructural degradation in spheroidal geometries. Transfer learning was used to train the model by using the previous coefficients obtained from the FiLM model. Because this model is almost equal to the FiLM model, the training time was much faster, as can be seen in the accuracy and loss curves. Blue is the standard U-Net, green is the FiLM model, and red is the FiLM+D (our contribution). As can be seen in the training, the model completed the training in less than half the epochs (mainly due to transfer learning, and also because both are indeed almost the same architecture).

<img width="1363" height="412" alt="image" src="https://github.com/user-attachments/assets/16c1df0c-4d8c-45b0-b225-d37826686ce6" />


 **Results**

 A subset of 10 images of higher resolution were tested and segmented by this framework, and segmentation performance was obtained. For the +D proposal also time degradation was estimated.
 
 <img width="4041" height="791" alt="segmentation_Comparison" src="https://github.com/user-attachments/assets/ee070f78-c3cd-4835-bb36-a861e1b58efe" />

Performance was measured against the ground truth over the 10 selected images and mean IoU was computed. The results are presented in the next table


<img width="816" height="445" alt="image" src="https://github.com/user-attachments/assets/a2e5170c-3473-4c8e-9259-52ac8964b485" />

Incorporating the +D auxiliary task yielded substantial gains across all evaluated microstructural classes. This approach aligns with the principles of Multi-Task Learning (MTL), first introduced by Caruana (1997). By training the network to predict the auxiliary variable alongside segmenting the images, the architecture exploits shared latent representations—benefiting from the core MTL principle where 'learning tasks in parallel while using a shared representation [allows] what is learned for each task [to] help other tasks be learned better.'

**Conclusions**
Key Research Contributions
Markdown
* Enhanced Feature Conditioning via FiLM Integration: Incorporating Feature-wise Linear Modulation (FiLM) into the standard U-Net architecture yields a measurable performance boost over the baseline model by effectively modulating intermediate feature maps with temporal heat-treatment metadata.

Superior Accuracy via Auxiliary Multi-Task Learning (+D): Introducing an auxiliary time-demodulation regression branch (+D) creates a powerful inductive bias that dramatically increases overall segmentation accuracy—reaching 95.69% mIoU (excluding outliers)—with substantial gains in visually ambiguous transitional phases like segmented (+8.93%) and spheroidized (+5.96%) lamellae.

Computational Efficiency and Optimized Training Dynamics: The multi-task framework optimizes shared latent representations, accelerating training convergence and reducing overall computational training time compared to training standalone single-task models.

Direct Microstructural Degradation Time Estimation: The auxiliary branch enables the model to solve an inverse problem: accurately estimating heat-treatment / degradation time directly from raw micrographs during blind inference, eliminating reliance on explicit input metadata.

Localized Degradation Heatmapping: Beyond scalar time estimation, the architecture allows for spatial mapping of degradation levels across a single image, generating visual heatmaps that identify micro-scale structural variations and heterogeneous phase evolution within the same specimen.
