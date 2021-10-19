import math


def css(length):
    print("|" + "---+" * (length + 1) + "---|")


class Page_replace:

    def __init__(self, block_num):
        self.page_trends = [1, 2, 1, 0, 4, 1, 3, 4, 2, 1]  # 静态初始
        self.block_num = block_num  # 块数
        self.block = []  # 块
        self.out_list = []  # 淘汰页
        self.count = 0  # 页面中断次数
        self.print_list = []

    def page_clear(self, block):
        self.block = block
        self.out_list = []  # 淘汰页
        self.count = 0  # 页面中断次数
        self.print_list = []

    def get_form(self, get_list, row):
        rows = row
        columns = int(math.ceil(len(get_list) / rows))
        css(columns)
        for i in range(rows):
            if i == 0:
                print("|页面走向\t", end='')
            else:
                print("|  块" + str(i - 1) + '\t', end='')
            for j in range(columns):
                the_next = i + j * rows
                if the_next < len(get_list):
                    print('| ' + str(get_list[the_next]), end=' ')
            print('|')
        print("|  中断\t", end='')
        for i in range(len(self.out_list)):
            if self.out_list[i] != ' ' or self.out_list[i] == '-':
                print('| ' + chr(8730), end=' ')
            else:
                print('| ' + str(self.out_list[i]), end=' ')
        print('|')
        print("| 淘汰页\t", end='')
        for i in range(len(self.out_list)):
            if self.out_list[i] == '-':
                print('| ' + ' ', end=' ')
            else:
                print('| ' + str(self.out_list[i]), end=' ')
        print('|')
        css(columns)

    def get_page_trend(self):
        """页面走向"""
        self.page_trends.clear()
        self.page_trends = list(map(int, input("作业的页面走向：").split()))
        print(self.page_trends)
        return self.page_trends

    def get_block(self, block_num):
        """内存块"""
        self.block = list(map(int, input("物理块已有页：").split()))
        while len(self.block) > block_num:
            self.block.clear()
            print("错误，重新输入：")
            self.block = list(map(int, input().split()))
        return self.block

    def fifo(self):
        """FIFO算法"""
        i = 0
        col = 1  # 计算列号
        for page_trend in self.page_trends:
            self.print_list.append(page_trend)
            if page_trend not in self.block and \
                    len(self.block) != self.block_num:
                self.block.append(page_trend)
                self.print_list += self.block
                self.out_list.append('-')
                self.count += 1
            elif page_trend not in self.block and \
                    len(self.block) == self.block_num:
                copy_block = self.block[i]
                self.block[i] = page_trend
                self.out_list.append(copy_block)
                self.print_list += self.block
                if i < self.block_num - 1:
                    i += 1
                else:
                    i = 0
                self.count += 1
            else:
                self.print_list += self.block
                self.out_list.append(' ')
            while len(self.print_list) < (self.block_num + 1) * col:
                self.print_list.append(' ')
            col += 1
        return self.print_list

    def lru(self):
        """LRU算法"""
        col = 1  # 计算列号
        copy_block = self.block.copy()
        for page_trend in self.page_trends:
            self.print_list.append(page_trend)
            if page_trend not in self.block and \
                    len(self.block) != self.block_num:
                self.block.append(page_trend)
                copy_block.append(page_trend)
                self.print_list += self.block
                self.count += 1
                self.out_list.append('-')

            elif page_trend in self.block and \
                    len(self.block) == self.block_num:
                copy_block.remove(page_trend)
                copy_block.append(page_trend)
                self.print_list += self.block
                self.out_list.append(' ')

            elif page_trend not in self.block and \
                    len(self.block) == self.block_num:
                replace_head = copy_block.pop(0)
                self.block[self.block.index(replace_head)] = page_trend
                copy_block.append(page_trend)
                self.out_list.append(replace_head)
                self.print_list += self.block
                self.count += 1

            else:
                self.print_list += self.block
                if page_trend != self.block[-1]:
                    copy_block.remove(page_trend)
                    copy_block.append(page_trend)
                self.out_list.append(' ')
            while len(self.print_list) < (self.block_num + 1) * col:
                self.print_list.append(' ')
            col += 1
        return self.print_list

    def not_page_rate(self):
        """计算缺页率"""
        not_page_rate = self.count / len(self.page_trends) * 100
        for i in range(self.out_list.count('-')):
            self.out_list.remove('-')
        for i in range(self.out_list.count(' ')):
            self.out_list.remove(' ')
        print("\n淘汰页为：" + str(self.out_list))
        print("缺页中断：" + str(self.count) + "次" +
              "\t\t缺页率为：" + str(round(not_page_rate, 1)) + "%")
        print()


def main():
    n = input("分配给作业的物理块数：")
    while bool(n) and int(n) > 0:
        page = Page_replace(int(n))
        # page.get_page_trend()
        block = page.get_block(int(n)).copy()
        print("FIFO算法内存状态为：")
        page.get_form(page.fifo(), int(n) + 1)
        page.not_page_rate()

        page.page_clear(block)  # 初始化
        print("LRU算法内存状态为：")
        page.get_form(page.lru(), int(n) + 1)
        page.not_page_rate()
        break
    print("--------------------------------")


if __name__ == "__main__":
    while True:
        main()
