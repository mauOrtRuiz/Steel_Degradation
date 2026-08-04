# Steel_Degradation
End-to-end FiLM architecture for spheroidal feature enhancement, dual parameter ($T$) modulation-demodulation, and localized 256x256 degradation heatmaps.

The present work presents a Deep Learning framework for the analysis and degradation-age estimation of microstructural low-carbon steel after long-term service.
A novel Feature-wise Linear Modulator-Demodulator (FiLM+D) network is proposed and trained for the spheroidization estimation and degradation exposure time determination.

**The Data**

To simulate the natural degradation experienced by ferrite-perlite steels during service, selected low carbonite steel was subjected to an artificial aging treatment via isothermal heating in a laboratory furnace, followed by air cooling. From this process, a set of optical microscopy images was scanned to observe the microstructural evolution across different thermal aging intervals: $T = 0$, $500$, $1000$, and $1500$ hours (Thesis: DESARROLLO DE UN ALGORITMO DE PROCESAMIENTO 
DE IMÁGENES PARA LA CUANTIFICACIÓN DEL ENVEJECIMIENTO ARTIFICIAL EN ACEROS AL CARBONO by Nayte Guadalupe López Sánchez)

**Ground Truth Dataset Construction**

The microstructural images were processed using computer vision techniques and analyzed morphologically to categorize the pearlite lamellae into three distinct structural degradation stages, which are the corresponding classes for the segmentation models: Complete lamella, fragmented lamella and spheroidized. The classification criteria applied for automatic feature extraction are summarized in Table 1. 

<img width="866" height="268" alt="image" src="https://github.com/user-attachments/assets/3ef31803-b14f-47a1-a7f9-0262c3ee80b5" />

Every image was processed and was visually observed for quality assurance; images at a magnification within the range 2500X-5000X are used; magnifications of 1000X and above 10,000X are discarded, as well as images out of focus and images with no significant information. Finally, every image was split into patches of size 256x256 to generate the ground truth dataset for model training and evaluation. 


**Methodology**

A U-Net model was selected initially to perform the segmentation of a microscope image, and performance was measured by means of accuracy, Jaccard, and IoU. This resulted in satisfactory results


As the main purpose of the research is to correlate the degradation process against time, T variable is also considered a valuable parameter that can be used to give extra information to the DL model. Initially, a Physics-Informed Network (PINN) by incorporating the Avrami-Kolmogorov (JMAK) phase transformation kinetic model into the loss function. A Physics-Informed Neural Network (PINN) is a neural network that embeds physical laws, expressed as differential equations, directly into its loss function to constrain model learning. However, incorporating this temporal kinetic penalty into a standard U-Net architecture yielded no statistically significant improvement over an unconstrained baseline model.

To have a stronger influence on the model from the time parameter, a conditioned network was next explored, followed by the modulated FiLM architecture. This network was originally presented as a successful framework to process images with data coming from different questions about the image. In our approach, this multimodal system only involves the image alongside a time variable that determines the age degradation, thus demonstrating the relevance of modulating the network with this parameter. 


However, to address the problem of determining time degradation, a modification of the original FiLM is proposed, which we name FiLM+D as it adds a demodulation process. The proposed framework addresses both the forward conditioning (modulation) and the inverse inference (demodulation) of a continuous physical parameter associated with microstructural degradation in spheroidal geometries. 


 
