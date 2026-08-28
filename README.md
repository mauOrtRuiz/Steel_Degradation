# Steel_Degradation

# Microstructural Degradation Time Estimation via SEM Image Analysis: Benchmarking Classical Fractals, Semantic Segmentation, and Deep Learning

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


An example of a reference image for file "Acero T0B-12_e.jpg" for the case T=0

<img width="1768" height="619" alt="image" src="https://github.com/user-attachments/assets/4e2af2c1-7c0f-4426-9950-8c4bc7dadb71" />
An example of an image ( file "Acero 1045 500C 1500 T1500A-13.jpg"  ) for T= 1500

<img width="1360" height="541" alt="image" src="https://github.com/user-attachments/assets/2185a684-6c14-460c-8297-a9ee86237d99" />

It can be seen that after a degradation process aplied by 1500 UV time there is an increase in fragmented lammelae and spheriodization

**Methodology**

The proposed pipeline evaluates three distinct computational frameworks to estimate microstructural degradation time (0 h, 500 h, 1,000 h, and 1,500 h) under accelerated ultraviolet (UV) exposure using high-resolution SEM micrographs. The methodological workflow comprises data preparation, model training, statistical thresholding, and macro-level performance evaluation across all approaches.

Approach 1: U-Net Semantic Segmentation and Morphological Thresholding. A U-Net architecture was trained to perform semantic segmentation of the microstructural phases. Following model convergence:The segmented masks were processed to extract morphological metrics, specifically quantifying the relative phase area fraction (%F) of degraded regions and lamellar structures. A rigorous statistical analysis was conducted on the distribution of %F across exposure intervals (0h to 1500h) to establish quantitative cutoff thresholds (decision boundaries). Degradation time was assigned deterministically based on these empirical percentage thresholds. The cut off values established are
<img width="521" height="164" alt="image" src="https://github.com/user-attachments/assets/10eba7b9-54f0-4108-8c1f-90d30ba65631" />


Approach 2: Direct Classification via ResNet-50
A ResNet-50 deep convolutional neural network was trained for direct, end-to-end multi-class classification using the original, unsegmented image patches:

The architecture leveraged hierarchical residual connections to learn fine-grained texture gradients and spatial distribution patterns of carburbide spheroidization without requiring manual feature engineering.

During inference on full-sized micrographs (including the blind dataset), a macro-level soft-voting strategy was implemented, aggregating the probabilistic patch-level predictions across each micrograph to yield the final predicted degradation stage.


Approach 3: Classical Deterministic 2D Fractal Dimension AnalysisTo evaluate whether first-order geometric metrics could achieve class separability:A classical Box-Counting algorithm was applied to map the total boundary/edge density (D) across all microstructural patches.Statistical separability tests (ANOVA F-test and Kruskal-Wallis H-test) and threshold-based classification rules were executed to assess whether D alone could differentiate between degradation stages.


Methodological Performance ComparisonTo rigorously compare the predictive capability of all three approaches on the blind test dataset (N=15), classification performance was quantified using standard macro-averaged evaluation metrics:

<img width="748" height="171" alt="image" src="https://github.com/user-attachments/assets/c3a13368-f578-45e2-ad58-48dea9dff05c" />

The trainig curves for the unet model:

<img width="1117" height="440" alt="image" src="https://github.com/user-attachments/assets/5697b2d8-7f7d-47d7-8672-78b326a34dfa" />

Training for the Resnet 50 model

<img width="1003" height="410" alt="image" src="https://github.com/user-attachments/assets/14605e9a-307c-47fc-b98d-c68010362429" />


 **Results**

 A subset of 15 images of higher resolution were tested and for evaluated for segmentation task and for clasification task into the 4 differnt intervals (classes) by this framework. 

 Both deep learning architectures, U-Net and ResNet-50, were trained using PyTorch on an NVIDIA GPU environment with identical data splitting strategies to ensure a fair experimental comparison. To enhance model generalization and mitigate overfitting across microstructural variations, dynamic data augmentation techniques—including random horizontal and vertical flips, affine transformations, and intensity adjustments—were applied continuously throughout the training process. All input patches were resized to a standardized resolution of 256×256 pixels.The U-Net model was optimized for pixel-wise multi-class semantic segmentation of the microstructural phases. To effectively handle potential class imbalances across fine lamellar and spheroidized features, a hybrid loss function combining Focal Loss and Dice Loss was implemented. Optimization was driven by the AdamW algorithm with an initial learning rate of 1 x 10^(-4) and a weight decay coefficient of 1x 10^(-4).  The network was trained for up to 35 epochs using a batch size of 16, with early stopping enforced after 15 epochs of non-improving validation Dice similarity scores to prevent over-segmentation artifacts. The ResNet-50 architecture was initialized with ImageNet pre-trained weights and fine-tuned for direct four-class categorization corresponding to the UV exposure intervals of 0, 500, 1000, and 1500 hours using unsegmented patches. The model was optimized using standard categorical cross-entropy loss to evaluate predicted softmax probabilities against ground-truth labels. 
 


Segmentation performance was measured against the ground truth over the 15 selected images and mean IoU was computed only for the UNET model. The results are presented in the next table

