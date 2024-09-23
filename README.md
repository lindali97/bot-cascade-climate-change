# Social bots spoil activist sentiment without eroding engagement

This repository contains the code and data required to replicate the results presented in the article:  
Li, L., Vasarhelyi, O., & Vedres, B. (2024). Social bots sour activist sentiment without eroding engagement. *Scientific Reports*, forthcoming.

It is designed to provide a straightforward replication process for the primary findings discussed in the paper.

## Contents

- **Code**: All the scripts used to conduct the analyses presented in the main text.
- **Data**: Processed datasets necessary for replication.
- **Svg**: Figures that appear in the main text.

## Directory Structure

```
.
├── analysis
├── bot_detection
├── data
│   ├── cascade_analysis_data
│   ├── for_cascade_vis
│   ├── for_pred_vis
│   └── regression_data
├── data_collection
│   ├── create_matching
│   └── get_full_cascade_timeline
└── svg
```

### Description of Folders

- **analysis**: Contains scripts and notebooks used for analyzing the data and generating results reported in the article.
- **bot_detection**: Houses code and models related to the detection of bot accounts within the dataset.
- **data**: This folder includes various datasets used throughout the analysis.
  - **cascade_analysis_data**: Data specifically prepared for analyzing cascades of retweets and interactions.
  - **for_cascade_vis**: Datasets intended for visualization of cascade patterns.
  - **for_pred_vis**: Data used for visualizing predictive models and their outputs.
  - **regression_data**: Contains the data used in regression analyses.
- **data_collection**: Scripts and processes used to collect and prepare the data for analysis.
  - **create_matching**: Code to create treated and matched sample for analysis.
  - **get_full_cascade_timeline**: Scripts that compile timelines of retweet cascades for analysis.
- **svg**: This directory contains visualizations included in the article.

## How to Use

1. Clone or download the repository.
2. Follow the instructions in the provided scripts for replication of the main analyses.
3. The data included here is a minimal subset required for replicating the key results.

### Important Notes

- This repository **only includes the data and code relevant to the main text** of the article.
- **Additional materials**, such as the supplementary information (SI), raw data, and extended analysis scripts, are not included due to their size and complexity.
- If you require access to the raw data, supplementary materials, or other extended analyses, please feel free to contact the repository owner directly, or the corresponding author at vedresb@ceu.edu.
