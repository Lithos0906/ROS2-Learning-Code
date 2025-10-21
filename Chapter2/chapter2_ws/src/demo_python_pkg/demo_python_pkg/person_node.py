import rclpy
from rclpy.node import Node

class PersonNode(Node):
    def __init__(self, node_name:str, name_value:str, age_value:int) -> None:
        print('PersonNode __init__ method is called, adding two attributes.')
        super().__init__(node_name)
        self.name = name_value
        self.age = age_value

    def eat(self, food_name:str):
        # print(f"{self.name}, {self.age} years old, loves to eat {food_name}")
        self.get_logger().info(f"{self.name}, {self.age} years old, loves to eat {food_name}")

def main():
    rclpy.init()
    node = PersonNode('Duomi', 'Duomi', 2)
    node.eat('Mcdonald')
    rclpy.spin(node)
    rclpy.shutdown()
