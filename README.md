# Biomark - Cancer Multi-Omics Biomarker Platform

Production-ready Streamlit platform for breast-cancer multi-omics biomarker discovery.

## Key Capabilities
- Role-based authentication (`admin`, `researcher`, `clinician`)
- Monolithic single-page workflow (no repeated navigation options)
- Multi-omics ingestion (RNA, proteomics, miRNA, SNP, clinical)
- Built-in breast cancer cohort sample data (Luminal A/B, HER2-enriched, TNBC)
- Preprocessing + QC (missing values, normalization, batch correction, PCA/boxplot/heatmap)
- Early/Late/Multi-view integration
- Biomarker discovery (LASSO, RF, mutual information, differential expression)
- ML models (Logistic Regression, Random Forest, XGBoost, SVM, Deep Learning)
- Statistical analyses (univariate, multivariate, biomarker ranking, survival)
- Pathway + text-mining context scoring
- Validation (k-fold CV, feature stability, external validation, reproducibility score)
- Clinical reporting (PDF, Word, CSV)

## Folder Structure
```
multiomics_app/
├── app.py
├── api/
├── ui_pages/
├── modules/
├── utils/
├── data/
│   ├── sample/
│   └── pathway_sets.json
├── models/
├── reports/
└── requirements.txt
```

## Quick Start
```bash
cd multiomics_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Use the project virtual environment to avoid NumPy/compiled-package mismatch from global Python installations.

## Validation
```bash
cd multiomics_app
source .venv/bin/activate
python scripts/smoke_validate.py
```

## Default Login
- Username: `admin`
- Password: `admin123`

## Typical Workflow
1. Load built-in breast cancer sample datasets or upload your own files.
2. Run preprocessing and QC for each omics table.
3. Run early integration.
4. Train model and discover top biomarkers.
5. Inspect statistical/pathway/validation outputs.
6. Generate and export report artifacts.

## Optional API Mode
```bash
cd multiomics_app
uvicorn api.main:app --reload
```
