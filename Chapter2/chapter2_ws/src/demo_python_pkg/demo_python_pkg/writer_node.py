import rclpy
from rclpy.node import Node
from demo_python_pkg.person_node import PersonNode

class WriterNode(PersonNode):
    def __init__(self, node:str, name:str, age:int, book_name:str) -> None:
        print('WriterNode __init__ method is called, adding one attribute.')
        super().__init__(node, name, age)
        self.book = book_name
        self.get_logger().info(f"{self.name}, {self.age} years old, loves to read {book_name}")

def main():
    rclpy.init()
    node = WriterNode('Duomi', 'Duomi', 2, 'How to play MC')
    node.eat('Mcdonald')
    rclpy.spin(node)
    rclpy.shutdown()
