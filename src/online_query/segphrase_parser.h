#ifndef __SEG_PHRASE_PARSER_H__
#define __SEG_PHRASE_PARSER_H__

#include "../utils/helper.h"

#include <unordered_map>
using namespace std;

class SegPhraseParser
{
private:
    static const double INF;

// need to load
    double penalty;
    unordered_map<string, double> prob;

// generated
    int maxLen;

    void loadPhraseProb(FILE* in, size_t topK) {
        vector<string> phrases;
        size_t size;
        fread(&size, sizeof(size), 1, in);
        phrases.resize(size);

        for (size_t i = 0; i < size; ++ i) {
            Binary::read(in, phrases[i]);
        }

        vector<double> probability;
        probability.resize(size);
        if (size > 0) {
            fread(&probability[0], sizeof(probability[0]), size, in);
        }

        if (topK > 0) {
            size = min(size, topK);
        }

        vector< pair<double, size_t> > order;
        for (size_t i = 0; i < size; ++ i) {
            order.push_back(make_pair(probability[i], i));
        }

        sort(order.rbegin(), order.rend());

        for (size_t iter = 0; iter < size; ++ iter) {
            size_t i = order[iter].second;
            if (log(probability[i]) > -INF) {
                prob[phrases[i]] = log(probability[i]);
            }
        }
    }

    void loadModel(string filename, size_t topK) {
        FILE* in = tryOpen(filename, "rb");

        fread(&penalty, sizeof(penalty), 1, in);

        cerr << "[Model] penalty = " << penalty << endl;

        prob.clear();
        // unigrams
        loadPhraseProb(in, 0);

        cerr << "[Model] # unigrams = " << prob.size() << endl;

        // real phrases
        loadPhraseProb(in, topK);

        cerr << "[Model] # total phrases = " << prob.size() << endl;

        maxLen = 0;
        double logPenalty = log(penalty);
        FOR (pairs, prob) {
            int parts = 1;
            FOR (ch, pairs->first) {
                if ((*ch) == ' ') {
                    ++ parts;
                }
            }
            pairs->second -= (parts - 1) * logPenalty;
            maxLen = max(maxLen, parts + 1);
        }
    }

public:
    SegPhraseParser(string modelFilename, int topK = 0) {
        loadModel(modelFilename, topK);
    }

    unordered_set<string> dict;

    void setDict(const unordered_set<string> &x) {
        dict = x;
    }

    vector<pair<string, bool>> segment(const string &sentence) {
        vector<string> tokens = splitBy(sentence, ' ');

    	vector<double> f(tokens.size() + 1, -INF);
    	vector<int> pre(tokens.size() + 1, -1);
    	f[0] = 0;
    	pre[0] = 0;
    	double penaltyForUnrecognizedUnigram = -1e50 / tokens.size();
    	for (size_t i = 0 ; i < tokens.size(); ++ i) {
    		if (f[i] < -1e80) {
    			continue;
    		}
    		string token = "";
    		size_t j = i;
    		while (j < tokens.size()) {
    			if (j == i) {
    				token = tokens[i];
    			} else {
    				token += " ";
    				token += tokens[j];
    			}
    			if (prob.count(token) && (dict.size() == 0 || dict.count(token))) {
    				double p = prob[token];
    				if (f[i] + p > f[j + 1]) {
    					f[j + 1] = f[i] + p;
    					pre[j + 1] = i;
    				}
    			} else {
    			    if (i == j) {
    			        double p = penaltyForUnrecognizedUnigram;
    			        if (f[i] + p > f[j + 1]) {
        					f[j + 1] = f[i] + p;
        					pre[j + 1] = i;
        				}
    			    }
    				if (j > maxLen + i) {
    					break;
    				}
    			}
    			++ j;
    		}
    	}
    	if (true) {
    	    // get the segmentation plan
    		int i = (int)tokens.size();
            vector<pair<string,bool>> segments;
    		while (i > 0) {
    			int j = pre[i];
    			string token = "";
    			for (int k = j; k < i; ++ k) {
    				if (k > j) {
    					token += " ";
    				}
    				token += tokens[k];
    			}
    			i = j;
                segments.push_back(make_pair(token, dict.count(token)));
    		}
    		reverse(segments.begin(), segments.end());
    		return segments;
    	}
    }

    vector<vector<pair<string, bool>>> segment(const string &sentence, int K) {
        vector<string> tokens = splitBy(sentence, ' ');

    	vector<vector<double>> f(tokens.size() + 1, vector<double>(K, -INF));
    	vector<vector<pair<int, int>>> pre(tokens.size() + 1, vector<pair<int, int>>(K, make_pair(-1, -1)));
    	f[0][0] = 0;
    	pre[0][0] = make_pair(0, 0);
    	double penaltyForUnrecognizedUnigram = -1e50 / tokens.size();
    	for (size_t i = 0 ; i < tokens.size(); ++ i) {
            for (int top_k = 0; top_k < K; ++ top_k) {
                if (f[i][top_k] < -1e80) {
                    continue;
                }
//cerr << i << " " << top_k << ": " << f[i][top_k] << endl;
                string token = "";
                size_t j = i;
                for (size_t j = i; j <= i + maxLen && j < tokens.size(); ++ j) {
                    if (j == i) {
                        token = tokens[i];
                    } else {
                        token += " ";
                        token += tokens[j];
                    }
                    if (prob.count(token) && (dict.size() == 0 || dict.count(token)) || i == j) {
                        double p = penaltyForUnrecognizedUnigram;
                        if (prob.count(token) && (dict.size() == 0 || dict.count(token))) {
                            p = prob[token];
                        }
                        for (int new_top_k = 0; new_top_k < K; ++ new_top_k) {
                            if (f[i][top_k] + p > f[j + 1][new_top_k]) {
                                for (int iter = K - 1; iter > new_top_k; -- iter) {
                                    f[j + 1][iter] = f[j + 1][iter - 1];
                                    pre[j + 1][iter] = pre[j + 1][iter - 1];
                                }
                                f[j + 1][new_top_k] = f[i][top_k] + p;
                                pre[j + 1][new_top_k] = make_pair(i, top_k);
                                break;
                            }
                        }
                    }
                }
            }
    	}
    	if (true) {
            // get the segmentation plan
            myAssert(f[tokens.size()][0] >= -1e80, "[ERROR] at least unigram segmentation!");
            vector<vector<pair<string, bool>>> top_k_segments;
            for (int top_k = 0; top_k < K; ++ top_k) {
                int i = (int)tokens.size();
                if (f[i][top_k] < -1e80) {
                    continue;
                }
                int cur_k = top_k;
                vector<pair<string,bool>> segments;
                while (i > 0) {
                    int j = pre[i][cur_k].first;
                    cur_k = pre[i][cur_k].second;
                    string token = "";
                    for (int k = j; k < i; ++ k) {
                        if (k > j) {
                            token += " ";
                        }
                        token += tokens[k];
                    }
                    i = j;
                    segments.push_back(make_pair(token, dict.count(token)));
                }
                reverse(segments.begin(), segments.end());
                top_k_segments.push_back(segments);
            }
    		return top_k_segments;
    	}
    }
};

const double SegPhraseParser::INF = 1e100;

#endif
