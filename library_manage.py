import json
import os
import time
from datetime import datetime, timedelta

# ===================== 个性化配置区（可自行修改） =====================
# 系统名称
SYSTEM_NAME = "我的私人图书管理系统"
# 管理员名称
ADMIN_NAME = "图书管理员小助手"
# 欢迎语
WELCOME_WORDS = "欢迎使用专属图书管理系统，让阅读更有条理～"
# 退出语
EXIT_WORDS = "感谢使用，愿你与好书相伴，下次见！"
# 配色（Windows终端需开启ANSI支持，Linux/Mac默认支持）
COLOR_RED = "\033[31m"    # 红色（警告/错误）
COLOR_GREEN = "\033[32m"  # 绿色（成功）
COLOR_YELLOW = "\033[33m" # 黄色（提示/预警）
COLOR_BLUE = "\033[34m"   # 蓝色（标题）
COLOR_PURPLE = "\033[35m" # 紫色（个性化文字）
COLOR_RESET = "\033[0m"   # 重置颜色

# 数据文件路径
DATA_FILE = "my_library_books.json"
# 图书分类（可自定义）
BOOK_CATEGORIES = ["小说", "科技", "教材", "历史", "传记", "其他"]

# ===================== 核心功能函数 =====================
# 初始化图书数据
def init_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

# 读取所有图书数据
def load_books():
    init_data()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 保存图书数据到文件
def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

# 清屏 + 显示个性化菜单
def show_menu():
    # 跨平台清屏
    os.system("cls" if os.name == "nt" else "clear")
    # 个性化标题
    print(COLOR_BLUE + "="*50 + COLOR_RESET)
    print(COLOR_PURPLE + f"         {SYSTEM_NAME} V2.0" + COLOR_RESET)
    print(COLOR_BLUE + "="*50 + COLOR_RESET)
    print(COLOR_YELLOW + WELCOME_WORDS + COLOR_RESET)
    print("┌─────────────────────────────────────────┐")
    print("│  1. 添加图书（支持分类）                 │")
    print("│  2. 查看所有图书（彩色排版）             │")
    print("│  3. 搜索图书（编号/名称/分类）           │")
    print("│  4. 借阅图书（记录借阅时长）             │")
    print("│  5. 归还图书（自动计算逾期）             │")
    print("│  6. 删除图书（二次确认）                 │")
    print("│  7. 库存预警（低库存标红）               │")
    print("│  8. 我的借阅记录                         │")
    print("│  9. 退出系统                             │")
    print("└─────────────────────────────────────────┘")
    return input(COLOR_GREEN + "请输入你的选择（1-9）：" + COLOR_RESET)

# 添加图书（新增分类、个性化提示）
def add_book():
    books = load_books()
    print("\n" + COLOR_BLUE + "【添加新图书】" + COLOR_RESET)
    
    # 图书编号去重
    while True:
        book_id = input("请输入图书编号（如B001）：")
        if any(book["id"] == book_id for book in books):
            print(COLOR_RED + f"编号{book_id}已存在，请重新输入！" + COLOR_RESET)
        else:
            break
    
    # 输入基础信息
    book_name = input("请输入图书名称：")
    author = input("请输入作者：")
    
    # 选择分类（个性化）
    print("\n可选分类：", " | ".join(BOOK_CATEGORIES))
    while True:
        category = input("请输入图书分类（直接选上面的选项）：")
        if category in BOOK_CATEGORIES:
            break
        print(COLOR_RED + "分类输入错误，请选择列表中的选项！" + COLOR_RESET)
    
    # 库存输入校验
    while True:
        try:
            stock = int(input("请输入库存数量："))
            if stock >= 0:
                break
            print(COLOR_RED + "库存数量不能为负数，请重新输入！" + COLOR_RESET)
        except ValueError:
            print(COLOR_RED + "请输入有效的数字！" + COLOR_RESET)
    
    # 组装图书信息
    new_book = {
        "id": book_id,
        "name": book_name,
        "author": author,
        "category": category,
        "stock": stock,
        "borrowed": 0,
        "borrow_records": []
    }
    
    # 保存数据
    books.append(new_book)
    save_books(books)
    print(COLOR_GREEN + f"《{book_name}》添加成功！分类：{category}，库存：{stock}" + COLOR_RESET)
    input("按回车返回菜单...")

