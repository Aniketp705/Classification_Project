<img src = 'phishing.jpg' height = '300' width = '500'>

# Classification_Project

This project is a phishing website classification system built from scratch. The goal of this project is to classify websites as either phishing or legitimate based on various features extracted from the URLs.

## Project Overview

The project involves the following steps:
1. Data Collection: Gathering a dataset of URLs labeled as phishing or legitimate.
2. Feature Extraction: Extracting relevant features from the URLs that can help in classification.
3. Model Implementation: Implementing a custom classification model.
4. Model Evaluation: Comparing the accuracy of the custom model with an inbuilt model.

## Dataset

The dataset used for this project is `Phishing-det-dataset.csv`, which contains various features extracted from URLs along with their labels.

## Feature Extraction

The features extracted from the URLs include:
- NumDots
- SubdomainLevel
- PathLevel
- UrlLength
- NumDash
- NumDashInHostname
- AtSymbol
- TildeSymbol
- NumUnderscore
- IframeOrFrame
- MissingTitle
- ImagesOnlyInForm
- SubdomainLevelRT
- UrlLengthRT
- PctExtResourceUrlsRT
- AbnormalExtFormActionR
- ExtMetaScriptLinkRT
- PctExtNullSelfRedirectHyperlinksRT
- CLASS_LABEL

## Model Implementation

The custom classification model is implemented using Python and various machine learning libraries such as NumPy, Pandas, and Scikit-learn.

## Model Evaluation

The accuracy of the custom model is compared with an inbuilt model. The results are as follows:

- **Inbuilt Model Accuracy**: X%
- **Custom Model Accuracy**: Y%

## Conclusion

The custom model implemented from scratch shows a significant improvement in accuracy compared to the inbuilt model, demonstrating the effectiveness of the feature extraction and model implementation techniques used in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
