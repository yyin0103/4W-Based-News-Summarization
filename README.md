# 4W-Based-News-Summarization
Course Project for 2022 Fall Language Generation and Summarization at Columbia University

Note: This project is based on the Bart model in https://github.com/neulab/guided_summarization.

```
@inproceedings{dou2021gsum,
  title={GSum: A General Framework for Guided Neural Abstractive Summarization},
  author={Dou, Zi-Yi and Liu, Pengfei and Hayashi, Hiroaki and Jiang, Zhengbao and Neubig, Graham},
  booktitle={Conference of the North American Chapter of the Association for Computational Linguistics (NAACL)},
  year={2021}
}
```

# Steps #
1. Install requirements
```
pip install -r requirements.txt
```
2. Set up fairseq
```
cd fairseq
pip install --editable ./
```

3. Prepare a txt file with a list of the documents to summarize.

4. Extract keywords
`generate_keywords.py` is expected to include several keyword ranking and extraction methods based on sPaCy's NER and pytextRank.

```
python3 generate_keywords.py --data_path /PATH/TO/YOUR/FILE --method manually_tuned --max_num --output_path /PATH/TO/STORE/KEYWORDS
```

Command line args:  
* data_path: the path to your file
* method: the method to extract keywords. Currently this repository only support manually_tuned weighted rerank keyword mechanism. In the future, it will support neural-network-based or more other keywords generator.
* max_num: the maximum number of keywords (no more than 30)
* output_path: output path of the keyword list

5. Generate Summary: To train or test a summarization model with Bart using the above keywords extracted, please refer to the steps in 
```
GSum-README.md
```