<img width="866" height="329" alt="image" src="https://github.com/user-attachments/assets/9c70754f-f01b-4dca-8810-9e4d7886e8a1" />

An example of the segmentation compared to the reference ground truth is presented in the next image

<img width="1357" height="403" alt="image" src="https://github.com/user-attachments/assets/9f55ddd9-c3dd-46f5-b583-6f2f85a2001c" />


Next, performance for T interval estimation over the 4 classes was evaluated by means of the accuracy computed over the blind dataset for the 2 deep learning models. In the case of measure of the fractal analysis, as this methodology is not based in a training and validation process the same set of training images were all used for the statistical analysis by means of fractal estimation. 

The comparative performance of the three evaluated approaches—classical Box-Counting Fractal Dimension (D), U-Net semantic segmentation with phase fraction (%F) quantification, and ResNet-50 direct classification with macro-level soft-voting—was benchmarked on the independent blind test dataset comprising 15 fully isolated SEM micrographs across the four UV exposure stages (0h, 500h, 1,000h, and 1,500h).The classical deterministic Fractal Dimension approach demonstrated severe topological limitations, yielding an overall accuracy of only 20.00% with a macro-averaged precision of 0.1958, recall of 0.2083, and F1 of 0.1984. Analysis of the individual class metrics revealed that the model achieved low F1 for 0h (0.2857), 500h (0.2857), and 1,000 h (0.2222), while completely failing to identify the advanced 1,500 h exposure stage, resulting in a precision, recall, and F1 of $0.0000$. Inferential statistical testing confirmed that the global mean differences in fractal dimension were statistically insignificant across the blind sample set (ANOVA -test = 0.1844, p = 0.9048$; Kruskal-Wallis H -test = 1.2542, p = 0.7400), proving that first-order boundary edge density signatures overlap substantially across exposure times and fail to provide reliable class separability, as can be seen in the next figure.

<img width="1156" height="637" alt="image" src="https://github.com/user-attachments/assets/1cdf4ec6-5f67-4c84-8714-415cd64c2292" />

Also the confusion matrix computed over the full training dataset
<img width="722" height="628" alt="image" src="https://github.com/user-attachments/assets/5cce12e3-355f-424a-85c3-eea1548c47ed" />



The U-Net semantic segmentation framework coupled with empirical phase fraction thresholding achieved a moderate performance, attaining an overall classification accuracy of 66.67\% with a macro-averaged F1-score of 65.00%. By successfully isolating microstructural phases and calculating relative area percentages, the model effectively captured the primary trend of surface and phase transformation. However, its accuracy was constrained by rigid thresholding boundaries and localized segmentation errors along complex phase interfaces, leading to misclassifications in intermediate degradation stages. The corresponding confusion matrix is

<img width="794" height="635" alt="image" src="https://github.com/user-attachments/assets/5db8c34b-9a9b-4b0c-9239-cf883ad14795" />


In contrast, the ResNet-50 architecture utilizing macro-level soft-voting probability inference demonstrated superior classification capability, achieving flawless performance with an overall accuracy of 100.00% and a macro-averaged precision, recall, and F1-score of 1.0000 (100.00%) across all four exposure categories. By aggregating patch-level probabilistic outputs across each full-sized micrograph, the deep convolutional neural network extracted rich, multi-scale hierarchical texture patterns and spatial feature distributions that completely bypassed localized noise and boundary artifacts, outperforming both first-order geometric descriptors and thresholded semantic segmentation. Within this majority voting framework, individual patches within a single micrograph do not always achieve 100% agreement toward the true ground-truth label; however, because the overwhelming majority of constituent patches are correctly predicted, the aggregated macro-level decision consistently yields a perfect 100.00% micrograph-level accuracy.

<img width="700" height="632" alt="image" src="https://github.com/user-attachments/assets/cb34ab30-783f-423a-8da2-7a48583f4e99" />



Furthermore, mapping these patch-level predictions back onto their spatial coordinates produces a detailed classification heatmap that provides critical insights into localized degradation heterogeneities within a single sample. Rather than treating the micrograph as a monolithic structure, this spatial mapping reveals intra-sample variations in degradation severity across different micro-regions. For instance, in specimens exposed to 500 hours of ultraviolet radiation, spatial heatmaps demonstrate that certain micro-regions exhibit negligible surface damage and are locally identified as unexposed state (0 hours), whereas neighboring patches within the same micrograph display advanced degradation signatures. This granular spatial representation delivers highly valuable diagnostic information regarding localized degradation kinetics and non-uniform wear patterns that standard global metrics inherently fail to capture.

<img width="1357" height="573" alt="image" src="https://github.com/user-attachments/assets/71c926fc-a95f-40e8-b658-c3ac8a82c535" />

Spatial prediction heatmap generated by the ResNet-50 patch-level classification pipeline on an SEM micrograph exposed to 500 hours of accelerated UV degradation ($T=500\text{ h}$). The vast majority of localized patches are correctly identified as T=500 h, while three isolated patches are predicted as unexposed control material (T=0 h). Visual inspection confirms that these three misclassified regions exhibit minimal microstructural fragmentation and low local surface damage, demonstrating the capability of the patch-based approach to resolve intra-sample degradation heterogeneities and localized wear variations within a single micrograph.


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
