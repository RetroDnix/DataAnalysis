import os, json, sys, shutil, time
import subprocess
from concurrent.futures import ProcessPoolExecutor
from typing import List
from tqdm import tqdm


def checker(command: str)->int:
    # 运行代码检查命令
    result = subprocess.run(
        command[1:],
        capture_output=True,
        text=True,
    )
    # 无输出表示代码检查通过
    if result.stdout == "" and result.stderr == "":
        return int(command[0])
    else: return -1


if __name__ == "__main__":

    # 解析命令行参数
    if len(sys.argv) == 1:
        print("Usage: python %s <config_file>" % sys.argv[0])
        exit(0)

    # 读取配置文件
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            conf = json.load(file)
            SrcPath: str = conf["SrcPath"]
            TarPath: str = conf["TarPath"]
            CachePath: str = conf["CachePath"]
            FileName: str = conf["FileName"]
            Executable: str = conf["Executable"]
            Args: List[str] = conf["Args"]
    except:
        print("Error: Can't Load Config File!")
        exit(0)

    # 读取源代码
    try:
        with open(SrcPath, encoding="utf-8") as finput:
            dataset = finput.readlines()
            length = len(dataset)  # 数据总条数
            cnt = 0
            print("Restoring files...")
            if not os.path.exists(CachePath):
                os.makedirs(CachePath)
            for i, data in tqdm(enumerate(dataset), total=length):
                sample = json.loads(data)
                code: str = sample["content"]
                # 去除代码第一行可能存在的标记语句，并更新数据集
                if code.startswith("<"):
                    code = code[code.find("\n") + 1 :]
                sample["content"] = code
                dataset[i] = json.dumps(sample, ensure_ascii=False) + "\n"
                # 将代码写入临时文件中
                with open(
                    (CachePath + FileName) % cnt,
                    "w",
                    encoding="utf-8",
                ) as foutput:
                    foutput.write(code)
                cnt += 1
    except:
        print("Error: Can't load src file!")
        exit(0)

    # 分析代码
    try:
        print("Analysing...")
        # 拼接命令
        commands = [([id, Executable, os.path.join(CachePath,FileName % id)] + Args) for id in range(length)]
        # 启动线程池
        with ProcessPoolExecutor() as executor:
            results = list(tqdm(executor.map(checker, commands), total=length))
    except:
        print("Error: Analysing failed!")
        exit(0)

    # 输出结果
    try:
        print("Generating output...")
        res_num = 0
        with open(TarPath, "w", encoding="utf-8") as foutput:
            for resultid in results:
                if resultid != -1:
                    foutput.write(dataset[resultid])
                    res_num += 1
        print("%d files in total, while %d files passed." % (length, res_num))
    except:
        print("Error: Can't output results!")
        exit(0)

    # 清除缓存
    try:
        print("Removing cache dictionary...")
        shutil.rmtree(CachePath, ignore_errors=True)
    except:
        print("Errpo: Can't remove cache dictionary!")
