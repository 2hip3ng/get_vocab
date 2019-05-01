#encoding=utf-8
from __future__ import print_function 
import argparse
import os
import codecs
from collections import Counter



def main():
    parser = argparse.ArgumentParser()

    ## 必须参数
    parser.add_argument("--data_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="获取词表vocab的语料目录")
    parser.add_argument("--output_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="输出词表vocab的目录")
    ## 可选参数
    parser.add_argument("--mode",
                        default='all',
                        type=str,
                        choices=["all", "top_K", "threshold"],
                        help="获取词表vocab的模式")
    parser.add_argument("--top_K",
                        default=50000,
                        type=int,
                        help="词表vocab的长度")
    parser.add_argument("--threshold",
                        default=1,
                        type=int,
                        help="词表vocab过滤低频的阈值")
    args = parser.parse_args()

    vocab = Counter()
    files = os.listdir(args.data_dir)
    for file in files:
    	if not os.path.isdir(file):
    		f = codecs.open(os.path.join(args.data_dir+'/' + file), 'r')
    		for line in f.readlines():
    			vocab.update(line.strip().split())
    		f.close()
    
    f = codecs.open(os.path.join(args.output_dir+'/vocab.txt'), 'w')
    if args.mode =='all':
    	# 打印全部
    	vocab = vocab.items()
    	vocab = sorted(vocab, key=lambda x:x[1], reverse=True)
    	for _ in vocab:
    		f.write(_[0] + '\t' + str(_[1]) + '\n')

    elif args.mode == 'top_K':
    	# 打印前K个
    	vocab = vocab.most_common(args.top_K)
    	for _ in vocab:
    		f.write(_[0] + '\t' + str(_[1]) + '\n')
    	
    elif args.mode == 'threshold':
    	# 过滤词频低于threshold
    	vocab = vocab.items()
    	vocab = sorted(vocab, key=lambda x:x[1], reverse=True)
    	for _ in vocab:
    		if _[1] >= args.threshold:
    			f.write(_[0] + '\t' + str(_[1]) + '\n')
    		else:
    			break
    f.close()

if __name__ == '__main__':
    main()
