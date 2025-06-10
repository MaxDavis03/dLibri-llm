# dLibri-llm
A simple categorization script that uses LLM AI filename generation to add Dewey Decimal System codes to the filenames of a digital PDF library.

Usage instructions:

Install python dependecies
pip install pymupdf
pip install pytest

Ensure Ollama is running:
ollama run mistral
This will download and start the mistral model used for classification.

Clone the repository:
git clone https://github.com/max_davis03/dLibri-llm.git
cd dLibri-llm

Place the files to be categorised into the 'input-files' folder.
Supported file types:
.pdf (directly processed)
.docx, .pptx, .xlsx, .txt (automatically converted to PDF if extended logic is used)

Run the script:
python dLibri-llm.py


Categorized and renamed files will be saved in the output-files/ folder.


System Requirements
Python 3.10+

Ollama with a local LLM model (e.g., mistral)

Recommended:
A modern machine with GPU acceleration

Sufficient RAM for handling large PDFs
Wait for the program to complete. You will then find your categorised files in the 'output-files' folder.
It is highly reccomended to use a powerful computer with a suitable GPU for fast LLM processing. Large PDF libraries may take a while to be categorised if the program is run on a local machine with typical hardware.


Notes
The classification is done locally—no internet or cloud APIs required.

Large libraries may take time to process depending on your system.

The Dewey Decimal code is estimated by the LLM and may not be 100% accurate. You can manually adjust as needed.


005 Computer Science - Programming Fundamentals.pdf  
302 Social Sciences - Psychology of Influence.pdf  
641 Food & Drink - French Cuisine Explained.pdf
