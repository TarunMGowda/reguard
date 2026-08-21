import numpy
import pandas
import sklearn
import streamlit
import fitz
import sentence_transformers
from rank_bm25 import BM25Okapi

print("NumPy:", numpy.__version__)
print("Pandas:", pandas.__version__)
print("Scikit-learn:", sklearn.__version__)
print("Streamlit:", streamlit.__version__)
print("PyMuPDF:", fitz.__doc__.split()[1] if fitz.__doc__ else "installed")
print("Sentence Transformers:", sentence_transformers.__version__)
print("BM25: installed")

print("\nEnvironment setup successful.")