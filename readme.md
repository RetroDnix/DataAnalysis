# 任务要求
为了提高预训练数据的质量，我们希望能够利用一系列的自动化工具和技术，实现一个代码数据质量过滤器，过滤掉提供的代码中低质量的数据，包括但不限于对代码进行静态代码分析，语义分析（类型检查）等，期待大家提出自己的解决方案，如有问题，欢迎在微信群中提问。



**评价指标**  
1. 正确性
2. 高效性

# 数据集介绍
提供两种数据来源，两种编程语言  
数据来源：starcoder、the-stack-dedup  
编程语言：cpp、python

**数据集目录**
- /test_datatset
  - /starcoder
    - starcoder-cpp.jsonl
    - starcoder-python.jsonl
  - /the-stack-dedup
    - the-stack-dedup-cpp.jsonl
    - the-stack-dedup-python.jsonl

**数据集格式**  
提供的jsonl文件中的每一行示例如下：  
{
  "max_stars_repo_path": "project/race3d/src/Menus/MenuManager.h",  
  "max_stars_repo_name": "maximbilan/cpp_marmalade_sdk_the_pursuit_3d",  
  "max_stars_count": 5,    
  "id": "4010666",  
  **"content": "程序"**
}  
我们主要关注content键所对应的代码程序
上面是来源于starcoder的数据的格式，the-stack-dedup有所差异,但仍只需关注content的内容




