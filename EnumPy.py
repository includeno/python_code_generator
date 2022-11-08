from enum import Enum
# 声明值类型 模板还是文本
class NodeType(Enum):
    Test = 1
    Model = 2
    ModelList = 3

if __name__ == '__main__':
    print(NodeType.Model.name)