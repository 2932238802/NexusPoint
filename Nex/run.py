import subprocess
import os

PROJECT_ROOT = None 

# 你要运行的爬虫的名字
SPIDER_NAME = "Nex"  # 确保这是你爬虫的 name 属性
OUTPUT_FILENAME = "output.csv"


def run_scrapy_crawl(mode: str,salary:int):
    """
    
    """
    # 模式种类
    command = ["scrapy", "crawl", SPIDER_NAME]
    
    if mode == "overwrite":
        command.extend(["-O", OUTPUT_FILENAME,"-a",f"salary={salary}"])
        print(f"\n >>> 将以覆写模式运行，输出到: {OUTPUT_FILENAME}")
    elif mode == "append":
        command.extend(["-o", OUTPUT_FILENAME,"-a",f"salary={salary}"])
        print(f"\n >>> 将以追加模式运行，输出到: {OUTPUT_FILENAME}")
    else:
        print(" >>> 无效的模式选择")
        return

    # 切换工作目录到 Scrapy 项目的根目录 
    # Scrapy 命令通常需要在包含 scrapy.cfg 文件的目录中运行
    current_dir = os.getcwd()
    if PROJECT_ROOT and os.path.isdir(PROJECT_ROOT):
        try:
            os.chdir(PROJECT_ROOT)
            print(f" >>> 切换工作目录到: {PROJECT_ROOT}")
        except Exception as e:
            print(f" >>>error 无法切换到项目目录 '{PROJECT_ROOT}': {e}")
            print("请确保 PROJECT_ROOT 配置正确，或者将此脚本放在 Scrapy 项目的根目录下运行")
            return
    elif not os.path.exists("scrapy.cfg") and not PROJECT_ROOT:
        print(" >>>warning : 当前目录下未找到 'scrapy.cfg' 文件，并且 PROJECT_ROOT 未设置")
        print(" >>> 如果爬虫无法启动,请将此脚本移至Scrapy项目根目录,或正确设置 PROJECT_ROOT")


    print(f" >>> 即将执行命令: {' '.join(command)}")
    try:
        # 使用 subprocess.run 来执行命令
        # check=True 会在命令返回非零退出码时抛出 CalledProcessError
        # capture_output=False (默认) 会让 Scrapy 的输出直接打印到控制台
        result = subprocess.run(command, check=True, text=True)
        print("\n >>> Scrapy 命令执行成功。")
        print(f" >>> 退出码: {result.returncode}")
    except subprocess.CalledProcessError as e:
        print("\n >>> Scrapy 命令执行失败。")
        print(f" >>> 错误详情: {e}")
        print(f" >>> 退出码: {e.returncode}")
        if e.stdout:
            print(f" >>> 标准输出:\n{e.stdout}")
        if e.stderr:
            print(f" >>> 标准错误:\n{e.stderr}")
            
    except FileNotFoundError:
        print("\n >>> 错误：找不到 'scrapy' 命令。")
        print(" >>> 请确保 Scrapy 已经正确安装并且其路径已添加到系统的 PATH 环境变量中。")
        
    except Exception as e:
        print(f"\n >>> 执行过程中发生未知错误: {e}")
        
    finally:
        # 如果切换了目录，切换回去
        if PROJECT_ROOT and os.path.isdir(PROJECT_ROOT) and os.getcwd() != current_dir:
            os.chdir(current_dir)
            # print(f"已切换回原工作目录: {current_dir}")

if __name__ == "__main__":
    while True:
        print("\n >>> 请选择 CSV 文件写入模式:")
        print(" >>> 1. 覆写模式 (如果文件存在，则覆盖)")
        print(" >>> 2. 追加模式 (如果文件存在，则在末尾追加内容)")
        print(" >>> Q. 退出")

        choice = input(" >>> 请输入选项 (1, 2, 或 Q): ").strip().lower()
        print(" >>> 查询")
        salary = input("\n >>> 需要查询工资的工资范围\n >>> [1:表示查询3K以下]\n >>> [2:表示查询3-5K]\n >>> [3:表示查询5-10K]\n >>> [4:表示查询10-20K]\n >>> [5:表示查询20-50K]\n >>> [6:表示查询50K以上]\n >>> [0:不限]\n").strip().lower()

        if choice == '1':
            run_scrapy_crawl("overwrite",salary=int(salary))
            break
        elif choice == '2':
            run_scrapy_crawl("append",salary=int(salary))
            break
        elif choice == 'q':
            print(" >>> 脚本已退出。")
            break
        else:
            print(" >>> 无效的输入，请输入 1, 2, 或 Q。")
