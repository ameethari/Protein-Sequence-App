Protein Search App

A Python application with a simple graphical interface for searching the NCBI protein database, retrieving FASTA sequences, and displaying basic metadata about proteins.

---

Features

* Search for proteins by name (for example: *human hemoglobin*, *insulin*).
* Retrieve amino acid sequences in FASTA format.
* Display key protein metadata including ID, title, length, and organism.
* Copy sequences to the clipboard or save them as `.fasta` files.
* Built with a modern interface using CustomTkinter.

---

Technologies Used

* **Python 3.10+**
* **Biopython** (Entrez API for NCBI queries)
* **CustomTkinter**
* **Tkinter**
* **Git** for version control

---

Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/protein-search-app.git
cd protein-search-app
```

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

---

Usage

Run the app with:

```bash
python Protein_app.py
```

1. Enter your **email address** (required by NCBI Entrez).
2. Type a **protein name** (e.g., *human insulin*).
3. Press **Search Protein** or hit Enter.
4. View the protein’s sequence and metadata.
5. Save the sequence to a file or copy it to clipboard.

---

Example Output

Metadata Example:

```
ID: 123456789
Title: Hemoglobin subunit beta
Length: 147 amino acids
Organism: Homo sapiens
```

FASTA Sequence Example:

```
>gi|123456789| hemoglobin subunit beta [Homo sapiens]
MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQR...
```

---

Contributing

Contributions are welcome. Please open an issue to discuss changes before submitting a pull request.

---

License

This project is licensed under the MIT License.

---

Acknowledgements

* Biopython for bioinformatics tools.
* NCBI Entrez for access to protein sequence data.
* CustomTkinter for modern UI components.
