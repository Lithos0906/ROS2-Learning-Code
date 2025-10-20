#include "iostream"

int main(int argc, char** argv)
{
    std::cout << "param numbers = " << argc << std::endl;
    std::cout << "program name = " << argv[0] << std::endl;
    std::string arg1 = argv[1];
    if(arg1 == "--help")
    {
        std::cout << "Here are code help, but nothing use." << std::endl; 
    }

    return 0;
}