# 查看所有图书（彩色排版、分类展示）
def show_all_books():
    books = load_books()
    if not books:
        print(COLOR_YELLOW + "暂无图书数据！" + COLOR_RESET)
        input("按回车返回菜单...")
        return
    
    print("\n" + COLOR_BLUE + "【全量图书列表】" + COLOR_RESET)
    print("="*85)
    header = f"{'编号':<8}{'名称':<20}{'作者':<15}{'分类':<10}{'库存':<8}{'已借出':<8}{'状态'}"
    print(COLOR_PURPLE + header + COLOR_RESET)
    print("="*85)
    
    # 按分类排序展示
    books_sorted = sorted(books, key=lambda x: x["category"])
    for book in books_sorted:
        status = "可借阅" if book["stock"] > 0 else "无库存"
        # 低库存标黄
        stock_display = COLOR_YELLOW + str(book["stock"]) + COLOR_RESET if book["stock"] <= 3 else str(book["stock"])
        # 无库存标红
        status_display = COLOR_RED + status + COLOR_RESET if status == "无库存" else status
        
        line = f"{book['id']:<8}{book['name']:<20}{book['author']:<15}{book['category']:<10}{stock_display:<8}{book['borrowed']:<8}{status_display}"
        print(line)
    print("="*85)
    input("按回车返回菜单...")

# 搜索图书（多维度搜索）
def search_book():
    books = load_books()
    if not books:
        print(COLOR_YELLOW + "暂无图书数据！" + COLOR_RESET)
        input("按回车返回菜单...")
        return
    
    print("\n" + COLOR_BLUE + "【图书搜索】" + COLOR_RESET)
    search_type = input("请选择搜索方式（1-编号 2-名称 3-分类）：")
    keyword = input("请输入搜索关键词：").strip()
    results = []
    
    # 多维度搜索逻辑
    if search_type == "1":
        results = [b for b in books if b["id"] == keyword]
    elif search_type == "2":
        results = [b for b in books if keyword in b["name"]]
    elif search_type == "3":
        results = [b for b in books if b["category"] == keyword]
    else:
        print(COLOR_RED + "搜索方式选择错误！" + COLOR_RESET)
        input("按回车返回菜单...")
        return
    
    # 展示结果
    if not results:
        print(COLOR_YELLOW + "未找到匹配的图书！" + COLOR_RESET)
    else:
        print("\n搜索结果：")
        print("="*85)
        print(COLOR_PURPLE + f"{'编号':<8}{'名称':<20}{'作者':<15}{'分类':<10}{'库存':<8}" + COLOR_RESET)
        print("="*85)
        for b in results:
            print(f"{b['id']:<8}{b['name']:<20}{b['author']:<15}{b['category']:<10}{b['stock']:<8}")
    
    print("="*85)
    input("按回车返回菜单...")

# 借阅图书（记录时长、个性化提示）
def borrow_book():
    books = load_books()
    if not books:
        print(COLOR_YELLOW + "暂无图书数据！" + COLOR_RESET)
        input("按回车返回菜单...")
        return
    
    print("\n" + COLOR_BLUE + "【图书借阅】" + COLOR_RESET)
    book_id = input("请输入要借阅的图书编号：")
    borrower = input("请输入借阅人姓名：")
    
    # 查找图书
    target_book = None
    for b in books:
        if b["id"] == book_id:
            target_book = b
            break
    
    if not target_book:
        print(COLOR_RED + "未找到该编号的图书！" + COLOR_RESET)
    elif target_book["stock"] <= 0:
        print(COLOR_RED + f"《{target_book['name']}》无库存，无法借阅！" + COLOR_RESET)
    else:
        # 记录借阅信息
        borrow_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 默认借阅期限30天
        return_deadline = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        target_book["stock"] -= 1
        target_book["borrowed"] += 1
        target_book["borrow_records"].append({
            "borrower": borrower,
            "borrow_time": borrow_time,
            "return_deadline": return_deadline,
            "return_time": ""
        })
        
        save_books(books)
        print(COLOR_GREEN + f"借阅成功！《{target_book['name']}》剩余库存：{target_book['stock']}" + COLOR_RESET)
        print(COLOR_YELLOW + f"借阅期限：{return_deadline}（超期将提醒）" + COLOR_RESET)
    
    input("按回车返回菜单...")

# 归还图书（计算逾期）
def return_book():
    books = load_books()
    if not books:
        print(COLOR_YELLOW + "暂无图书数据！" + COLOR_RESET)
        input("按回车返回菜单...")
        return
    
    print("\n" + COLOR_BLUE + "【图书归还】" + COLOR_RESET)
    book_id = input("请输入要归还的图书编号：")
    borrower = input("请输入借阅人姓名：")
    
    # 查找图书
    target_book = None
    for b in books:
        if b["id"] == book_id:
            target_book = b
            break
    
    if not target_book:
        print(COLOR_RED + "未找到该编号的图书！" + COLOR_RESET)
    elif target_book["borrowed"] <= 0:
        print(COLOR_YELLOW + "该图书暂无借出记录！" + COLOR_RESET)
    else:
        # 查找未归还的记录
        unreturned = [r for r in target_book["borrow_records"] if r["return_time"] == "" and r["borrower"] == borrower]
        if not unreturned:
            print(COLOR_RED + f"未找到{borrower}借阅该图书的未归还记录！" + COLOR_RESET)
        else:
            # 更新归还信息
            return_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unreturned[0]["return_time"] = return_time
            
            # 计算逾期
            borrow_time = datetime.strptime(unreturned[0]["borrow_time"], "%Y-%m-%d %H:%M:%S")
            deadline = datetime.strptime(unreturned[0]["return_deadline"], "%Y-%m-%d")
            overdue_days = (datetime.now() - deadline).days if datetime.now() > deadline else 0
            
            # 更新库存
            target_book["stock"] += 1
            target_book["borrowed"] -= 1
            save_books(books)
            
            # 个性化提示
            print(COLOR_GREEN + f"归还成功！《{target_book['name']}》当前库存：{target_book['stock']}" + COLOR_RESET)
            if overdue_days > 0:
                print(COLOR_RED + f"注意：该图书逾期{overdue_days}天归还！" + COLOR_RESET)
    
    input("按回车返回菜单...")

