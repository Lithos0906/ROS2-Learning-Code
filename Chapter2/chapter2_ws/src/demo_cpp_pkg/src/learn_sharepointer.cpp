#include <iostream>
#include <memory>

int main()
{
    auto p1 = std::make_shared<std::string>("This is a str.");
    std::cout << "p1: " << p1.use_count() << "address: " << p1.get() << std::endl;    // 1

    auto p2 = p1;
    std::cout << "p1: " << p1.use_count() << "address: " << p1.get() << std::endl;    // 2
    std::cout << "p2: " << p2.use_count() << "address: " << p2.get() << std::endl;    // 2

    p1.reset();
    std::cout << "p1: " << p1.use_count() << "address: " << p1.get() << std::endl;    // 0
    std::cout << "p2: " << p2.use_count() << "address: " << p2.get() << std::endl;    // 1

    std::cout << "p2's address data: " << p2->c_str() << std::endl;    // This is a str.

    return 0;
}
