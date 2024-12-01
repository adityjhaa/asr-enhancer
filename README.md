# **ASR Enhancer**  

## **Overview**  

**ASR Enhancer** is a tool designed to improve the accuracy of automatic speech recognition (ASR) systems, particularly for voice-enabled assistants. The system leverages **phoneme-based corrections** and **hill-climbing algorithms** to optimize the output of ASR models, correcting misrecognized words and phrases to deliver higher-quality transcriptions.  

---

## **Key Features**  
- **Phoneme-Based Corrections:** Improves recognition accuracy by utilizing an inverse phoneme table to fix ASR errors.  
- **Hill-Climbing Algorithm:** Iteratively refines sentence outputs by exploring and selecting optimal corrections based on a defined cost function.  
- **Bigram and Unigram Analysis:** Enhances correction efficiency by identifying and addressing errors in common word pairings.  
- **Flexible Algorithms:** Various approaches, including greedy and hill-climbing methods, were explored and evaluated for efficiency and effectiveness.  

---

## **Algorithm Overview**  

### **Core Steps**  
1. **State Definition:**  
   The current best-corrected sentence is considered the "state" at each iteration.  

2. **Neighbor Generation:**  
   - For each character in the sentence, the algorithm identifies its presence in the **inverse phoneme table**.  
   - The phoneme table maps erroneous phonemes to their corrected forms.  
   - Replacements are made for single characters or bigrams, generating a list of potential corrections, each associated with a cost.  

3. **Best Neighbor Selection:**  
   - Among the generated neighbors, the one with the **lowest cost** is selected as the next state.  
   - The process continues iteratively until no further improvement is possible.  

---

## **Installation**  

### **Prerequisites**  
- **Python 3.x**  
- **Conda** (recommended for environment management)  

### **Steps to Set Up**  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/adityjhaa/asr-enhancer.git  
   cd asr-enhancer  
   ```  

2. Install required dependencies using Conda:  
   ```bash  
   conda env create -f environment.yml  
   ```  

3. Activate the environment:  
   ```bash  
   conda activate asr-enhancer  
   ```  

4. Run the ASR Enhancer:  
   ```bash  
   python asr_enhancer.py  
   ```  

---

## **Algorithm Variants and Performance**  

### 1. Greedy Algorithm Without Word Correction  
- **Description:** Updates characters from left to right, replacing them with the lowest-cost neighbors.  
- **Results:**  
  - **Average Loss:** 2.1136  
  - **Average Time per Sentence:** 13 seconds  

### 2. Hill Climbing Without Word Correction  
- **Description:** Examines all characters before making updates but does not consider bigrams.  
- **Results:**  
  - **Average Loss:** 2.0243  
  - **Average Time per Sentence:** 50 seconds  

### 3. Greedy Algorithm with Word Updates Before Character Correction  
- **Description:** Adds missing words to the beginning and end of the sentence, then performs character corrections.  
- **Results:**  
  - **Average Loss:** 1.8454  
  - **Average Time per Sentence:** 25 seconds  

### 4. Greedy Algorithm with Word Updates After Character Correction  
- **Description:** Performs word corrections after character corrections, avoiding unnecessary modifications.  
- **Results:**  
  - **Average Loss:** 1.8058  
  - **Average Time per Sentence:** 25 seconds  

### 5. Hill Climbing with Word Updates After Character Correction  
- **Description:** Combines hill climbing with word corrections applied post character correction.  
- **Results:**  
  - **Average Loss:** 1.7099  
  - **Average Time per Sentence:** 55 seconds  

### 6. Hill Climbing with Unigram and Bigram Corrections  
- **Description:** Integrates bigram checks to address errors in common word pairings (e.g., "SH").  
- **Results:**  
  - **Average Loss:** 1.5158  
  - **Average Time per Sentence:** 60 seconds  

---

## **Analysis and Insights**  
- **Bigram Corrections:** Incorporating bigrams significantly reduced the loss, highlighting the importance of contextual analysis in phoneme corrections.  
- **Word Updates After Character Correction:** This approach consistently outperformed others, demonstrating the effectiveness of correcting broader context only after addressing finer details.  
- **Algorithm Choice:** While hill climbing with Word and Bigram updates achieved the best results, it required more computational time compared to greedy algorithms.  

---

## **Future Improvements**  
- **Dynamic Phoneme Correction:** Enhance the inverse phoneme table with adaptive learning to handle rare or context-specific errors.  
- **Deep Learning Integration:** Incorporate neural networks to predict corrections based on semantic understanding.  
- **Performance Optimization:** Reduce time complexity by parallelizing bigram and unigram analyses.  
- **Real-World Integration:** Extend support to process real-time ASR outputs from popular systems like Google ASR or Alexa.  

---

## **Acknowledgments**  
This project was developed under the guidance of the **COL333: Artificial Intelligence** faculty at **IIT Delhi**. It builds upon foundational ideas in ASR error correction, phonetics, and heuristic algorithms.  