# 删除图书（二次确认）
def delete_book():
    books = load_books()
    if not books:
        print(COLOR_YELLOW + "暂无图书数据！" + COLOR_RESET)
        input("按回车返回菜单...")
        return
    
    print("\n" + COLOR_BLUE + "【删除图书】" + COLOR_RESET)
    book_id = input("请输入要删除的图书编号：")
    # 二次确认
    confirm = input(f"确定要删除编号{book_id}的图书吗？（y/n）：")
    if confirm.lower() != "y":
        print(COLOR_YELLOW + "已取消删除操作！" + COLOR_RESET)
        input("按回车返回菜单...")
        return
    
    # 执行删除
    new_books = [b for b in books if b["id"] != book_id]
    if len(new_books) == len(books):
        print(COLOR_RED + "未找到该编号的图书，删除失败！" + COLOR_RESET)
    else:
        save_books(new_books)
        print(COLOR_GREEN + f"编号{book_id}的图书已成功删除！" + COLOR_RESET)
    
    input("按回车返回菜单...")

# 库存预警（低库存标红）
def check_stock_warning():
    books = load_books()
    if not books:
        print(COLOR_YELLOW + "暂无图书数据！" + COLOR_RESET)
        input("按回车返回菜单...")
        return
    
    print("\n" + COLOR_BLUE + "【库存预警检查】" + COLOR_RESET)
    warning_books = [b for b in books if b["stock"] <= 3]
    if not warning_books:
        print(COLOR_GREEN + "所有图书库存充足，无预警！" + COLOR_RESET)
    else:
        print("低库存图书列表（库存≤3）：")
        print("="*70)
        print(COLOR_PURPLE + f"{'编号':<8}{'名称':<20}{'分类':<10}{'当前库存':<10}{'建议'}" + COLOR_RESET)
        print("="*70)
        for b in warning_books:
            print(f"{b['id']:<8}{b['name']:<20}{b['category']:<10}{COLOR_RED}{b['stock']:<10}{COLOR_RESET}立即补货")
    print("="*70)
    input("按回车返回菜单...")

# 我的借阅记录
def show_my_borrow_records():
    books = load_books()
    if not books:
        print(COLOR_YELLOW + "暂无图书数据！" + COLOR_RESET)
        input("按回车返回菜单...")
        return
    
    print("\n" + COLOR_BLUE + "【我的借阅记录】" + COLOR_RESET)
    borrower = input("请输入你的姓名：")
    records = []
    
    # 收集所有借阅记录
    for b in books:
        for r in b["borrow_records"]:
            if r["borrower"] == borrower:
                records.append({
                    "book_name": b["name"],
                    "borrow_time": r["borrow_time"],
                    "return_deadline": r["return_deadline"],
                    "return_time": r["return_time"] or "未归还"
                })
    
    if not records:
        print(COLOR_YELLOW + f"未找到{borrower}的借阅记录！" + COLOR_RESET)
    else:
        print("="*80)
        print(COLOR_PURPLE + f"{'图书名称':<20}{'借阅时间':<20}{'归还期限':<15}{'归还状态'}" + COLOR_RESET)
        print("="*80)
        for r in records:
            status = COLOR_RED + r["return_time"] + COLOR_RESET if r["return_time"] == "未归还" else r["return_time"]
            print(f"{r['book_name']:<20}{r['borrow_time']:<20}{r['return_deadline']:<15}{status}")
    
    print("="*80)
    input("按回车返回菜单...")

# 主程序入口
def main():
    # 初始化数据
    init_data()
    # 个性化欢迎
    print(COLOR_PURPLE + f"【{SYSTEM_NAME}】- 管理员：{ADMIN_NAME}" + COLOR_RESET)
    time.sleep(1)
    
    while True:
        choice = show_menu()
        if choice == "1":
            add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            borrow_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            delete_book()
        elif choice == "7":
            check_stock_warning()
        elif choice == "8":
            show_my_borrow_records()
        elif choice == "9":
            print(COLOR_BLUE + EXIT_WORDS + COLOR_RESET)
            break
        else:
            print(COLOR_RED + "输入错误，请选择1-9之间的数字！" + COLOR_RESET)
            input("按回车返回菜单...")

if __name__ == "__main__":
    main()